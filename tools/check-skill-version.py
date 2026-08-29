#!/usr/bin/env python3
"""The `/new-delve` skill's version declarations, held to what they each claim.

WHY THIS EXISTS (ADR-0016, third version line)

ADR-0016 settles three independent version lines: `dsl_version` (format),
`delvec` (engine, semver from v1.0.0), and the `/new-delve` skill (product) —
"its own version, declared in the skill itself, together with the `delvec`
version range it drives". Lines 1 and 2 have machinery behind them
(`DW0141`'s per-stage fences; `crates/compiler/Cargo.toml` -> `DELVEC_VERSION`
-> `manifest.json` -> `versions.toml`). Line 3 had none: the skill's frontmatter
carried `name` and `description` and nothing else.

A `requires:` line nobody checks is the failure class this project keeps being
bitten by — the **unbound declaration** (CLAUDE.md; `playtest-methodology.md`
rule 1). The island's combat floor gate was green for nineteen rounds because it
examined zero enemies. A hand-typed engine range would be green forever for the
same reason: nothing would ever read it.

TWO FIELDS, BECAUSE THEY ARE TWO DIFFERENT CLAIMS

    requires:
      delvec: ">=1.0.0 <2.0.0"   # COMPATIBILITY — the major window it drives
    verified_with: 1.0.0          # EVIDENCE — the engine the page is proven on

`requires.delvec` is what a creator reads as "older engines will not work". It is
ADR-0016's own shape (`e.g. delvec >= 1.0 < 2`): a **major window**, stable
across the whole 1.x line, because format compatibility is guaranteed by the
per-stage fences and an engine may release many times inside one window.

`verified_with` is the narrower, provable claim: the one engine the page is
actually exercised against — `authoring_ref`. Collapsing the two — pinning the window's floor to
the current engine — would make the frontmatter assert, after every engine
release, that older engines are unsupported, which nobody tested and which is
probably false. It would also make ADR-0016's own example un-writable the moment
the engine reached 1.1.0.

WHAT IS CHECKED

1. **Shape.** The frontmatter carries `version:` (semver), `requires: delvec:`
   (a `>=X.Y.Z <A.B.C` range) and `verified_with:` (semver), alongside the
   loader's own `name`/`description`.

2. **`requires.delvec` binds by MEMBERSHIP.** The window is a well-formed semver
   major window — ceiling == floor's next major — and the authoring engine is
   INSIDE it: `floor <= engine < ceiling`. That is what catches a major bump:
   `delvec 2.0.0` reached by the authoring pin while the page still says
   `<2.0.0` is a page declaring it does not drive the engine it sends the
   author to build.

3. **`verified_with` binds by EQUALITY** to `crates/compiler/Cargo.toml`'s
   `[package] version` — the single source `DELVEC_VERSION` derives from
   (`env!("CARGO_PKG_VERSION")`), so this script never carries a second
   hand-typed copy. BOTH directions are red:

   - ABOVE it names a compiler that does not exist, so no run anywhere produced
     that evidence (the same falsification `check-storybook-version.py` applies
     to `last verified with delvec <Y>`);
   - BELOW it is stale: the authoring pin moved and nobody re-ran the skill
     against it, so the field records evidence from a build no pin now names.

   Restamping it is one line in the engine's own release commit, and it is NOT a
   product-version bump — ADR-0016 keeps `version:` independent precisely so
   engine fixes never touch it.

4. **Every `delvec` subcommand the skill names EXISTS**, and every long flag it
   names alongside one exists on that subcommand or is a global. This is what
   makes the window a claim about something real rather than a shrug: the range
   is a claim about a CLI surface, so the gate reads that surface out of
   `crates/compiler/src/main.rs` (the clap `Command`/`EditAction` subcommand
   enums and the global `Cli` args) and holds the skill's own command spans
   against it. `delvec calibrate` losing its `--layout`, or a subcommand renamed
   out from under step 9, is exactly the drift a version range is supposed to
   make impossible.

5. **Every campaign stage document the ENGINE defines, the skill names.** Checks
   2-4 all run one way — is what the skill CLAIMS real? — and that is the
   direction that does not drift. A skill is written once and the engine moves,
   so the live failure is the engine growing an authoring surface the skill never
   learned, and nothing noticed: the map pipeline (spec-0049) landed
   `geometry-brief`, `layout-graph` and `site-plan` while the skill went on
   describing a six-stage loop, so an agent driving it authored campaigns with no
   way to say where anything was. The denominator is `Stage::name` in
   `crates/dsl/src/envelope.rs` — the crate's own one enumeration, the same one
   `delvec schema --stage all` exports from — so a stage added tomorrow is an
   unmentioned stage the moment it lands. There is no exemption list: a stage
   deliberately outside `/new-delve` says so IN the skill, because a list of
   stages nobody has to write is how the silence came back.

6. **Every number the page states about the engine's idiom index is true.** The
   page tells an author to read the idiom index before writing a grammar
   program, and it states that index's size in prose ("ten techniques",
   "usually one of the ten"). That is a claim about a table in the engine's
   `docs/reference/grammar.md`, and it goes stale the moment a technique is
   added there — silently, because prose has no compiler.

   The oracle and the phrasings are NOT re-implemented here. They are the
   engine's own `tools/check-stated-counts.py`, vendored beside this file and
   proven byte-identical to the pinned engine by `tools/check-vendored.py`, and
   this gate imports `ORACLES["idiom-techniques"]` from it. A private copy of a
   markdown-table parse rule is the defect CLAUDE.md names by name ("the parse
   rule is one shared authority, never a private copy per gate"); byte identity
   against the engine is what keeps that sentence true across two repositories
   rather than aspirational.

WHAT THIS GATE DOES *NOT* PROVE

Check 5 asks only that each stage is NAMED, as a whole token, somewhere in the
skill. It cannot tell a workflow step from a passing mention, and four of the ten
stage names (`world`, `classes`, `quests`, `dialogue`) are ordinary English words
that a skill about campaigns would contain by accident. That is deliberate and
the trade is stated rather than hidden: the surfaces this check exists for arrive
with compound names nobody writes incidentally, and demanding a stricter form —
backticks, a `.json` suffix — would red six stages the skill already covers and
buy a cosmetic edit instead of a workflow.

A floor that has become **too low**. If the skill starts driving a subcommand
that only appeared in `delvec` 1.1.0 while the window still says `>=1.0.0`, check
4 passes — it tests the skill against the engine at `authoring_ref`, which of
course has that subcommand — and nothing here notices that an engine at the
declared floor would choke. Catching it honestly needs older engines to test
against, and this gate judges against exactly one.

That gap is the reason `verified_with` earns its place: the window states intent
and is checked for internal consistency, while the field a reader can actually
rely on states which single engine anybody has run. Do not read a green here as
"the whole 1.x line was tested" — nothing tested it.

THE ONE COPY THIS FILE STILL CARRIES, AND WHAT CLOSES IT

The clap parser below (`parse_cli` and the regexes around it) is a SECOND COPY
of the engine's, and it is the one thing here that is not held to its source by
a machine. The engine has the same parser at `tools/lib/clap_surface.py`, where
`tools/build-release-binaries.sh` uses it to hold a released binary's `--help`
to its sources; this file cannot vendor it yet, because a vendored path must
exist at the revision `[engine].authoring_ref` names and that extraction landed
after it. Moving the pin to reach it is not a repair available here: this pin
moves only when somebody has WALKED `/new-delve` Init end to end against a
candidate revision, which is a decision with a different owner.

So it is recorded rather than hidden, with the exact condition that ends it:
**when `authoring_ref` next moves to a revision carrying
`tools/lib/clap_surface.py`, add that path to the `engine-authoring` entry's
`vendors`, import it here, and delete the copy below.** Until then the risk is
bounded and worth naming: the two parsers agree today, and a drift between them
makes THIS gate wrong about the engine's command surface — check 4 would go on
believing in a subcommand the engine had renamed. Nothing in either repository
would say so, which is precisely why the sentence is here instead of in a
planner's note.

WHY THE GATE LIVES HERE AND NOT IN THE ENGINE

It used to live in the engine repository, beside a copy of the skill page. The
page moved here (ADR-0014: a creator clones this repository and no other), the
gate did not, and for as long as that lasted the page an author executes was
checked by nothing while the gate held a copy nobody ran — the unbound
declaration it was written to prevent, recreated one repository over.

Two properties decide the home, and only this one has both. The gate must fire
on the event it guards: an EDIT TO THE PAGE, which happens in this repository,
so a job here is the only place that sees it when it happens. And it must judge
against the engine the declaration is ABOUT — not whatever engine sits in the
same checkout, but the one `/new-delve` Init step 2 tells the author to build,
which `versions.toml` `[engine].authoring_ref` names. The engine repository can
supply the second and structurally cannot supply the first: it reads this
repository only at a re-pin, so a page edited today would be judged whenever
somebody next moved the content pin, if ever.

THE ENGINE IS AN INSTRUMENT, SO IT IS NAMED BY REVISION

`--engine` is a path to an engine checkout; the REVISION read out of it is
`authoring_ref` from `versions.toml`, never the checkout's working tree and
never its HEAD. A checkout is a moving thing and a pin is not, so every file
this gate reads is materialised out of git at that one revision — which is also
why the CI checkout may sit at some other commit entirely, as it does: the audit
job's tree is at `ADMIT_REF` and fetches the authoring revision beside it.

There is NO default and NO fallback. A missing `--engine`, a path that is not a
git repository, a revision the checkout cannot serve, or a file absent at that
revision are each a refusal by name. A version gate that skipped when it could
not find its engine would be green exactly when it had checked nothing, which is
the UNRUN shape wearing a pass's colour.

On a creator's own machine the engine is the clone Init step 2 already made:

    python3 tools/check-skill-version.py --engine ../delvewright

BINDING COUNT

Every run prints what it examined: `delvec` mentions found in the skill's code
spans, subcommand references checked (and how many distinct), long-flag
references checked, how many of the engine's campaign stage documents the skill
names — stated as a fraction, because a coverage count without its denominator
is about a smaller world than the tool claims to cover — and how many stated
idiom-index counts were bound. **Zero subcommand references is a FAILURE, not a
pass** — it means the extraction stopped matching the skill's prose and checks
2-3 are all that is left standing. **Zero stage documents parsed is likewise a
FAILURE**: check 5 would then be silent about every surface at once. **Zero
stated idiom counts is a FAILURE** for the same reason: the page carried two
when this check was written, and a phrasing that stopped matching is
indistinguishable from a page that stopped claiming. A gate that binds to
nothing is vacuous.

Deterministic and dependency-free (Python 3 stdlib). The one thing it is not is
OFFLINE-from-the-engine: it reads a second repository, by path, at a pinned
revision, and refuses rather than guessing when it cannot.

    python3 tools/check-skill-version.py --engine <engine checkout>

Exit 0 = the declarations are true, 1 = a finding (see stderr), 2 = the engine
checkout or the manifest is unusable.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / ".claude" / "skills" / "new-delve" / "SKILL.md"
MANIFEST = REPO / "versions.toml"
STATED_COUNTS = REPO / "tools" / "check-stated-counts.py"

# Paths INSIDE the engine tree, materialised at `authoring_ref`. `crates/compiler/src`
# is taken whole rather than as one file: a `#[command(flatten)]`ed subcommand enum
# may be declared in any module of the crate, and a parse that stopped at `main.rs`
# would report a subcommand named after the flattening variant and miss the real ones.
ENGINE_PATHS = (
    "crates/compiler/Cargo.toml",
    "crates/compiler/src",
    "crates/dsl/src/envelope.rs",
    "docs/reference/grammar.md",
)

# `Stage::World => "world",` — the arms of `Stage::name`, which is the ONE
# enumeration of the campaign's stage documents and the same one
# `delvec schema --stage all` exports from.
STAGE_ARM_RE = re.compile(r'Stage::\w+\s*=>\s*"([a-z][a-z0-9-]*)"')

SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")

# `>=X.Y.Z <A.B.C` — the only range shape this project declares. Deliberately
# strict: the expected form is printed verbatim in every failure.
RANGE_RE = re.compile(r"^>=(?P<floor>\d+\.\d+\.\d+)\s+<(?P<ceiling>\d+\.\d+\.\d+)$")

CARGO_VERSION_RE = re.compile(r'(?m)^version\s*=\s*"([^"]+)"')

# --------------------------------------------------------------- frontmatter --

# YAML is not in the stdlib and the frontmatter is two levels deep at most, so
# it is parsed by hand rather than by pulling a dependency into a CI gate.
TOP_KEY_RE = re.compile(r"^(?P<key>[A-Za-z][\w-]*):\s*(?P<value>.*?)\s*$")
NESTED_KEY_RE = re.compile(r"^  (?P<key>[A-Za-z][\w-]*):\s*(?P<value>.*?)\s*$")


def read_frontmatter(path: Path) -> dict[str, object]:
    """`name`/`description`/`version` plus one level of nesting (`requires:`)."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise SystemExit(f"{path} does not open with a `---` frontmatter fence")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise SystemExit(f"{path}'s frontmatter fence is never closed") from exc

    out: dict[str, object] = {}
    current: str | None = None
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        nested = NESTED_KEY_RE.match(line)
        if nested and current is not None:
            sub = out.setdefault(current, {})
            if isinstance(sub, dict):
                sub[nested.group("key")] = unquote(nested.group("value"))
            continue
        top = TOP_KEY_RE.match(line)
        if top is None:
            continue
        value = top.group("value")
        if value == "":
            out[top.group("key")] = {}
            current = top.group("key")
        else:
            out[top.group("key")] = unquote(value)
            current = None
    return out


def unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


# ------------------------------------------------------------------- the CLI --

# A clap subcommand enum: `#[derive(Subcommand)] enum <Name> { ... }`. Variants
# sit at four spaces, their fields at eight — the shape rustfmt guarantees.
ENUM_RE = re.compile(
    r"(?ms)^#\[derive\(Subcommand\)\]\s*\n(?:pub\s+)?enum\s+(\w+)\s*\{(.*?)\n\}"
)
# `#[command(flatten)] View(some::path::ViewCommand),` — the flattened enum's own
# variants ARE top-level subcommands, so a parser that stopped at the variant
# name would report a subcommand (`view`) the CLI does not have and miss the six
# it does. The enum may live in any module of the crate, so its declaration is
# looked up across the crate's sources rather than in `main.rs` alone.
FLATTEN_ATTR_RE = re.compile(r"^\s*#\[command\(flatten\)\]")
FLATTEN_VARIANT_RE = re.compile(r"^    (?P<name>[A-Z]\w*)\((?P<ty>[\w:]+)\)")
VARIANT_RE = re.compile(r"^    (?P<name>[A-Z]\w*)\s*(?P<open>\{)?")
FIELD_RE = re.compile(r"^        (?P<name>[a-z]\w*)\s*:")
ARG_ATTR_RE = re.compile(r"^\s*#\[(?:arg|clap)\((?P<body>.*)")
EXPLICIT_LONG_RE = re.compile(r'long\s*=\s*"(?P<name>[^"]+)"')
SUBCOMMAND_ATTR_RE = re.compile(r"^\s*#\[command\(subcommand\)\]")
NESTED_TYPE_RE = re.compile(r":\s*(?:Option<)?(?P<name>[A-Z]\w*)")
GLOBAL_STRUCT_RE = re.compile(r"(?ms)^struct\s+Cli\s*\{(.*?)\n\}")
GLOBAL_FIELD_RE = re.compile(r"^    (?P<name>[a-z]\w*)\s*:")
# The top-level subcommand enum is whatever `Cli`'s own `#[command(subcommand)]`
# field names — everything else is a nested action set.
TOP_ENUM_RE = re.compile(
    r"#\[command\(subcommand\)\]\s*\n\s*command:\s*(?:Option<)?(?P<name>\w+)"
)


