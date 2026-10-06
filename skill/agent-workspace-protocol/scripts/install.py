#!/usr/bin/env python3
"""Install the reusable skill and optionally bootstrap a workspace."""

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
    force: bool,
    backup: bool,
) -> None:
    destination = (root / SKILL_NAME).resolve()
    plan = planned_skill_files(source, destination)
    if destination.exists() and not destination.is_dir():
        raise FileExistsError(
            f"skill destination exists and is not a directory: {destination}"
        )
    conflicts = [
        target
        for source_file, target in plan
        if target.exists()
        and (
            not target.is_file()
            or target.read_bytes() != source_file.read_bytes()
        )
    ]

    if conflicts and not force:
        joined = "\n".join(f"  - {path}" for path in conflicts)
        raise FileExistsError(
            "refusing to overwrite an existing skill; use --force and optionally "
            f"--backup:\n{joined}"
        )

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    if dry_run:
        print(f"PLAN      skill destination: {destination}")
        for _, target in plan:
            action = "OVERWRITE" if target.exists() else "CREATE"
            print(f"{action:9} {target}")
        return

    if destination.exists() and backup:
        backup_root = root / f".{SKILL_NAME}.bak-{stamp}"
        counter = 2
        while backup_root.exists():
            backup_root = root / f".{SKILL_NAME}.bak-{stamp}-{counter}"
            counter += 1
        shutil.copytree(destination, backup_root)
        print(f"BACKUP    {destination} -> {backup_root}")

    for source_file, target in plan:
        existed = target.exists()
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, target)
        action = "OVERWRITE" if existed else "CREATE"
        print(f"{action:9} {target}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Install agent-workspace-protocol. Agent scope installs a reusable "
            "skill; workspace scope installs project entry files and memory."
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
    parser.add_argument("--workspace", help="Workspace to bootstrap.")
    parser.add_argument(
        "--agents",
        default="all",
        help="Workspace adapters: codex,claude,cursor,gemini,copilot,all,none.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Plan without writing.")
    parser.add_argument("--force", action="store_true", help="Overwrite conflicts.")
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Back up files or skill trees before overwrite.",
    )
    parser.add_argument(
        "--no-skill",
        action="store_true",
        help="Do not install the reusable skill.",
    )
    parser.add_argument(
        "--no-workspace",
        action="store_true",
        help="Do not bootstrap workspace entry files.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    workspace = Path(args.workspace).expanduser().resolve() if args.workspace else None
    do_workspace = bool(workspace) and not args.no_workspace
    do_skill = not args.no_skill

    if not do_workspace and not do_skill:
        parser.error("nothing to do: both --no-skill and --no-workspace were supplied")
    if args.scope == "project" and workspace is None:
        parser.error("--workspace is required with --scope project")
    if not do_workspace and args.workspace is None and args.no_workspace:
        pass

    try:
        agents = parse_agents(args.agents)
        if do_skill:
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
                force=args.force,
                backup=args.backup,
            )

        if do_workspace:
            assert workspace is not None
            bootstrap(
                workspace=workspace,
                agents=agents,
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
        if do_skill:
            print(
                "Skill discovery may require a new agent session or a reload of "
                "the runtime."
            )
        if do_workspace:
            print(
                "Review MEMORY/01-rules/workspace-protocol.md before committing "
                "the workspace changes."
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
