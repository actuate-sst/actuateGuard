# backend/

API + signer. Design: [docs/design.md §3, §6, §7](../docs/design.md).

**Not started yet.** The stack is decision D3.

Planned pieces:
- **API:** enroll with invite code, fetch and refresh grant, revocation list, `/time`, log ingestion.
- **`signer/`:** signs grants, revocation lists and time responses, and nothing else. It issues grants **only within approvals signed by an admin passkey** (checked against keys pinned in its own config) and never trusts the DB or API for who is approved. CODEOWNERS: @shreyansh-malviya.
- **DB:** users, invites (only `SHA-256(code)` stored), grants, revocations, logs (append-only, 90-day retention).

Rules:
- Phase A runs on a **throwaway account** with **mock keys**. Preview builds get no production secrets.
- The gate's log token can only **insert** log rows. Nothing can update or delete logs except the retention job. Rows with a clashing `(gate_id, seq)` are stored and flagged, never rejected.
- One log token per gate, rotatable; inserts rate-limited per token. The enroll endpoint is rate-limited too.
