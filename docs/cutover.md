# Phase B cutover checklist

**Status: to be written (Phase A deliverable).** Phase B is run by @shreyansh-malviya.

Goal: move from mock to production by changing **keys and config only, with zero code changes**. If a step needs a code change, that's a Phase A bug.

Start from [design.md §11](design.md#11-phase-a--phase-b-everything-that-changes). The checklist should cover:
- [ ] Back up the current live firmware
- [ ] Generate the production signer key pair, and store the private key (decision D4)
- [ ] Register production admin passkeys; pin their public keys in the signer config and remove the mock admin key
- [ ] Create or move the backend to the club account; set environment secrets
- [ ] Create the production log token (one per gate)
- [ ] Build production firmware from a **signed git tag** (`GATE_MODE_MOCK` off); record the binary's SHA-256 here
- [ ] Provision the gate's NVS: gate ID, signer public key, URL, CA cert, WiFi, token
- [ ] Burn secure boot v2 and flash encryption, disable JTAG, set secure download mode
- [ ] Flash, then test: unlock, deny, revoke (person and single phone), guest, offline unlock, signed time sync, log upload, relay through a reset
- [ ] Confirm alerts fire: new approval, admin login, gate offline > 1 h
- [ ] Enroll and approve real members (fingerprint check + passkey)
- [ ] Retire the old firmware and its key
- [ ] Rollback plan: re-flash the backup