def kebab(name: str) -> str:
    """clap's default rename (heck's kebab-case): `L10nInventory` -> `l10n-inventory`."""
    spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "-", name)
    spaced = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", "-", spaced)
    return spaced.replace("_", "-").lower()


def normalize(name: str) -> str:
    """Hyphen-insensitive key, so this gate never has to re-implement heck exactly.

    The failure it exists to catch — the skill naming a subcommand or flag that
    does NOT exist — is caught either way; re-deriving clap's word-boundary rules
    would only add a way for the gate itself to be wrong.
    """
    return name.replace("-", "").replace("_", "").lower()


def parse_cli(source: str) -> tuple[dict[str, set[str]], set[str]]:
    """`{top-level subcommand: {long flags}}` and the set of global long flags.

    A nested action set (`delvec edit apply|preview`) is NOT a top-level
    subcommand — `delvec apply` does not exist — but its flags are folded into
    its parent's allowed set, so `delvec edit apply --batch` reads correctly.
    """
    enums: dict[str, dict[str, set[str]]] = {}
    nested: dict[str, dict[str, str]] = {}
    flattened: dict[str, set[str]] = {}

    for enum_name, body in ENUM_RE.findall(source):
        variants: dict[str, set[str]] = {}
        links: dict[str, str] = {}
        variant: str | None = None
        pending_long: str | None = None
        pending_is_long = False
        pending_subcommand = False
        pending_flatten = False
        for line in body.splitlines():
            attr = ARG_ATTR_RE.match(line)
            if attr is not None:
                attr_body = attr.group("body")
                explicit = EXPLICIT_LONG_RE.search(attr_body)
                pending_is_long = bool(re.search(r"\blong\b", attr_body))
                pending_long = explicit.group("name") if explicit else None
                continue
            if SUBCOMMAND_ATTR_RE.match(line):
                pending_subcommand = True
                continue
            field = FIELD_RE.match(line)
            if field is not None and variant is not None:
                if pending_is_long:
                    variants[variant].add(pending_long or kebab(field.group("name")))
                if pending_subcommand:
                    link = NESTED_TYPE_RE.search(line)
                    if link is not None:
                        links[variant] = link.group("name")
                pending_long, pending_is_long = None, False
                pending_subcommand = False
                continue
            if FLATTEN_ATTR_RE.match(line):
                pending_flatten = True
                continue
            if pending_flatten:
                flat = FLATTEN_VARIANT_RE.match(line)
                if flat is not None:
                    flattened.setdefault(enum_name, set()).add(
                        flat.group("ty").split("::")[-1]
                    )
                    pending_flatten = False
                    variant = None
                    continue
                pending_flatten = False
            var = VARIANT_RE.match(line)
            if var is not None:
                variant = kebab(var.group("name"))
                variants.setdefault(variant, set())
                pending_long, pending_is_long = None, False
                pending_subcommand = False
        enums[enum_name] = variants
        nested[enum_name] = links

    top_name_match = TOP_ENUM_RE.search(source)
    top_name = top_name_match.group("name") if top_name_match else "Command"
    subcommands = {name: set(flags) for name, flags in enums.get(top_name, {}).items()}
    for variant, child in nested.get(top_name, {}).items():
        for flags in enums.get(child, {}).values():
            subcommands.setdefault(variant, set()).update(flags)
    # A flattened enum contributes its OWN variants as top-level subcommands.
    for child in flattened.get(top_name, set()):
        for name, flags in enums.get(child, {}).items():
            subcommands.setdefault(name, set()).update(flags)

    globals_: set[str] = set()
    struct = GLOBAL_STRUCT_RE.search(source)
    if struct is not None:
        pending_long = None
        pending_is_long = False
        for line in struct.group(1).splitlines():
            attr = ARG_ATTR_RE.match(line)
            if attr is not None:
                attr_body = attr.group("body")
                explicit = EXPLICIT_LONG_RE.search(attr_body)
                pending_is_long = bool(re.search(r"\blong\b", attr_body))
                pending_long = explicit.group("name") if explicit else None
                continue
            field = GLOBAL_FIELD_RE.match(line)
            if field is not None:
                if pending_is_long:
                    globals_.add(pending_long or kebab(field.group("name")))
                pending_long, pending_is_long = None, False
    # `--help` is clap's, not ours, and never appears in the enum.
    globals_.add("help")
    return subcommands, globals_


