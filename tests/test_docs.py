from __future__ import annotations

import re
import unittest
from pathlib import Path
from urllib.parse import unquote


REPO_ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
TEMPLATE_ROOT = (
    REPO_ROOT
    / "skill"
    / "agent-workspace-protocol"
    / "assets"
    / "workspace"
)
CHINESE_TEMPLATE_ROOT = (
    REPO_ROOT
    / "skill"
    / "agent-workspace-protocol"
    / "assets"
    / "workspace-zh-CN"
)
VIRTUAL_TEMPLATE_TARGETS = {
    TEMPLATE_ROOT / "MEMORY" / "01-rules" / "workspace-protocol.md":
    REPO_ROOT
    / "skill"
    / "agent-workspace-protocol"
    / "references"
    / "workspace-protocol.md",
    CHINESE_TEMPLATE_ROOT / "MEMORY" / "01-rules" / "workspace-protocol.md":
    REPO_ROOT
    / "skill"
    / "agent-workspace-protocol"
    / "references"
    / "workspace-protocol.zh-CN.md",
}


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in REPO_ROOT.rglob("*.md")
        if ".git" not in path.parts
    )


class DocumentationLinkTests(unittest.TestCase):
    def test_language_template_trees_match(self) -> None:
        english = {
            path.relative_to(TEMPLATE_ROOT).as_posix()
            for path in TEMPLATE_ROOT.rglob("*")
            if path.is_file()
        }
        chinese = {
            path.relative_to(CHINESE_TEMPLATE_ROOT).as_posix()
            for path in CHINESE_TEMPLATE_ROOT.rglob("*")
            if path.is_file()
        }
        self.assertEqual(english, chinese)

    def test_relative_markdown_links_exist(self) -> None:
        failures: list[str] = []
        for document in markdown_files():
            text = document.read_text(encoding="utf-8")
            for raw_target in MARKDOWN_LINK.findall(text):
                target = raw_target.strip().split("#", 1)[0]
                if not target or "://" in target or target.startswith("mailto:"):
                    continue
                if target.startswith("<") and target.endswith(">"):
                    target = target[1:-1]
                resolved = (document.parent / unquote(target)).resolve()
                if resolved in VIRTUAL_TEMPLATE_TARGETS:
                    if VIRTUAL_TEMPLATE_TARGETS[resolved].is_file():
                        continue
                if not resolved.exists():
                    failures.append(
                        f"{document.relative_to(REPO_ROOT)} -> {raw_target}"
                    )

        self.assertEqual(
            failures,
            [],
            "broken relative link(s):\n" + "\n".join(failures),
        )


if __name__ == "__main__":
    unittest.main()
