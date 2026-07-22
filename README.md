# Sous-Vide Precision Telemetry

> A **tamper-evident** (hash-chained) temperature ledger plus a **HACCP cook-safety** check —
> proof-of-compliance for sous-vide and other time-and-temperature cooking.
>
> Part of the **Technika11y** suite · *Root access for everyone.*

[![ci](https://github.com/technika11y/sous-vide-telemetry/actions/workflows/ci.yml/badge.svg)](https://github.com/technika11y/sous-vide-telemetry/actions/workflows/ci.yml)
![status](https://img.shields.io/badge/status-pre--alpha-orange)
![license](https://img.shields.io/badge/license-Apache--2.0-blue)
![python](https://img.shields.io/badge/python-3.10%2B-informational)

---

## Quick start

```bash
git clone https://github.com/technika11y/sous-vide-telemetry && cd sous-vide-telemetry
PYTHONPATH=src python3 -m sousvide.cli check examples/cook.json
```

## Status — read this first

**Pre-alpha (`v0.1.0a0`). Honest state of the code:**

| Capability | State |
|---|---|
| Hash-chained ledger (SHA-256) over temperature readings | ✅ works, tested |
| Verify detects alteration / insertion / removal / reorder | ✅ works, tested |
| HACCP check: temp held ≥ threshold for ≥ N contiguous minutes | ✅ works, tested |
| `log` / `verify` / `check` CLI, exit codes for CI | ✅ works |
| Live circulator integration, signed ledgers, multi-stage cook profiles | ⚠️ not built — [roadmap](#roadmap) |

**Scope of the guarantee:** the chain proves a stored log was **not altered after the fact**. It
does *not* prove the readings were true when captured — trust the sensor, and sign the ledger if you
need non-repudiation. See [`SECURITY.md`](SECURITY.md).

## Why it exists

Health inspectors want evidence a cook hit its time-and-temperature target — and that the log
wasn't edited afterward. This produces both: a HACCP pass/fail from the readings, and a hash chain
where changing any past reading is detectable.

## Usage

```bash
# produce a ledger you can persist
PYTHONPATH=src python -m sousvide.cli log examples/cook.json > ledger.json

# later, prove it wasn't touched
PYTHONPATH=src python -m sousvide.cli verify ledger.json

# HACCP cook-safety + chain integrity in one shot
PYTHONPATH=src python -m sousvide.cli check examples/cook.json
```

Alter any reading in `ledger.json` and `verify` reports exactly which entry broke the chain.

## Roadmap

- [ ] Adapters for common immersion circulators
- [ ] Cryptographic signing of the chain head (non-repudiation)
- [ ] Multi-stage cook profiles (sear → hold → chill)
- [ ] Pairs with the Inventory Traceability Ledger (OPS-03)
- [ ] SARIF output + the shared Technika11y CI gate

## License

[Apache-2.0](LICENSE). See [`SECURITY.md`](SECURITY.md).

---

**Part of the [Technika11y](https://github.com/technika11y) suite** · [technika11y.github.io](https://technika11y.github.io/) · security, compliance, and accessibility as one discipline.
