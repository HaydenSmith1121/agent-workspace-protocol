from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
PLUGIN = REPO_ROOT / ".codex-plugin" / "plugin.json"


class CodexPluginMetadataTests(unittest.TestCase):
    def test_marketplace_points_to_this_repository(self) -> None:
        data = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
        self.assertEqual(data["name"], "agent-workspace-protocol")
        self.assertEqual(len(data["plugins"]), 1)

        plugin = data["plugins"][0]
        self.assertEqual(plugin["name"], "agent-workspace-protocol")
        self.assertEqual(
            plugin["source"]["url"],
            "https://github.com/HaydenSmith1121/agent-workspace-protocol.git",
        )
        self.assertEqual(plugin["source"]["ref"], "main")

    def test_plugin_manifest_exposes_the_skill_tree(self) -> None:
        data = json.loads(PLUGIN.read_text(encoding="utf-8"))
        self.assertEqual(data["name"], "agent-workspace-protocol")
        self.assertEqual(data["skills"], "./skill/")

        skill = (
            REPO_ROOT
            / "skill"
            / "agent-workspace-protocol"
            / "SKILL.md"
        )
        self.assertTrue(skill.is_file())


if __name__ == "__main__":
    unittest.main()
