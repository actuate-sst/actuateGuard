"""Gate controller schematic (current setup).

Regenerate after editing:
    pip install schemdraw==0.19
    python hardware/schematic.py            # writes hardware/schematic.svg

Optional PNG preview (needs matplotlib):
    python hardware/schematic.py --png out.png
"""

import re
import sys
from pathlib import Path

import schemdraw
import schemdraw.elements as elm

OUT = Path(__file__).with_name("schematic.svg")

RED, BLUE, PURPLE = "#c0392b", "#2471a3", "#7d3c98"
GAP = 4.5  # horizontal space between blocks


def pin(name, side, anchor=None):
    return elm.IcPin(name=name, side=side, anchorname=anchor or name)


def draw(backend="svg"):
    schemdraw.use(backend)
    d = schemdraw.Drawing(fontsize=12, lw=1.6)
    d.config(unit=2.5, bgcolor="white", margin=0.6)  # white bg so it reads in GitHub dark mode

    # ESP32 dev board
    esp = d.add(
        elm.Ic(
            pins=[
                pin("GND", "left", "USBGND"),
                pin("USB 5V", "left", "USB5V"),
                pin("GPIO13", "right", "IO13"),
                pin("GND", "right", "GND"),
                pin("VIN (5V)", "right", "VIN"),
            ],
            size=(5.0, 4.0),
            pinspacing=1.0,
            label="ESP32\ndev board",
            lblsize=13,
        )
    )

    # Power, aligned to the ESP32's left pins
    ux, uy = esp.USB5V
    psu = d.add(
        elm.Ic(
            pins=[pin("GND", "right", "PGND"), pin("5V", "right", "P5V")],
            size=(3.6, 2.0),
            pinspacing=1.0,
            label="5 V USB\nadapter",
            lblsize=11,
        ).anchor("P5V").at((ux - GAP, uy))
    )

    # Relay module, aligned to the ESP32's right pins
    vx, vy = esp.VIN
    relay = d.add(
        elm.Ic(
            pins=[
                pin("IN", "left", "IN"),
                pin("GND", "left", "RGND"),
                pin("VCC", "left", "VCC"),
                pin("NC", "right", "NC"),
                pin("NO", "right", "NO"),
                pin("COM", "right", "COM"),
            ],
            size=(5.0, 4.0),
            pinspacing=1.0,
            label="Relay module\n(1-channel)",
            lblsize=13,
        ).anchor("VCC").at((vx + GAP, vy))
    )

    # Door lock controller, aligned to the relay's COM/NO
    cx, cy = relay.COM
    lock = d.add(
        elm.Ic(
            pins=[pin("EXIT B", "left", "EXB"), pin("EXIT A", "left", "EXA")],
            size=(4.6, 3.0),
            pinspacing=1.0,
            label="Door lock\ncontroller",
            lblsize=13,
        ).anchor("EXA").at((cx + 10.0, cy))
    )

    # Power -> ESP32
    d.add(elm.Wire("-").at(psu.P5V).to(esp.USB5V).color(RED))
    d.add(elm.Wire("-").at(psu.PGND).to(esp.USBGND))

    # ESP32 -> relay module
    d.add(elm.Wire("-").at(esp.VIN).to(relay.VCC).color(RED))
    d.add(elm.Wire("-").at(esp.GND).to(relay.RGND))
    d.add(
        elm.Wire("-").at(esp.IO13).to(relay.IN).color(BLUE)
        .label("signal (active-LOW)", loc="bottom", fontsize=10)
    )

    # Relay contacts -> exit-button terminals (in parallel with the button)
    d.add(elm.Wire("-").at(relay.COM).to(lock.EXA).color(PURPLE))
    d.add(elm.Wire("-").at(relay.NO).to(lock.EXB).color(PURPLE))
    d.add(elm.Dot(open=True).at(relay.NC).label("unused", loc="right", fontsize=10))

    # Existing exit button across the same two lines
    ax, ay = lock.EXA
    _, by = lock.EXB
    bx = cx + 4.0
    d.add(elm.Dot().at((bx, ay)))
    d.add(elm.Dot().at((bx, by)))
    d.add(
        elm.Button().at((bx, ay)).to((bx, by))
        .label("existing exit button\n(still works)", loc="bottom", ofst=0.3, fontsize=10)
    )

    # Caption under everything
    _, iy = esp.IO13
    d.add(
        elm.Label().at(((psu.P5V[0] + ax) / 2, iy - 2.2)).label(
            "Relay COM/NO is wired in parallel with the lock's exit button: "
            "closing the relay = pressing the button.",
            fontsize=11,
        )
    )
    return d


if __name__ == "__main__":
    if "--png" in sys.argv:
        out = sys.argv[sys.argv.index("--png") + 1]
        draw("matplotlib").save(out, dpi=150)
        print(f"wrote {out}")
    else:
        draw("svg").save(str(OUT))
        # Insert a solid white rect behind the drawing: CSS backgrounds are not
        # always honoured when GitHub renders an SVG as <img>.
        svg = OUT.read_text(encoding="utf-8")
        x, y, w, h = re.search(r'viewBox="([^"]+)"', svg).group(1).split()
        rect = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="white" />'
        svg = re.sub(r"(<svg[^>]*>)", r"\1" + rect, svg, count=1)
        OUT.write_text(svg, encoding="utf-8")
        print(f"wrote {OUT}")
