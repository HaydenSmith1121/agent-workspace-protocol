from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skill" / "agent-workspace-protocol"
INSTALLER = SKILL_ROOT / "scripts" / "install.py"
BOOTSTRAP = SKILL_ROOT / "scripts" / "bootstrap_workspace.py"


def run_script(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class BootstrapTests(unittest.TestCase):
    def test_dry_run_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp) / "new-workspace"
            result = run_script(
                BOOTSTRAP,
                "--workspace",
                str(workspace),
                "--agents",
                "all",
                "--dry-run",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Dry run complete", result.stdout)
            self.assertFalse(workspace.exists())

    def test_bootstrap_all_agents(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp) / "sample"
            result = run_script(
                BOOTSTRAP,
                "--workspace",
                str(workspace),
                "--agents",
                "all",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            expected = (
                "AGENTS.md",
                "CLAUDE.md",
                "GEMINI.md",
                "MEMORY/README.md",
                "MEMORY/01-rules/workspace-protocol.md",
                ".cursor/rules/000-agent-workspace.mdc",
                ".github/copilot-instructions.md",
            )
            for relative in expected:
                self.assertTrue((workspace / relative).is_file(), relative)

    def test_conflict_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            first = run_script(
                BOOTSTRAP,
                "--workspace",
                temp,
                "--agents",
                "codex",
            )
            self.assertEqual(first.returncode, 0, first.stderr)

            (Path(temp) / "AGENTS.md").write_text("local change\n", encoding="utf-8")
            second = run_script(
                BOOTSTRAP,
                "--workspace",
                temp,
                "--agents",
                "codex",
            )
            self.assertEqual(second.returncode, 2)
            self.assertIn("refusing to overwrite", second.stderr)
            self.assertEqual(
                (Path(temp) / "AGENTS.md").read_text(encoding="utf-8"),
                "local change\n",
            )


class InstallerTests(unittest.TestCase):
    def test_install_skill_to_explicit_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            skill_root = Path(temp) / "skills"
            result = run_script(
                INSTALLER,
                "--scope",
                "agent",
                "--runtime",
                "custom",
                "--skill-root",
                str(skill_root),
                "--no-workspace",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(
                (
                    skill_root
                    / "agent-workspace-protocol"
                    / "SKILL.md"
                ).is_file()
            )

    def test_install_and_bootstrap(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            skill_root = Path(temp) / "skills"
            workspace = Path(temp) / "workspace"
            result = run_script(
                INSTALLER,
                "--scope",
                "agent",
                "--runtime",
                "custom",
                "--skill-root",
                str(skill_root),
                "--workspace",
                str(workspace),
                "--agents",
                "codex,claude",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((workspace / "AGENTS.md").is_file())
            self.assertTrue((workspace / "CLAUDE.md").is_file())
            self.assertFalse((workspace / "GEMINI.md").exists())


if __name__ == "__main__":
    unittest.main()
