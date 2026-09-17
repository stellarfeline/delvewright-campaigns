#!/usr/bin/env python3
"""Is the drawing shorter than the generator's share?

Standard library only. The generator is read as TEXT, through `tokenize`; none
of it is imported or executed. Both sides are reduced to what a reader must
read: the Python loses comments, docstrings, blank lines and indentation; the
drawing loses every `note` and all whitespace.

    python3 measure.py

Prints the two byte counts and the verdict, then the informational figures
spec-0072 criterion 10 asks for: both files' committed line counts, the number
of operations in the drawing, and the number of `Expr` objects with their share
of the drawing's bytes.
"""
import io
import json
import sys
import token
import tokenize
from pathlib import Path

HERE = Path(__file__).resolve().parent
GENERATOR = HERE.parents[1] / "campaigns/doune-castle-tour/design/programs/castle/gatehouse.py"
DRAWING = HERE / "drawing.json"

OPERATIONS = {"box", "cylinder", "sphere", "prism", "pyramid", "line",
              "scope", "use", "repeat", "mirror", "grammar", "mark", "claim"}


def strip_python(source):
    """The generator with comments, docstrings, blank lines and indentation gone.

    One token stream, one pass: a COMMENT is dropped; a STRING that stands alone
    as a statement is a docstring and is dropped; INDENT / DEDENT / NL carry no
    text a reader needs once the structure is gone. Tokens are re-joined with a
    single space only where two of them would otherwise fuse into one token.
    """
    out, line = [], []
    prev = None
    start_of_statement = True
    for tok in tokenize.generate_tokens(io.StringIO(source).readline):
        kind, text = tok.type, tok.string
        if kind in (token.COMMENT, token.NL, token.INDENT, token.DEDENT,
                    token.ENCODING, token.ENDMARKER):
            continue
        if kind == token.NEWLINE:
            if line:
                out.append("".join(line))
            line, prev, start_of_statement = [], None, True
            continue
        if kind == token.STRING and start_of_statement:
            continue                      # a docstring: a statement that is a string
        if prev is not None and _would_fuse(prev, text):
            line.append(" ")
        line.append(text)
        prev = text
        start_of_statement = False
    if line:
        out.append("".join(line))
    return "\n".join(out) + "\n"


def _would_fuse(a, b):
    tail, head = a[-1], b[:1]
    word = lambda c: c.isalnum() or c == "_"
    return word(tail) and word(head)


def strip_notes(node):
    """The drawing with every `note` removed — the engine never reads one."""
    if isinstance(node, dict):
        return {k: strip_notes(v) for k, v in node.items() if k != "note"}
    if isinstance(node, list):
        return [strip_notes(v) for v in node]
    return node


def walk(node, on_dict):
    if isinstance(node, dict):
        on_dict(node)
        for v in node.values():
            walk(v, on_dict)
    elif isinstance(node, list):
        for v in node:
            walk(v, on_dict)


def compact(node):
    return json.dumps(node, separators=(",", ":"), sort_keys=True)


def main():
    if not GENERATOR.exists():
        sys.exit(f"generator not found: {GENERATOR}")
    if not DRAWING.exists():
        sys.exit(f"drawing not found: {DRAWING}")

    raw_py = GENERATOR.read_text(encoding="utf-8")
    stripped_py = strip_python(raw_py)
    py_bytes = len(stripped_py.encode("utf-8"))

    raw_json = DRAWING.read_text(encoding="utf-8")
    drawing = json.loads(raw_json)
    bare = strip_notes(drawing)
    json_bytes = len(compact(bare).encode("utf-8"))

    ops = []
    exprs = []
    walk(bare, lambda d: ops.append(d) if d.get("op") in OPERATIONS else None)
    walk(bare, lambda d: exprs.append(d) if "expr" in d and isinstance(d.get("expr"), str) else None)
    # An Expr nested in an Expr is counted once, in the outermost one's bytes.
    outer, seen = [], set()

    def mark_nested(d):
        for v in d.values():
            walk(v, lambda inner: seen.add(id(inner)))

    for e in exprs:
        mark_nested(e)
    for e in exprs:
        if id(e) not in seen:
            outer.append(e)
    expr_bytes = sum(len(compact(e).encode("utf-8")) for e in outer)

    print(f"{'generator, stripped':<34} {py_bytes:>8} bytes   "
          f"{GENERATOR.name}")
    print(f"{'drawing, compact, notes removed':<34} {json_bytes:>8} bytes   "
          f"{DRAWING.name}")
    verdict = "SHORTER" if json_bytes < py_bytes else "NOT SHORTER"
    print(f"{'verdict':<34} {verdict}  "
          f"({json_bytes - py_bytes:+d} bytes, "
          f"{json_bytes / py_bytes:.2f}x)")
    print()
    print("informational")
    print(f"  {'committed lines':<32} "
          f"{len(raw_py.splitlines()):>8} {GENERATOR.name}   "
          f"{len(raw_json.splitlines()):>8} {DRAWING.name}")
    print(f"  {'committed bytes':<32} "
          f"{len(raw_py.encode('utf-8')):>8} {GENERATOR.name}   "
          f"{len(raw_json.encode('utf-8')):>8} {DRAWING.name}")
    print(f"  {'stripped lines':<32} {len(stripped_py.splitlines()):>8}")
    print(f"  {'operations written':<32} {len(ops):>8}")
    print(f"  {'Expr objects (outermost)':<32} {len(outer):>8}")
    print(f"  {'Expr bytes':<32} {expr_bytes:>8} "
          f"({expr_bytes / json_bytes:.1%} of the drawing)")


if __name__ == "__main__":
    main()
