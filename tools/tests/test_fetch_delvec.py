r"""Guards for `tools/fetch-delvec.py`, the one way `release.yml` obtains `delvec`.

The release never compiles the engine; it runs the binary the pinned engine
release published, after checking it against that release's `SHA256SUMS`. Each
refusal the script claims is planted here offline — the download is replaced by
a copy from a fixture directory standing in for the Release — and the script is
required to refuse on it: a pin that is not a release, a pin of another line, a
missing asset, a `SHA256SUMS` with no line for the archive, a tampered archive,
and a binary that reports a different version than its tag. The clean fixture
must pass and report the archive's digest.

Digests are computed at run time, never written out: this file is a `**/*.py`
and therefore a fetch site for `tools/ci/check-pins.py`.
"""

from __future__ import annotations

import hashlib
import importlib.util
import io
import pathlib
import platform
import shutil
import sys
import tarfile
import tempfile
import unittest
import urllib.error
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

REPO = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = REPO / "tools" / "fetch-delvec.py"

spec = importlib.util.spec_from_file_location("fetch_delvec", SCRIPT)
fd = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(fd)

TARGET = fd.TARGETS.get((platform.system(), platform.machine()))


def make_release(root: pathlib.Path, version: str, reports: str, sums_for: str | None = None) -> str:
    """A fixture Release: one archive for this machine plus SHA256SUMS. Returns the archive name."""
    archive = fd.archive_name(version, TARGET)
    script = root / "delvec-src"
    script.write_text(f"#!/bin/sh\necho 'delvec {reports}, dsl 0.0.0, mc 1.21.11'\n", encoding="utf-8")
    script.chmod(0o755)
    with tarfile.open(root / archive, "w:gz") as tf:
        tf.add(script, arcname="delvec")
    digest = hashlib.sha256((root / archive).read_bytes()).hexdigest()
    other = hashlib.sha256(b"other").hexdigest()
    (root / "SHA256SUMS").write_text(
        f"{other}  delvec-v{version}-x86_64-pc-windows-msvc.tar.gz\n"
        f"{digest} *{sums_for or archive}\n",
        encoding="utf-8",
    )
    return archive


def fake_download(release: pathlib.Path):
    def download(url: str, dest: pathlib.Path, what: str) -> None:
        src = release / url.rsplit("/", 1)[1]
        if not src.is_file():
            raise fd.Refused(f"{what} could not be downloaded ({url}: HTTP 404)")
        shutil.copyfile(src, dest)

    return download


def run(tmp: pathlib.Path, release: pathlib.Path, ref: str) -> tuple[int, str, str]:
    versions = tmp / "versions.toml"
    versions.write_text('[engine]\nrepo = "o/r"\nref = "delvec--v1.0.0"\n', encoding="utf-8")
    argv = ["fetch-delvec.py", "--versions", str(versions), "--dest", str(tmp / "dest")]
    if ref:
        argv += ["--ref", ref]
    out, err = io.StringIO(), io.StringIO()
    with mock.patch.object(sys, "argv", argv), mock.patch.object(fd, "download", fake_download(release)):
        with redirect_stdout(out), redirect_stderr(err):
            code = fd.main()
    return code, out.getvalue(), err.getvalue()


class PinGrammar(unittest.TestCase):
    def test_a_delvec_release_tag_names_its_version(self) -> None:
        self.assertEqual(fd.release_version("delvec--v1.12.0"), "1.12.0")

    def test_a_commit_is_not_a_release(self) -> None:
        with self.assertRaisesRegex(fd.Refused, "is not a release"):
            fd.release_version("0123456789abcdef" * 2 + "01234567")

    def test_a_legacy_v_tag_is_not_a_release(self) -> None:
        with self.assertRaisesRegex(fd.Refused, "is not a release"):
            fd.release_version("v1.5.0")

    def test_another_line_is_refused(self) -> None:
        with self.assertRaisesRegex(fd.Refused, "not of `delvec`"):
            fd.release_version("delvewright--v1.4.3")

    def test_an_unknown_machine_has_no_archive(self) -> None:
        with self.assertRaisesRegex(fd.Refused, "no engine release archive"):
            fd.target_for("Plan9", "mips")

    def test_the_ci_runner_and_the_workstation_resolve(self) -> None:
        self.assertEqual(fd.target_for("Linux", "x86_64"), "x86_64-unknown-linux-gnu")
        self.assertEqual(fd.target_for("Darwin", "arm64"), "aarch64-apple-darwin")


