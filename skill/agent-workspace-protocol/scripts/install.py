#!/usr/bin/env python3
"""Install the reusable skill and initialize a workspace."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import shutil
import sys
from pathlib import Path

from bootstrap_workspace import bootstrap, parse_agents


SKILL_NAME = "agent-workspace-protocol"
SKIP_PARTS = {"__pycache__", ".DS_Store"}


def skill_source() -> Path:
    return Path(__file__).resolve().parent.parent


def resolve_skill_root(
    scope: str,
    runtime: str,
    workspace: Path | None,
    explicit: str | None,
) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()

    if scope == "project":
        if workspace is None:
            raise ValueError("--workspace is required when --scope project is used")
        if runtime == "codex":
            return (workspace / ".agents" / "skills").resolve()
        if runtime == "claude":
            return (workspace / ".claude" / "skills").resolve()
        raise ValueError("--skill-root is required with --runtime custom")

    if runtime == "codex":
        codex_home = os.environ.get("CODEX_HOME")
        base = Path(codex_home).expanduser() if codex_home else Path.home() / ".codex"
        return (base / "skills").resolve()

    if runtime == "claude":
        return (Path.home() / ".claude" / "skills").resolve()

    raise ValueError("--skill-root is required with --runtime custom")


def iter_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and not any(part in SKIP_PARTS for part in path.parts)
    )


def planned_skill_files(source: Path, destination: Path) -> list[tuple[Path, Path]]:
    return [
        (path, destination / path.relative_to(source))
        for path in iter_files(source)
    ]


def install_skill(
    source: Path,
    root: Path,
    dry_run: bool,
    backup: bool,
) -> None:
    destination = (root / SKILL_NAME).resolve()
    plan = planned_skill_files(source, destination)
    if destination.exists() and not destination.is_dir():
        raise FileExistsError(
            f"skill destination exists and is not a directory: {destination}"
        )
    changed = {
        target
        for source_file, target in plan
        if target.exists()
        and (
            not target.is_file()
            or target.read_bytes() != source_file.read_bytes()
        )
    }

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    if dry_run:
        print(f"PLAN      skill destination: {destination}")
        for _, target in plan:
            if not target.exists():
                action = "CREATE"
            elif target in changed:
                action = "UPDATE"
            else:
                action = "UNCHANGED"
            print(f"{action:9} {target}")
        return

    if changed and backup:
        backup_root = root / f".{SKILL_NAME}.bak-{stamp}"
        counter = 2
        while backup_root.exists():
            backup_root = root / f".{SKILL_NAME}.bak-{stamp}-{counter}"
            counter += 1
        shutil.copytree(destination, backup_root)
        print(f"BACKUP    {destination} -> {backup_root}")

    for source_file, target in plan:
        if target.exists() and target not in changed:
            continue
        existed = target.exists()
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, target)
        action = "UPDATE" if existed else "CREATE"
        print(f"{action:9} {target}")
    if changed and not backup:
        print(
            "Note: the agent-level skill is refreshed in place. "
            "Pass --backup to keep the previous copy."
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Install agent-workspace-protocol and initialize a workspace. "
            "Agent scope installs the reusable skill; workspace scope installs "
            "project entry files and memory."
        )
    )
    parser.add_argument(
        "--scope",
        choices=("agent", "project"),
        default="agent",
        help="Agent-level skill or project-level skill.",
    )
    parser.add_argument(
        "--runtime",
        choices=("codex", "claude", "custom"),
        default="codex",
        help="Known runtime or a custom root.",
    )
    parser.add_argument("--skill-root", help="Explicit skill root directory.")
    parser.add_argument(
        "--workspace", required=True, help="Workspace to initialize."
    )
    parser.add_argument(
        "--agents",
        default="all",
        help="Workspace adapters: codex,claude,cursor,gemini,copilot,all,none.",
    )
    parser.add_argument(
        "--language",
        choices=("en", "zh-CN"),
        default="en",
        help="Workspace template language: en or zh-CN.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Plan without writing.")
    parser.add_argument(
        "--force", action="store_true", help="Overwrite existing workspace files."
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Back up files or skill trees before overwrite.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    workspace = Path(args.workspace).expanduser().resolve()

    try:
        agents = parse_agents(args.agents)
        root = resolve_skill_root(
            scope=args.scope,
            runtime=args.runtime,
            workspace=workspace,
            explicit=args.skill_root,
        )
        install_skill(
            source=skill_source(),
            root=root,
            dry_run=args.dry_run,
            backup=args.backup,
        )
        bootstrap(
            workspace=workspace,
            agents=agents,
            language=args.language,
            dry_run=args.dry_run,
            force=args.force,
            backup=args.backup,
        )
    except (FileExistsError, FileNotFoundError, NotADirectoryError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        print("\nDry run complete. No files were written.")
    else:
        print("\nInstallation complete.")
        print(
            "Skill discovery may require a new agent session or a reload of "
            "the runtime."
        )
        print(
            "Review MEMORY/01-rules/workspace-protocol.md before committing "
            "the workspace changes."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
