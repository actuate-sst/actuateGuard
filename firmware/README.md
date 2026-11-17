# firmware/

ESP32 gate firmware. Design: [docs/design.md §8](../docs/design.md#8-gate-firmware).

**Not started yet.** The toolchain (PlatformIO / arduino-cli) is decision D7.

Planned layout:

```
src/
  main.cpp        setup/loop and wiring only
  config.*        reads gate ID, signer public key, URL, CA cert, WiFi, token from NVS
  ble_gatt.*      GATT service, MTU, connection timeout
  auth/           grant + signature checks (CODEOWNERS: @shreyansh-malviya)
  relay.*         fail-safe relay control (CODEOWNERS)
  clock.*         DS3231 RTC + HTTPS time sync
  log_buffer.*    flash ring buffer with sequence numbers
  uploader.*      log upload, revocation list pull, time sync
```

Rules:
- **No secrets or device-specific values in source.** They're written into NVS by `tools/provision`.
- The relay pin is driven to *locked* before `pinMode(OUTPUT)`, with a hard max-open time. See §8.2.
- No serial commands that print or change keys.
- Read [docs/live-board.md](../docs/live-board.md) before flashing the real gate board.
