# backend/

API + signer. Design: [docs/design.md §3, §6, §7](../docs/design.md).

**Not started yet.** The stack is decision D3.

Planned pieces:
- **API:** enroll with invite code, fetch and refresh grant, revocation list, `/time`, log ingestion.
- **`signer/`:** signs grants and revocation lists, and nothing else. CODEOWNERS: @shreyansh-malviya.
- **DB:** users, invites (only `SHA-256(code)` stored), grants, revocations, logs (append-only, 90-day retention).

Rules:
- Phase A runs on a **throwaway account** with **mock keys**. Preview builds get no production secrets.
- The gate's log token can only **insert** log rows. Nothing can update or delete logs except the retention job.
