# Phase B cutover checklist

**Status: to be written (Phase A deliverable).** Phase B is run by @shreyansh-malviya.

Goal: move from mock to production by changing **keys and config only, with zero code changes**. If a step needs a code change, that's a Phase A bug.

Start from [design.md §11](design.md#11-phase-a--phase-b-everything-that-changes). The checklist should cover:
- [ ] Back up the current live firmware
- [ ] Generate the production signer key pair, and store the private key (decision D4)
- [ ] Create or move the backend to the club account; set environment secrets
- [ ] Create the production log token
- [ ] Build production firmware (`GATE_MODE_MOCK` off)
- [ ] Provision the gate's NVS: gate ID, signer public key, URL, CA cert, WiFi, token
- [ ] Flash, then test: unlock, deny, revoke, guest, offline unlock, log upload, relay through a reset
- [ ] Enroll and approve real members
- [ ] Retire the old firmware and its key
- [ ] Rollback plan: re-flash the backup
