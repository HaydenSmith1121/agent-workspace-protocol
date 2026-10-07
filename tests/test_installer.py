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

    def test_existing_files_are_skipped_by_default(self) -> None:
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
            (Path(temp) / "MEMORY" / "05-state" / "current.md").unlink()
            second = run_script(
                BOOTSTRAP,
                "--workspace",
                temp,
                "--agents",
                "codex",
            )
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn("SKIP", second.stdout)
            self.assertIn("Left 1 existing file(s) untouched", second.stdout)
            self.assertEqual(
                (Path(temp) / "AGENTS.md").read_text(encoding="utf-8"),
                "local change\n",
            )
            self.assertTrue(
                (Path(temp) / "MEMORY" / "05-state" / "current.md").is_file()
            )

    def test_force_with_backup_replaces_and_keeps_a_copy(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp)
            (workspace / "AGENTS.md").write_text("local change\n", encoding="utf-8")

            result = run_script(
                BOOTSTRAP,
                "--workspace",
                temp,
                "--agents",
                "codex",
                "--force",
                "--backup",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            agents = (workspace / "AGENTS.md").read_text(encoding="utf-8")
            self.assertNotEqual(agents, "local change\n")
            backups = list(workspace.glob("AGENTS.md.bak-*"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(encoding="utf-8"), "local change\n")

    def test_bootstrap_chinese_templates(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp) / "sample"
            result = run_script(
                BOOTSTRAP,
                "--workspace",
                str(workspace),
                "--agents",
                "all",
                "--language",
                "zh-CN",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            protocol = (
                workspace / "MEMORY" / "01-rules" / "workspace-protocol.md"
            ).read_text(encoding="utf-8")
            agents = (workspace / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("# 智能体工作区协议", protocol)
            self.assertIn("本文件只是导航地图", agents)

    def test_adopting_an_existing_workspace_adds_only_missing_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp)
            (workspace / "AGENTS.md").write_text("local change\n", encoding="utf-8")

            result = run_script(
                BOOTSTRAP,
                "--workspace",
                temp,
                "--agents",
                "all",
                "--language",
                "zh-CN",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                (workspace / "AGENTS.md").read_text(encoding="utf-8"),
                "local change\n",
            )
            self.assertTrue((workspace / "CLAUDE.md").is_file())
            self.assertTrue(
                (
                    workspace / "MEMORY" / "01-rules" / "workspace-protocol.md"
                ).is_file()
            )


class InstallerTests(unittest.TestCase):
    def test_existing_skill_is_refreshed_in_place(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            skill_root = Path(temp) / "skills"
            workspace = Path(temp) / "workspace"
            installed = skill_root / "agent-workspace-protocol"
            installed.mkdir(parents=True)
            (installed / "SKILL.md").write_text("old skill\n", encoding="utf-8")

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
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("UPDATE", result.stdout)
            self.assertNotEqual(
                (installed / "SKILL.md").read_text(encoding="utf-8"),
                "old skill\n",
            )
            self.assertTrue((workspace / "AGENTS.md").is_file())

    def test_install_skill_and_workspace_to_explicit_root(self) -> None:
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
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(
                (
                    skill_root
                    / "agent-workspace-protocol"
                    / "SKILL.md"
                ).is_file()
            )
            self.assertTrue((workspace / "AGENTS.md").is_file())

    def test_workspace_is_required(self) -> None:
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
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("required", result.stderr)

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

    def test_install_and_bootstrap_chinese(self) -> None:
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
                "codex",
                "--language",
                "zh-CN",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            readme = (workspace / "README.md").read_text(encoding="utf-8")
            self.assertIn("本工作区遵循", readme)


if __name__ == "__main__":
    unittest.main()
