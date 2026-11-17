# Working on the live gate board

Phase A is tested **on the real gate board**, which people use every day. These rules keep it working.

## Before you start
1. **Back up the current firmware:** `esptool.py read_flash 0 ALL flash-backup-<date>.bin`. Keep the file **off the repo** (it's gitignored), and check that it isn't empty.
2. **One person holds the mock signer private key.** It never goes in the repo, the group chat or a shared drive.

## During a session
3. **Someone is physically at the gate** for the whole session.
4. Mock firmware rejects grants longer than **about 1 hour**.
5. The **inside release and mechanical key keep working** at all times. Test them at the start.
6. Relay fail-safe: there's a max-open time and a cooldown. Check that the relay stays **off through a reset** (press EN/RST and watch it).

## Ending a session
7. **Flash the known-good firmware back.** Mock firmware never stays overnight.
8. Test one normal unlock with the known-good firmware before leaving.
9. Note the session in the PR or issue: date, who was there, what was flashed, and that it was restored.

## Relay pin
Avoid ESP32 strapping pins (GPIO 0, 2, 12, 15). They change state during boot and can click the relay.
