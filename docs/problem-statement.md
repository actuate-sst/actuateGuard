# Club Gate Access: Secure Auth Upgrade

Owner: Shreyansh · Draft, 18 Nov 2026

## Current state

- An ESP32 on the live gate opens it through a relay when a phone is near (BLE RSSI). It works and the gate is in use today, so don't break it.
- Auth is one fixed shared secret typed into every phone. It's shared by everyone, can't be revoked per person, and leaves no record of who opened the gate. It must be replaced.

## Goal

Per-person, revocable, cryptographic access, including temporary guest access and a log of who opened the gate and when, with the gate working at all times.

## Plan

- **Phase A (team, this repo):** build and test the full system with throwaway keys and a throwaway backend account, on the real gate board, following the live-board rules below. Work lands on `main` through reviewed PRs.
- **Phase B (Shreyansh, cutover):** real keys, backend moved to the club account, live gate flashed with the real public key. This must need config and secrets changes only, zero code changes.
- **Phase C (pipeline):** dashboard and backend auto-deploy from `main`. App builds are produced by CI and released manually. Firmware is flashed manually or via signed OTA only, never auto-deployed.

## Phase A scope

**Phone and onboarding**

- Each phone generates its own keypair, and the private key never leaves the phone.
- Onboarding via a one-time invite code (the server stores only its hash).
- Guests enroll with the app too. Guests without a smartphone are out of scope.
- Decide the phone platform (Android or iPhone) and justify it in the design doc. iOS limits background BLE.

**Gate**

- RSSI only triggers the check. The phone must sign a random nonce (challenge-response) to prove identity.
- The ESP verifies everything offline and holds no secret that can open the gate.

**Signed grants**

- A signer service issues grants: user, phone public key, gate ID, valid from, valid until, grant ID.
- The ESP verifies the grant with the signer public key from its config, then verifies the phone's signature on the nonce, the time window, and the revocation list.

**Temporary access and revocation**

- Temporary access is just a short expiry.
- The ESP polls a revoked-grant list over HTTPS (outbound only, no open ports).

**Admin dashboard**

- Approve members, issue temporary grants, revoke access, view the access log.
- Admin login with passkey or 2FA.

**Access logs**

- The ESP logs every attempt: user ID from the verified grant, gate ID, timestamp, and allowed or denied with the reason (expired, revoked, bad signature).
- Events are buffered in flash and uploaded over HTTPS when online, so logs survive WiFi outages.
- A trusted clock is required (RTC such as DS3231, or time from the server over HTTPS).
- The ESP's upload token is write-only for logging, so a leak allows only fake log entries.
- The server stores logs append-only. The dashboard can filter by person and date.
- Optional: a reed switch to confirm the gate was actually opened.
- Members are told they are logged. Retention is 90 days.
- Note: the log records which grant opened the gate, not which person walked in.

**Config-driven**

- Signer public key, backend URL, and gate ID live in config, not in logic. This is what makes Phase B a config-only swap.

## Hard rules

- No secrets in the repo or the firmware image. The ESP holds no secret that can open the gate: only public keys, plus a write-only log token and WiFi credentials stored in its config (NVS).
- Proximity alone never opens the gate.
- A valid grant must work offline, as long as the gate has trusted time (RTC). With no trusted time it fails closed, and people use the physical key or inside release.
- The gate must always open from inside, and relay and ESP wiring must not be reachable from outside.
- Use standard crypto libraries only (mbedTLS or Monocypher, Ed25519 or ECDSA P-256). No custom crypto.
- Mock keys are never left on the live gate outside a supervised session.

## Live-board rules (working on the real gate)

- Back up the current firmware first (`esptool read_flash`) and keep the file, so you can always restore it.
- One person holds the mock private key. It never goes in the repo or the group chat.
- Test in supervised sessions: someone is physically at the gate, and the known-good firmware is flashed back at the end. Mock firmware does not stay overnight.
- Mock firmware rejects grants longer than about an hour.
- Relay fail-safe: a cooldown and a max-open time, so a crash loop can't leave the gate stuck open.
- Relay pin: avoid ESP32 strapping pins (GPIO 0, 2, 12, 15), or confirm the relay stays off through a reset.
- The inside release and mechanical key keep working at all times.

Step-by-step version: [live-board.md](live-board.md).

## Process

- Write a design doc first ([design.md](design.md)). Shreyansh reviews it before you build.
- `main` is protected: PR plus approval, no direct pushes.
- Changes to the signer, grant verification, relay control, and key handling (gate, app, keygen and provisioning tools) need Shreyansh's review (CODEOWNERS).
- The mock backend runs on a throwaway account, and preview builds get no production secrets.
- Secret scanning is on. Never commit keys, tokens, or WiFi passwords.

## Deliverables

1. Design doc ([design.md](design.md)).
2. Working end-to-end mock on the gate board, including the access log.
3. Threat list ([threats.md](threats.md)): how you would attack your own system (replay, relay, clone, flash dump, stolen phone, expired grant, tampered log).
4. Cutover checklist for Phase B ([cutover.md](cutover.md)).

## Out of scope

Production keys, flashing the live gate with real keys, and burning secure boot and flash encryption (Shreyansh, Phase B).

---

### Changes from the original draft

- **Current state:** removed "it is replayable". The current system uses single-use challenges, so recordings can't be replayed. Its real flaws are listed instead.
- **Plan:** Phase A happens in this repo on `main` via PRs (the `mock/door-auth` branch was for the old repo). Phase C says the dashboard *and backend* auto-deploy; a phone app can't, so its builds come from CI and are released by hand.
- **Gate / hard rules:** "no secrets on the ESP" became "no secret that can open the gate". The log token and WiFi password have to live on the ESP; they're stored in config, never in the firmware image.
- **Signed grants:** "baked-in signer public key" became "from its config", matching the config-driven rule.
- **Offline rule:** added the exception for no trusted time (fails closed).
- **Onboarding:** stated that guests use the app too.
- **Process:** spelled out which code counts as "key handling" for CODEOWNERS, and added relay control.