# ------------------------------------------------- what the skill claims to drive --

FENCE_RE = re.compile(r"^\s*```")
# A markdown code span may wrap across a line (it renders as a space) but never
# across a blank line — `delvec calibrate <report> --layout …` in this skill is
# split over two source lines, and a newline-free pattern silently misses it.
INLINE_CODE_RE = re.compile(r"`((?:[^`\n]|\n(?!\s*\n))+?)`")
SUBCOMMAND_TOKEN_RE = re.compile(r"^[a-z][a-z0-9-]*$")
LONG_FLAG_RE = re.compile(r"^--(?P<name>[a-z][a-z0-9-]*)(?:=.*)?$")

# `` `delvec <sub>` (`--flag …`, `--flag …`) `` — the paren must open IMMEDIATELY
# after the span, so this keys off syntax rather than paragraph proximity: it is
# how `delvec snapshot`'s flags are documented, and a looser "same bullet" rule
# would red on an innocent later edit.
PARENTHETICAL_RE = re.compile(r"`delvec ([a-z][a-z0-9-]*)[^`]*`\s*\(")


def code_spans(markdown: str) -> list[str]:
    """Every inline-code span and fenced-block line, in document order.

    Only code is read. A version gate that tried to parse commands out of prose
    would red on a sentence and pass on a broken invocation.
    """
    spans: list[str] = []
    fenced = False
    prose: list[str] = []
    for line in markdown.splitlines():
        if FENCE_RE.match(line):
            fenced = not fenced
            continue
        if fenced:
            spans.append(line)
        else:
            prose.append(line)
    spans.extend(INLINE_CODE_RE.findall("\n".join(prose)))
    return spans


def parenthetical_flags(markdown: str) -> list[tuple[str, list[str]]]:
    """Flags documented in the parenthesis that opens right after a subcommand span."""
    out: list[tuple[str, list[str]]] = []
    for match in PARENTHETICAL_RE.finditer(markdown):
        depth = 1
        i = match.end()
        while i < len(markdown) and depth:
            if markdown[i] == "(":
                depth += 1
            elif markdown[i] == ")":
                depth -= 1
            i += 1
        inner = markdown[match.end() : i - 1]
        flags = [
            m.group("name")
            for span in INLINE_CODE_RE.findall(inner)
            for token in span.split()
            if (m := LONG_FLAG_RE.match(token.strip(",.;:()[]'\"")))
        ]
        if flags:
            out.append((match.group(1), flags))
    return out


