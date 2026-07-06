"""Tamper-evident temperature ledger via a SHA-256 hash chain.

Each entry's hash covers the previous entry's hash plus the reading, so altering, inserting,
removing, or reordering any reading breaks the chain from that point on. Pure and deterministic —
timestamps live in the readings, never read from the clock.
"""
import hashlib
import json

GENESIS = "0" * 64


def _hash(prev_hash, reading):
    payload = prev_hash + json.dumps(reading, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def build_chain(readings):
    """Return a list of {reading, prev, hash} entries chaining the readings."""
    chain, prev = [], GENESIS
    for reading in readings:
        h = _hash(prev, reading)
        chain.append({"reading": reading, "prev": prev, "hash": h})
        prev = h
    return chain


def verify_chain(chain):
    """Return {ok, broken_at, reason}. Detects any alteration/insertion/removal/reorder."""
    prev = GENESIS
    for i, entry in enumerate(chain):
        if entry.get("prev") != prev:
            return {"ok": False, "broken_at": i,
                    "reason": "prev-hash mismatch (entry inserted, removed, or reordered)"}
        if _hash(prev, entry.get("reading")) != entry.get("hash"):
            return {"ok": False, "broken_at": i, "reason": "hash mismatch (reading altered)"}
        prev = entry["hash"]
    return {"ok": True, "broken_at": None, "reason": "chain intact"}
