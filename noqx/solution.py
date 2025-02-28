"""Generate clingo program for the given problem."""


class ClingoProgram:
    """A program for clingo."""

    def __init__(self):
        """Initialize a program."""
        self.program: str = ""

    def add_program_line(self, line: str):
        """Add a line to the program."""
        if line != "":
            self.program += line + "\n"

    def reset(self):
        """Clear the program."""
        self.program = ""


solver = ClingoProgram()
