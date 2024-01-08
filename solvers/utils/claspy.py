# Copyright 2013 Dany Qumsiyeh (dany@qhex.org)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Claspy
#
# A python constraint solver based on the answer set solver 'clasp'.
# Compiles constraints to an ASP problem in lparse's internal format.
#
## Main interface ##
#
# BoolVar() : Create a boolean variable.
# IntVar() : Create a non-negative integer variable.
# IntVar(1,9) : Integer variable in range 1-9, inclusive.
# IntVar([1,2,3]) : Integer variable with one of the given values.
# MultiVar('a','b') : Generalized variable with one of the given values.
# Atom() : An atom is only true if it is proven, with Atom.prove_if(<b>).
# cond(<pred>, <cons>, <alt>) : Create an "if" statement.
# require(<expr>) : Constrain a variable or expression to be true.
# clasp_solve() : Runs clasp and returns True if satisfiable.
#
# After running solve, print the variables or call var.value() to get
# the result.
#
## Additional functions ##
#
# reset() : Resets the system.  Do not use any old variables after reset.
# set_bits(8) : Set the number of bits for integer variables.
#               Must be called before any variables are created.
# set_max_val(100) : Set the max number of bits as necessary for the given value.
#                    Must be called before any variables are created.
# require_all_diff(lst) : Constrain all vars in a list to be different.
# sum_vars(lst) : Convenience function to sum a list of variables.
# at_least(n, bools) : Whether at least n of the booleans are true.
# at_most(n, bools) : Whether at most n of the booleans are true.
# sum_bools(n, bools) : Whether exactly n of the booleans are true.
# required(<expr>, <str>) : Print the debug string if the expression
#   is false.  You can change a 'require' statement to 'required' for debugging.
# var_in(v, lst) : Whether var v is equal to some element in lst.
#
## Variable methods ##
#
# v.value() : The solution value.
#
## Gotchas ##
#
# Do not use and/or/not with variables. Only use &, |, ~.
# Subtracting from an IntVar requires that the result is positive,
# so you usually want to add to the other side of the equation instead.

import itertools
import subprocess
from functools import reduce
from time import time
from typing import Any, List, Union


CLASP_COMMAND = "python -m clingo --mode=clasp --sat-prepro --eq=1 --trans-ext=dynamic"


class SolverStorage:
    """Storage for all global variables"""

    def __init__(self):
        self.NUM_BITS = 16
        self.BITS = range(self.NUM_BITS)

        self.clasp_rules = []
        self.single_vars = set()
        self.last_bool = 1  # reserved in clasp

        self.memo_caches = []  # list of caches to clear on reset
        self.TRUE_BOOL = True
        self.FALSE_BOOL = False
        self.solution = set()

    def reset(self):
        """Reset the solver storage."""
        self.NUM_BITS = 16
        self.BITS = range(self.NUM_BITS)

        self.clasp_rules = []
        self.single_vars = set()
        self.last_bool = 1  # reserved in clasp

        self.TRUE_BOOL = BoolVar()
        self.solution = set([self.TRUE_BOOL.index])
        require(self.TRUE_BOOL)
        self.FALSE_BOOL = ~self.TRUE_BOOL

        for cache in self.memo_caches:
            cache.clear()


gs = SolverStorage()  # initialize global storage


################################################################################
###############################  Infrastructure  ###############################
################################################################################


class memoized:
    """Decorator that caches a function's return value."""

    def __init__(self, func):
        self.func = func
        self.cache = {}
        gs.memo_caches.append(self.cache)

    def __call__(self, *args):
        try:
            key = tuple(map(hash, args))
            return self.cache[key]
        except KeyError:
            value = self.func(*args)
            self.cache[key] = value
            return value
        except TypeError:  # uncacheable
            return self.func(*args)

    def __get__(self, obj, objtype):
        """Support instance methods."""

        def result(*args):
            return self(obj, *args)

        return result


class memoized_symmetric(memoized):
    """Decorator that memoizes a function where the order of the arguments doesn't matter."""

    def __call__(self, *args):
        try:
            key = tuple(sorted(map(hash, args)))
            return self.cache[key]
        except KeyError:
            value = self.func(*args)
            self.cache[key] = value
            return value
        except TypeError:
            return self.func(*args)


