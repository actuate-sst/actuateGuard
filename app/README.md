# app/

The phone app: onboarding with an invite code, a hardware-backed key pair, grant refresh, and unlock over BLE. Design: [docs/design.md §9](../docs/design.md#9-phone-app).

**Not started yet.** The platform (Android / iOS / both) is decision D1. Subfolders (`android/`, `ios/`) get created once it's decided.

Rules:
- The private key is generated in the Android Keystore / iOS Secure Enclave and is **never exported**, logged or shown.
- The grant isn't secret; ordinary app storage is fine.
- Onboarding tells the person they're **logged** (what's recorded, kept 90 days, visible to admins) and needs their OK **before** the key is created.
- After creating the key, show the **6-digit fingerprint** (first 20 bits of SHA-256 of the public key) for the admin to compare.
- Signal strength only triggers an unlock attempt. The gate makes the decision.
