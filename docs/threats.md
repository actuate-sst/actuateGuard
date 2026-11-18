# Threat list

**Status: to be written (Phase A deliverable).** How would you attack your own system?

For each threat, give: **attack → what it gets the attacker → how the design stops it (or why the leftover risk is accepted) → how we tested it.**

Must cover at least:
- [ ] Replay (record and resend an unlock)
- [ ] Relay (forward messages between a member's phone and the gate)
- [ ] Clone (copy a grant or app data to another phone)
- [ ] Flash dump of the ESP32
- [ ] Stolen or lost phone
- [ ] Expired grant, and messing with the gate's clock
- [ ] Tampered, deleted or fake log entries
- [ ] Old revocation list replayed / fake backend
- [ ] Bluetooth denial of service (holding the connection, flooding bad attempts)
- [ ] Power cut / brownout / crash loop (does the relay fail safe?)
- [ ] Leaked mock key / leaked log token / leaked signer key
- [ ] Hacked backend or database (can it mint access without an admin passkey?)
- [ ] Stolen admin passkey device
- [ ] Intercepted invite code (enrollment hijack)
- [ ] Revoked person still holding an older, unexpired grant
- [ ] Gate's internet deliberately blocked to dodge a revocation

Start from [design.md §10](design.md#10-security-properties-and-known-residual-risks).
