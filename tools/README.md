# tools/

Helper scripts. **Not started yet.**

| Tool | Purpose |
|---|---|
| `keygen/` | Generate a **mock** signer key pair for Phase A. The output goes outside the repo (`keys/` and `*.pem` are gitignored). CODEOWNERS. |
| `provision/` | Write gate ID, signer public key, backend URL, CA cert, WiFi and log token into the ESP's NVS partition, reading from a local `provisioning.local.*` file that is never committed. |
| `grant-inspect/` | Decode a grant and check it against a public key, for debugging. |
