# ActuateGuard

Secure, per-person access for the robotics club gate. Phones open the gate over Bluetooth using **signed, revocable grants** in place of one shared password. Every attempt is logged.

> **Status: Phase A (mock build).** Everything here uses throwaway keys and a throwaway backend. Nothing in this repo can open the real gate.

<!-- PHOTO: hero image of the gate board on the bench → docs/photos/board-bench.jpg (see issue "Photo: gate board on the bench") -->
<p align="center"><i>📷 Photo coming soon: the gate controller on the bench</i></p>

---

## How it works (30-second version)

1. **You get invited.** An admin gives you a one-time invite code. The app makes a key pair inside your phone's security chip, and the private key never leaves the phone.
2. **An admin approves you.** The backend's *signer* issues you a **grant**: a signed note saying "this phone may open gate X from date A to date B".
3. **At the gate,** your phone gets a random challenge, signs it, and sends it with your grant. The gate checks everything **offline** using only public keys, then opens the relay.
4. **Revoking** someone means their grant stops being renewed and goes on a signed revocation list that the gate pulls over HTTPS.
5. **Every attempt is logged** (allowed or denied, with the reason), buffered on the gate, and uploaded when online.

Bluetooth signal strength only *starts* the check. Being close to the gate alone never opens it.

Full details: **[docs/design.md](docs/design.md)**.

<!-- PHOTO: system diagram or wiring diagram → docs/photos/wiring-diagram.png (see issue "Photo: wiring diagram") -->

---

## Repo layout

| Folder | What goes there |
|---|---|
| [`firmware/`](firmware/) | ESP32 gate firmware: BLE, grant checking, relay, RTC, logs |
| [`app/`](app/) | Phone app (platform decided in the design review, D1) |
| [`backend/`](backend/) | API and the **signer** (the only part that holds a private signing key) |
| [`dashboard/`](dashboard/) | Admin web dashboard: approve, revoke, guest access, logs |
| [`tools/`](tools/) | Mock key generation, ESP provisioning, grant inspector |
| [`hardware/`](hardware/) | Parts list and wiring diagram |
| [`docs/`](docs/) | Design doc, threat list, cutover checklist, live-board rules, photos |

---

## Getting started

1. Read [docs/design.md](docs/design.md). It's the source of truth.
2. Read [docs/live-board.md](docs/live-board.md) **before touching the real gate board.**
3. Pick an [open issue](../../issues). Issues labelled `good first issue` (mostly photos and docs) are a good warm-up.
4. Branch from `main`, open a PR, and get a review. `main` is protected.

---

## Rules (non-negotiable)

- **No secrets in the repo, ever:** no keys, tokens, WiFi passwords or `.env` files. This repo is public. Secret scanning is on, and a leaked secret means rotating it, not just deleting the commit.
- **The gate holds public keys only.** Device-specific values go into the ESP's NVS storage at provisioning time, never into source code.
- **Signal strength alone never opens the gate.**
- **Standard crypto libraries only** (mbedTLS on the ESP, platform keystores on phones). No hand-rolled crypto.
- **The inside release and mechanical key must keep working at all times.**
- Changes to `firmware/src/auth/`, `backend/signer/` and `tools/keygen/` need review from @shreyansh-malviya (see [CODEOWNERS](.github/CODEOWNERS)).

Found a security problem? See [SECURITY.md](SECURITY.md). Please don't open a public issue for it.

---

## Photos

<!-- Add photos to docs/photos/ and replace the placeholders below. Each one has an issue. -->

| | |
|---|---|
| *📷 Gate board on the bench* | *📷 Relay module close-up* |
| *🖼️ Wiring diagram (drawn, not a photo)* | *📱 App screenshots* |
| *🖥️ Dashboard screenshots* | |

**Never post photos of the installed gate:** not its location, the outside of the gate, the enclosure in place, the lock model, or the wiring where it's mounted. This is a public repo, and those photos would show an attacker where to work. See [docs/photos/README.md](docs/photos/README.md).

---

## Team

Robotics club, `actuate-sst`. Design and security review: @shreyansh-malviya.