################################################################################
###################################  Solver  ###################################
################################################################################
def new_literal() -> int:
    """Returns the number of a new literal."""
    gs.last_bool += 1
    return gs.last_bool


def require(x: Any):
    """Constrains the variable x to be true."""
    x = BoolVar(x)
    add_basic_rule(1, [-x.index])  # basic rule with no head


def add_rule(vals: List[int]):
    """The rule is encoded as a series of integers, according to the SMODELS internal format."""
    gs.clasp_rules.append(vals)


def add_basic_rule(head: int, literals: List[int]):
    # See rule types in lparse.pdf pp.88 (pdf p.92)
    assert head > 0
    literals = optimize_basic_rule(head, literals)
    if literals is None:  # optimization says to skip this rule
        return
    # format: 1 head #literals #negative [negative] [positive]
    negative_literals = list(map(abs, filter(lambda x: x < 0, literals)))
    positive_literals = list(filter(lambda x: x > 0, literals))
    add_rule([1, head, len(literals), len(negative_literals)] + negative_literals + positive_literals)


def add_choice_rule(heads: List[int], literals: List[int]):
    for i in heads:
        assert i > 0
    # format: 3 #heads [heads] #literals #negative [negative] [positive]
    negative_literals = list(map(abs, filter(lambda x: x < 0, literals)))
    positive_literals = list(filter(lambda x: x > 0, literals))
    add_rule([3, len(heads)] + heads + [len(literals), len(negative_literals)] + negative_literals + positive_literals)


def add_weight_rule(head: int, bound: int, literals: List[int]):
    # Unlike constraint rules, weight rules count repeated literals
    assert head > 0
    # format: 5 head bound #literals #negative [negative] [positive] [weights]
    negative_literals = list(map(abs, filter(lambda x: x < 0, literals)))
    positive_literals = list(filter(lambda x: x > 0, literals))
    weights = [1 for i in range(len(literals))]
    add_rule([5, head, bound, len(literals), len(negative_literals)] + negative_literals + positive_literals + weights)


def optimize_basic_rule(head: int, literals: List[int]) -> Union[List[int], None]:
    """Optimizes a basic rule, returning a new set of literals, or
    None if the rule can be skipped."""
    if len(literals) == 0:  # the head must be true
        if head in gs.single_vars:
            return None
        gs.single_vars.add(head)
    elif head == 1 and len(literals) == 1:  # the literal must be false
        if -literals[0] in gs.single_vars:
            return None
        gs.single_vars.add(-literals[0])
    elif head == 1:  # we can optimize headless rules
        for x in literals:
            # if the literal is false, the clause is unnecessary
            if -x in gs.single_vars:
                return None
            # if the literal is true, the literal is unnecessary
            if x in gs.single_vars:
                new_literals = list(filter(lambda y: y != x, literals))
                return optimize_basic_rule(head, new_literals)
    return literals


def parse_atoms(line: str) -> List[int]:
    """Grab the indices from a line of clasp output.

    For example, parse_atoms("v2  v3") will output [2, 3].
    """
    parsed = []
    for token in line.split():
        if token[0] == "v":
            parsed.append(int(token[1:]))
    return parsed