class Sums(unittest.TestCase):
    def test_text_and_binary_forms_are_read(self) -> None:
        d = hashlib.sha256(b"x").hexdigest()
        self.assertEqual(fd.expected_sha256(f"{d}  a.tar.gz\n", "a.tar.gz"), d)
        self.assertEqual(fd.expected_sha256(f"{d} *a.tar.gz\n", "a.tar.gz"), d)

    def test_no_line_is_refused(self) -> None:
        d = hashlib.sha256(b"x").hexdigest()
        with self.assertRaisesRegex(fd.Refused, "no line for a.tar.gz"):
            fd.expected_sha256(f"{d}  b.tar.gz\n", "a.tar.gz")

    def test_disagreeing_lines_are_refused(self) -> None:
        d1, d2 = hashlib.sha256(b"x").hexdigest(), hashlib.sha256(b"y").hexdigest()
        with self.assertRaisesRegex(fd.Refused, "disagreeing"):
            fd.expected_sha256(f"{d1}  a.tar.gz\n{d2}  a.tar.gz\n", "a.tar.gz")


@unittest.skipIf(TARGET is None, "this machine has no engine release target")
class EndToEnd(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = pathlib.Path(self._tmp.name)
        self.release = self.tmp / "release"
        self.release.mkdir()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_a_clean_release_passes_and_reports_its_digest(self) -> None:
        archive = make_release(self.release, "1.0.0", "1.0.0")
        code, out, err = run(self.tmp, self.release, "")
        self.assertEqual(code, 0, out + err)
        digest = hashlib.sha256((self.release / archive).read_bytes()).hexdigest()
        self.assertIn(f"archive_sha256={digest}\n", out)
        self.assertIn("tag=delvec--v1.0.0\n", out)
        self.assertIn(f"archive={archive}\n", out)

    def test_a_tampered_archive_is_refused(self) -> None:
        archive = make_release(self.release, "1.0.0", "1.0.0")
        with (self.release / archive).open("ab") as fh:
            fh.write(b"\0")
        code, out, err = run(self.tmp, self.release, "")
        self.assertEqual(code, 1, out + err)
        self.assertIn("!= SHA256SUMS", err)
        self.assertNotIn("bin=", out)

    def test_a_missing_sums_line_is_refused(self) -> None:
        make_release(self.release, "1.0.0", "1.0.0", sums_for="somebody-else.tar.gz")
        code, out, err = run(self.tmp, self.release, "")
        self.assertEqual(code, 1, out + err)
        self.assertIn("SHA256SUMS has no line", err)

    def test_a_missing_archive_is_refused(self) -> None:
        archive = make_release(self.release, "1.0.0", "1.0.0")
        (self.release / archive).unlink()
        code, out, err = run(self.tmp, self.release, "")
        self.assertEqual(code, 1, out + err)
        self.assertIn("could not be downloaded", err)

    def test_a_binary_reporting_another_version_is_refused(self) -> None:
        make_release(self.release, "1.0.0", "1.0.1")
        code, out, err = run(self.tmp, self.release, "")
        self.assertEqual(code, 1, out + err)
        self.assertIn("reports delvec 1.0.1", err)

    def test_an_override_that_is_not_a_release_is_refused(self) -> None:
        make_release(self.release, "1.0.0", "1.0.0")
        code, out, err = run(self.tmp, self.release, "main")
        self.assertEqual(code, 1, out + err)
        self.assertIn("is not a release", err)


if __name__ == "__main__":
    unittest.main()
