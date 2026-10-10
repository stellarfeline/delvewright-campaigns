#!/usr/bin/env python3
"""Fetch the pinned engine release's `delvec` binary, verified, for this machine.

A release of this content is built by the engine release `versions.toml`
`[engine].ref` pins, and by nothing else: `.github/workflows/release.yml` never
compiles `delvec`, it runs the binary the engine published. This script is the
one place that turns the pin into that binary.

1. The pin is a release tag of the `delvec` line in the engine's own grammar
   (`delvec--v<major>.<minor>.<patch>`, judged by the vendored
   `tools/lib/release_tags.py`). Anything else is refused: a commit, a branch,
   or another line's tag is not a release this script can download.
2. The archive for this machine's target, `delvec-v<version>-<target>.tar.gz`,
   and the release's `SHA256SUMS` are downloaded from the engine repository's
   GitHub Release for that tag. A missing release, a missing asset, or a
   `SHA256SUMS` with no line for the archive refuses.
3. The archive's sha256 must equal its `SHA256SUMS` line. A mismatch refuses.
4. The archive is unpacked and the binary must report the tag's own version on
   `delvec --version`. A disagreement refuses.

There is no fallback to building from source: a refusal here refuses the release.

Outputs `key=value` lines (also appended to `--github-output` when given):
`repo`, `tag`, `version`, `target`, `archive`, `archive_sha256`, `bin`,
`delvec_version`.

Stdlib only. Exit 0 = the binary is ready, 1 = refused, 2 = usage / unusable input.
"""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import platform
import re
import stat
import subprocess
import sys
import tarfile
import tomllib
import urllib.error
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "lib"))
import release_tags  # noqa: E402  — one grammar, vendored, never a second copy

LINE = "delvec"

# (`uname -s`, `uname -m`) -> the Rust target triple the engine release names its
# archives by. A machine outside this table has no archive and is refused.
TARGETS = {
    ("Linux", "x86_64"): "x86_64-unknown-linux-gnu",
    ("Linux", "aarch64"): "aarch64-unknown-linux-gnu",
    ("Linux", "arm64"): "aarch64-unknown-linux-gnu",
    ("Darwin", "arm64"): "aarch64-apple-darwin",
    ("Darwin", "x86_64"): "x86_64-apple-darwin",
}

VERSION_OUT_RE = re.compile(r"^delvec (\d+\.\d+\.\d+)\b")


class Refused(Exception):
    """The release cannot be built with this engine pin; the message says why."""


def release_version(tag: str) -> str:
    """The `delvec` version a pin names; `Refused` unless it is a `delvec` release tag."""
    try:
        name, version = release_tags.parse(tag)
    except release_tags.Refused as exc:
        raise Refused(
            f"engine pin {tag!r} is not a release: {exc} A release is built by a "
            f"published `{LINE}--v<major>.<minor>.<patch>` engine release and by "
            f"nothing else."
        ) from None
    if name != LINE:
        raise Refused(
            f"engine pin {tag!r} is a release of `{name}`, not of `{LINE}`: only a "
            f"`{LINE}--v<version>` release carries the binary a delve is built with."
        )
    return version


def target_for(system: str, machine: str) -> str:
    try:
        return TARGETS[(system, machine)]
    except KeyError:
        raise Refused(
            f"no engine release archive exists for this machine ({system} {machine}); "
            f"targets with an archive: {sorted(set(TARGETS.values()))}"
        ) from None


def archive_name(version: str, target: str) -> str:
    return f"{LINE}-v{version}-{target}.tar.gz"


def expected_sha256(sums: str, archive: str) -> str:
    """The digest `SHA256SUMS` records for `archive` (`sha256sum` text or binary form)."""
    found = []
    for raw in sums.splitlines():
        parts = raw.strip().split(maxsplit=1)
        if len(parts) != 2:
            continue
        digest, name = parts
        if name.startswith("*"):
            name = name[1:]
        if name == archive:
            found.append(digest.lower())
    if not found:
        raise Refused(f"SHA256SUMS has no line for {archive}")
    if len(set(found)) != 1:
        raise Refused(f"SHA256SUMS has {len(found)} disagreeing lines for {archive}")
    if not re.fullmatch(r"[0-9a-f]{64}", found[0]):
        raise Refused(f"SHA256SUMS line for {archive} is not a sha256 digest")
    return found[0]


