"""Sony monitor models with pages under /monitor-repair/<slug>.

kind: crt, oled or lcd. size and display come from the model pages the owner supplied.
"""

SONY_MONITORS = [
    {"name": "Sony PVM-A250", "slug": "sony-pvm-a250", "kind": "oled", "display": "OLED", "size": "25 inches"},
    {"name": "Sony PVM-1741A", "slug": "sony-pvm-1741a", "kind": "oled", "display": "OLED", "size": "17 inches"},
    {"name": "Sony PVM-X3200", "slug": "sony-pvm-x3200", "kind": "lcd", "display": "4K HDR LCD with LED backlight", "size": "32 inches"},
    {"name": "Sony BVM-HX300", "slug": "sony-bvm-hx300", "kind": "lcd", "display": "4K HDR dual-layer LCD", "size": "30 inches"},
    {"name": "Sony BVM-HX310", "slug": "sony-bvm-hx310", "kind": "lcd", "display": "4K HDR dual-layer LCD", "size": "31 inches"},
    {"name": "Sony LMD-A240", "slug": "sony-lmd-a240", "kind": "lcd", "display": "LCD", "size": "24 inches"},
    {"name": "Sony LMD-2451TD", "slug": "sony-lmd-2451td", "kind": "lcd", "display": "LCD", "size": None},
    {"name": "Sony BVM-D24E1WU", "slug": "sony-bvm-d24e1wu", "kind": "crt", "display": "CRT", "size": "24 inches (16:9)"},
    {"name": "Sony BVM-20F1U", "slug": "sony-bvm-20f1u", "kind": "crt", "display": "CRT", "size": "20 inches (4:3)"},
    {"name": "Sony PVM-20M2U", "slug": "sony-pvm-20m2u", "kind": "crt", "display": "CRT", "size": "20 inches (4:3)"},
]

SONY_BY_SLUG = {m["slug"]: m for m in SONY_MONITORS}

# Problems and services by display kind (from the owner's monitor repair pages)
PROBLEMS = {
    "crt": [
        "No power or dead unit",
        "Screen dark, or a dim image from weak tube emission",
        "Poor convergence and color fringing",
        "Geometry problems: bowing, pincushion, trapezoid",
        "Color purity patches",
        "Soft or out-of-focus picture",
        "Vertical collapse, flicker or an unstable image",
    ],
    "oled": [
        "No power or won't boot",
        "Image persistence and burn-in",
        "Color shift or calibration off",
        "SDI and HDMI input port damage",
        "Lines, flicker or artifacts",
        "Power supply failure",
    ],
    "lcd": [
        "No power or won't boot",
        "Backlight and inverter failure",
        "Dead or stuck pixels",
        "Lines, flicker or artifacts",
        "SDI and HDMI input port damage",
        "Color shift or calibration off",
    ],
}

SERVICES = {
    "crt": [
        "Full diagnostic and evaluation",
        "Power supply and deflection board recap",
        "CRT board service",
        "Convergence alignment",
        "Geometry and purity calibration",
        "Grayscale and color calibration",
    ],
    "oled": [
        "Full diagnostic and evaluation",
        "Power supply repair",
        "Input board (SDI and HDMI) repair",
        "Panel and image persistence evaluation",
        "Color calibration",
    ],
    "lcd": [
        "Full diagnostic and evaluation",
        "Power supply repair",
        "Backlight repair",
        "Input board (SDI and HDMI) repair",
        "Color calibration",
    ],
}