def clasp_solve() -> bool:
    """Solves for all defined variables.  If satisfiable, returns True
    and stores the solution so that variables can print out their
    values."""
    start_time = time()  # time when solving process is invoked

    print("Solving", gs.last_bool, "variables,", len(gs.clasp_rules), "rules")

    clasp_process = subprocess.Popen(CLASP_COMMAND.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def clasp_write(s):
        clasp_process.stdin.write(bytes(s, encoding="ascii"))

    try:
        for rule in gs.clasp_rules:
            clasp_write(" ".join(map(str, rule)) + "\n")
    except IOError:
        # The stream may be closed early if there is obviously no
        # solution.
        print("Stream closed early!")
        return False

    clasp_write("0\n")  # end of rules
    # print the literal names
    for i in range(2, gs.last_bool + 1):
        clasp_write(f"{i}, {'v' + str(i)}\n")
    # print the compute statement
    clasp_write("0\nB+\n0\nB-\n1\n0\n1\n")
    if clasp_process.stdout is None:  # debug mode
        return
    clasp_process.stdin.close()
    found_solution = False
    clasp_output = []
    for line in clasp_process.stdout:
        line = line.decode(encoding="ascii").lstrip().rstrip()
        print(line.rstrip())
        if line.startswith("Answer:"):
            gs.solution = set()
        if line.startswith("v"):  # this is a solution line
            assert not found_solution
            gs.solution = set(parse_atoms(line))
            found_solution = True
        else:
            clasp_output.append(line.rstrip())
    if "SATISFIABLE" in clasp_output:
        print("SATISFIABLE")
    elif "UNSATISFIABLE" in clasp_output:
        print("UNSATISFIABLE")
    else:
        print("\n".join(clasp_output))  # show info if there was an error
    print()
    print("Total time: %.2fs" % (time() - start_time))
    print()
    return found_solution


################################################################################
##################################  Booleans  ##################################
################################################################################


# BoolVar is the root variable type, and represents a boolean that can
# take on either value.  Every boolean has an index, starting at 2,
# which is used when it's encoded to SMODELS internal representation.
# BoolVars can also have a negative index, indicating that its value
# is the inverse of the corresponding boolean.
class BoolVar:
    index = None  # integer <= -2 or >= 2.  Treat as immutable.

    def __init__(self, val: Any = None):
        """BoolVar() : Creates a boolean variable.
        BoolVar(x) : Constraints to a particular value, or converts
        from another type."""
        if val is None:
            self.index = new_literal()
            add_choice_rule([self.index], [])  # define the var with a choice rule
        elif isinstance(val, str) and val == "internal":  # don't create a choice rule. (for internal use)
            self.index = new_literal()
        elif isinstance(val, str) and val == "noinit":  # don't allocate an index. (for internal use)
            return
        elif isinstance(val, BoolVar):
            self.index = val.index
        elif isinstance(val, (bool, int)):
            self.index = gs.TRUE_BOOL.index if val else gs.FALSE_BOOL.index
        elif isinstance(val, IntVar):
            result = reduce(lambda a, b: a | b, val.bits)  # if any bits are non-zero
            self.index = result.index
        elif isinstance(val, MultiVar):
            # Use boolean_op to convert val to boolean because there's
            # no unary operator, and 'val != False' is inefficient.
            result = BoolVar(val.boolean_op(lambda a, b: a and b, True))
            self.index = result.index
        else:
            raise TypeError("Can't convert to BoolVar: " + str(val) + " " + str(type(val)))

    def __hash__(self) -> int:
        return hash(("BoolVar", self.index))

    def value(self) -> bool:
        """The value of BoolVar."""
        if self.index > 0:
            return self.index in gs.solution
        else:
            return -self.index not in gs.solution

    def __repr__(self) -> str:
        return str(int(self.value()))

    def __invert__(self) -> "BoolVar":
        # Invert the bool by creating one with a negative index.
        result = BoolVar("noinit")
        result.index = -self.index
        return result

    @memoized_symmetric
    def __eq__(self, other: Any) -> "BoolVar":
        other = BoolVar(other)
        if other.index == gs.TRUE_BOOL.index:
            return self  # opt
        if other.index == gs.FALSE_BOOL.index:
            return ~self  # opt
        result = BoolVar("internal")
        add_basic_rule(result.index, [self.index, other.index])
        add_basic_rule(result.index, [-self.index, -other.index])
        return result

    def __ne__(self, other: Any) -> "BoolVar":
        return ~(self == other)

    @memoized_symmetric
    def __and__(self, other: Any) -> "BoolVar":
        other = BoolVar(other)
        if other.index == gs.TRUE_BOOL.index:
            return self  # opt
        if other.index == gs.FALSE_BOOL.index:
            return gs.FALSE_BOOL  # opt
        result = BoolVar("internal")
        add_basic_rule(result.index, [self.index, other.index])
        return result

    __rand__ = __and__

    @memoized_symmetric
    def __or__(self, other: Any) -> "BoolVar":
        other = BoolVar(other)
        if other.index == gs.TRUE_BOOL.index:
            return gs.TRUE_BOOL  # opt
        if other.index == gs.FALSE_BOOL.index:
            return self  # opt
        result = BoolVar("internal")
        add_basic_rule(result.index, [self.index])
        add_basic_rule(result.index, [other.index])
        return result

    __ror__ = __or__

    @memoized_symmetric
    def __xor__(self, other: Any) -> "BoolVar":
        other = BoolVar(other)
        if other.index == gs.TRUE_BOOL.index:
            return ~self  # opt
        if other.index == gs.FALSE_BOOL.index:
            return self  # opt
        result = BoolVar("internal")
        add_basic_rule(result.index, [self.index, -other.index])
        add_basic_rule(result.index, [other.index, -self.index])
        return result

    __rxor__ = __xor__

    @memoized
    def __gt__(self, other: Any) -> "BoolVar":
        other = BoolVar(other)
        if other.index == gs.TRUE_BOOL.index:
            return gs.FALSE_BOOL  # opt
        if other.index == gs.FALSE_BOOL.index:
            return self  # opt
        result = BoolVar("internal")
        add_basic_rule(result.index, [self.index, -other.index])
        return result

    def __lt__(self, other: Any) -> "BoolVar":
        return BoolVar(other) > self

    def __ge__(self, other: Any) -> "BoolVar":
        return ~(self < other)

    def __le__(self, other: Any) -> "BoolVar":
        return ~(self > other)

    @memoized_symmetric
    def __add__(self, other: Any) -> "IntVar":
        return IntVar(self) + other

    def cond(self, pred: Any, alt: Any) -> "BoolVar":
        """Returns a BoolVar indicating whether the value of self is."""
        pred = BoolVar(pred)
        alt = BoolVar(alt)
        if self.index == alt.index:
            return self  # opt
        result = BoolVar("internal")
        add_basic_rule(result.index, [pred.index, self.index])
        add_basic_rule(result.index, [-pred.index, alt.index])
        return result


def at_least(n: int, bools: List[Any]) -> "BoolVar":
    """Returns a BoolVar indicating whether at least n of the given bools are True."""
    assert isinstance(n, int)
    bools = map(BoolVar, bools)
    result = BoolVar("internal")
    add_weight_rule(result.index, n, list(map(lambda x: x.index, bools)))
    return result


def at_most(n: int, bools: List[Any]) -> "BoolVar":
    """Returns a BoolVar indicating whether at most n of the given bools are True."""
    return ~at_least(n + 1, bools)


def sum_bools(n: int, bools: List[Any]) -> "BoolVar":
    """Returns a BoolVar indicating whether exactly n of the given bools are True."""
    return at_least(n, bools) & at_most(n, bools)


################################################################################
####################################  Atoms  ###################################
################################################################################


# An atom is only true if it is proven.
class Atom(BoolVar):
    def __init__(self):
        BoolVar.__init__(self, "internal")

    def prove_if(self, x):
        """Proves the atom if x is true."""
        x = BoolVar(x)
        add_basic_rule(self.index, [x.index])


################################################################################
##################################  Integers  ##################################
################################################################################


def set_bits(n: int):
    """Sets the number of bits used for IntVars."""
    if gs.last_bool > 2:  # true/false already defined
        raise RuntimeError("Can't change number of bits after defining variables")
    print("Setting integers to", n, "bits")
    gs.NUM_BITS = n
    gs.BITS = range(gs.NUM_BITS)


def set_max_val(n: int):
    """Sets the number of bits corresponding to maximum value n."""
    i = 0
    while n >> i != 0:
        i += 1
    set_bits(i)


# IntVar is an integer variable, represented as a list of boolean variable bits.
class IntVar:
    bits = []  # An array of BoolVar bits, LSB first.  Treat as immutable.

    def __init__(
        self, val: Union[None, bool, int, "BoolVar", "IntVar", List[int]] = None, max_val: Union[None, int] = None
    ):
        """Creates an integer variable.
        IntVar() : Can be any integer in the range of the number of bits.
        IntVar(3) : A fixed integer.
        IntVar(1,9) : An integer in range 1 to 9, inclusive.
        IntVar(<IntVar>) : Copy another IntVar.
        IntVar(<BoolVar>) : Cast from BoolVar.
        IntVar([1,2,3]) : An integer resticted to one of these values."""
        if val is None:
            self.bits = [BoolVar() for i in gs.BITS]
        elif max_val is not None:
            if not (isinstance(val, int) and isinstance(max_val, int)):
                raise RuntimeError("Expected two integers for IntVar() but got: " + str(val) + ", " + str(max_val))
            if max_val < val:
                raise RuntimeError("Invalid integer range: " + str(val) + ", " + str(max_val))
            if max_val >= (1 << gs.NUM_BITS):
                raise RuntimeError("Not enough bits to represent max value: " + str(max_val))
            self.bits = [(gs.FALSE_BOOL if max_val >> i == 0 else BoolVar()) for i in gs.BITS]
            if val > 0:
                require(self >= val)
            require(self <= max_val)
        elif isinstance(val, IntVar):
            self.bits = val.bits
        elif isinstance(val, BoolVar):
            self.bits = [val] + [gs.FALSE_BOOL for i in gs.BITS[1:]]
        elif isinstance(val, int) and val >> gs.NUM_BITS == 0:
            self.bits = [(gs.TRUE_BOOL if ((val >> i) & 1) else gs.FALSE_BOOL) for i in gs.BITS]
        elif isinstance(val, bool):
            self.bits = [gs.TRUE_BOOL if val else gs.FALSE_BOOL] + [gs.FALSE_BOOL for i in gs.BITS[1:]]
        elif isinstance(val, list):
            self.bits = [BoolVar() for i in gs.BITS]
            require(reduce(lambda a, b: a | b, map(lambda x: self == x, val)))
        else:
            raise TypeError("Can't convert to IntVar: " + str(val))

    def __hash__(self):
        return hash(("IntVar",) + tuple(map(lambda b: b.index, self.bits)))

    def value(self) -> int:
        return sum((1 << i) for i in gs.BITS if self.bits[i].value())

    def __repr__(self) -> str:
        return str(self.value())

    @memoized_symmetric
    def __eq__(self, other: Any) -> "BoolVar":
        other = IntVar(other)
        return reduce(lambda a, b: a & b, [self.bits[i] == other.bits[i] for i in gs.BITS])

    def __ne__(self, other: Any) -> "BoolVar":
        return ~(self == other)

    @memoized_symmetric
    def __add__(self, other: Any) -> "IntVar":
        other = IntVar(other)
        # Optimization: only allocate the necessary number of bits.
        max_bit = max(
            [i for i in gs.BITS if self.bits[i].index != gs.FALSE_BOOL.index]
            + [i for i in gs.BITS if other.bits[i].index != gs.FALSE_BOOL.index]
            + [-1]
        )
        result = IntVar(0)  # don't allocate bools yet
        result.bits = [(gs.FALSE_BOOL if i > max_bit + 1 else BoolVar()) for i in gs.BITS]
        IntVar.constrain_sum(self, other, result)
        return result

    __radd__ = __add__

    @memoized
    def __sub__(self, other: Any) -> "IntVar":
        other = IntVar(other)
        result = IntVar()
        IntVar.constrain_sum(result, other, self)
        return result

    __rsub__ = __sub__  # is this right?

    @memoized
    def __gt__(self, other: Any) -> "BoolVar":
        other = IntVar(other)
        result = gs.FALSE_BOOL
        for i in gs.BITS:
            result = cond(
                self.bits[i] > other.bits[i], gs.TRUE_BOOL, cond(self.bits[i] < other.bits[i], gs.FALSE_BOOL, result)
            )
        return result

    def __lt__(self, other: Any) -> "BoolVar":
        return IntVar(other) > self

    def __ge__(self, other: Any) -> "BoolVar":
        return ~(self < other)

    def __le__(self, other: Any) -> "BoolVar":
        return ~(self > other)

    def cond(self, pred: Any, alt: Any) -> "IntVar":
        pred = BoolVar(pred)
        alt = IntVar(alt)
        result = IntVar(0)  # don't allocate bools yet
        result.bits = list(map(lambda c, a: c.cond(pred, a), self.bits, alt.bits))
        return result

    @memoized
    def __lshift__(self, i: int) -> "IntVar":
        assert isinstance(i, int)
        if i == 0:
            return self
        if i >= gs.NUM_BITS:
            return IntVar(0)
        result = IntVar(0)  # don't allocate bools
        result.bits = [gs.FALSE_BOOL for _ in range(i)] + self.bits[:-i]
        return result

    @memoized
    def __rshift__(self, i: int) -> "IntVar":
        assert isinstance(i, int)
        result = IntVar(0)  # don't allocate bools
        result.bits = self.bits[i:] + [gs.FALSE_BOOL for _ in range(i)]
        return result

    @memoized_symmetric
    def __mul__(self, other: Any) -> "IntVar":
        other = IntVar(other)
        result = IntVar(0)
        for i in gs.BITS:
            result += cond(other.bits[i], self << i, 0)
        return result

    @staticmethod
    def constrain_sum(a: "IntVar", b: "IntVar", result: "IntVar") -> "IntVar":
        """Constrain a + b == result.  Note that overflows are forbidden,
        even if the result is never used."""
        # This is a ripple-carry adder.
        c = BoolVar(False)  # carry bit
        # Optimization: stop at the the necessary number of bits.
        max_bit = max(
            [i + 1 for i in gs.BITS if a.bits[i].index != gs.FALSE_BOOL.index]
            + [i + 1 for i in gs.BITS if b.bits[i].index != gs.FALSE_BOOL.index]
            + [i for i in gs.BITS if result.bits[i].index != gs.FALSE_BOOL.index]
        )
        for i in gs.BITS:
            d = a.bits[i] ^ b.bits[i]
            require(result.bits[i] == (d ^ c))
            if i == max_bit:  # opt: we know the rest of the bits are false.
                return result
            c = (a.bits[i] & b.bits[i]) | (d & c)
        require(~c)  # forbid overflows
        return result


@memoized
def cond(pred: Any, cons: Any, alt: Any):
    """An IF statement."""
    if isinstance(pred, bool):
        return cons if pred else alt
    pred = BoolVar(pred)
    if pred.index == gs.TRUE_BOOL.index:
        return cons  # opt
    if pred.index == gs.FALSE_BOOL.index:
        return alt  # opt
    if isinstance(cons, (bool, BoolVar)) and isinstance(alt, (bool, BoolVar)):
        cons = BoolVar(cons)
        alt = BoolVar(alt)
        return cons.cond(pred, alt)
    if isinstance(cons, (int, IntVar)) and isinstance(alt, (int, IntVar)):
        cons = IntVar(cons)
        alt = IntVar(alt)
        return cons.cond(pred, alt)
    # Convert everything else to MultiVars
    cons = MultiVar(cons)
    return cons.cond(pred, alt)


def require_all_diff(lst: List[Any]):
    """Constrain all variables in the list to be different. Note that this creates C(N,2) rules."""
    for a, b in itertools.combinations(lst, 2):
        require(a != b)


def sum_vars(lst: List[Any]) -> Any:
    """Sum a list of vars, using a tree. This is often more efficient than adding in sequence, as bits can be saved."""
    if len(lst) < 2:
        return lst[0]
    middle = len(lst) // 2
    return sum_vars(lst[:middle]) + sum_vars(lst[middle:])


################################################################################
##################################  MultiVar  ##################################
################################################################################


# MultiVar is a generic variable which can take on the value of one of
# a given set of python objects, and supports many operations on those
# objects.  It is implemented as a set of BoolVars, one for each
# possible value.
class MultiVar:
    vals = None  # Dictionary from value to boolean variable,

    # representing that selection.  Treat as immutable.
    def __init__(self, *values):
        for v in values:
            hash(v)  # MultiVar elements must be hashable
        self.vals = {}
        if len(values) == 0:
            return  # uninitialized object: just for internal use
        if len(values) == 1:
            if isinstance(values[0], MultiVar):
                self.vals = values[0].vals
            else:
                self.vals = {values[0]: gs.TRUE_BOOL}
            return
        for v in values:
            if isinstance(v, (BoolVar, IntVar, MultiVar)):
                raise RuntimeError("Can't convert other variables to MultiVar")
        # TODO: optimize two-value case to single boolean
        for v in set(values):
            self.vals[v] = BoolVar()
        # constrain exactly one value to be true
        require(sum_bools(1, self.vals.values()))

    def __hash__(self) -> int:
        return hash(("MultiVar",) + tuple([(v, b.index) for (v, b) in self.vals.items()]))

    def value(self) -> Any:
        for v, b in self.vals.items():
            if b.value():
                return v
        return "???"  # unknown

    def __repr__(self) -> str:
        return str(self.value())

    @staticmethod
    def boolean_op(a, op, b):
        """Computes binary op(a, b) where 'a' is a MultiVar.  Returns a BoolVar."""
        if not isinstance(b, MultiVar):
            b = MultiVar(b)
        # Optimization: see if there are fewer terms for op=true or
        # op=false.  For example, if testing for equality, it may be
        # better to test for all terms which are NOT equal.
        true_count = 0
        false_count = 0
        for a_val, a_bool in a.vals.items():
            for b_val, b_bool in b.vals.items():
                if op(a_val, b_val):
                    true_count += 1
                else:
                    false_count += 1
        invert = false_count < true_count
        terms = []
        for a_val, a_bool in a.vals.items():
            for b_val, b_bool in b.vals.items():
                term = op(a_val, b_val) ^ invert
                terms.append(cond(term, a_bool & b_bool, False))
        if terms:
            result = reduce(lambda a, b: a | b, terms)
            # Subtle bug: this must be cast to BoolVar,
            # otherwise we might compute ~True for __ne__ below.
            return BoolVar(result) ^ invert
        else:
            return gs.FALSE_BOOL ^ invert

    @staticmethod
    def generic_op(a, op, b):
        """Computes op(a, b) where 'a' is a MultiVar.  Returns a new MultiVar."""
        if not isinstance(b, MultiVar):
            b = MultiVar(b)
        result = MultiVar()
        for a_val, a_bool in a.vals.items():
            for b_val, b_bool in b.vals.items():
                result_val = op(a_val, b_val)
                result_bool = a_bool & b_bool
                # TODO: make this work for b as a variable
                if result_val in result.vals:
                    result.vals[result_val] = result.vals[result_val] | result_bool
                else:
                    result.vals[result_val] = result_bool
        return result

    @memoized_symmetric
    def __eq__(self, other: Any) -> "BoolVar":
        return MultiVar.boolean_op(self, lambda x, y: x == y, other)

    def __ne__(self, other: Any) -> "BoolVar":
        return ~(self == other)

    @memoized_symmetric
    def __add__(self, other: Any) -> "MultiVar":
        return MultiVar.generic_op(self, lambda x, y: x + y, other)

    @memoized
    def __sub__(self, other: Any) -> "MultiVar":
        return MultiVar.generic_op(self, lambda x, y: x - y, other)

    @memoized
    def __mul__(self, other: Any) -> "MultiVar":
        return MultiVar.generic_op(self, lambda x, y: x * y, other)

    @memoized
    def __truediv__(self, other: Any) -> "MultiVar":
        return MultiVar.generic_op(self, lambda x, y: x / y, other)

    @memoized
    def __gt__(self, other: Any) -> "BoolVar":
        return MultiVar.boolean_op(self, lambda x, y: x > y, other)

    def __lt__(self, other: Any) -> "BoolVar":
        if not isinstance(other, MultiVar):
            other = MultiVar(other)
        return other > self

    def __ge__(self, other: Any) -> "BoolVar":
        return ~(self < other)

    def __le__(self, other: Any) -> "BoolVar":
        return ~(self > other)

    @memoized
    def __getitem__(self, key: Any) -> "MultiVar":
        return MultiVar.generic_op(self, lambda x, y: x[y], key)

    def cond(self, pred, alt):
        pred = BoolVar(pred)
        alt = MultiVar(alt)
        result = MultiVar()
        for v, b in self.vals.items():
            result.vals[v] = pred & b
        for v, b in alt.vals.items():
            if v in result.vals:
                result.vals[v] = result.vals[v] | (~pred & b)
            else:
                result.vals[v] = ~pred & b
        return result


def var_in(v, lst) -> Union[bool, BoolVar]:
    return reduce(lambda a, b: a | b, map(lambda x: v == x, lst))


def reset():
    """Reset the solver. Any variables defined before a reset will have bogus values and should not be used."""
    gs.reset()


# initialize on startup
reset()
