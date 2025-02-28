(() => {
  var e = {
      100: (e, r, t) => {
        "use strict";
        t.r(r), t.d(r, { Module: () => o }), (e = t.hmd(e));
        var n,
          o =
            ((n =
              (n = "undefined" != typeof document && document.currentScript ? document.currentScript.src : void 0) ||
              "/index.js"),
            function (e) {
              var r, o;
              (e = void 0 !== (e = e || {}) ? e : {}).ready = new Promise(function (e, t) {
                (r = e), (o = t);
              });
              var i,
                a,
                s,
                u,
                c,
                l,
                f = Object.assign({}, e),
                d = [],
                h = "./this.program",
                m = (e, r) => {
                  throw r;
                },
                p = "object" == typeof window,
                w = "function" == typeof importScripts,
                v =
                  "object" == typeof process &&
                  "object" == typeof process.versions &&
                  "string" == typeof process.versions.node,
                g = "";
              v
                ? ((g = w ? t(247).dirname(g) + "/" : "//"),
                  (l = () => {
                    c || ((u = t(603)), (c = t(247)));
                  }),
                  (i = function (e, r) {
                    return l(), (e = c.normalize(e)), u.readFileSync(e, r ? void 0 : "utf8");
                  }),
                  (s = (e) => {
                    var r = i(e, !0);
                    return r.buffer || (r = new Uint8Array(r)), r;
                  }),
                  (a = (e, r, t) => {
                    l(),
                      (e = c.normalize(e)),
                      u.readFile(e, function (e, n) {
                        e ? t(e) : r(n.buffer);
                      });
                  }),
                  process.argv.length > 1 && (h = process.argv[1].replace(/\\/g, "/")),
                  (d = process.argv.slice(2)),
                  process.on("uncaughtException", function (e) {
                    if (!(e instanceof ne)) throw e;
                  }),
                  process.on("unhandledRejection", function (e) {
                    throw e;
                  }),
                  (m = (e, r) => {
                    if (Y()) throw ((process.exitCode = e), r);
                    var t;
                    (t = r) instanceof ne || E("exiting due to exception: " + t), process.exit(e);
                  }),
                  (e.inspect = function () {
                    return "[Emscripten Module object]";
                  }))
                : (p || w) &&
                  (w
                    ? (g = self.location.href)
                    : "undefined" != typeof document && document.currentScript && (g = document.currentScript.src),
                  n && (g = n),
                  (g = 0 !== g.indexOf("blob:") ? g.substr(0, g.replace(/[?#].*/, "").lastIndexOf("/") + 1) : ""),
                  (i = (e) => {
                    var r = new XMLHttpRequest();
                    return r.open("GET", e, !1), r.send(null), r.responseText;
                  }),
                  w &&
                    (s = (e) => {
                      var r = new XMLHttpRequest();
                      return (
                        r.open("GET", e, !1), (r.responseType = "arraybuffer"), r.send(null), new Uint8Array(r.response)
                      );
                    }),
                  (a = (e, r, t) => {
                    var n = new XMLHttpRequest();
                    n.open("GET", e, !0),
                      (n.responseType = "arraybuffer"),
                      (n.onload = () => {
                        200 == n.status || (0 == n.status && n.response) ? r(n.response) : t();
                      }),
                      (n.onerror = t),
                      n.send(null);
                  }));
              var y = e.print || console.log.bind(console),
                E = e.printErr || console.warn.bind(console);
              Object.assign(e, f),
                (f = null),
                e.arguments && (d = e.arguments),
                e.thisProgram && (h = e.thisProgram),
                e.quit && (m = e.quit);
              var _,
                b = 0;
              e.wasmBinary && (_ = e.wasmBinary);
              var k,
                S = e.noExitRuntime || !0;
              "object" != typeof WebAssembly && K("no native wasm support detected");
              var D,
                M,
                F,
                A,
                P,
                x,
                T,
                R = !1,
                O = "undefined" != typeof TextDecoder ? new TextDecoder("utf8") : void 0;
              function j(e, r, t) {
                for (var n = r + t, o = r; e[o] && !(o >= n); ) ++o;
                if (o - r > 16 && e.buffer && O) return O.decode(e.subarray(r, o));
                for (var i = ""; r < o; ) {
                  var a = e[r++];
                  if (128 & a) {
                    var s = 63 & e[r++];
                    if (192 != (224 & a)) {
                      var u = 63 & e[r++];
                      if (
                        (a =
                          224 == (240 & a)
                            ? ((15 & a) << 12) | (s << 6) | u
                            : ((7 & a) << 18) | (s << 12) | (u << 6) | (63 & e[r++])) < 65536
                      )
                        i += String.fromCharCode(a);
                      else {
                        var c = a - 65536;
                        i += String.fromCharCode(55296 | (c >> 10), 56320 | (1023 & c));
                      }
                    } else i += String.fromCharCode(((31 & a) << 6) | s);
                  } else i += String.fromCharCode(a);
                }
                return i;
              }
              function z(e, r) {
                return e ? j(A, e, r) : "";
              }
              function N(e, r, t, n) {
                if (!(n > 0)) return 0;
                for (var o = t, i = t + n - 1, a = 0; a < e.length; ++a) {
                  var s = e.charCodeAt(a);
                  if (
                    (s >= 55296 && s <= 57343 && (s = (65536 + ((1023 & s) << 10)) | (1023 & e.charCodeAt(++a))),
                    s <= 127)
                  ) {
                    if (t >= i) break;
                    r[t++] = s;
                  } else if (s <= 2047) {
                    if (t + 1 >= i) break;
                    (r[t++] = 192 | (s >> 6)), (r[t++] = 128 | (63 & s));
                  } else if (s <= 65535) {
                    if (t + 2 >= i) break;
                    (r[t++] = 224 | (s >> 12)), (r[t++] = 128 | ((s >> 6) & 63)), (r[t++] = 128 | (63 & s));
                  } else {
                    if (t + 3 >= i) break;
                    (r[t++] = 240 | (s >> 18)),
                      (r[t++] = 128 | ((s >> 12) & 63)),
                      (r[t++] = 128 | ((s >> 6) & 63)),
                      (r[t++] = 128 | (63 & s));
                  }
                }
                return (r[t] = 0), t - o;
              }
              function B(e) {
                for (var r = 0, t = 0; t < e.length; ++t) {
                  var n = e.charCodeAt(t);
                  n <= 127 ? r++ : n <= 2047 ? (r += 2) : n >= 55296 && n <= 57343 ? ((r += 4), ++t) : (r += 3);
                }
                return r;
              }
              function I(r) {
                (M = r),
                  (e.HEAP8 = F = new Int8Array(r)),
                  (e.HEAP16 = P = new Int16Array(r)),
                  (e.HEAP32 = x = new Int32Array(r)),
                  (e.HEAPU8 = A = new Uint8Array(r)),
                  (e.HEAPU16 = new Uint16Array(r)),
                  (e.HEAPU32 = T = new Uint32Array(r)),
                  (e.HEAPF32 = new Float32Array(r)),
                  (e.HEAPF64 = new Float64Array(r));
              }
              e.INITIAL_MEMORY;
              var C,
                L = [],
                U = [],
                H = [];
              function Y() {
                return S;
              }
              var W = 0,
                q = null,
                G = null;
              function X(r) {
                W++, e.monitorRunDependencies && e.monitorRunDependencies(W);
              }
              function V(r) {
                if (
                  (W--,
                  e.monitorRunDependencies && e.monitorRunDependencies(W),
                  0 == W && (null !== q && (clearInterval(q), (q = null)), G))
                ) {
                  var t = G;
                  (G = null), t();
                }
              }
              function K(r) {
                e.onAbort && e.onAbort(r),
                  E((r = "Aborted(" + r + ")")),
                  (R = !0),
                  (D = 1),
                  (r += ". Build with -sASSERTIONS for more info.");
                var t = new WebAssembly.RuntimeError(r);
                throw (o(t), t);
              }
              var $, J, Q, Z;
              function ee(e) {
                return e.startsWith("data:application/octet-stream;base64,");
              }
              function re(e) {
                return e.startsWith("file://");
              }
              function te(e) {
                try {
                  if (e == $ && _) return new Uint8Array(_);
                  if (s) return s(e);
                  throw "both async and sync fetching of the wasm failed";
                } catch (e) {
                  K(e);
                }
              }
              function ne(e) {
                (this.name = "ExitStatus"),
                  (this.message = "Program terminated with exit(" + e + ")"),
                  (this.status = e);
              }
              function oe(r) {
                for (; r.length > 0; ) r.shift()(e);
              }
              function ie(e, r) {
                F.set(e, r);
              }
              ee(($ = "clingo.wasm")) || ((J = $), ($ = e.locateFile ? e.locateFile(J, g) : g + J));
              var ae = [];
              function se(e) {
                var r = ae[e];
                return r || (e >= ae.length && (ae.length = e + 1), (ae[e] = r = C.get(e))), r;
              }
              var ue = [];
              function ce(e) {
                (this.excPtr = e),
                  (this.ptr = e - 24),
                  (this.set_type = function (e) {
                    T[(this.ptr + 4) >> 2] = e;
                  }),
                  (this.get_type = function () {
                    return T[(this.ptr + 4) >> 2];
                  }),
                  (this.set_destructor = function (e) {
                    T[(this.ptr + 8) >> 2] = e;
                  }),
                  (this.get_destructor = function () {
                    return T[(this.ptr + 8) >> 2];
                  }),
                  (this.set_refcount = function (e) {
                    x[this.ptr >> 2] = e;
                  }),
                  (this.set_caught = function (e) {
                    (e = e ? 1 : 0), (F[(this.ptr + 12) | 0] = e);
                  }),
                  (this.get_caught = function () {
                    return 0 != F[(this.ptr + 12) | 0];
                  }),
                  (this.set_rethrown = function (e) {
                    (e = e ? 1 : 0), (F[(this.ptr + 13) | 0] = e);
                  }),
                  (this.get_rethrown = function () {
                    return 0 != F[(this.ptr + 13) | 0];
                  }),
                  (this.init = function (e, r) {
                    this.set_adjusted_ptr(0),
                      this.set_type(e),
                      this.set_destructor(r),
                      this.set_refcount(0),
                      this.set_caught(!1),
                      this.set_rethrown(!1);
                  }),
                  (this.add_ref = function () {
                    var e = x[this.ptr >> 2];
                    x[this.ptr >> 2] = e + 1;
                  }),
                  (this.release_ref = function () {
                    var e = x[this.ptr >> 2];
                    return (x[this.ptr >> 2] = e - 1), 1 === e;
                  }),
                  (this.set_adjusted_ptr = function (e) {
                    T[(this.ptr + 16) >> 2] = e;
                  }),
                  (this.get_adjusted_ptr = function () {
                    return T[(this.ptr + 16) >> 2];
                  }),
                  (this.get_exception_ptr = function () {
                    if (Ce(this.get_type())) return T[this.excPtr >> 2];
                    var e = this.get_adjusted_ptr();
                    return 0 !== e ? e : this.excPtr;
                  });
              }
              var le = {
                  isAbs: (e) => "/" === e.charAt(0),
                  splitPath: (e) => /^(\/?|)([\s\S]*?)((?:\.{1,2}|[^\/]+?|)(\.[^.\/]*|))(?:[\/]*)$/.exec(e).slice(1),
                  normalizeArray: (e, r) => {
                    for (var t = 0, n = e.length - 1; n >= 0; n--) {
                      var o = e[n];
                      "." === o ? e.splice(n, 1) : ".." === o ? (e.splice(n, 1), t++) : t && (e.splice(n, 1), t--);
                    }
                    if (r) for (; t; t--) e.unshift("..");
                    return e;
                  },
                  normalize: (e) => {
                    var r = le.isAbs(e),
                      t = "/" === e.substr(-1);
                    return (
                      (e = le
                        .normalizeArray(
                          e.split("/").filter((e) => !!e),
                          !r
                        )
                        .join("/")) ||
                        r ||
                        (e = "."),
                      e && t && (e += "/"),
                      (r ? "/" : "") + e
                    );
                  },
                  dirname: (e) => {
                    var r = le.splitPath(e),
                      t = r[0],
                      n = r[1];
                    return t || n ? (n && (n = n.substr(0, n.length - 1)), t + n) : ".";
                  },
                  basename: (e) => {
                    if ("/" === e) return "/";
                    var r = (e = (e = le.normalize(e)).replace(/\/$/, "")).lastIndexOf("/");
                    return -1 === r ? e : e.substr(r + 1);
                  },
                  join: function () {
                    var e = Array.prototype.slice.call(arguments, 0);
                    return le.normalize(e.join("/"));
                  },
                  join2: (e, r) => le.normalize(e + "/" + r),
                },
                fe = {
                  resolve: function () {
                    for (var e = "", r = !1, t = arguments.length - 1; t >= -1 && !r; t--) {
                      var n = t >= 0 ? arguments[t] : we.cwd();
                      if ("string" != typeof n) throw new TypeError("Arguments to path.resolve must be strings");
                      if (!n) return "";
                      (e = n + "/" + e), (r = le.isAbs(n));
                    }
                    return (
                      (r ? "/" : "") +
                        (e = le
                          .normalizeArray(
                            e.split("/").filter((e) => !!e),
                            !r
                          )
                          .join("/")) || "."
                    );
                  },
                  relative: (e, r) => {
                    function t(e) {
                      for (var r = 0; r < e.length && "" === e[r]; r++);
                      for (var t = e.length - 1; t >= 0 && "" === e[t]; t--);
                      return r > t ? [] : e.slice(r, t - r + 1);
                    }
                    (e = fe.resolve(e).substr(1)), (r = fe.resolve(r).substr(1));
                    for (
                      var n = t(e.split("/")), o = t(r.split("/")), i = Math.min(n.length, o.length), a = i, s = 0;
                      s < i;
                      s++
                    )
                      if (n[s] !== o[s]) {
                        a = s;
                        break;
                      }
                    var u = [];
                    for (s = a; s < n.length; s++) u.push("..");
                    return (u = u.concat(o.slice(a))).join("/");
                  },
                };
              function de(e, r, t) {
                var n = t > 0 ? t : B(e) + 1,
                  o = new Array(n),
                  i = N(e, o, 0, o.length);
                return r && (o.length = i), o;
              }
              var he = {
                ttys: [],
                init: function () {},
                shutdown: function () {},
                register: function (e, r) {
                  (he.ttys[e] = { input: [], output: [], ops: r }), we.registerDevice(e, he.stream_ops);
                },
                stream_ops: {
                  open: function (e) {
                    var r = he.ttys[e.node.rdev];
                    if (!r) throw new we.ErrnoError(43);
                    (e.tty = r), (e.seekable = !1);
                  },
                  close: function (e) {
                    e.tty.ops.flush(e.tty);
                  },
                  flush: function (e) {
                    e.tty.ops.flush(e.tty);
                  },
                  read: function (e, r, t, n, o) {
                    if (!e.tty || !e.tty.ops.get_char) throw new we.ErrnoError(60);
                    for (var i = 0, a = 0; a < n; a++) {
                      var s;
                      try {
                        s = e.tty.ops.get_char(e.tty);
                      } catch (e) {
                        throw new we.ErrnoError(29);
                      }
                      if (void 0 === s && 0 === i) throw new we.ErrnoError(6);
                      if (null == s) break;
                      i++, (r[t + a] = s);
                    }
                    return i && (e.node.timestamp = Date.now()), i;
                  },
                  write: function (e, r, t, n, o) {
                    if (!e.tty || !e.tty.ops.put_char) throw new we.ErrnoError(60);
                    try {
                      for (var i = 0; i < n; i++) e.tty.ops.put_char(e.tty, r[t + i]);
                    } catch (e) {
                      throw new we.ErrnoError(29);
                    }
                    return n && (e.node.timestamp = Date.now()), i;
                  },
                },
                default_tty_ops: {
                  get_char: function (e) {
                    if (!e.input.length) {
                      var r = null;
                      if (v) {
                        var t = Buffer.alloc(256),
                          n = 0;
                        try {
                          n = u.readSync(process.stdin.fd, t, 0, 256, -1);
                        } catch (e) {
                          if (!e.toString().includes("EOF")) throw e;
                          n = 0;
                        }
                        r = n > 0 ? t.slice(0, n).toString("utf-8") : null;
                      } else
                        "undefined" != typeof window && "function" == typeof window.prompt
                          ? null !== (r = window.prompt("Input: ")) && (r += "\n")
                          : "function" == typeof readline && null !== (r = readline()) && (r += "\n");
                      if (!r) return null;
                      e.input = de(r, !0);
                    }
                    return e.input.shift();
                  },
                  put_char: function (e, r) {
                    null === r || 10 === r ? (y(j(e.output, 0)), (e.output = [])) : 0 != r && e.output.push(r);
                  },
                  flush: function (e) {
                    e.output && e.output.length > 0 && (y(j(e.output, 0)), (e.output = []));
                  },
                },
                default_tty1_ops: {
                  put_char: function (e, r) {
                    null === r || 10 === r ? (E(j(e.output, 0)), (e.output = [])) : 0 != r && e.output.push(r);
                  },
                  flush: function (e) {
                    e.output && e.output.length > 0 && (E(j(e.output, 0)), (e.output = []));
                  },
                },
              };
              function me(e) {
                K();
              }
              var pe = {
                ops_table: null,
                mount: function (e) {
                  return pe.createNode(null, "/", 16895, 0);
                },
                createNode: function (e, r, t, n) {
                  if (we.isBlkdev(t) || we.isFIFO(t)) throw new we.ErrnoError(63);
                  pe.ops_table ||
                    (pe.ops_table = {
                      dir: {
                        node: {
                          getattr: pe.node_ops.getattr,
                          setattr: pe.node_ops.setattr,
                          lookup: pe.node_ops.lookup,
                          mknod: pe.node_ops.mknod,
                          rename: pe.node_ops.rename,
                          unlink: pe.node_ops.unlink,
                          rmdir: pe.node_ops.rmdir,
                          readdir: pe.node_ops.readdir,
                          symlink: pe.node_ops.symlink,
                        },
                        stream: { llseek: pe.stream_ops.llseek },
                      },
                      file: {
                        node: { getattr: pe.node_ops.getattr, setattr: pe.node_ops.setattr },
                        stream: {
                          llseek: pe.stream_ops.llseek,
                          read: pe.stream_ops.read,
                          write: pe.stream_ops.write,
                          allocate: pe.stream_ops.allocate,
                          mmap: pe.stream_ops.mmap,
                          msync: pe.stream_ops.msync,
                        },
                      },
                      link: {
                        node: {
                          getattr: pe.node_ops.getattr,
                          setattr: pe.node_ops.setattr,
                          readlink: pe.node_ops.readlink,
                        },
                        stream: {},
                      },
                      chrdev: {
                        node: { getattr: pe.node_ops.getattr, setattr: pe.node_ops.setattr },
                        stream: we.chrdev_stream_ops,
                      },
                    });
                  var o = we.createNode(e, r, t, n);
                  return (
                    we.isDir(o.mode)
                      ? ((o.node_ops = pe.ops_table.dir.node),
                        (o.stream_ops = pe.ops_table.dir.stream),
                        (o.contents = {}))
                      : we.isFile(o.mode)
                      ? ((o.node_ops = pe.ops_table.file.node),
                        (o.stream_ops = pe.ops_table.file.stream),
                        (o.usedBytes = 0),
                        (o.contents = null))
                      : we.isLink(o.mode)
                      ? ((o.node_ops = pe.ops_table.link.node), (o.stream_ops = pe.ops_table.link.stream))
                      : we.isChrdev(o.mode) &&
                        ((o.node_ops = pe.ops_table.chrdev.node), (o.stream_ops = pe.ops_table.chrdev.stream)),
                    (o.timestamp = Date.now()),
                    e && ((e.contents[r] = o), (e.timestamp = o.timestamp)),
                    o
                  );
                },
                getFileDataAsTypedArray: function (e) {
                  return e.contents
                    ? e.contents.subarray
                      ? e.contents.subarray(0, e.usedBytes)
                      : new Uint8Array(e.contents)
                    : new Uint8Array(0);
                },
                expandFileStorage: function (e, r) {
                  var t = e.contents ? e.contents.length : 0;
                  if (!(t >= r)) {
                    (r = Math.max(r, (t * (t < 1048576 ? 2 : 1.125)) >>> 0)), 0 != t && (r = Math.max(r, 256));
                    var n = e.contents;
                    (e.contents = new Uint8Array(r)), e.usedBytes > 0 && e.contents.set(n.subarray(0, e.usedBytes), 0);
                  }
                },
                resizeFileStorage: function (e, r) {
                  if (e.usedBytes != r)
                    if (0 == r) (e.contents = null), (e.usedBytes = 0);
                    else {
                      var t = e.contents;
                      (e.contents = new Uint8Array(r)),
                        t && e.contents.set(t.subarray(0, Math.min(r, e.usedBytes))),
                        (e.usedBytes = r);
                    }
                },
                node_ops: {
                  getattr: function (e) {
                    var r = {};
                    return (
                      (r.dev = we.isChrdev(e.mode) ? e.id : 1),
                      (r.ino = e.id),
                      (r.mode = e.mode),
                      (r.nlink = 1),
                      (r.uid = 0),
                      (r.gid = 0),
                      (r.rdev = e.rdev),
                      we.isDir(e.mode)
                        ? (r.size = 4096)
                        : we.isFile(e.mode)
                        ? (r.size = e.usedBytes)
                        : we.isLink(e.mode)
                        ? (r.size = e.link.length)
                        : (r.size = 0),
                      (r.atime = new Date(e.timestamp)),
                      (r.mtime = new Date(e.timestamp)),
                      (r.ctime = new Date(e.timestamp)),
                      (r.blksize = 4096),
                      (r.blocks = Math.ceil(r.size / r.blksize)),
                      r
                    );
                  },
                  setattr: function (e, r) {
                    void 0 !== r.mode && (e.mode = r.mode),
                      void 0 !== r.timestamp && (e.timestamp = r.timestamp),
                      void 0 !== r.size && pe.resizeFileStorage(e, r.size);
                  },
                  lookup: function (e, r) {
                    throw we.genericErrors[44];
                  },
                  mknod: function (e, r, t, n) {
                    return pe.createNode(e, r, t, n);
                  },
                  rename: function (e, r, t) {
                    if (we.isDir(e.mode)) {
                      var n;
                      try {
                        n = we.lookupNode(r, t);
                      } catch (e) {}
                      if (n) for (var o in n.contents) throw new we.ErrnoError(55);
                    }
                    delete e.parent.contents[e.name],
                      (e.parent.timestamp = Date.now()),
                      (e.name = t),
                      (r.contents[t] = e),
                      (r.timestamp = e.parent.timestamp),
                      (e.parent = r);
                  },
                  unlink: function (e, r) {
                    delete e.contents[r], (e.timestamp = Date.now());
                  },
                  rmdir: function (e, r) {
                    var t = we.lookupNode(e, r);
                    for (var n in t.contents) throw new we.ErrnoError(55);
                    delete e.contents[r], (e.timestamp = Date.now());
                  },
                  readdir: function (e) {
                    var r = [".", ".."];
                    for (var t in e.contents) e.contents.hasOwnProperty(t) && r.push(t);
                    return r;
                  },
                  symlink: function (e, r, t) {
                    var n = pe.createNode(e, r, 41471, 0);
                    return (n.link = t), n;
                  },
                  readlink: function (e) {
                    if (!we.isLink(e.mode)) throw new we.ErrnoError(28);
                    return e.link;
                  },
                },
                stream_ops: {
                  read: function (e, r, t, n, o) {
                    var i = e.node.contents;
                    if (o >= e.node.usedBytes) return 0;
                    var a = Math.min(e.node.usedBytes - o, n);
                    if (a > 8 && i.subarray) r.set(i.subarray(o, o + a), t);
                    else for (var s = 0; s < a; s++) r[t + s] = i[o + s];
                    return a;
                  },
                  write: function (e, r, t, n, o, i) {
                    if ((r.buffer === F.buffer && (i = !1), !n)) return 0;
                    var a = e.node;
                    if (((a.timestamp = Date.now()), r.subarray && (!a.contents || a.contents.subarray))) {
                      if (i) return (a.contents = r.subarray(t, t + n)), (a.usedBytes = n), n;
                      if (0 === a.usedBytes && 0 === o) return (a.contents = r.slice(t, t + n)), (a.usedBytes = n), n;
                      if (o + n <= a.usedBytes) return a.contents.set(r.subarray(t, t + n), o), n;
                    }
                    if ((pe.expandFileStorage(a, o + n), a.contents.subarray && r.subarray))
                      a.contents.set(r.subarray(t, t + n), o);
                    else for (var s = 0; s < n; s++) a.contents[o + s] = r[t + s];
                    return (a.usedBytes = Math.max(a.usedBytes, o + n)), n;
                  },
                  llseek: function (e, r, t) {
                    var n = r;
                    if (
                      (1 === t ? (n += e.position) : 2 === t && we.isFile(e.node.mode) && (n += e.node.usedBytes),
                      n < 0)
                    )
                      throw new we.ErrnoError(28);
                    return n;
                  },
                  allocate: function (e, r, t) {
                    pe.expandFileStorage(e.node, r + t), (e.node.usedBytes = Math.max(e.node.usedBytes, r + t));
                  },
                  mmap: function (e, r, t, n, o) {
                    if (!we.isFile(e.node.mode)) throw new we.ErrnoError(43);
                    var i,
                      a,
                      s = e.node.contents;
                    if (2 & o || s.buffer !== M) {
                      if (
                        ((t > 0 || t + r < s.length) &&
                          (s = s.subarray ? s.subarray(t, t + r) : Array.prototype.slice.call(s, t, t + r)),
                        (a = !0),
                        !(i = me()))
                      )
                        throw new we.ErrnoError(48);
                      F.set(s, i);
                    } else (a = !1), (i = s.byteOffset);
                    return { ptr: i, allocated: a };
                  },
                  msync: function (e, r, t, n, o) {
                    if (!we.isFile(e.node.mode)) throw new we.ErrnoError(43);
                    return 2 & o || pe.stream_ops.write(e, r, 0, n, t, !1), 0;
                  },
                },
              };
              var we = {
                  root: null,
                  mounts: [],
                  devices: {},
                  streams: [],
                  nextInode: 1,
                  nameTable: null,
                  currentPath: "/",
                  initialized: !1,
                  ignorePermissions: !0,
                  ErrnoError: null,
                  genericErrors: {},
                  filesystems: null,
                  syncFSRequests: 0,
                  lookupPath: (e, r = {}) => {
                    if (!(e = fe.resolve(we.cwd(), e))) return { path: "", node: null };
                    if ((r = Object.assign({ follow_mount: !0, recurse_count: 0 }, r)).recurse_count > 8)
                      throw new we.ErrnoError(32);
                    for (
                      var t = le.normalizeArray(
                          e.split("/").filter((e) => !!e),
                          !1
                        ),
                        n = we.root,
                        o = "/",
                        i = 0;
                      i < t.length;
                      i++
                    ) {
                      var a = i === t.length - 1;
                      if (a && r.parent) break;
                      if (
                        ((n = we.lookupNode(n, t[i])),
                        (o = le.join2(o, t[i])),
                        we.isMountpoint(n) && (!a || (a && r.follow_mount)) && (n = n.mounted.root),
                        !a || r.follow)
                      )
                        for (var s = 0; we.isLink(n.mode); ) {
                          var u = we.readlink(o);
                          if (
                            ((o = fe.resolve(le.dirname(o), u)),
                            (n = we.lookupPath(o, { recurse_count: r.recurse_count + 1 }).node),
                            s++ > 40)
                          )
                            throw new we.ErrnoError(32);
                        }
                    }
                    return { path: o, node: n };
                  },
                  getPath: (e) => {
                    for (var r; ; ) {
                      if (we.isRoot(e)) {
                        var t = e.mount.mountpoint;
                        return r ? ("/" !== t[t.length - 1] ? t + "/" + r : t + r) : t;
                      }
                      (r = r ? e.name + "/" + r : e.name), (e = e.parent);
                    }
                  },
                  hashName: (e, r) => {
                    for (var t = 0, n = 0; n < r.length; n++) t = ((t << 5) - t + r.charCodeAt(n)) | 0;
                    return ((e + t) >>> 0) % we.nameTable.length;
                  },
                  hashAddNode: (e) => {
                    var r = we.hashName(e.parent.id, e.name);
                    (e.name_next = we.nameTable[r]), (we.nameTable[r] = e);
                  },
                  hashRemoveNode: (e) => {
                    var r = we.hashName(e.parent.id, e.name);
                    if (we.nameTable[r] === e) we.nameTable[r] = e.name_next;
                    else
                      for (var t = we.nameTable[r]; t; ) {
                        if (t.name_next === e) {
                          t.name_next = e.name_next;
                          break;
                        }
                        t = t.name_next;
                      }
                  },
                  lookupNode: (e, r) => {
                    var t = we.mayLookup(e);
                    if (t) throw new we.ErrnoError(t, e);
                    for (var n = we.hashName(e.id, r), o = we.nameTable[n]; o; o = o.name_next) {
                      var i = o.name;
                      if (o.parent.id === e.id && i === r) return o;
                    }
                    return we.lookup(e, r);
                  },
                  createNode: (e, r, t, n) => {
                    var o = new we.FSNode(e, r, t, n);
                    return we.hashAddNode(o), o;
                  },
                  destroyNode: (e) => {
                    we.hashRemoveNode(e);
                  },
                  isRoot: (e) => e === e.parent,
                  isMountpoint: (e) => !!e.mounted,
                  isFile: (e) => 32768 == (61440 & e),
                  isDir: (e) => 16384 == (61440 & e),
                  isLink: (e) => 40960 == (61440 & e),
                  isChrdev: (e) => 8192 == (61440 & e),
                  isBlkdev: (e) => 24576 == (61440 & e),
                  isFIFO: (e) => 4096 == (61440 & e),
                  isSocket: (e) => !(49152 & ~e),
                  flagModes: { r: 0, "r+": 2, w: 577, "w+": 578, a: 1089, "a+": 1090 },
                  modeStringToFlags: (e) => {
                    var r = we.flagModes[e];
                    if (void 0 === r) throw new Error("Unknown file open mode: " + e);
                    return r;
                  },
                  flagsToPermissionString: (e) => {
                    var r = ["r", "w", "rw"][3 & e];
                    return 512 & e && (r += "w"), r;
                  },
                  nodePermissions: (e, r) =>
                    we.ignorePermissions ||
                    ((!r.includes("r") || 292 & e.mode) &&
                      (!r.includes("w") || 146 & e.mode) &&
                      (!r.includes("x") || 73 & e.mode))
                      ? 0
                      : 2,
                  mayLookup: (e) => we.nodePermissions(e, "x") || (e.node_ops.lookup ? 0 : 2),
                  mayCreate: (e, r) => {
                    try {
                      return we.lookupNode(e, r), 20;
                    } catch (e) {}
                    return we.nodePermissions(e, "wx");
                  },
                  mayDelete: (e, r, t) => {
                    var n;
                    try {
                      n = we.lookupNode(e, r);
                    } catch (e) {
                      return e.errno;
                    }
                    var o = we.nodePermissions(e, "wx");
                    if (o) return o;
                    if (t) {
                      if (!we.isDir(n.mode)) return 54;
                      if (we.isRoot(n) || we.getPath(n) === we.cwd()) return 10;
                    } else if (we.isDir(n.mode)) return 31;
                    return 0;
                  },
                  mayOpen: (e, r) =>
                    e
                      ? we.isLink(e.mode)
                        ? 32
                        : we.isDir(e.mode) && ("r" !== we.flagsToPermissionString(r) || 512 & r)
                        ? 31
                        : we.nodePermissions(e, we.flagsToPermissionString(r))
                      : 44,
                  MAX_OPEN_FDS: 4096,
                  nextfd: (e = 0, r = we.MAX_OPEN_FDS) => {
                    for (var t = e; t <= r; t++) if (!we.streams[t]) return t;
                    throw new we.ErrnoError(33);
                  },
                  getStream: (e) => we.streams[e],
                  createStream: (e, r, t) => {
                    we.FSStream ||
                      ((we.FSStream = function () {
                        this.shared = {};
                      }),
                      (we.FSStream.prototype = {}),
                      Object.defineProperties(we.FSStream.prototype, {
                        object: {
                          get: function () {
                            return this.node;
                          },
                          set: function (e) {
                            this.node = e;
                          },
                        },
                        isRead: {
                          get: function () {
                            return 1 != (2097155 & this.flags);
                          },
                        },
                        isWrite: {
                          get: function () {
                            return !!(2097155 & this.flags);
                          },
                        },
                        isAppend: {
                          get: function () {
                            return 1024 & this.flags;
                          },
                        },
                        flags: {
                          get: function () {
                            return this.shared.flags;
                          },
                          set: function (e) {
                            this.shared.flags = e;
                          },
                        },
                        position: {
                          get: function () {
                            return this.shared.position;
                          },
                          set: function (e) {
                            this.shared.position = e;
                          },
                        },
                      })),
                      (e = Object.assign(new we.FSStream(), e));
                    var n = we.nextfd(r, t);
                    return (e.fd = n), (we.streams[n] = e), e;
                  },
                  closeStream: (e) => {
                    we.streams[e] = null;
                  },
                  chrdev_stream_ops: {
                    open: (e) => {
                      var r = we.getDevice(e.node.rdev);
                      (e.stream_ops = r.stream_ops), e.stream_ops.open && e.stream_ops.open(e);
                    },
                    llseek: () => {
                      throw new we.ErrnoError(70);
                    },
                  },
                  major: (e) => e >> 8,
                  minor: (e) => 255 & e,
                  makedev: (e, r) => (e << 8) | r,
                  registerDevice: (e, r) => {
                    we.devices[e] = { stream_ops: r };
                  },
                  getDevice: (e) => we.devices[e],
                  getMounts: (e) => {
                    for (var r = [], t = [e]; t.length; ) {
                      var n = t.pop();
                      r.push(n), t.push.apply(t, n.mounts);
                    }
                    return r;
                  },
                  syncfs: (e, r) => {
                    "function" == typeof e && ((r = e), (e = !1)),
                      we.syncFSRequests++,
                      we.syncFSRequests > 1 &&
                        E(
                          "warning: " +
                            we.syncFSRequests +
                            " FS.syncfs operations in flight at once, probably just doing extra work"
                        );
                    var t = we.getMounts(we.root.mount),
                      n = 0;
                    function o(e) {
                      return we.syncFSRequests--, r(e);
                    }
                    function i(e) {
                      if (e) return i.errored ? void 0 : ((i.errored = !0), o(e));
                      ++n >= t.length && o(null);
                    }
                    t.forEach((r) => {
                      if (!r.type.syncfs) return i(null);
                      r.type.syncfs(r, e, i);
                    });
                  },
                  mount: (e, r, t) => {
                    var n,
                      o = "/" === t,
                      i = !t;
                    if (o && we.root) throw new we.ErrnoError(10);
                    if (!o && !i) {
                      var a = we.lookupPath(t, { follow_mount: !1 });
                      if (((t = a.path), (n = a.node), we.isMountpoint(n))) throw new we.ErrnoError(10);
                      if (!we.isDir(n.mode)) throw new we.ErrnoError(54);
                    }
                    var s = { type: e, opts: r, mountpoint: t, mounts: [] },
                      u = e.mount(s);
                    return (
                      (u.mount = s),
                      (s.root = u),
                      o ? (we.root = u) : n && ((n.mounted = s), n.mount && n.mount.mounts.push(s)),
                      u
                    );
                  },
                  unmount: (e) => {
                    var r = we.lookupPath(e, { follow_mount: !1 });
                    if (!we.isMountpoint(r.node)) throw new we.ErrnoError(28);
                    var t = r.node,
                      n = t.mounted,
                      o = we.getMounts(n);
                    Object.keys(we.nameTable).forEach((e) => {
                      for (var r = we.nameTable[e]; r; ) {
                        var t = r.name_next;
                        o.includes(r.mount) && we.destroyNode(r), (r = t);
                      }
                    }),
                      (t.mounted = null);
                    var i = t.mount.mounts.indexOf(n);
                    t.mount.mounts.splice(i, 1);
                  },
                  lookup: (e, r) => e.node_ops.lookup(e, r),
                  mknod: (e, r, t) => {
                    var n = we.lookupPath(e, { parent: !0 }).node,
                      o = le.basename(e);
                    if (!o || "." === o || ".." === o) throw new we.ErrnoError(28);
                    var i = we.mayCreate(n, o);
                    if (i) throw new we.ErrnoError(i);
                    if (!n.node_ops.mknod) throw new we.ErrnoError(63);
                    return n.node_ops.mknod(n, o, r, t);
                  },
                  create: (e, r) => ((r = void 0 !== r ? r : 438), (r &= 4095), (r |= 32768), we.mknod(e, r, 0)),
                  mkdir: (e, r) => ((r = void 0 !== r ? r : 511), (r &= 1023), (r |= 16384), we.mknod(e, r, 0)),
                  mkdirTree: (e, r) => {
                    for (var t = e.split("/"), n = "", o = 0; o < t.length; ++o)
                      if (t[o]) {
                        n += "/" + t[o];
                        try {
                          we.mkdir(n, r);
                        } catch (e) {
                          if (20 != e.errno) throw e;
                        }
                      }
                  },
                  mkdev: (e, r, t) => (void 0 === t && ((t = r), (r = 438)), (r |= 8192), we.mknod(e, r, t)),
                  symlink: (e, r) => {
                    if (!fe.resolve(e)) throw new we.ErrnoError(44);
                    var t = we.lookupPath(r, { parent: !0 }).node;
                    if (!t) throw new we.ErrnoError(44);
                    var n = le.basename(r),
                      o = we.mayCreate(t, n);
                    if (o) throw new we.ErrnoError(o);
                    if (!t.node_ops.symlink) throw new we.ErrnoError(63);
                    return t.node_ops.symlink(t, n, e);
                  },
                  rename: (e, r) => {
                    var t,
                      n,
                      o = le.dirname(e),
                      i = le.dirname(r),
                      a = le.basename(e),
                      s = le.basename(r);
                    if (
                      ((t = we.lookupPath(e, { parent: !0 }).node),
                      (n = we.lookupPath(r, { parent: !0 }).node),
                      !t || !n)
                    )
                      throw new we.ErrnoError(44);
                    if (t.mount !== n.mount) throw new we.ErrnoError(75);
                    var u,
                      c = we.lookupNode(t, a),
                      l = fe.relative(e, i);
                    if ("." !== l.charAt(0)) throw new we.ErrnoError(28);
                    if ("." !== (l = fe.relative(r, o)).charAt(0)) throw new we.ErrnoError(55);
                    try {
                      u = we.lookupNode(n, s);
                    } catch (e) {}
                    if (c !== u) {
                      var f = we.isDir(c.mode),
                        d = we.mayDelete(t, a, f);
                      if (d) throw new we.ErrnoError(d);
                      if ((d = u ? we.mayDelete(n, s, f) : we.mayCreate(n, s))) throw new we.ErrnoError(d);
                      if (!t.node_ops.rename) throw new we.ErrnoError(63);
                      if (we.isMountpoint(c) || (u && we.isMountpoint(u))) throw new we.ErrnoError(10);
                      if (n !== t && (d = we.nodePermissions(t, "w"))) throw new we.ErrnoError(d);
                      we.hashRemoveNode(c);
                      try {
                        t.node_ops.rename(c, n, s);
                      } catch (e) {
                        throw e;
                      } finally {
                        we.hashAddNode(c);
                      }
                    }
                  },
                  rmdir: (e) => {
                    var r = we.lookupPath(e, { parent: !0 }).node,
                      t = le.basename(e),
                      n = we.lookupNode(r, t),
                      o = we.mayDelete(r, t, !0);
                    if (o) throw new we.ErrnoError(o);
                    if (!r.node_ops.rmdir) throw new we.ErrnoError(63);
                    if (we.isMountpoint(n)) throw new we.ErrnoError(10);
                    r.node_ops.rmdir(r, t), we.destroyNode(n);
                  },
                  readdir: (e) => {
                    var r = we.lookupPath(e, { follow: !0 }).node;
                    if (!r.node_ops.readdir) throw new we.ErrnoError(54);
                    return r.node_ops.readdir(r);
                  },
                  unlink: (e) => {
                    var r = we.lookupPath(e, { parent: !0 }).node;
                    if (!r) throw new we.ErrnoError(44);
                    var t = le.basename(e),
                      n = we.lookupNode(r, t),
                      o = we.mayDelete(r, t, !1);
                    if (o) throw new we.ErrnoError(o);
                    if (!r.node_ops.unlink) throw new we.ErrnoError(63);
                    if (we.isMountpoint(n)) throw new we.ErrnoError(10);
                    r.node_ops.unlink(r, t), we.destroyNode(n);
                  },
                  readlink: (e) => {
                    var r = we.lookupPath(e).node;
                    if (!r) throw new we.ErrnoError(44);
                    if (!r.node_ops.readlink) throw new we.ErrnoError(28);
                    return fe.resolve(we.getPath(r.parent), r.node_ops.readlink(r));
                  },
                  stat: (e, r) => {
                    var t = we.lookupPath(e, { follow: !r }).node;
                    if (!t) throw new we.ErrnoError(44);
                    if (!t.node_ops.getattr) throw new we.ErrnoError(63);
                    return t.node_ops.getattr(t);
                  },
                  lstat: (e) => we.stat(e, !0),
                  chmod: (e, r, t) => {
                    var n;
                    if (!(n = "string" == typeof e ? we.lookupPath(e, { follow: !t }).node : e).node_ops.setattr)
                      throw new we.ErrnoError(63);
                    n.node_ops.setattr(n, { mode: (4095 & r) | (-4096 & n.mode), timestamp: Date.now() });
                  },
                  lchmod: (e, r) => {
                    we.chmod(e, r, !0);
                  },
                  fchmod: (e, r) => {
                    var t = we.getStream(e);
                    if (!t) throw new we.ErrnoError(8);
                    we.chmod(t.node, r);
                  },
                  chown: (e, r, t, n) => {
                    var o;
                    if (!(o = "string" == typeof e ? we.lookupPath(e, { follow: !n }).node : e).node_ops.setattr)
                      throw new we.ErrnoError(63);
                    o.node_ops.setattr(o, { timestamp: Date.now() });
                  },
                  lchown: (e, r, t) => {
                    we.chown(e, r, t, !0);
                  },
                  fchown: (e, r, t) => {
                    var n = we.getStream(e);
                    if (!n) throw new we.ErrnoError(8);
                    we.chown(n.node, r, t);
                  },
                  truncate: (e, r) => {
                    if (r < 0) throw new we.ErrnoError(28);
                    var t;
                    if (!(t = "string" == typeof e ? we.lookupPath(e, { follow: !0 }).node : e).node_ops.setattr)
                      throw new we.ErrnoError(63);
                    if (we.isDir(t.mode)) throw new we.ErrnoError(31);
                    if (!we.isFile(t.mode)) throw new we.ErrnoError(28);
                    var n = we.nodePermissions(t, "w");
                    if (n) throw new we.ErrnoError(n);
                    t.node_ops.setattr(t, { size: r, timestamp: Date.now() });
                  },
                  ftruncate: (e, r) => {
                    var t = we.getStream(e);
                    if (!t) throw new we.ErrnoError(8);
                    if (!(2097155 & t.flags)) throw new we.ErrnoError(28);
                    we.truncate(t.node, r);
                  },
                  utime: (e, r, t) => {
                    var n = we.lookupPath(e, { follow: !0 }).node;
                    n.node_ops.setattr(n, { timestamp: Math.max(r, t) });
                  },
                  open: (r, t, n) => {
                    if ("" === r) throw new we.ErrnoError(44);
                    var o;
                    if (
                      ((n = void 0 === n ? 438 : n),
                      (n = 64 & (t = "string" == typeof t ? we.modeStringToFlags(t) : t) ? (4095 & n) | 32768 : 0),
                      "object" == typeof r)
                    )
                      o = r;
                    else {
                      r = le.normalize(r);
                      try {
                        o = we.lookupPath(r, { follow: !(131072 & t) }).node;
                      } catch (e) {}
                    }
                    var i = !1;
                    if (64 & t)
                      if (o) {
                        if (128 & t) throw new we.ErrnoError(20);
                      } else (o = we.mknod(r, n, 0)), (i = !0);
                    if (!o) throw new we.ErrnoError(44);
                    if ((we.isChrdev(o.mode) && (t &= -513), 65536 & t && !we.isDir(o.mode)))
                      throw new we.ErrnoError(54);
                    if (!i) {
                      var a = we.mayOpen(o, t);
                      if (a) throw new we.ErrnoError(a);
                    }
                    512 & t && !i && we.truncate(o, 0), (t &= -131713);
                    var s = we.createStream({
                      node: o,
                      path: we.getPath(o),
                      flags: t,
                      seekable: !0,
                      position: 0,
                      stream_ops: o.stream_ops,
                      ungotten: [],
                      error: !1,
                    });
                    return (
                      s.stream_ops.open && s.stream_ops.open(s),
                      !e.logReadFiles ||
                        1 & t ||
                        (we.readFiles || (we.readFiles = {}), r in we.readFiles || (we.readFiles[r] = 1)),
                      s
                    );
                  },
                  close: (e) => {
                    if (we.isClosed(e)) throw new we.ErrnoError(8);
                    e.getdents && (e.getdents = null);
                    try {
                      e.stream_ops.close && e.stream_ops.close(e);
                    } catch (e) {
                      throw e;
                    } finally {
                      we.closeStream(e.fd);
                    }
                    e.fd = null;
                  },
                  isClosed: (e) => null === e.fd,
                  llseek: (e, r, t) => {
                    if (we.isClosed(e)) throw new we.ErrnoError(8);
                    if (!e.seekable || !e.stream_ops.llseek) throw new we.ErrnoError(70);
                    if (0 != t && 1 != t && 2 != t) throw new we.ErrnoError(28);
                    return (e.position = e.stream_ops.llseek(e, r, t)), (e.ungotten = []), e.position;
                  },
                  read: (e, r, t, n, o) => {
                    if (n < 0 || o < 0) throw new we.ErrnoError(28);
                    if (we.isClosed(e)) throw new we.ErrnoError(8);
                    if (1 == (2097155 & e.flags)) throw new we.ErrnoError(8);
                    if (we.isDir(e.node.mode)) throw new we.ErrnoError(31);
                    if (!e.stream_ops.read) throw new we.ErrnoError(28);
                    var i = void 0 !== o;
                    if (i) {
                      if (!e.seekable) throw new we.ErrnoError(70);
                    } else o = e.position;
                    var a = e.stream_ops.read(e, r, t, n, o);
                    return i || (e.position += a), a;
                  },
                  write: (e, r, t, n, o, i) => {
                    if (n < 0 || o < 0) throw new we.ErrnoError(28);
                    if (we.isClosed(e)) throw new we.ErrnoError(8);
                    if (!(2097155 & e.flags)) throw new we.ErrnoError(8);
                    if (we.isDir(e.node.mode)) throw new we.ErrnoError(31);
                    if (!e.stream_ops.write) throw new we.ErrnoError(28);
                    e.seekable && 1024 & e.flags && we.llseek(e, 0, 2);
                    var a = void 0 !== o;
                    if (a) {
                      if (!e.seekable) throw new we.ErrnoError(70);
                    } else o = e.position;
                    var s = e.stream_ops.write(e, r, t, n, o, i);
                    return a || (e.position += s), s;
                  },
                  allocate: (e, r, t) => {
                    if (we.isClosed(e)) throw new we.ErrnoError(8);
                    if (r < 0 || t <= 0) throw new we.ErrnoError(28);
                    if (!(2097155 & e.flags)) throw new we.ErrnoError(8);
                    if (!we.isFile(e.node.mode) && !we.isDir(e.node.mode)) throw new we.ErrnoError(43);
                    if (!e.stream_ops.allocate) throw new we.ErrnoError(138);
                    e.stream_ops.allocate(e, r, t);
                  },
                  mmap: (e, r, t, n, o) => {
                    if (2 & n && !(2 & o) && 2 != (2097155 & e.flags)) throw new we.ErrnoError(2);
                    if (1 == (2097155 & e.flags)) throw new we.ErrnoError(2);
                    if (!e.stream_ops.mmap) throw new we.ErrnoError(43);
                    return e.stream_ops.mmap(e, r, t, n, o);
                  },
                  msync: (e, r, t, n, o) => (e && e.stream_ops.msync ? e.stream_ops.msync(e, r, t, n, o) : 0),
                  munmap: (e) => 0,
                  ioctl: (e, r, t) => {
                    if (!e.stream_ops.ioctl) throw new we.ErrnoError(59);
                    return e.stream_ops.ioctl(e, r, t);
                  },
                  readFile: (e, r = {}) => {
                    if (
                      ((r.flags = r.flags || 0),
                      (r.encoding = r.encoding || "binary"),
                      "utf8" !== r.encoding && "binary" !== r.encoding)
                    )
                      throw new Error('Invalid encoding type "' + r.encoding + '"');
                    var t,
                      n = we.open(e, r.flags),
                      o = we.stat(e).size,
                      i = new Uint8Array(o);
                    return (
                      we.read(n, i, 0, o, 0),
                      "utf8" === r.encoding ? (t = j(i, 0)) : "binary" === r.encoding && (t = i),
                      we.close(n),
                      t
                    );
                  },
                  writeFile: (e, r, t = {}) => {
                    t.flags = t.flags || 577;
                    var n = we.open(e, t.flags, t.mode);
                    if ("string" == typeof r) {
                      var o = new Uint8Array(B(r) + 1),
                        i = N(r, o, 0, o.length);
                      we.write(n, o, 0, i, void 0, t.canOwn);
                    } else {
                      if (!ArrayBuffer.isView(r)) throw new Error("Unsupported data type");
                      we.write(n, r, 0, r.byteLength, void 0, t.canOwn);
                    }
                    we.close(n);
                  },
                  cwd: () => we.currentPath,
                  chdir: (e) => {
                    var r = we.lookupPath(e, { follow: !0 });
                    if (null === r.node) throw new we.ErrnoError(44);
                    if (!we.isDir(r.node.mode)) throw new we.ErrnoError(54);
                    var t = we.nodePermissions(r.node, "x");
                    if (t) throw new we.ErrnoError(t);
                    we.currentPath = r.path;
                  },
                  createDefaultDirectories: () => {
                    we.mkdir("/tmp"), we.mkdir("/home"), we.mkdir("/home/web_user");
                  },
                  createDefaultDevices: () => {
                    we.mkdir("/dev"),
                      we.registerDevice(we.makedev(1, 3), { read: () => 0, write: (e, r, t, n, o) => n }),
                      we.mkdev("/dev/null", we.makedev(1, 3)),
                      he.register(we.makedev(5, 0), he.default_tty_ops),
                      he.register(we.makedev(6, 0), he.default_tty1_ops),
                      we.mkdev("/dev/tty", we.makedev(5, 0)),
                      we.mkdev("/dev/tty1", we.makedev(6, 0));
                    var e = (function () {
                      if ("object" == typeof crypto && "function" == typeof crypto.getRandomValues) {
                        var e = new Uint8Array(1);
                        return () => (crypto.getRandomValues(e), e[0]);
                      }
                      if (v)
                        try {
                          var r = t(401);
                          return () => r.randomBytes(1)[0];
                        } catch (e) {}
                      return () => K("randomDevice");
                    })();
                    we.createDevice("/dev", "random", e),
                      we.createDevice("/dev", "urandom", e),
                      we.mkdir("/dev/shm"),
                      we.mkdir("/dev/shm/tmp");
                  },
                  createSpecialDirectories: () => {
                    we.mkdir("/proc");
                    var e = we.mkdir("/proc/self");
                    we.mkdir("/proc/self/fd"),
                      we.mount(
                        {
                          mount: () => {
                            var r = we.createNode(e, "fd", 16895, 73);
                            return (
                              (r.node_ops = {
                                lookup: (e, r) => {
                                  var t = +r,
                                    n = we.getStream(t);
                                  if (!n) throw new we.ErrnoError(8);
                                  var o = {
                                    parent: null,
                                    mount: { mountpoint: "fake" },
                                    node_ops: { readlink: () => n.path },
                                  };
                                  return (o.parent = o), o;
                                },
                              }),
                              r
                            );
                          },
                        },
                        {},
                        "/proc/self/fd"
                      );
                  },
                  createStandardStreams: () => {
                    e.stdin ? we.createDevice("/dev", "stdin", e.stdin) : we.symlink("/dev/tty", "/dev/stdin"),
                      e.stdout
                        ? we.createDevice("/dev", "stdout", null, e.stdout)
                        : we.symlink("/dev/tty", "/dev/stdout"),
                      e.stderr
                        ? we.createDevice("/dev", "stderr", null, e.stderr)
                        : we.symlink("/dev/tty1", "/dev/stderr"),
                      we.open("/dev/stdin", 0),
                      we.open("/dev/stdout", 1),
                      we.open("/dev/stderr", 1);
                  },
                  ensureErrnoError: () => {
                    we.ErrnoError ||
                      ((we.ErrnoError = function (e, r) {
                        (this.node = r),
                          (this.setErrno = function (e) {
                            this.errno = e;
                          }),
                          this.setErrno(e),
                          (this.message = "FS error");
                      }),
                      (we.ErrnoError.prototype = new Error()),
                      (we.ErrnoError.prototype.constructor = we.ErrnoError),
                      [44].forEach((e) => {
                        (we.genericErrors[e] = new we.ErrnoError(e)),
                          (we.genericErrors[e].stack = "<generic error, no stack>");
                      }));
                  },
                  staticInit: () => {
                    we.ensureErrnoError(),
                      (we.nameTable = new Array(4096)),
                      we.mount(pe, {}, "/"),
                      we.createDefaultDirectories(),
                      we.createDefaultDevices(),
                      we.createSpecialDirectories(),
                      (we.filesystems = { MEMFS: pe });
                  },
                  init: (r, t, n) => {
                    (we.init.initialized = !0),
                      we.ensureErrnoError(),
                      (e.stdin = r || e.stdin),
                      (e.stdout = t || e.stdout),
                      (e.stderr = n || e.stderr),
                      we.createStandardStreams();
                  },
                  quit: () => {
                    we.init.initialized = !1;
                    for (var e = 0; e < we.streams.length; e++) {
                      var r = we.streams[e];
                      r && we.close(r);
                    }
                  },
                  getMode: (e, r) => {
                    var t = 0;
                    return e && (t |= 365), r && (t |= 146), t;
                  },
                  findObject: (e, r) => {
                    var t = we.analyzePath(e, r);
                    return t.exists ? t.object : null;
                  },
                  analyzePath: (e, r) => {
                    try {
                      e = (n = we.lookupPath(e, { follow: !r })).path;
                    } catch (e) {}
                    var t = {
                      isRoot: !1,
                      exists: !1,
                      error: 0,
                      name: null,
                      path: null,
                      object: null,
                      parentExists: !1,
                      parentPath: null,
                      parentObject: null,
                    };
                    try {
                      var n = we.lookupPath(e, { parent: !0 });
                      (t.parentExists = !0),
                        (t.parentPath = n.path),
                        (t.parentObject = n.node),
                        (t.name = le.basename(e)),
                        (n = we.lookupPath(e, { follow: !r })),
                        (t.exists = !0),
                        (t.path = n.path),
                        (t.object = n.node),
                        (t.name = n.node.name),
                        (t.isRoot = "/" === n.path);
                    } catch (e) {
                      t.error = e.errno;
                    }
                    return t;
                  },
                  createPath: (e, r, t, n) => {
                    e = "string" == typeof e ? e : we.getPath(e);
                    for (var o = r.split("/").reverse(); o.length; ) {
                      var i = o.pop();
                      if (i) {
                        var a = le.join2(e, i);
                        try {
                          we.mkdir(a);
                        } catch (e) {}
                        e = a;
                      }
                    }
                    return a;
                  },
                  createFile: (e, r, t, n, o) => {
                    var i = le.join2("string" == typeof e ? e : we.getPath(e), r),
                      a = we.getMode(n, o);
                    return we.create(i, a);
                  },
                  createDataFile: (e, r, t, n, o, i) => {
                    var a = r;
                    e && ((e = "string" == typeof e ? e : we.getPath(e)), (a = r ? le.join2(e, r) : e));
                    var s = we.getMode(n, o),
                      u = we.create(a, s);
                    if (t) {
                      if ("string" == typeof t) {
                        for (var c = new Array(t.length), l = 0, f = t.length; l < f; ++l) c[l] = t.charCodeAt(l);
                        t = c;
                      }
                      we.chmod(u, 146 | s);
                      var d = we.open(u, 577);
                      we.write(d, t, 0, t.length, 0, i), we.close(d), we.chmod(u, s);
                    }
                    return u;
                  },
                  createDevice: (e, r, t, n) => {
                    var o = le.join2("string" == typeof e ? e : we.getPath(e), r),
                      i = we.getMode(!!t, !!n);
                    we.createDevice.major || (we.createDevice.major = 64);
                    var a = we.makedev(we.createDevice.major++, 0);
                    return (
                      we.registerDevice(a, {
                        open: (e) => {
                          e.seekable = !1;
                        },
                        close: (e) => {
                          n && n.buffer && n.buffer.length && n(10);
                        },
                        read: (e, r, n, o, i) => {
                          for (var a = 0, s = 0; s < o; s++) {
                            var u;
                            try {
                              u = t();
                            } catch (e) {
                              throw new we.ErrnoError(29);
                            }
                            if (void 0 === u && 0 === a) throw new we.ErrnoError(6);
                            if (null == u) break;
                            a++, (r[n + s] = u);
                          }
                          return a && (e.node.timestamp = Date.now()), a;
                        },
                        write: (e, r, t, o, i) => {
                          for (var a = 0; a < o; a++)
                            try {
                              n(r[t + a]);
                            } catch (e) {
                              throw new we.ErrnoError(29);
                            }
                          return o && (e.node.timestamp = Date.now()), a;
                        },
                      }),
                      we.mkdev(o, i, a)
                    );
                  },
                  forceLoadFile: (e) => {
                    if (e.isDevice || e.isFolder || e.link || e.contents) return !0;
                    if ("undefined" != typeof XMLHttpRequest)
                      throw new Error(
                        "Lazy loading should have been performed (contents set) in createLazyFile, but it was not. Lazy loading only works in web workers. Use --embed-file or --preload-file in emcc on the main thread."
                      );
                    if (!i) throw new Error("Cannot load without read() or XMLHttpRequest.");
                    try {
                      (e.contents = de(i(e.url), !0)), (e.usedBytes = e.contents.length);
                    } catch (e) {
                      throw new we.ErrnoError(29);
                    }
                  },
                  createLazyFile: (e, r, t, n, o) => {
                    function i() {
                      (this.lengthKnown = !1), (this.chunks = []);
                    }
                    if (
                      ((i.prototype.get = function (e) {
                        if (!(e > this.length - 1 || e < 0)) {
                          var r = e % this.chunkSize,
                            t = (e / this.chunkSize) | 0;
                          return this.getter(t)[r];
                        }
                      }),
                      (i.prototype.setDataGetter = function (e) {
                        this.getter = e;
                      }),
                      (i.prototype.cacheLength = function () {
                        var e = new XMLHttpRequest();
                        if (
                          (e.open("HEAD", t, !1),
                          e.send(null),
                          !((e.status >= 200 && e.status < 300) || 304 === e.status))
                        )
                          throw new Error("Couldn't load " + t + ". Status: " + e.status);
                        var r,
                          n = Number(e.getResponseHeader("Content-length")),
                          o = (r = e.getResponseHeader("Accept-Ranges")) && "bytes" === r,
                          i = (r = e.getResponseHeader("Content-Encoding")) && "gzip" === r,
                          a = 1048576;
                        o || (a = n);
                        var s = this;
                        s.setDataGetter((e) => {
                          var r = e * a,
                            o = (e + 1) * a - 1;
                          if (
                            ((o = Math.min(o, n - 1)),
                            void 0 === s.chunks[e] &&
                              (s.chunks[e] = ((e, r) => {
                                if (e > r)
                                  throw new Error("invalid range (" + e + ", " + r + ") or no bytes requested!");
                                if (r > n - 1) throw new Error("only " + n + " bytes available! programmer error!");
                                var o = new XMLHttpRequest();
                                if (
                                  (o.open("GET", t, !1),
                                  n !== a && o.setRequestHeader("Range", "bytes=" + e + "-" + r),
                                  (o.responseType = "arraybuffer"),
                                  o.overrideMimeType && o.overrideMimeType("text/plain; charset=x-user-defined"),
                                  o.send(null),
                                  !((o.status >= 200 && o.status < 300) || 304 === o.status))
                                )
                                  throw new Error("Couldn't load " + t + ". Status: " + o.status);
                                return void 0 !== o.response
                                  ? new Uint8Array(o.response || [])
                                  : de(o.responseText || "", !0);
                              })(r, o)),
                            void 0 === s.chunks[e])
                          )
                            throw new Error("doXHR failed!");
                          return s.chunks[e];
                        }),
                          (!i && n) ||
                            ((a = n = 1),
                            (n = this.getter(0).length),
                            (a = n),
                            y("LazyFiles on gzip forces download of the whole file when length is accessed")),
                          (this._length = n),
                          (this._chunkSize = a),
                          (this.lengthKnown = !0);
                      }),
                      "undefined" != typeof XMLHttpRequest)
                    ) {
                      if (!w)
                        throw "Cannot do synchronous binary XHRs outside webworkers in modern browsers. Use --embed-file or --preload-file in emcc";
                      var a = new i();
                      Object.defineProperties(a, {
                        length: {
                          get: function () {
                            return this.lengthKnown || this.cacheLength(), this._length;
                          },
                        },
                        chunkSize: {
                          get: function () {
                            return this.lengthKnown || this.cacheLength(), this._chunkSize;
                          },
                        },
                      });
                      var s = { isDevice: !1, contents: a };
                    } else s = { isDevice: !1, url: t };
                    var u = we.createFile(e, r, s, n, o);
                    s.contents ? (u.contents = s.contents) : s.url && ((u.contents = null), (u.url = s.url)),
                      Object.defineProperties(u, {
                        usedBytes: {
                          get: function () {
                            return this.contents.length;
                          },
                        },
                      });
                    var c = {};
                    function l(e, r, t, n, o) {
                      var i = e.node.contents;
                      if (o >= i.length) return 0;
                      var a = Math.min(i.length - o, n);
                      if (i.slice) for (var s = 0; s < a; s++) r[t + s] = i[o + s];
                      else for (s = 0; s < a; s++) r[t + s] = i.get(o + s);
                      return a;
                    }
                    return (
                      Object.keys(u.stream_ops).forEach((e) => {
                        var r = u.stream_ops[e];
                        c[e] = function () {
                          return we.forceLoadFile(u), r.apply(null, arguments);
                        };
                      }),
                      (c.read = (e, r, t, n, o) => (we.forceLoadFile(u), l(e, r, t, n, o))),
                      (c.mmap = (e, r, t, n, o) => {
                        we.forceLoadFile(u);
                        var i = me();
                        if (!i) throw new we.ErrnoError(48);
                        return l(e, F, i, r, t), { ptr: i, allocated: !0 };
                      }),
                      (u.stream_ops = c),
                      u
                    );
                  },
                  createPreloadedFile: (e, r, t, n, o, i, s, u, c, l) => {
                    var f = r ? fe.resolve(le.join2(e, r)) : e;
                    function d(t) {
                      function a(t) {
                        l && l(), u || we.createDataFile(e, r, t, n, o, c), i && i(), V();
                      }
                      Browser.handledByPreloadPlugin(t, f, a, () => {
                        s && s(), V();
                      }) || a(t);
                    }
                    X(),
                      "string" == typeof t
                        ? (function (e, r, t, n) {
                            var o = n ? "" : "al " + e;
                            a(
                              e,
                              (t) => {
                                t || K('Loading data file "' + e + '" failed (no arrayBuffer).'),
                                  r(new Uint8Array(t)),
                                  o && V();
                              },
                              (r) => {
                                if (!t) throw 'Loading data file "' + e + '" failed.';
                                t();
                              }
                            ),
                              o && X();
                          })(t, (e) => d(e), s)
                        : d(t);
                  },
                  indexedDB: () =>
                    window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || window.msIndexedDB,
                  DB_NAME: () => "EM_FS_" + window.location.pathname,
                  DB_VERSION: 20,
                  DB_STORE_NAME: "FILE_DATA",
                  saveFilesToDB: (e, r, t) => {
                    (r = r || (() => {})), (t = t || (() => {}));
                    var n = we.indexedDB();
                    try {
                      var o = n.open(we.DB_NAME(), we.DB_VERSION);
                    } catch (e) {
                      return t(e);
                    }
                    (o.onupgradeneeded = () => {
                      y("creating db"), o.result.createObjectStore(we.DB_STORE_NAME);
                    }),
                      (o.onsuccess = () => {
                        var n = o.result.transaction([we.DB_STORE_NAME], "readwrite"),
                          i = n.objectStore(we.DB_STORE_NAME),
                          a = 0,
                          s = 0,
                          u = e.length;
                        function c() {
                          0 == s ? r() : t();
                        }
                        e.forEach((e) => {
                          var r = i.put(we.analyzePath(e).object.contents, e);
                          (r.onsuccess = () => {
                            ++a + s == u && c();
                          }),
                            (r.onerror = () => {
                              s++, a + s == u && c();
                            });
                        }),
                          (n.onerror = t);
                      }),
                      (o.onerror = t);
                  },
                  loadFilesFromDB: (e, r, t) => {
                    (r = r || (() => {})), (t = t || (() => {}));
                    var n = we.indexedDB();
                    try {
                      var o = n.open(we.DB_NAME(), we.DB_VERSION);
                    } catch (e) {
                      return t(e);
                    }
                    (o.onupgradeneeded = t),
                      (o.onsuccess = () => {
                        var n = o.result;
                        try {
                          var i = n.transaction([we.DB_STORE_NAME], "readonly");
                        } catch (e) {
                          return void t(e);
                        }
                        var a = i.objectStore(we.DB_STORE_NAME),
                          s = 0,
                          u = 0,
                          c = e.length;
                        function l() {
                          0 == u ? r() : t();
                        }
                        e.forEach((e) => {
                          var r = a.get(e);
                          (r.onsuccess = () => {
                            we.analyzePath(e).exists && we.unlink(e),
                              we.createDataFile(le.dirname(e), le.basename(e), r.result, !0, !0, !0),
                              ++s + u == c && l();
                          }),
                            (r.onerror = () => {
                              u++, s + u == c && l();
                            });
                        }),
                          (i.onerror = t);
                      }),
                      (o.onerror = t);
                  },
                },
                ve = {
                  DEFAULT_POLLMASK: 5,
                  calculateAt: function (e, r, t) {
                    if (le.isAbs(r)) return r;
                    var n;
                    if (-100 === e) n = we.cwd();
                    else {
                      var o = we.getStream(e);
                      if (!o) throw new we.ErrnoError(8);
                      n = o.path;
                    }
                    if (0 == r.length) {
                      if (!t) throw new we.ErrnoError(44);
                      return n;
                    }
                    return le.join2(n, r);
                  },
                  doStat: function (e, r, t) {
                    try {
                      var n = e(r);
                    } catch (e) {
                      if (e && e.node && le.normalize(r) !== le.normalize(we.getPath(e.node))) return -54;
                      throw e;
                    }
                    return (
                      (x[t >> 2] = n.dev),
                      (x[(t + 8) >> 2] = n.ino),
                      (x[(t + 12) >> 2] = n.mode),
                      (x[(t + 16) >> 2] = n.nlink),
                      (x[(t + 20) >> 2] = n.uid),
                      (x[(t + 24) >> 2] = n.gid),
                      (x[(t + 28) >> 2] = n.rdev),
                      (Z = [
                        n.size >>> 0,
                        ((Q = n.size),
                        +Math.abs(Q) >= 1
                          ? Q > 0
                            ? (0 | Math.min(+Math.floor(Q / 4294967296), 4294967295)) >>> 0
                            : ~~+Math.ceil((Q - +(~~Q >>> 0)) / 4294967296) >>> 0
                          : 0),
                      ]),
                      (x[(t + 40) >> 2] = Z[0]),
                      (x[(t + 44) >> 2] = Z[1]),
                      (x[(t + 48) >> 2] = 4096),
                      (x[(t + 52) >> 2] = n.blocks),
                      (Z = [
                        Math.floor(n.atime.getTime() / 1e3) >>> 0,
                        ((Q = Math.floor(n.atime.getTime() / 1e3)),
                        +Math.abs(Q) >= 1
                          ? Q > 0
                            ? (0 | Math.min(+Math.floor(Q / 4294967296), 4294967295)) >>> 0
                            : ~~+Math.ceil((Q - +(~~Q >>> 0)) / 4294967296) >>> 0
                          : 0),
                      ]),
                      (x[(t + 56) >> 2] = Z[0]),
                      (x[(t + 60) >> 2] = Z[1]),
                      (x[(t + 64) >> 2] = 0),
                      (Z = [
                        Math.floor(n.mtime.getTime() / 1e3) >>> 0,
                        ((Q = Math.floor(n.mtime.getTime() / 1e3)),
                        +Math.abs(Q) >= 1
                          ? Q > 0
                            ? (0 | Math.min(+Math.floor(Q / 4294967296), 4294967295)) >>> 0
                            : ~~+Math.ceil((Q - +(~~Q >>> 0)) / 4294967296) >>> 0
                          : 0),
                      ]),
                      (x[(t + 72) >> 2] = Z[0]),
                      (x[(t + 76) >> 2] = Z[1]),
                      (x[(t + 80) >> 2] = 0),
                      (Z = [
                        Math.floor(n.ctime.getTime() / 1e3) >>> 0,
                        ((Q = Math.floor(n.ctime.getTime() / 1e3)),
                        +Math.abs(Q) >= 1
                          ? Q > 0
                            ? (0 | Math.min(+Math.floor(Q / 4294967296), 4294967295)) >>> 0
                            : ~~+Math.ceil((Q - +(~~Q >>> 0)) / 4294967296) >>> 0
                          : 0),
                      ]),
                      (x[(t + 88) >> 2] = Z[0]),
                      (x[(t + 92) >> 2] = Z[1]),
                      (x[(t + 96) >> 2] = 0),
                      (Z = [
                        n.ino >>> 0,
                        ((Q = n.ino),
                        +Math.abs(Q) >= 1
                          ? Q > 0
                            ? (0 | Math.min(+Math.floor(Q / 4294967296), 4294967295)) >>> 0
                            : ~~+Math.ceil((Q - +(~~Q >>> 0)) / 4294967296) >>> 0
                          : 0),
                      ]),
                      (x[(t + 104) >> 2] = Z[0]),
                      (x[(t + 108) >> 2] = Z[1]),
                      0
                    );
                  },
                  doMsync: function (e, r, t, n, o) {
                    var i = A.slice(e, e + t);
                    we.msync(r, i, o, t, n);
                  },
                  varargs: void 0,
                  get: function () {
                    return (ve.varargs += 4), x[(ve.varargs - 4) >> 2];
                  },
                  getStr: function (e) {
                    return z(e);
                  },
                  getStreamFromFD: function (e) {
                    var r = we.getStream(e);
                    if (!r) throw new we.ErrnoError(8);
                    return r;
                  },
                };
              function ge(e) {
                return (x[Oe() >> 2] = e), e;
              }
              function ye(e) {
                return T[e >> 2] + 4294967296 * x[(e + 4) >> 2];
              }
              function Ee(e) {
                var r = B(e) + 1,
                  t = Re(r);
                return t && N(e, F, t, r), t;
              }
              function _e(e) {
                try {
                  return k.grow((e - M.byteLength + 65535) >>> 16), I(k.buffer), 1;
                } catch (e) {}
              }
              var be = {};
              function ke() {
                if (!ke.strings) {
                  var e = {
                    USER: "web_user",
                    LOGNAME: "web_user",
                    PATH: "/",
                    PWD: "/",
                    HOME: "/home/web_user",
                    LANG:
                      (("object" == typeof navigator && navigator.languages && navigator.languages[0]) || "C").replace(
                        "-",
                        "_"
                      ) + ".UTF-8",
                    _: h || "./this.program",
                  };
                  for (var r in be) void 0 === be[r] ? delete e[r] : (e[r] = be[r]);
                  var t = [];
                  for (var r in e) t.push(r + "=" + e[r]);
                  ke.strings = t;
                }
                return ke.strings;
              }
              function Se(r) {
                (D = r), Y() || (e.onExit && e.onExit(r), (R = !0)), m(r, new ne(r));
              }
              function De(e) {
                return e % 4 == 0 && (e % 100 != 0 || e % 400 == 0);
              }
              var Me = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
                Fe = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
              function Ae(e, r, t, n) {
                var o = x[(n + 40) >> 2],
                  i = {
                    tm_sec: x[n >> 2],
                    tm_min: x[(n + 4) >> 2],
                    tm_hour: x[(n + 8) >> 2],
                    tm_mday: x[(n + 12) >> 2],
                    tm_mon: x[(n + 16) >> 2],
                    tm_year: x[(n + 20) >> 2],
                    tm_wday: x[(n + 24) >> 2],
                    tm_yday: x[(n + 28) >> 2],
                    tm_isdst: x[(n + 32) >> 2],
                    tm_gmtoff: x[(n + 36) >> 2],
                    tm_zone: o ? z(o) : "",
                  },
                  a = z(t),
                  s = {
                    "%c": "%a %b %d %H:%M:%S %Y",
                    "%D": "%m/%d/%y",
                    "%F": "%Y-%m-%d",
                    "%h": "%b",
                    "%r": "%I:%M:%S %p",
                    "%R": "%H:%M",
                    "%T": "%H:%M:%S",
                    "%x": "%m/%d/%y",
                    "%X": "%H:%M:%S",
                    "%Ec": "%c",
                    "%EC": "%C",
                    "%Ex": "%m/%d/%y",
                    "%EX": "%H:%M:%S",
                    "%Ey": "%y",
                    "%EY": "%Y",
                    "%Od": "%d",
                    "%Oe": "%e",
                    "%OH": "%H",
                    "%OI": "%I",
                    "%Om": "%m",
                    "%OM": "%M",
                    "%OS": "%S",
                    "%Ou": "%u",
                    "%OU": "%U",
                    "%OV": "%V",
                    "%Ow": "%w",
                    "%OW": "%W",
                    "%Oy": "%y",
                  };
                for (var u in s) a = a.replace(new RegExp(u, "g"), s[u]);
                var c = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                  l = [
                    "January",
                    "February",
                    "March",
                    "April",
                    "May",
                    "June",
                    "July",
                    "August",
                    "September",
                    "October",
                    "November",
                    "December",
                  ];
                function f(e, r, t) {
                  for (var n = "number" == typeof e ? e.toString() : e || ""; n.length < r; ) n = t[0] + n;
                  return n;
                }
                function d(e, r) {
                  return f(e, r, "0");
                }
                function h(e, r) {
                  function t(e) {
                    return e < 0 ? -1 : e > 0 ? 1 : 0;
                  }
                  var n;
                  return (
                    0 === (n = t(e.getFullYear() - r.getFullYear())) &&
                      0 === (n = t(e.getMonth() - r.getMonth())) &&
                      (n = t(e.getDate() - r.getDate())),
                    n
                  );
                }
                function m(e) {
                  switch (e.getDay()) {
                    case 0:
                      return new Date(e.getFullYear() - 1, 11, 29);
                    case 1:
                      return e;
                    case 2:
                      return new Date(e.getFullYear(), 0, 3);
                    case 3:
                      return new Date(e.getFullYear(), 0, 2);
                    case 4:
                      return new Date(e.getFullYear(), 0, 1);
                    case 5:
                      return new Date(e.getFullYear() - 1, 11, 31);
                    case 6:
                      return new Date(e.getFullYear() - 1, 11, 30);
                  }
                }
                function p(e) {
                  var r = (function (e, r) {
                      for (var t = new Date(e.getTime()); r > 0; ) {
                        var n = De(t.getFullYear()),
                          o = t.getMonth(),
                          i = (n ? Me : Fe)[o];
                        if (!(r > i - t.getDate())) return t.setDate(t.getDate() + r), t;
                        (r -= i - t.getDate() + 1),
                          t.setDate(1),
                          o < 11 ? t.setMonth(o + 1) : (t.setMonth(0), t.setFullYear(t.getFullYear() + 1));
                      }
                      return t;
                    })(new Date(e.tm_year + 1900, 0, 1), e.tm_yday),
                    t = new Date(r.getFullYear(), 0, 4),
                    n = new Date(r.getFullYear() + 1, 0, 4),
                    o = m(t),
                    i = m(n);
                  return h(o, r) <= 0 ? (h(i, r) <= 0 ? r.getFullYear() + 1 : r.getFullYear()) : r.getFullYear() - 1;
                }
                var w = {
                  "%a": function (e) {
                    return c[e.tm_wday].substring(0, 3);
                  },
                  "%A": function (e) {
                    return c[e.tm_wday];
                  },
                  "%b": function (e) {
                    return l[e.tm_mon].substring(0, 3);
                  },
                  "%B": function (e) {
                    return l[e.tm_mon];
                  },
                  "%C": function (e) {
                    return d(((e.tm_year + 1900) / 100) | 0, 2);
                  },
                  "%d": function (e) {
                    return d(e.tm_mday, 2);
                  },
                  "%e": function (e) {
                    return f(e.tm_mday, 2, " ");
                  },
                  "%g": function (e) {
                    return p(e).toString().substring(2);
                  },
                  "%G": function (e) {
                    return p(e);
                  },
                  "%H": function (e) {
                    return d(e.tm_hour, 2);
                  },
                  "%I": function (e) {
                    var r = e.tm_hour;
                    return 0 == r ? (r = 12) : r > 12 && (r -= 12), d(r, 2);
                  },
                  "%j": function (e) {
                    return d(
                      e.tm_mday +
                        (function (e, r) {
                          for (var t = 0, n = 0; n <= r; t += e[n++]);
                          return t;
                        })(De(e.tm_year + 1900) ? Me : Fe, e.tm_mon - 1),
                      3
                    );
                  },
                  "%m": function (e) {
                    return d(e.tm_mon + 1, 2);
                  },
                  "%M": function (e) {
                    return d(e.tm_min, 2);
                  },
                  "%n": function () {
                    return "\n";
                  },
                  "%p": function (e) {
                    return e.tm_hour >= 0 && e.tm_hour < 12 ? "AM" : "PM";
                  },
                  "%S": function (e) {
                    return d(e.tm_sec, 2);
                  },
                  "%t": function () {
                    return "\t";
                  },
                  "%u": function (e) {
                    return e.tm_wday || 7;
                  },
                  "%U": function (e) {
                    var r = e.tm_yday + 7 - e.tm_wday;
                    return d(Math.floor(r / 7), 2);
                  },
                  "%V": function (e) {
                    var r = Math.floor((e.tm_yday + 7 - ((e.tm_wday + 6) % 7)) / 7);
                    if (((e.tm_wday + 371 - e.tm_yday - 2) % 7 <= 2 && r++, r)) {
                      if (53 == r) {
                        var t = (e.tm_wday + 371 - e.tm_yday) % 7;
                        4 == t || (3 == t && De(e.tm_year)) || (r = 1);
                      }
                    } else {
                      r = 52;
                      var n = (e.tm_wday + 7 - e.tm_yday - 1) % 7;
                      (4 == n || (5 == n && De((e.tm_year % 400) - 1))) && r++;
                    }
                    return d(r, 2);
                  },
                  "%w": function (e) {
                    return e.tm_wday;
                  },
                  "%W": function (e) {
                    var r = e.tm_yday + 7 - ((e.tm_wday + 6) % 7);
                    return d(Math.floor(r / 7), 2);
                  },
                  "%y": function (e) {
                    return (e.tm_year + 1900).toString().substring(2);
                  },
                  "%Y": function (e) {
                    return e.tm_year + 1900;
                  },
                  "%z": function (e) {
                    var r = e.tm_gmtoff,
                      t = r >= 0;
                    return (
                      (r = ((r = Math.abs(r) / 60) / 60) * 100 + (r % 60)),
                      (t ? "+" : "-") + String("0000" + r).slice(-4)
                    );
                  },
                  "%Z": function (e) {
                    return e.tm_zone;
                  },
                  "%%": function () {
                    return "%";
                  },
                };
                for (var u in ((a = a.replace(/%%/g, "\0\0")), w))
                  a.includes(u) && (a = a.replace(new RegExp(u, "g"), w[u](i)));
                var v = de((a = a.replace(/\0\0/g, "%")), !1);
                return v.length > r ? 0 : (ie(v, e), v.length - 1);
              }
              var Pe = function (e, r, t, n) {
                e || (e = this),
                  (this.parent = e),
                  (this.mount = e.mount),
                  (this.mounted = null),
                  (this.id = we.nextInode++),
                  (this.name = r),
                  (this.mode = t),
                  (this.node_ops = {}),
                  (this.stream_ops = {}),
                  (this.rdev = n);
              };
              Object.defineProperties(Pe.prototype, {
                read: {
                  get: function () {
                    return !(365 & ~this.mode);
                  },
                  set: function (e) {
                    e ? (this.mode |= 365) : (this.mode &= -366);
                  },
                },
                write: {
                  get: function () {
                    return !(146 & ~this.mode);
                  },
                  set: function (e) {
                    e ? (this.mode |= 146) : (this.mode &= -147);
                  },
                },
                isFolder: {
                  get: function () {
                    return we.isDir(this.mode);
                  },
                },
                isDevice: {
                  get: function () {
                    return we.isChrdev(this.mode);
                  },
                },
              }),
                (we.FSNode = Pe),
                we.staticInit();
              var xe,
                Te = {
                  q: function (e, r) {
                    se(e)(r);
                  },
                  a: function (e) {
                    return Re(e + 24) + 24;
                  },
                  C: function () {
                    var e = ue.pop();
                    e || K("no exception to throw");
                    var r = e.excPtr;
                    throw (e.get_rethrown() || (ue.push(e), e.set_rethrown(!0), e.set_caught(!1)), r);
                  },
                  b: function (e, r, t) {
                    throw (new ce(e).init(r, t), e);
                  },
                  z: function (e, r, t) {
                    try {
                      var n = ve.getStreamFromFD(e);
                      if (n.fd === r) return -28;
                      var o = we.getStream(r);
                      return o && we.close(o), we.createStream(n, r, r + 1).fd;
                    } catch (e) {
                      if (void 0 === we || !(e instanceof we.ErrnoError)) throw e;
                      return -e.errno;
                    }
                  },
                  g: function (e, r, t) {
                    ve.varargs = t;
                    try {
                      var n = ve.getStreamFromFD(e);
                      switch (r) {
                        case 0:
                          return (o = ve.get()) < 0 ? -28 : we.createStream(n, o).fd;
                        case 1:
                        case 2:
                        case 6:
                        case 7:
                          return 0;
                        case 3:
                          return n.flags;
                        case 4:
                          var o = ve.get();
                          return (n.flags |= o), 0;
                        case 5:
                          return (o = ve.get()), (P[(o + 0) >> 1] = 2), 0;
                        case 16:
                        case 8:
                        default:
                          return -28;
                        case 9:
                          return ge(28), -1;
                      }
                    } catch (e) {
                      if (void 0 === we || !(e instanceof we.ErrnoError)) throw e;
                      return -e.errno;
                    }
                  },
                  B: function (e, r, t) {
                    ve.varargs = t;
                    try {
                      var n = ve.getStreamFromFD(e);
                      switch (r) {
                        case 21509:
                        case 21505:
                        case 21510:
                        case 21511:
                        case 21512:
                        case 21506:
                        case 21507:
                        case 21508:
                        case 21523:
                        case 21524:
                          return n.tty ? 0 : -59;
                        case 21519:
                          if (!n.tty) return -59;
                          var o = ve.get();
                          return (x[o >> 2] = 0), 0;
                        case 21520:
                          return n.tty ? -28 : -59;
                        case 21531:
                          return (o = ve.get()), we.ioctl(n, r, o);
                        default:
                          return -28;
                      }
                    } catch (e) {
                      if (void 0 === we || !(e instanceof we.ErrnoError)) throw e;
                      return -e.errno;
                    }
                  },
                  u: function (e, r) {
                    try {
                      return (e = ve.getStr(e)), ve.doStat(we.lstat, e, r);
                    } catch (e) {
                      if (void 0 === we || !(e instanceof we.ErrnoError)) throw e;
                      return -e.errno;
                    }
                  },
                  l: function (e, r, t, n) {
                    ve.varargs = n;
                    try {
                      (r = ve.getStr(r)), (r = ve.calculateAt(e, r));
                      var o = n ? ve.get() : 0;
                      return we.open(r, t, o).fd;
                    } catch (e) {
                      if (void 0 === we || !(e instanceof we.ErrnoError)) throw e;
                      return -e.errno;
                    }
                  },
                  v: function (e, r, t, n) {
                    try {
                      return (
                        (r = ve.getStr(r)),
                        (n = ve.getStr(n)),
                        (r = ve.calculateAt(e, r)),
                        (n = ve.calculateAt(t, n)),
                        we.rename(r, n),
                        0
                      );
                    } catch (e) {
                      if (void 0 === we || !(e instanceof we.ErrnoError)) throw e;
                      return -e.errno;
                    }
                  },
                  w: function (e) {
                    try {
                      return (e = ve.getStr(e)), we.rmdir(e), 0;
                    } catch (e) {
                      if (void 0 === we || !(e instanceof we.ErrnoError)) throw e;
                      return -e.errno;
                    }
                  },
                  j: function (e, r, t) {
                    try {
                      return (
                        (r = ve.getStr(r)),
                        (r = ve.calculateAt(e, r)),
                        0 === t ? we.unlink(r) : 512 === t ? we.rmdir(r) : K("Invalid flags passed to unlinkat"),
                        0
                      );
                    } catch (e) {
                      if (void 0 === we || !(e instanceof we.ErrnoError)) throw e;
                      return -e.errno;
                    }
                  },
                  d: function () {
                    return Date.now();
                  },
                  D: function () {
                    return !0;
                  },
                  s: function () {
                    throw 1 / 0;
                  },
                  E: function (e, r) {
                    var t = new Date(1e3 * ye(e));
                    (x[r >> 2] = t.getUTCSeconds()),
                      (x[(r + 4) >> 2] = t.getUTCMinutes()),
                      (x[(r + 8) >> 2] = t.getUTCHours()),
                      (x[(r + 12) >> 2] = t.getUTCDate()),
                      (x[(r + 16) >> 2] = t.getUTCMonth()),
                      (x[(r + 20) >> 2] = t.getUTCFullYear() - 1900),
                      (x[(r + 24) >> 2] = t.getUTCDay());
                    var n = Date.UTC(t.getUTCFullYear(), 0, 1, 0, 0, 0, 0),
                      o = ((t.getTime() - n) / 864e5) | 0;
                    x[(r + 28) >> 2] = o;
                  },
                  F: function (e, r) {
                    var t = new Date(1e3 * ye(e));
                    (x[r >> 2] = t.getSeconds()),
                      (x[(r + 4) >> 2] = t.getMinutes()),
                      (x[(r + 8) >> 2] = t.getHours()),
                      (x[(r + 12) >> 2] = t.getDate()),
                      (x[(r + 16) >> 2] = t.getMonth()),
                      (x[(r + 20) >> 2] = t.getFullYear() - 1900),
                      (x[(r + 24) >> 2] = t.getDay());
                    var n = new Date(t.getFullYear(), 0, 1),
                      o = ((t.getTime() - n.getTime()) / 864e5) | 0;
                    (x[(r + 28) >> 2] = o), (x[(r + 36) >> 2] = -60 * t.getTimezoneOffset());
                    var i = new Date(t.getFullYear(), 6, 1).getTimezoneOffset(),
                      a = n.getTimezoneOffset(),
                      s = 0 | (i != a && t.getTimezoneOffset() == Math.min(a, i));
                    x[(r + 32) >> 2] = s;
                  },
                  G: function (e) {
                    var r = new Date(
                        x[(e + 20) >> 2] + 1900,
                        x[(e + 16) >> 2],
                        x[(e + 12) >> 2],
                        x[(e + 8) >> 2],
                        x[(e + 4) >> 2],
                        x[e >> 2],
                        0
                      ),
                      t = x[(e + 32) >> 2],
                      n = r.getTimezoneOffset(),
                      o = new Date(r.getFullYear(), 0, 1),
                      i = new Date(r.getFullYear(), 6, 1).getTimezoneOffset(),
                      a = o.getTimezoneOffset(),
                      s = Math.min(a, i);
                    if (t < 0) x[(e + 32) >> 2] = Number(i != a && s == n);
                    else if (t > 0 != (s == n)) {
                      var u = Math.max(a, i),
                        c = t > 0 ? s : u;
                      r.setTime(r.getTime() + 6e4 * (c - n));
                    }
                    x[(e + 24) >> 2] = r.getDay();
                    var l = ((r.getTime() - o.getTime()) / 864e5) | 0;
                    return (
                      (x[(e + 28) >> 2] = l),
                      (x[e >> 2] = r.getSeconds()),
                      (x[(e + 4) >> 2] = r.getMinutes()),
                      (x[(e + 8) >> 2] = r.getHours()),
                      (x[(e + 12) >> 2] = r.getDate()),
                      (x[(e + 16) >> 2] = r.getMonth()),
                      (r.getTime() / 1e3) | 0
                    );
                  },
                  H: function e(r, t, n) {
                    e.called ||
                      ((e.called = !0),
                      (function (e, r, t) {
                        var n = new Date().getFullYear(),
                          o = new Date(n, 0, 1),
                          i = new Date(n, 6, 1),
                          a = o.getTimezoneOffset(),
                          s = i.getTimezoneOffset(),
                          u = Math.max(a, s);
                        function c(e) {
                          var r = e.toTimeString().match(/\(([A-Za-z ]+)\)$/);
                          return r ? r[1] : "GMT";
                        }
                        (x[e >> 2] = 60 * u), (x[r >> 2] = Number(a != s));
                        var l = c(o),
                          f = c(i),
                          d = Ee(l),
                          h = Ee(f);
                        s < a ? ((T[t >> 2] = d), (T[(t + 4) >> 2] = h)) : ((T[t >> 2] = h), (T[(t + 4) >> 2] = d));
                      })(r, t, n));
                  },
                  c: function () {
                    K("");
                  },
                  i: function (e) {
                    setTimeout(function () {
                      !(function (e) {
                        if (!R)
                          try {
                            e();
                          } catch (e) {
                            !(function (e) {
                              if (e instanceof ne || "unwind" == e) return D;
                              m(1, e);
                            })(e);
                          }
                      })(function () {
                        je(14);
                      });
                    }, 1e3 * e);
                  },
                  I: function (e, r, t) {
                    A.copyWithin(e, r, r + t);
                  },
                  t: function (e) {
                    var r,
                      t = A.length,
                      n = 2147483648;
                    if ((e >>>= 0) > n) return !1;
                    for (var o = 1; o <= 4; o *= 2) {
                      var i = t * (1 + 0.2 / o);
                      if (
                        ((i = Math.min(i, e + 100663296)),
                        _e(Math.min(n, (r = Math.max(e, i)) + ((65536 - (r % 65536)) % 65536))))
                      )
                        return !0;
                    }
                    return !1;
                  },
                  x: function (e, r) {
                    var t = 0;
                    return (
                      ke().forEach(function (n, o) {
                        var i = r + t;
                        (T[(e + 4 * o) >> 2] = i),
                          (function (e, r) {
                            for (var t = 0; t < e.length; ++t) F[0 | r++] = e.charCodeAt(t);
                            F[0 | r] = 0;
                          })(n, i),
                          (t += n.length + 1);
                      }),
                      0
                    );
                  },
                  y: function (e, r) {
                    var t = ke();
                    T[e >> 2] = t.length;
                    var n = 0;
                    return (
                      t.forEach(function (e) {
                        n += e.length + 1;
                      }),
                      (T[r >> 2] = n),
                      0
                    );
                  },
                  K: function (e, r) {
                    (D = e), Se(e);
                  },
                  f: function (e) {
                    try {
                      var r = ve.getStreamFromFD(e);
                      return we.close(r), 0;
                    } catch (e) {
                      if (void 0 === we || !(e instanceof we.ErrnoError)) throw e;
                      return e.errno;
                    }
                  },
                  A: function (e, r, t, n) {
                    try {
                      var o = (function (e, r, t) {
                        for (var n = 0, o = 0; o < t; o++) {
                          var i = T[r >> 2],
                            a = T[(r + 4) >> 2];
                          r += 8;
                          var s = we.read(e, F, i, a, undefined);
                          if (s < 0) return -1;
                          if (((n += s), s < a)) break;
                        }
                        return n;
                      })(ve.getStreamFromFD(e), r, t);
                      return (x[n >> 2] = o), 0;
                    } catch (e) {
                      if (void 0 === we || !(e instanceof we.ErrnoError)) throw e;
                      return e.errno;
                    }
                  },
                  p: function (e, r, t, n, o) {
                    try {
                      var i = ((u = t) + 2097152) >>> 0 < 4194305 - !!(s = r) ? (s >>> 0) + 4294967296 * u : NaN;
                      if (isNaN(i)) return 61;
                      var a = ve.getStreamFromFD(e);
                      return (
                        we.llseek(a, i, n),
                        (Z = [
                          a.position >>> 0,
                          ((Q = a.position),
                          +Math.abs(Q) >= 1
                            ? Q > 0
                              ? (0 | Math.min(+Math.floor(Q / 4294967296), 4294967295)) >>> 0
                              : ~~+Math.ceil((Q - +(~~Q >>> 0)) / 4294967296) >>> 0
                            : 0),
                        ]),
                        (x[o >> 2] = Z[0]),
                        (x[(o + 4) >> 2] = Z[1]),
                        a.getdents && 0 === i && 0 === n && (a.getdents = null),
                        0
                      );
                    } catch (e) {
                      if (void 0 === we || !(e instanceof we.ErrnoError)) throw e;
                      return e.errno;
                    }
                    var s, u;
                  },
                  k: function (e, r, t, n) {
                    try {
                      var o = (function (e, r, t) {
                        for (var n = 0, o = 0; o < t; o++) {
                          var i = T[r >> 2],
                            a = T[(r + 4) >> 2];
                          r += 8;
                          var s = we.write(e, F, i, a, undefined);
                          if (s < 0) return -1;
                          n += s;
                        }
                        return n;
                      })(ve.getStreamFromFD(e), r, t);
                      return (T[n >> 2] = o), 0;
                    } catch (e) {
                      if (void 0 === we || !(e instanceof we.ErrnoError)) throw e;
                      return e.errno;
                    }
                  },
                  h: function () {
                    return b;
                  },
                  o: function (e, r, t) {
                    var n = Ne();
                    try {
                      se(e)(r, t);
                    } catch (e) {
                      if ((Be(n), e !== e + 0)) throw e;
                      ze(1, 0);
                    }
                  },
                  J: Se,
                  e: function (e) {
                    b = e;
                  },
                  n: Ae,
                  r: function (e, r, t, n) {
                    return Ae(e, r, t, n);
                  },
                  m: function (e) {
                    if (v) {
                      if (!e) return 1;
                      var r = z(e);
                      if (!r.length) return 0;
                      var n = t(994).spawnSync(r, [], { shell: !0, stdio: "inherit" }),
                        o = (e, r) => (e << 8) | r;
                      return null === n.status
                        ? o(
                            0,
                            ((e) => {
                              switch (e) {
                                case "SIGHUP":
                                  return 1;
                                case "SIGINT":
                                  return 2;
                                case "SIGQUIT":
                                  return 3;
                                case "SIGFPE":
                                  return 8;
                                case "SIGKILL":
                                  return 9;
                                case "SIGALRM":
                                  return 14;
                                case "SIGTERM":
                                  return 15;
                              }
                              return 2;
                            })(n.signal)
                          )
                        : o(n.status, 0);
                    }
                    return e ? (ge(52), -1) : 0;
                  },
                },
                Re =
                  ((function () {
                    var r = { a: Te };
                    function t(r, t) {
                      var n,
                        o = r.exports;
                      (e.asm = o), I((k = e.asm.L).buffer), (C = e.asm.O), (n = e.asm.M), U.unshift(n), V();
                    }
                    function n(e) {
                      t(e.instance);
                    }
                    function i(e) {
                      return (function () {
                        if (!_ && (p || w)) {
                          if ("function" == typeof fetch && !re($))
                            return fetch($, { credentials: "same-origin" })
                              .then(function (e) {
                                if (!e.ok) throw "failed to load wasm binary file at '" + $ + "'";
                                return e.arrayBuffer();
                              })
                              .catch(function () {
                                return te($);
                              });
                          if (a)
                            return new Promise(function (e, r) {
                              a(
                                $,
                                function (r) {
                                  e(new Uint8Array(r));
                                },
                                r
                              );
                            });
                        }
                        return Promise.resolve().then(function () {
                          return te($);
                        });
                      })()
                        .then(function (e) {
                          return WebAssembly.instantiate(e, r);
                        })
                        .then(function (e) {
                          return e;
                        })
                        .then(e, function (e) {
                          E("failed to asynchronously prepare wasm: " + e), K(e);
                        });
                    }
                    if ((X(), e.instantiateWasm))
                      try {
                        return e.instantiateWasm(r, t);
                      } catch (e) {
                        return E("Module.instantiateWasm callback failed with error: " + e), !1;
                      }
                    (_ ||
                    "function" != typeof WebAssembly.instantiateStreaming ||
                    ee($) ||
                    re($) ||
                    v ||
                    "function" != typeof fetch
                      ? i(n)
                      : fetch($, { credentials: "same-origin" }).then(function (e) {
                          return WebAssembly.instantiateStreaming(e, r).then(n, function (e) {
                            return (
                              E("wasm streaming compile failed: " + e),
                              E("falling back to ArrayBuffer instantiation"),
                              i(n)
                            );
                          });
                        })
                    ).catch(o);
                  })(),
                  (e.___wasm_call_ctors = function () {
                    return (e.___wasm_call_ctors = e.asm.M).apply(null, arguments);
                  }),
                  (e._run = function () {
                    return (e._run = e.asm.N).apply(null, arguments);
                  }),
                  (e._memset = function () {
                    return (e._memset = e.asm.P).apply(null, arguments);
                  }),
                  (e._malloc = function () {
                    return (Re = e._malloc = e.asm.Q).apply(null, arguments);
                  })),
                Oe = (e.___errno_location = function () {
                  return (Oe = e.___errno_location = e.asm.R).apply(null, arguments);
                }),
                je = (e._raise = function () {
                  return (je = e._raise = e.asm.S).apply(null, arguments);
                }),
                ze = (e._setThrew = function () {
                  return (ze = e._setThrew = e.asm.T).apply(null, arguments);
                }),
                Ne = (e.stackSave = function () {
                  return (Ne = e.stackSave = e.asm.U).apply(null, arguments);
                }),
                Be = (e.stackRestore = function () {
                  return (Be = e.stackRestore = e.asm.V).apply(null, arguments);
                }),
                Ie = (e.stackAlloc = function () {
                  return (Ie = e.stackAlloc = e.asm.W).apply(null, arguments);
                }),
                Ce = (e.___cxa_is_pointer_type = function () {
                  return (Ce = e.___cxa_is_pointer_type = e.asm.X).apply(null, arguments);
                });
              function Le(t) {
                function n() {
                  xe ||
                    ((xe = !0),
                    (e.calledRun = !0),
                    R ||
                      (e.noFSInit || we.init.initialized || we.init(),
                      (we.ignorePermissions = !1),
                      he.init(),
                      oe(U),
                      r(e),
                      e.onRuntimeInitialized && e.onRuntimeInitialized(),
                      (function () {
                        if (e.postRun)
                          for ("function" == typeof e.postRun && (e.postRun = [e.postRun]); e.postRun.length; )
                            (r = e.postRun.shift()), H.unshift(r);
                        var r;
                        oe(H);
                      })()));
                }
                (t = t || d),
                  W > 0 ||
                    ((function () {
                      if (e.preRun)
                        for ("function" == typeof e.preRun && (e.preRun = [e.preRun]); e.preRun.length; )
                          (r = e.preRun.shift()), L.unshift(r);
                      var r;
                      oe(L);
                    })(),
                    W > 0 ||
                      (e.setStatus
                        ? (e.setStatus("Running..."),
                          setTimeout(function () {
                            setTimeout(function () {
                              e.setStatus("");
                            }, 1),
                              n();
                          }, 1))
                        : n()));
              }
              if (
                ((e.ccall = function (r, t, n, o, i) {
                  var a = {
                      string: (e) => {
                        var r = 0;
                        if (null != e && 0 !== e) {
                          var t = 1 + (e.length << 2);
                          !(function (e, r, t) {
                            N(e, A, r, t);
                          })(e, (r = Ie(t)), t);
                        }
                        return r;
                      },
                      array: (e) => {
                        var r = Ie(e.length);
                        return ie(e, r), r;
                      },
                    },
                    s = (function (r) {
                      return e["_" + r];
                    })(r),
                    u = [],
                    c = 0;
                  if (o)
                    for (var l = 0; l < o.length; l++) {
                      var f = a[n[l]];
                      f ? (0 === c && (c = Ne()), (u[l] = f(o[l]))) : (u[l] = o[l]);
                    }
                  var d = s.apply(null, u);
                  return (function (e) {
                    return (
                      0 !== c && Be(c),
                      (function (e) {
                        return "string" === t ? z(e) : "boolean" === t ? Boolean(e) : e;
                      })(e)
                    );
                  })(d);
                }),
                (G = function e() {
                  xe || Le(), xe || (G = e);
                }),
                e.preInit)
              )
                for ("function" == typeof e.preInit && (e.preInit = [e.preInit]); e.preInit.length > 0; )
                  e.preInit.pop()();
              return Le(), e.ready;
            });
        "object" == typeof exports
          ? (e.exports = o)
          : "function" == typeof define && t.amdO
          ? define([], function () {
              return o;
            })
          : "object" == typeof exports && (exports.Module = o);
      },
      642: (e, r, t) => {
        "use strict";
        t.d(r, { A: () => n });
        const n = "/dist/clingo.wasm";
      },
      633: function (e, r, t) {
        "use strict";
        var n =
          (this && this.__awaiter) ||
          function (e, r, t, n) {
            return new (t || (t = Promise))(function (o, i) {
              function a(e) {
                try {
                  u(n.next(e));
                } catch (e) {
                  i(e);
                }
              }
              function s(e) {
                try {
                  u(n.throw(e));
                } catch (e) {
                  i(e);
                }
              }
              function u(e) {
                var r;
                e.done
                  ? o(e.value)
                  : ((r = e.value),
                    r instanceof t
                      ? r
                      : new t(function (e) {
                          e(r);
                        })).then(a, s);
              }
              u((n = n.apply(e, r || [])).next());
            });
          };
        Object.defineProperty(r, "__esModule", { value: !0 }),
          (r.Runner = void 0),
          (r.init = function () {
            return n(this, arguments, void 0, function* (e = {}) {
              const r = new i(e);
              return yield r.init(), r.run.bind(r);
            });
          });
        const o = t(100);
        class i {
          constructor(e = {}) {
            (this.extraParams = e), (this.results = []), (this.errors = []);
          }
          init() {
            return n(this, void 0, void 0, function* () {
              if ((console.info("Initialize Clingo"), !this.clingo)) {
                const e = Object.assign(
                  { print: (e) => this.results.push(e), printErr: (e) => this.errors.push(e) },
                  this.extraParams
                );
                o.Module ? (this.clingo = yield (0, o.Module)(e)) : (this.clingo = yield t(100)(e));
              }
            });
          }
          run(e, r = 1, t = []) {
            (this.results = []), (this.errors = []);
            try {
              this.clingo.ccall("run", "number", ["string", "string"], [e, `--outf=2 ${t.join(" ")} ${r}`]);
            } catch (e) {
              return { Result: "ERROR", Error: this.errors.join("\n") };
            }
            const n = JSON.parse(this.results.join(""));
            return delete n.Input, (n.Warnings = this.errors.join("\n").split("\n\n")), n;
          }
        }
        r.Runner = i;
      },
      317: function (e, r, t) {
        "use strict";
        var n =
          (this && this.__awaiter) ||
          function (e, r, t, n) {
            return new (t || (t = Promise))(function (o, i) {
              function a(e) {
                try {
                  u(n.next(e));
                } catch (e) {
                  i(e);
                }
              }
              function s(e) {
                try {
                  u(n.throw(e));
                } catch (e) {
                  i(e);
                }
              }
              function u(e) {
                var r;
                e.done
                  ? o(e.value)
                  : ((r = e.value),
                    r instanceof t
                      ? r
                      : new t(function (e) {
                          e(r);
                        })).then(a, s);
              }
              u((n = n.apply(e, r || [])).next());
            });
          };
        Object.defineProperty(r, "__esModule", { value: !0 });
        const o = t(633),
          i = t(642).A;
        let a;
        function s(e) {
          return n(this, void 0, void 0, function* () {
            a = yield (0, o.init)({ locateFile: (r) => e || (r.endsWith(".wasm") ? `${location.origin}/${i}` : r) });
          });
        }
        addEventListener("message", (e) =>
          n(void 0, void 0, void 0, function* () {
            const r = e.data;
            if ((console.info("Message", r), "run" === r.type)) {
              a || (yield s());
              const e = a(...r.args);
              postMessage(e, void 0);
            } else "init" === r.type && (yield s(r.wasmUrl), postMessage(null, void 0));
          })
        ),
          (r.default = null);
      },
      994: () => {},
      401: () => {},
      603: () => {},
      247: () => {},
    },
    r = {};
  function t(n) {
    var o = r[n];
    if (void 0 !== o) return o.exports;
    var i = (r[n] = { id: n, loaded: !1, exports: {} });
    return e[n].call(i.exports, i, i.exports, t), (i.loaded = !0), i.exports;
  }
  (t.amdO = {}),
    (t.d = (e, r) => {
      for (var n in r) t.o(r, n) && !t.o(e, n) && Object.defineProperty(e, n, { enumerable: !0, get: r[n] });
    }),
    (t.hmd = (e) => (
      (e = Object.create(e)).children || (e.children = []),
      Object.defineProperty(e, "exports", {
        enumerable: !0,
        set: () => {
          throw new Error(
            "ES Modules may not assign module.exports or exports.*, Use ESM export syntax, instead: " + e.id
          );
        },
      }),
      e
    )),
    (t.o = (e, r) => Object.prototype.hasOwnProperty.call(e, r)),
    (t.r = (e) => {
      "undefined" != typeof Symbol &&
        Symbol.toStringTag &&
        Object.defineProperty(e, Symbol.toStringTag, { value: "Module" }),
        Object.defineProperty(e, "__esModule", { value: !0 });
    }),
    t(317);
})();
