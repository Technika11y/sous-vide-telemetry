import unittest

from sousvide.ledger import build_chain, verify_chain, GENESIS

READINGS = [{"t": 0, "temp_c": 20}, {"t": 5, "temp_c": 55}, {"t": 95, "temp_c": 56}]


class LedgerTests(unittest.TestCase):
    def test_first_entry_links_to_genesis(self):
        self.assertEqual(build_chain(READINGS)[0]["prev"], GENESIS)

    def test_untampered_chain_verifies(self):
        self.assertTrue(verify_chain(build_chain(READINGS))["ok"])

    def test_altered_reading_breaks_chain(self):
        chain = build_chain(READINGS)
        chain[1]["reading"]["temp_c"] = 40  # someone edits a temperature after the fact
        v = verify_chain(chain)
        self.assertFalse(v["ok"])
        self.assertEqual(v["broken_at"], 1)

    def test_removed_entry_breaks_chain(self):
        chain = build_chain(READINGS)
        del chain[1]
        self.assertFalse(verify_chain(chain)["ok"])

    def test_reordered_entries_break_chain(self):
        chain = build_chain(READINGS)
        chain[1], chain[2] = chain[2], chain[1]
        self.assertFalse(verify_chain(chain)["ok"])


if __name__ == "__main__":
    unittest.main()
