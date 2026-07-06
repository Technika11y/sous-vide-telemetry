"""sous-vide-telemetry <log|verify|check> <file.json>

  log    <cook.json>   -> print the hash-chained ledger (persist this)
  verify <ledger.json> -> verify a stored ledger; exit 1 if tampered
  check  <cook.json>   -> HACCP cook-safety + chain integrity; exit 1 if either fails
"""
import argparse
import json
import sys

from .ledger import build_chain, verify_chain
from .haccp import cook_safety


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(prog="sous-vide-telemetry")
    parser.add_argument("command", choices=["log", "verify", "check"])
    parser.add_argument("file", help="cook JSON (log/check) or ledger JSON (verify)")
    args = parser.parse_args(argv)

    with open(args.file) as fh:
        data = json.load(fh)

    if args.command == "verify":
        v = verify_chain(data)  # data is the stored ledger (list of entries)
        print(f"chain: {v['reason']}", file=sys.stderr)
        return 0 if v["ok"] else 1

    readings = data.get("readings", [])
    if args.command == "log":
        print(json.dumps(build_chain(readings), indent=2))
        return 0

    # check
    chain_v = verify_chain(build_chain(readings))
    safety = cook_safety(readings, data.get("min_temp_c", 54.4), data.get("hold_minutes", 90))
    print(f"chain: {chain_v['reason']}", file=sys.stderr)
    print(f"haccp: {'PASS' if safety['pass'] else 'FAIL'} — held {safety['held_minutes']}min "
          f"(need {safety['required_minutes']}min at >= {safety['min_temp_c']}C)", file=sys.stderr)
    return 0 if (chain_v["ok"] and safety["pass"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
