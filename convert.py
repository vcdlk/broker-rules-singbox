#!/usr/bin/env python3
"""Convert Arthur-vx/broker-rules Broker.list to sing-box rule-set source JSON.

Output schema (version 2):
{
  "version": 2,
  "rules": [
    {
      "domain": [...],
      "domain_suffix": [...],
      "ip_cidr": [...]
    }
  ]
}
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def parse_broker_list(text: str) -> dict[str, list[str]]:
    domain: list[str] = []
    domain_suffix: list[str] = []
    ip_cidr: list[str] = []

    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 2:
            continue
        rule_type, value = parts[0].upper(), parts[1]
        if rule_type == "DOMAIN":
            domain.append(value)
        elif rule_type == "DOMAIN-SUFFIX":
            domain_suffix.append(value)
        elif rule_type == "IP-CIDR" or rule_type == "IP-CIDR6":
            ip_cidr.append(value)

    return {
        "domain": sorted(set(domain)),
        "domain_suffix": sorted(set(domain_suffix)),
        "ip_cidr": sorted(set(ip_cidr)),
    }


def build_ruleset(parsed: dict[str, list[str]]) -> dict:
    rule: dict[str, list[str]] = {}
    for key in ("domain", "domain_suffix", "ip_cidr"):
        if parsed[key]:
            rule[key] = parsed[key]
    if not rule:
        raise SystemExit("no rules parsed from input")
    return {"version": 2, "rules": [rule]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", "-i", required=True, help="path to Broker.list")
    ap.add_argument("--output", "-o", required=True, help="path to output JSON")
    args = ap.parse_args()

    text = Path(args.input).read_text(encoding="utf-8")
    parsed = parse_broker_list(text)
    ruleset = build_ruleset(parsed)

    Path(args.output).write_text(
        json.dumps(ruleset, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    counts = {k: len(v) for k, v in parsed.items()}
    print(
        f"wrote {args.output}: "
        f"domain={counts['domain']} "
        f"domain_suffix={counts['domain_suffix']} "
        f"ip_cidr={counts['ip_cidr']}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
