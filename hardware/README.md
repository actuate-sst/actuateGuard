# hardware/

Parts list and wiring for the gate controller.

## Parts (bill of materials)

| Part | Notes |
|---|---|
| ESP32 dev board | The current gate board |
| Relay module | Drives the gate lock. Check whether it's active-low or active-high, and that it stays **off through reset and power-up**. |
| DS3231 RTC module | Trusted time for grant expiry and logs, with coin-cell backup |
| Reed switch (optional) | Confirms the gate actually opened (decision D8) |

## Wiring

<!-- PHOTO/DIAGRAM: docs/photos/wiring-diagram.png (see issue "Photo: wiring diagram") -->
*🖼️ Wiring diagram coming soon.* Draw it (Fritzing, KiCad, draw.io or hand-drawn) instead of photographing the installed gate.

Pin rules:
- The relay must **not** use a strapping pin (GPIO 0, 2, 12, 15).
- The inside release and mechanical key work independently of the ESP.