def invocations(spans: list[str]) -> list[tuple[str | None, list[str]]]:
    """`(subcommand | None, [long flags])` for every `delvec …` span occurrence.

    `None` is a bare mention (`` `delvec` ``, `` `delvec --version` ``): its
    flags are still held against the globals. A token that is not a lowercase
    word — a placeholder `<version>`, a version number, a flag — yields no
    subcommand, which is how the storybook marker template in this same file
    ("last verified with delvec <version>.") contributes nothing.

    Since ADR-0017 the CARGO PACKAGE is also called `delvec`, so `delvec` now
    appears in the skill as an argument to cargo (`-p delvec`, `--bin delvec`)
    as well as as a command. Those occurrences are not invocations and the
    tokens after them belong to cargo, not to this CLI — reading them as
    invocations made `cargo build -p delvec --bin delvec` report that `delvec`
    was given a `--bin` flag it does not have.

    The discriminator is the selector in front TOGETHER with the `--` behind:
    `cargo run … --bin delvec -- schema` really does hand `schema` to this CLI,
    so that occurrence is an invocation, while `-p delvec` and a `--bin delvec`
    that ends the command are pure cargo arguments. Dropping only on the
    selector loses the `-- schema` binding, which the test beside this asserts
    in both directions.
    """
    CARGO_SELECTORS = {"-p", "--package", "--bin", "--example"}
    found: list[tuple[str | None, list[str]]] = []
    for span in spans:
        tokens = span.replace("`", " ").split()
        for i, token in enumerate(tokens):
            if token != "delvec":
                continue
            after = tokens[i + 1] if i + 1 < len(tokens) else None
            if i > 0 and tokens[i - 1] in CARGO_SELECTORS and after != "--":
                continue
            rest = tokens[i + 1 :]
            if rest and rest[0] == "--":  # `cargo run … --bin delvec -- schema`
                rest = rest[1:]
            sub: str | None = None
            if rest and SUBCOMMAND_TOKEN_RE.match(rest[0]):
                sub = rest[0]
                rest = rest[1:]
            flags: list[str] = []
            for tok in rest:
                if tok == "delvec":
                    break
                m = LONG_FLAG_RE.match(tok.strip("`,.;:()[]'\""))
                if m is not None:
                    flags.append(m.group("name"))
            found.append((sub, flags))
    return found


# ------------------------------------------------------------------- the gate --


def version_key(version: str) -> tuple[int, int, int]:
    m = SEMVER_RE.match(version)
    if m is None:
        raise SystemExit(f"not a semver version: {version!r}")
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)))


def engine_major_floor(version: str) -> str:
    """The start of `version`'s major window — what a suggested `requires:` opens at.

    The window floor is a COMPATIBILITY claim, so a suggestion never proposes the
    current engine as the floor: that would assert every earlier release in the
    same major is unsupported, which nothing tested.
    """
    return f"{version_key(version)[0]}.0.0"


def engine_version(cargo_toml: Path) -> str:
    text = cargo_toml.read_text(encoding="utf-8")
    match = CARGO_VERSION_RE.search(text)
    if match is None:
        raise SystemExit(
            f"could not read `version` from crates/compiler/Cargo.toml — the [package] "
            "version field moved or changed shape; fix this check, do not drop the gate"
        )
    return match.group(1)


def stage_names(envelope_rs: Path) -> list[str]:
    """Every campaign stage document the engine defines, in document order.

    Read out of `Stage::name`'s match arms, which is the crate's own one
    enumeration and the same one `delvec schema --stage all` exports from —
    parsed textually for the same reason check 4 parses the clap enums: this gate
    never builds the compiler to ask it, so it costs a `git archive` and no cargo.
    """
    return STAGE_ARM_RE.findall(envelope_rs.read_text(encoding="utf-8"))


# ----------------------------------------------------------- the engine tree --


def authoring_ref() -> str:
    """The engine revision an author builds — `versions.toml` `[engine].authoring_ref`.

    Read, never restated. `tools/check-authoring-pin.py` holds this key to being a
    full 40-hex revision and to living in this file alone; this gate is the second
    reader of the same value, and it reads it from the same place for the same
    reason a literal here would go stale the first time the pin moved.
    """
    try:
        manifest = tomllib.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise SystemExit(f"check-skill-version: FAIL — {MANIFEST} is unusable: {exc}")
    try:
        rev = manifest["engine"]["authoring_ref"]
    except (KeyError, TypeError):
        raise SystemExit(
            "check-skill-version: FAIL — versions.toml has no `[engine].authoring_ref`. "
            "That key names the engine `/new-delve` Init step 2 builds, which is the "
            "engine this gate's whole question is about; without it there is nothing "
            "to judge the page against and a pass would mean nothing was checked."
        )
    if not isinstance(rev, str) or not re.fullmatch(r"[0-9a-f]{40}", rev):
        raise SystemExit(
            f"check-skill-version: FAIL — `[engine].authoring_ref` is {rev!r}, not a "
            "full 40-hex revision. An instrument named by a branch or a tag is a "
            "moving instrument (tools/check-authoring-pin.py holds this too)."
        )
    return rev


