#!/usr/bin/env python3
"""Create a portable agent-ready workspace from the bundled templates."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from dataclasses import dataclass
from pathlib import Path


SUPPORTED_AGENTS = ("codex", "claude", "cursor", "gemini", "copilot")
SUPPORTED_LANGUAGES = ("en", "zh-CN")
LANGUAGE_LAYOUTS = {
    "en": {
        "assets": "workspace",
        "canonical": "workspace-protocol.md",
    },
    "zh-CN": {
        "assets": "workspace-zh-CN",
        "canonical": "workspace-protocol.zh-CN.md",
    },
}
AGENT_TEMPLATES = {
    "codex": ("AGENTS.md",),
    "claude": ("CLAUDE.md",),
    "cursor": (".cursor/rules/000-agent-workspace.mdc",),
    "gemini": ("GEMINI.md",),
    "copilot": (".github/copilot-instructions.md",),
}
BASE_TEMPLATES = (
    "README.md",
    ".gitignore",
    "MEMORY/README.md",
    "MEMORY/02-structure/directory-layout.md",
    "MEMORY/03-sessions/README.md",
    "MEMORY/04-glossary/README.md",
    "MEMORY/05-state/current.md",
    "MEMORY/06-decisions/README.md",
    "10-docs/README.md",
    "20-projects/README.md",
    "30-data/README.md",
    "40-deliverables/README.md",
    "50-assets/README.md",
    "60-research/README.md",
    "90-temp/README.md",
    "90-temp/inbox/README.md",
    "99-archive/README.md",
)
CANONICAL_TARGET = "MEMORY/01-rules/workspace-protocol.md"
PLACEHOLDER_PATTERN = re.compile(r"\{\{[A-Z0-9_]+\}\}")


@dataclass(frozen=True)
class PlannedFile:
    target: Path
    content: bytes
    source: Path
    action: str
    backup: Path | None = None


def parse_agents(value: str) -> list[str]:
    requested = [item.strip().lower() for item in value.split(",") if item.strip()]
    if not requested:
        raise ValueError("--agents must contain at least one agent or 'none'")
    if "none" in requested:
        if len(requested) != 1:
            raise ValueError("'none' cannot be combined with other agents")
        return []
    if "all" in requested:
        if len(requested) != 1:
            raise ValueError("'all' cannot be combined with other agents")
        return list(SUPPORTED_AGENTS)
    unknown = sorted(set(requested) - set(SUPPORTED_AGENTS))
    if unknown:
        raise ValueError(
            f"unsupported agents: {', '.join(unknown)}; "
            f"choose from {', '.join(SUPPORTED_AGENTS)}, all, or none"
        )
    return list(dict.fromkeys(requested))


def render_template(path: Path, workspace: Path) -> bytes:
    text = path.read_text(encoding="utf-8")
    replacements = {
        "{{DATE}}": dt.date.today().isoformat(),
        "{{PROJECT_NAME}}": workspace.name or "workspace",
        "{{PROTOCOL_VERSION}}": "1.0",
    }
    for token, value in replacements.items():
        text = text.replace(token, value)

    unresolved = sorted(set(PLACEHOLDER_PATTERN.findall(text)))
    if unresolved:
        raise ValueError(
            f"unresolved placeholder(s) in {path}: {', '.join(unresolved)}"
        )
    return text.encode("utf-8")


def unique_backup_path(path: Path, stamp: str) -> Path:
    candidate = path.with_name(f"{path.name}.bak-{stamp}")
    counter = 2
    while candidate.exists():
        candidate = path.with_name(f"{path.name}.bak-{stamp}-{counter}")
        counter += 1
    return candidate


def build_plan(
    workspace: Path,
    agents: list[str],
    language: str,
    force: bool,
    backup: bool,
) -> list[PlannedFile]:
    try:
        language_layout = LANGUAGE_LAYOUTS[language]
    except KeyError as exc:
        raise ValueError(
            f"unsupported language: {language}; "
            f"choose from {', '.join(SUPPORTED_LANGUAGES)}"
        ) from exc

    skill_root = Path(__file__).resolve().parent.parent
    asset_root = skill_root / "assets" / language_layout["assets"]
    canonical = skill_root / "references" / language_layout["canonical"]

    mappings: list[tuple[Path, str]] = [
        (asset_root / relative, relative) for relative in BASE_TEMPLATES
    ]
    for agent in agents:
        for relative in AGENT_TEMPLATES[agent]:
            mappings.append((asset_root / relative, relative))
    mappings.append((canonical, CANONICAL_TARGET))

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    plan: list[PlannedFile] = []
    conflicts: list[Path] = []

    for source, relative in mappings:
        if not source.is_file():
            raise FileNotFoundError(f"template not found: {source}")
        target = (workspace / relative).resolve()
        try:
            target.relative_to(workspace)
        except ValueError as exc:
            raise ValueError(f"template escapes workspace: {relative}") from exc

        content = render_template(source, workspace)
        if target.exists():
            if target.is_file() and target.read_bytes() == content:
                action = "unchanged"
            elif not force:
                action = "conflict"
                conflicts.append(target)
            else:
                action = "overwrite"
        else:
            action = "create"

        backup_path = None
        if action == "overwrite" and backup:
            backup_path = unique_backup_path(target, stamp)
        plan.append(
            PlannedFile(
                target=target,
                content=content,
                source=source,
                action=action,
                backup=backup_path,
            )
        )

    if conflicts and not force:
        joined = "\n".join(f"  - {path}" for path in conflicts)
        raise FileExistsError(
            "refusing to overwrite existing files; use --force and optionally "
            f"--backup:\n{joined}"
        )
    return plan


def apply_plan(plan: list[PlannedFile], dry_run: bool) -> None:
    if dry_run:
        for item in plan:
            if item.action == "conflict":
                continue
            suffix = f" (backup: {item.backup})" if item.backup else ""
            print(f"{item.action.upper():9} {item.target}{suffix}")
        return

    for item in plan:
        if item.action == "unchanged":
            continue
        item.target.parent.mkdir(parents=True, exist_ok=True)
        if item.backup is not None:
            item.target.replace(item.backup)
        item.target.write_bytes(item.content)
        print(f"{item.action.upper():9} {item.target}")


def bootstrap(
    workspace: Path,
    agents: list[str],
    language: str = "en",
    dry_run: bool = False,
    force: bool = False,
    backup: bool = False,
) -> int:
    workspace = workspace.expanduser().resolve()
    if workspace.exists() and not workspace.is_dir():
        raise NotADirectoryError(f"workspace is not a directory: {workspace}")

    if dry_run:
        print(f"PLAN      workspace: {workspace}")
        print(f"PLAN      agents: {', '.join(agents) if agents else 'none'}")
        print(f"PLAN      language: {language}")
    else:
        workspace.mkdir(parents=True, exist_ok=True)

    plan = build_plan(
        workspace,
        agents,
        language=language,
        force=force,
        backup=backup,
    )
    apply_plan(plan, dry_run=dry_run)

    if dry_run:
        print("\nDry run complete. No files were written.")
    else:
        print("\nWorkspace bootstrap complete.")
        print("Next steps:")
        print("  1. Review README.md and MEMORY/01-rules/workspace-protocol.md.")
        print("  2. Replace any remaining project-specific descriptions.")
        print("  3. Add secrets paths to .gitignore before committing.")
        print("  4. Remove categories the workspace does not need.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Bootstrap an Agent Workspace Protocol workspace."
    )
    parser.add_argument("--workspace", required=True, help="Target workspace path.")
    parser.add_argument(
        "--agents",
        default="all",
        help="Comma-separated: codex,claude,cursor,gemini,copilot,all,none.",
    )
    parser.add_argument(
        "--language",
        choices=SUPPORTED_LANGUAGES,
        default="en",
        help="Workspace template language: en or zh-CN.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Plan without writing.")
    parser.add_argument("--force", action="store_true", help="Overwrite conflicts.")
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Back up overwritten files before replacing them.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        agents = parse_agents(args.agents)
        return bootstrap(
            workspace=Path(args.workspace),
            agents=agents,
            language=args.language,
            dry_run=args.dry_run,
            force=args.force,
            backup=args.backup,
        )
    except (FileExistsError, FileNotFoundError, NotADirectoryError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
