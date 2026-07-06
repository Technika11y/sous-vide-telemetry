# Security Policy

This tool builds and verifies a tamper-evident temperature ledger; it reads a file and reports,
with no network or execution of input. The hash chain proves a stored log wasn't altered after the
fact — it does **not** attest that the readings were true when captured (trust the sensor, sign the
ledger). A verify path that misses tampering is the high-severity failure mode.

Report issues **in this tool** privately: GitHub **Report a vulnerability** on this repo, or email
the contact on the org profile. Target: **5 business days** to acknowledge, coordinated disclosure.