def materialise_engine(checkout: Path, rev: str, into: Path) -> Path:
    """Extract the engine paths this gate reads, at `rev`, out of `checkout`.

    `git archive | tar -x` rather than a checkout of the working tree, because the
    working tree is whatever somebody last ran and the pin is the instrument. In CI
    the checkout is at `ADMIT_REF` and the authoring revision is fetched beside it,
    so its working tree is a DIFFERENT engine — reading files off disk there would
    silently judge the page against a revision nobody chose.
    """
    if not (checkout / ".git").exists():
        raise SystemExit(
            f"check-skill-version: FAIL — {checkout} is not a git checkout. "
            "`--engine` wants a clone of stellarfeline/delvewright; on a creator's "
            "machine that is the clone `/new-delve` Init step 2 made."
        )
    try:
        subprocess.run(
            ["git", "-C", str(checkout), "cat-file", "-e", f"{rev}^{{commit}}"],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError:
        raise SystemExit(
            f"check-skill-version: FAIL — {checkout} cannot serve {rev[:8]}, the "
            "engine revision `versions.toml` `[engine].authoring_ref` names. Fetch it "
            f"(`git -C {checkout} fetch origin {rev}`) — this is the same fetch an "
            "author's Init performs, and a revision the remote will not serve fails "
            "for them too. Judging the page against some other engine instead is the "
            "one thing this gate may not do."
        )
    proc = subprocess.run(
        ["git", "-C", str(checkout), "archive", rev, *ENGINE_PATHS],
        capture_output=True,
    )
    if proc.returncode != 0:
        raise SystemExit(
            f"check-skill-version: FAIL — could not read {', '.join(ENGINE_PATHS)} "
            f"from the engine at {rev[:8]}: "
            f"{proc.stderr.decode('utf-8', 'replace').strip()}\n"
            "    A path this gate reads has moved in the engine. Fix the path, do "
            "not drop the gate."
        )
    tar = subprocess.run(
        ["tar", "-x", "-C", str(into)], input=proc.stdout, capture_output=True
    )
    if tar.returncode != 0:
        raise SystemExit(
            "check-skill-version: FAIL — could not unpack the engine archive: "
            f"{tar.stderr.decode('utf-8', 'replace').strip()}"
        )
    return into


def stated_counts_module():
    """The engine's own `check-stated-counts.py`, vendored beside this file.

    Imported rather than reimplemented. Its `ORACLES["idiom-techniques"]` carries
    both halves of the claim — how the §2c index table is parsed, and every prose
    phrasing that states its size — and a second copy of either is the private
    re-implementation CLAUDE.md forbids. `tools/check-vendored.py` proves this file
    byte-identical to the pinned engine's, which is what makes "one shared
    authority" true across two repositories instead of merely intended.
    """
    if not STATED_COUNTS.is_file():
        raise SystemExit(
            f"check-skill-version: FAIL — {STATED_COUNTS} is missing. It is the "
            "vendored oracle for every number this page states about the engine's "
            "idiom index; without it check 6 checks nothing."
        )
    spec = importlib.util.spec_from_file_location("_stated_counts", STATED_COUNTS)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--engine",
        required=True,
        type=Path,
        metavar="PATH",
        help=(
            "a git checkout of stellarfeline/delvewright. The REVISION read from it "
            "is `versions.toml` `[engine].authoring_ref`, never the checkout's HEAD "
            "or its working tree. Required and never defaulted: a version gate that "
            "guessed its engine would be green having compared the page to whatever "
            "happened to be lying about."
        ),
    )
    args = ap.parse_args(argv)

    if not SKILL.is_file():
        print(f"check-skill-version: FAIL — {SKILL} is missing", file=sys.stderr)
        return 2

    rev = authoring_ref()
    with tempfile.TemporaryDirectory(prefix="skill-version-engine-") as tmp:
        engine_root = materialise_engine(args.engine, rev, Path(tmp))
        return check(engine_root, rev)


