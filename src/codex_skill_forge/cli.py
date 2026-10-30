from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from .generator import add_member_cache, generate_skill, generate_skill_draft, validate_generated_skill
from .inspection import OpsError, inspect, resolve_root


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="codex-skill-forge", description="Generate project-specific Codex skills from read-only project inspection")
    parser.add_argument("--version", action="version", version="codex-skill-forge 1.2.0")
    sub = parser.add_subparsers(dest="command", required=True)
    inspect_parser = sub.add_parser("inspect", help="Inspect project stack and existing instructions without changing it")
    inspect_parser.add_argument("--project", required=True)
    generate = sub.add_parser("generate-skill", help="Preview and generate a separate Codex skill repository")
    generate.add_argument("--project", required=True)
    generate.add_argument("--member-id", required=True)
    generate.add_argument("--output", help="Optional generated-skill directory; default is sibling under skills/")
    generate.add_argument("--approval")
    validate = sub.add_parser("validate-skill", help="Validate generated Codex skill, local Git, and ignored member cache")
    validate.add_argument("--skill", required=True)
    validate.add_argument("--member-id", required=True)
    member = sub.add_parser("add-member", help="Add an ignored per-member reference cache to a generated skill")
    member.add_argument("--skill", required=True)
    member.add_argument("--member-id", required=True)
    member.add_argument("--approval")
    return parser


def _print(value: object) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False, default=str))


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "inspect":
            _print(inspect(resolve_root(args.project)))
        elif args.command == "generate-skill":
            draft = generate_skill_draft(args.project, args.member_id, args.output)
            print(f"Source project (read-only): {draft['project']}")
            print(f"Generated skill target: {draft['output']}")
            print(f"Detected stacks: {', '.join(draft['facts']['stack']) or 'none detected'}")
            print("Proposed files:")
            for path in sorted(draft["files"]):
                print(f"  {path}")
            result = generate_skill(draft, args.approval)
            _print(result)
        elif args.command == "validate-skill":
            result = validate_generated_skill(args.skill, args.member_id)
            _print(result)
            if not result["valid"]:
                return 2
        elif args.command == "add-member":
            _print(add_member_cache(args.skill, args.member_id, args.approval))
        return 0
    except (OpsError, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