def download(url: str, dest: pathlib.Path, what: str) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "delvewright-campaigns-release"})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp, dest.open("wb") as fh:
            while chunk := resp.read(1 << 20):
                fh.write(chunk)
    except urllib.error.HTTPError as exc:
        raise Refused(
            f"{what} could not be downloaded ({url}: HTTP {exc.code}); the pin must "
            f"name a published engine release that carries it"
        ) from None
    except urllib.error.URLError as exc:
        raise Refused(f"{what} could not be downloaded ({url}: {exc.reason})") from None


def unpack(archive: pathlib.Path, dest: pathlib.Path) -> pathlib.Path:
    with tarfile.open(archive, "r:gz") as tf:
        names = tf.getnames()
        if LINE not in names:
            raise Refused(f"{archive.name} carries no `{LINE}` at its root (members: {names})")
        tf.extractall(dest, filter="data")
    binary = dest / LINE
    binary.chmod(binary.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return binary


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--versions", default="versions.toml", help="the manifest whose [engine] is read")
    ap.add_argument("--ref", default="", help="a release tag to use instead of [engine].ref (refused unless it is one)")
    ap.add_argument("--dest", required=True, help="an empty or new directory to download and unpack into")
    ap.add_argument("--github-output", default="", help="append the key=value outputs to this file")
    args = ap.parse_args()

    try:
        with open(args.versions, "rb") as fh:
            engine = tomllib.load(fh)["engine"]
        repo, pinned = engine["repo"], engine["ref"]
    except (OSError, KeyError, tomllib.TOMLDecodeError) as exc:
        print(f"fetch-delvec: FATAL — {args.versions} has no usable [engine] repo/ref: {exc}", file=sys.stderr)
        return 2
    tag = args.ref or pinned

    try:
        version = release_version(tag)
        target = target_for(platform.system(), platform.machine())
        archive = archive_name(version, target)
        base = f"https://github.com/{repo}/releases/download/{tag}"
        dest = pathlib.Path(args.dest).resolve()
        dest.mkdir(parents=True, exist_ok=True)
        if any(dest.iterdir()):
            print(f"fetch-delvec: FATAL — {dest} is not empty", file=sys.stderr)
            return 2

        print(f"fetch-delvec: engine release {tag} ({'override' if args.ref else 'versions.toml [engine].ref'}), target {target}", file=sys.stderr)
        sums_path = dest / "SHA256SUMS"
        download(f"{base}/SHA256SUMS", sums_path, f"SHA256SUMS of {tag}")
        want = expected_sha256(sums_path.read_text(encoding="utf-8"), archive)
        arc_path = dest / archive
        download(f"{base}/{archive}", arc_path, f"{archive} of {tag}")
        got = hashlib.sha256(arc_path.read_bytes()).hexdigest()
        if got != want:
            raise Refused(f"{archive} sha256 {got} != SHA256SUMS {want}")
        print(f"fetch-delvec: {archive} sha256 {got} matches SHA256SUMS", file=sys.stderr)

        binary = unpack(arc_path, dest / "bin")
        run = subprocess.run([str(binary), "--version"], capture_output=True, text=True)
        out = run.stdout.strip()
        print(f"fetch-delvec: {binary} --version -> exit {run.returncode}: {out}", file=sys.stderr)
        m = VERSION_OUT_RE.match(out)
        if run.returncode != 0 or not m:
            raise Refused(f"the unpacked binary did not report a delvec version (exit {run.returncode}): {out!r} {run.stderr.strip()!r}")
        if m.group(1) != version:
            raise Refused(f"the binary reports delvec {m.group(1)}, and the release tag is {tag}")
    except Refused as exc:
        print(f"fetch-delvec: REFUSED — {exc}", file=sys.stderr)
        return 1

    lines = {
        "repo": repo,
        "tag": tag,
        "version": version,
        "target": target,
        "archive": archive,
        "archive_sha256": got,
        "bin": str(binary),
        "delvec_version": out,
    }
    text = "".join(f"{k}={v}\n" for k, v in lines.items())
    sys.stdout.write(text)
    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8") as fh:
            fh.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