def check(engine_root: Path, rev: str) -> int:
    compiler_cargo_toml = engine_root / "crates" / "compiler" / "Cargo.toml"
    compiler_main_rs = engine_root / "crates" / "compiler" / "src" / "main.rs"
    envelope_rs = engine_root / "crates" / "dsl" / "src" / "envelope.rs"

    for path in (compiler_cargo_toml, compiler_main_rs, envelope_rs):
        rel = path.relative_to(engine_root)
        if not path.is_file():
            print(
                f"check-skill-version: FAIL — the engine at {rev[:8]} has no {rel}. "
                "A file this gate reads has moved; fix the path, do not drop the gate",
                file=sys.stderr,
            )
            return 2

    findings: list[str] = []
    front = read_frontmatter(SKILL)
    engine = engine_version(compiler_cargo_toml)

    # -- 1. shape ------------------------------------------------------------
    for key in ("name", "description"):
        if not isinstance(front.get(key), str):
            findings.append(
                f"frontmatter has no `{key}:` — the skill loader needs it; this gate "
                "adds fields to that block, it never replaces it"
            )

    skill_version = front.get("version")
    if not isinstance(skill_version, str) or not SEMVER_RE.match(skill_version):
        findings.append(
            f"frontmatter `version:` is missing or not semver (got {skill_version!r}). "
            "ADR-0016 line 3: the /new-delve skill carries its OWN version, on its own "
            "cadence — engine fixes never bump it, skill rewording never forces an "
            "engine release. Expected e.g. `version: 1.0.0`"
        )

    requires = front.get("requires")
    declared = requires.get("delvec") if isinstance(requires, dict) else None
    range_match = RANGE_RE.match(declared) if isinstance(declared, str) else None
    if range_match is None:
        findings.append(
            f"frontmatter `requires: delvec:` is missing or malformed (got "
            f"{declared!r}). ADR-0016 line 3 pairs the skill's version with the "
            f"delvec window it DRIVES — a MAJOR window, stable across the whole "
            f"line. Expected exactly:\n"
            f'    requires:\n      delvec: ">={engine_major_floor(engine)} '
            f'<{version_key(engine)[0] + 1}.0.0"'
        )

    verified = front.get("verified_with")
    if not isinstance(verified, str) or not SEMVER_RE.match(verified):
        findings.append(
            f"frontmatter `verified_with:` is missing or not semver (got "
            f"{verified!r}). `requires.delvec` states COMPATIBILITY (what a creator "
            f"reads as 'older engines will not work'); `verified_with` states "
            f"EVIDENCE — the one engine the page is actually proven on. "
            f"Expected `verified_with: {engine}`"
        )

    # -- 2. the window is well formed, and this engine is INSIDE it ----------
    if range_match is not None:
        floor = range_match.group("floor")
        ceiling = range_match.group("ceiling")
        expected_ceiling = f"{version_key(floor)[0] + 1}.0.0"

        if ceiling != expected_ceiling:
            findings.append(
                f"declared ceiling {ceiling} is not the floor's next major "
                f"({expected_ceiling}). A major release may remove any subcommand the "
                f"skill drives, so the window closes at the next major and nowhere else"
            )
        elif not version_key(floor) <= version_key(engine) < version_key(ceiling):
            findings.append(
                f"the authoring engine's delvec {engine} is OUTSIDE the declared window "
                f"{declared} — the page drives an engine it says it does not drive.\n"
                f"    engine {rev[:8]} crates/compiler/Cargo.toml [package] version "
                f"= {engine} (== DELVEC_VERSION). Widen or move the window:\n"
                f'      delvec: ">={engine_major_floor(engine)} '
                f'<{version_key(engine)[0] + 1}.0.0"\n'
                f"    That is the WINDOW moving, not the product version: leave "
                f"`version: {skill_version}` alone unless the skill's own workflow changed."
            )

    # -- 3. `verified_with` IS this repo's engine, both directions -----------
    if isinstance(verified, str) and SEMVER_RE.match(verified) and verified != engine:
        direction = (
            "ABOVE the authoring engine — it names a compiler that does not exist, so "
            "no run anywhere produced that evidence"
            if version_key(verified) > version_key(engine)
            else "STALE — the engine moved and nobody re-ran the skill against it, so "
            "the field records evidence from a build the authoring pin no longer names. "
            "An unverifiable claim is an unbound declaration (CLAUDE.md)"
        )
        findings.append(
            f"`verified_with: {verified}` is {direction}.\n"
            f"    engine {rev[:8]} crates/compiler/Cargo.toml [package] version "
            f"= {engine} (== DELVEC_VERSION). Restamp it:\n"
            f"      verified_with: {engine}\n"
            f"    Leave `requires.delvec` alone unless the skill genuinely stopped "
            f"driving the older engines in its window — that is a compatibility "
            f"claim, and this one is only evidence."
        )

    # -- 4. every command the skill names exists -----------------------------
    # `main.rs` first, so its `Cli` struct decides which enum is top-level and
    # what the globals are; then every other module of the same directory tree,
    # because a `#[command(flatten)]`ed subcommand enum may be declared anywhere
    # in the crate — `delvec`'s CPU render arms are in `src/view/cli.rs` — and a
    # parser that stopped at `main.rs` would report a subcommand named after the
    # flattening variant and miss the six that actually exist.
    #
    # The scan root is DERIVED from `compiler_main_rs` rather than named
    # separately, so that redirecting that one path redirects the whole parse.
    # A second constant pointing at the real crate would let this gate's own
    # "an unparseable CLI is a failure, not a pass" case find real enums beside
    # the stub and go green having parsed something else entirely.
    sources = [compiler_main_rs.read_text(encoding="utf-8")]
    sources += [
        f.read_text(encoding="utf-8")
        for f in sorted(compiler_main_rs.parent.rglob("*.rs"))
        if f != compiler_main_rs
    ]
    subcommands, globals_ = parse_cli("\n".join(sources))
    if not subcommands:
        print(
            "check-skill-version: FAIL — parsed 0 subcommands from "
            f"crates/compiler/src at engine {rev[:8]}; the clap "
            "`#[derive(Subcommand)] enum` shape this gate keys off has changed. "
            "Fix the parser, do not drop the gate",
            file=sys.stderr,
        )
        return 1

    by_norm = {normalize(name): name for name in subcommands}
    flags_by_norm = {
        normalize(name): {normalize(f) for f in flags}
        for name, flags in subcommands.items()
    }
    global_norm = {normalize(f) for f in globals_}

    markdown = SKILL.read_text(encoding="utf-8")
    calls: list[tuple[str | None, list[str]]] = invocations(code_spans(markdown))
    calls.extend(parenthetical_flags(markdown))
    sub_refs = 0
    flag_refs = 0
    seen: set[str] = set()

    for sub, flags in calls:
        allowed = set(global_norm)
        if sub is not None:
            sub_refs += 1
            seen.add(sub)
            key = normalize(sub)
            if key not in by_norm:
                findings.append(
                    f"the skill drives `delvec {sub}`, which the CLI does not have.\n"
                    f"    engine {rev[:8]} crates/compiler/src/main.rs offers: "
                    f"{', '.join(sorted(subcommands))}"
                )
                continue
            allowed |= flags_by_norm[key]
        for flag in flags:
            flag_refs += 1
            if normalize(flag) not in allowed:
                where = f"`delvec {sub}`" if sub else "`delvec`"
                findings.append(
                    f"{where} is given `--{flag}`, which is neither one of its own "
                    f"args nor a global. Globals: "
                    f"{', '.join('--' + f for f in sorted(globals_))}"
                )

    # -- 5. every stage the ENGINE defines, the skill knows how to author -----
    #
    # The other direction, and the one nothing checked. Checks 2-4 all ask
    # whether what the SKILL claims exists in the engine — a skill naming a
    # subcommand that was renamed out from under it. Nothing asked the reverse:
    # a whole authoring pipeline the engine has and the skill is silent about.
    # That is a check which can only fail in the direction that does not drift.
    # Skills are written once and the engine moves, so the live failure is
    # always the engine growing a surface the skill never learned — the map
    # pipeline (spec-0049) landed three campaign stage documents and the skill
    # went on describing a six-stage loop, so an agent driving it authored
    # campaigns that could not state where anything was.
    #
    # The denominator is the engine's own enumeration, so a stage added tomorrow
    # is an unmentioned stage the moment it lands.
    stages = stage_names(envelope_rs)
    unmentioned = [
        s for s in stages if not re.search(rf"(?<![\w-]){re.escape(s)}(?![\w-])", markdown)
    ]
    for s in unmentioned:
        findings.append(
            f"the engine defines the campaign stage document `{s}.json` and the "
            f"skill never mentions it. An authoring surface the skill is silent "
            f"about is a surface no /new-delve run will ever write, however "
            f"complete the engine's side is — and nothing else in this repo "
            f"notices, because every other gate asks whether the SKILL's claims "
            f"exist rather than whether the ENGINE's surfaces are driven.\n"
            f"    engine {rev[:8]} crates/dsl/src/envelope.rs `Stage::name` "
            f"defines: "
            f"{', '.join(stages)}\n"
            f"    Add the stage to the skill's workflow — where in the loop it is "
            f"authored, what it states, and which check refuses a campaign that "
            f"skips it. If the stage is deliberately not part of /new-delve, say "
            f"so IN the skill; there is no exemption list here, because a list "
            f"of stages nobody has to write is how the silence came back."
        )

    # -- 6. every number the page states about the idiom index is true --------
    #
    # The page's own prose, held to a table in the engine. This claim used to be
    # a row in the engine's `tools/check-stated-counts.py` SITES table, pointing
    # at the engine's copy of this page; the page moved here and the row could
    # not follow it across a repository boundary, so the claim comes with it
    # rather than being dropped — dropping it would have been a silent loosening
    # of that gate, invisible in either repository's diff.
    #
    # The oracle and the phrasings are the engine's, imported from the vendored
    # copy. Nothing about the parse is restated here: `rows_matching` refusing a
    # row that a blank line detached from its table is a rule this gate gets for
    # free by not owning it.
    counts = stated_counts_module()
    techniques = counts.ORACLES["idiom-techniques"]
    try:
        expected, evidence = techniques["compute"](engine_root)
    except LookupError as exc:
        print(
            f"check-skill-version: FAIL — the engine's idiom index did not parse at "
            f"{rev[:8]}: {exc}",
            file=sys.stderr,
        )
        return 1

    page_text = counts.strip_code_fences(markdown)
    count_refs = 0
    for pattern, offset in techniques["phrasings"]:
        for match in re.finditer(pattern, page_text, re.I):
            count_refs += 1
            got, want = counts.parse_number(match.group(1)), expected + offset
            if got == want:
                continue
            claim = (
                f"claims there is no number {got}"
                if offset
                else f"claims there are {got}"
            )
            findings.append(
                f"the skill {claim} {techniques['describe']}, and the engine at "
                f"{rev[:8]} has {expected}.\n"
                f"    {evidence}\n"
                f"    The page sends an author to that index to pick a technique, "
                f"so a stale number there is a number they will act on. Restate it, "
                f"or — if the index really changed — this is the engine moving and "
                f"the authoring pin is what decides which index the page describes."
            )

    # -- vacuity guards ------------------------------------------------------
    #
    # Ordered widest-first: a tree whose `Stage::name` stopped parsing and a page
    # whose command spans stopped matching are each silent about a whole check,
    # while a page that states no idiom count is silent about one number. Report
    # the biggest silence first — the narrower one is usually a consequence.
    if not stages:
        print(
            f"check-skill-version: FAIL — parsed 0 stage documents from "
            f"crates/dsl/src/envelope.rs at engine {rev[:8]}; the `Stage::name` "
            f"match-arm shape "
            "this gate keys off has changed. Fix the parser, do not drop the gate",
            file=sys.stderr,
        )
        return 1
    if sub_refs == 0:
        print(
            "check-skill-version: FAIL — extracted 0 delvec subcommand references "
            f"from {SKILL.relative_to(REPO)}. The range would then be a claim "
            f"about a "
            "CLI surface nothing in this gate ever touched; a green that binds to "
            "nothing is vacuous, not a pass (CLAUDE.md).",
            file=sys.stderr,
        )
        return 1
    if count_refs == 0:
        print(
            "check-skill-version: FAIL — the skill states 0 idiom-index counts. It "
            "carried two when this check was written, and a phrasing that stopped "
            "matching is indistinguishable from a page that stopped claiming — both "
            "leave the number unchecked, which is the state this check ended. If the "
            "page genuinely no longer describes the index, delete this check and say "
            "so; do not leave it binding to nothing (CLAUDE.md).",
            file=sys.stderr,
        )
        return 1

    binding = (
        f"{len(calls)} delvec mention(s) in code spans, {sub_refs} subcommand "
        f"reference(s) over {len(seen)} distinct subcommand(s) "
        f"({', '.join(sorted(seen))}), {flag_refs} long-flag reference(s), "
        f"{len(stages) - len(unmentioned)} of the engine's {len(stages)} campaign "
        f"stage document(s) named in the skill, and {count_refs} stated "
        f"idiom-index count(s)"
    )
    # The instrument, named by revision rather than by "the pinned engine": a
    # frozen measurement that names its instrument through an indirection
    # re-reads every recorded figure against a different one the moment the pin
    # moves, and says nothing about it.
    instrument = f"engine {rev} (versions.toml [engine].authoring_ref)"

    if findings:
        print(
            f"check-skill-version: {len(findings)} finding(s) — bound to {binding}, "
            f"against {instrument}\n",
            file=sys.stderr,
        )
        for finding in findings:
            print(f"  - {finding}", file=sys.stderr)
        return 1

    print(
        f"check-skill-version: OK — new-delve {skill_version} drives {declared}, "
        f"verified_with {verified}, engine is {engine}. Bound to {binding}. "
        f"Judged against {instrument}. "
        f"(Membership only: nothing here tested an engine other than {engine}.)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
