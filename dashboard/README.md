# dashboard/

Admin web dashboard. Design: [docs/design.md §3](../docs/design.md#3-components).

**Not started yet.**

Features:
- Admin login with a **passkey only** (no TOTP fallback). Every approve or revoke asks for the passkey again.
- Create invites, approve pending members **after comparing the 6-digit key fingerprint** with the person's phone
- Approvals are signed by the admin's passkey (WebAuthn) and checked by the signer, not just stored in the DB
- Issue guest access (approval with a short end date)
- Revoke a person (all their grants) or a single phone
- Access log: filter by person and date, flag `seq` conflicts, show each gate's last sync time
- Alerts: every new approval, every admin login, and any gate offline for more than 1 hour
