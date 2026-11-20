"""Model-specific error messages, warning lights and status information.

Every entry here comes from the manufacturer's own documentation (operation
manuals, operating instructions, service bulletins). The source is named on
each block and shown on the page. Nothing is guessed: where a manufacturer
documents no error codes, the block says so.

Each block is a dict:
  title   heading text (the model name is added by the template)
  intro   one or two sentences
  rows    list of (what you see, what it means, what to do)
  note    optional extra paragraph
  source  the documents the block is based on
  faq     list of (question, answer) added to the page FAQ and FAQ schema
"""
import re

# ---------------------------------------------------------------- monitors

_SERVICE = "Turn the monitor off and have it serviced."

MONITOR_INFO = {
    "sony-pvm-a250": {
        "title": "warning lights and error signals",
        "intro": "Sony lists no numbered error codes for the PVM-A250. The monitor reports problems through the power switch indicator on the front panel.",
        "rows": [
            ("Power indicator flashes red",
             "Sony's instructions give the cause as an abnormality with the panel, the power supply or a sensor.",
             _SERVICE),
            ("Power indicator flashes amber once a second",
             "The monitor has lowered its brightness to protect the OLED panel from overheating.",
             "Make sure the vents are clear and the room is not hot. If it keeps happening, have the monitor checked."),
            ("Power indicator stays amber",
             "The screen is at its brightest.",
             "Sony's instructions say to reduce contrast or brightness."),
            ("Screen goes dark and the monitor turns off",
             "The internal temperature may have risen too high.",
             "Leave it off and have it serviced."),
            ("Buttons do not respond",
             "Key protection is on.",
             "Set Key Inhibit to Off in the Security menu."),
        ],
        "source": "Sony PVM-A250 / PVM-A170 Operating Instructions.",
        "faq": [
            ("What does a flashing red power light mean on the Sony PVM-A250?",
             "Sony's operating instructions say a red flashing power indicator means an abnormality with the panel, the power supply or a sensor. The monitor needs service."),
            ("Why is the power light on my Sony PVM-A250 amber?",
             "Flashing amber once a second means the monitor has lowered its brightness to protect the panel from overheating. A steady amber light means the screen is at its brightest, and Sony says to reduce contrast or brightness."),
        ],
    },
    "sony-pvm-1741a": {
        "title": "warning lights and error signals",
        "intro": "Sony's operating instructions for the PVM-2541A and PVM-1741A list no numbered error codes. The fault signal they describe is the fan error.",
        "rows": [
            ("Standby switch indicator blinks green and amber",
             "Fan error. The built-in cooling fan has stopped.",
             "Turn the power off and have the monitor serviced."),
            ("Buttons do not respond",
             "Key protection is on.",
             "Set KEY INHIBIT to OFF in the KEY INHIBIT menu."),
        ],
        "source": "Sony PVM-2541A / PVM-1741A Operating Instructions.",
        "faq": [
            ("What does a green and amber blinking light mean on the Sony PVM-1741A?",
             "It is the fan error signal. Sony's operating instructions say that when the cooling fan stops, the standby switch indicator on the front panel blinks green and amber. Turn the power off and have the monitor serviced."),
        ],
    },
    "sony-pvm-x3200": {
        "title": "warning lights and error signals",
        "intro": "Sony lists no numbered error codes for the PVM-X3200. The monitor reports problems through the power switch indicator and the CAUTION indicator on the front panel.",
        "rows": [
            ("Power indicator flashes red once a second",
             "Power, circuit board or sensor abnormality.",
             _SERVICE),
            ("Power indicator flashes red every two seconds",
             "Fan, circuit board or backlight abnormality. Sony's fan error note says to turn the power off when the fan stops and this light blinks red.",
             _SERVICE),
            ("CAUTION indicator flashes amber once a second",
             "The monitor has lowered its brightness to protect the panel from overheating. Sony notes this can happen in HDR display whatever the input signal.",
             "Keep the room around 25 °C (77 °F), as Sony advises, and keep the vents clear."),
            ("Power indicator is steady red",
             "Sleep mode. This is normal.",
             "No action needed."),
        ],
        "source": "Sony PVM-X3200 / PVM-X2400 / PVM-X1800 Operating Instructions.",
        "faq": [
            ("What does a flashing red power light mean on the Sony PVM-X3200?",
             "Sony's operating instructions give two patterns. Red once a second means a power, circuit board or sensor abnormality. Red every two seconds means a fan, circuit board or backlight abnormality. Both need service."),
            ("Why is the CAUTION light flashing amber on my Sony PVM-X3200?",
             "The monitor has lowered its brightness to protect the panel from overheating. Sony advises keeping the surrounding temperature around 25 °C (77 °F)."),
        ],
    },
    "sony-bvm-hx310": {
        "title": "warning lights and error messages",
        "intro": "Sony lists no numbered error codes for the BVM-HX310. The monitor reports problems through the power switch indicator and the CAUTION indicator on the front panel, plus a few on-screen messages.",
        "rows": [
            ("Power indicator flashes red once a second",
             "Power, circuit board or sensor abnormality.",
             _SERVICE),
            ("Power indicator flashes red every two seconds",
             "Fan or circuit board abnormality. Sony's fan error note says to turn the power off when the fan stops and this light blinks red.",
             _SERVICE),
            ("CAUTION indicator flashes amber once a second",
             "The monitor has lowered its brightness to protect the panel from overheating. Sony notes this can happen in HDR display whatever the input signal.",
             "Keep the room around 25 °C (77 °F), as Sony advises, and keep the vents clear."),
            ("Screen goes dark and the monitor turns off",
             "The internal temperature may be high.",
             "Sony says to check whether the vents are blocked by dust. If they are clear, have the monitor serviced."),
            ("“Invalid Input Combination” on screen",
             "In Quad View, the selected inputs cannot be shown together. The screen goes black.",
             "Change the input selection."),
            ("“Simulated ABL” on screen",
             "A notice, not a fault. It belongs to the Simulated ABL setting, which imitates the brightness limiting of the BVM-X300.",
             "No action needed. The notice can be turned off in the menu."),
            ("Power indicator is steady red",
             "Sleep mode, set from the controller. This is normal.",
             "No action needed."),
            ("Buttons do not respond",
             "Key protection is on.",
             "Press and hold KEY INHIBIT for more than two seconds."),
        ],
        "source": "Sony BVM-HX310 Operating Instructions.",
        "faq": [
            ("What does a flashing red power light mean on the Sony BVM-HX310?",
             "Sony's operating instructions give two patterns. Red once a second means a power, circuit board or sensor abnormality. Red every two seconds means a fan or circuit board abnormality. Both need service."),
            ("Why is the CAUTION light flashing amber on my Sony BVM-HX310?",
             "The monitor has lowered its brightness to protect the panel from overheating. Sony advises keeping the surrounding temperature around 25 °C (77 °F)."),
        ],
    },
    "sony-lmd-a240": {
        "title": "warning lights and error signals",
        "intro": "Sony lists no numbered error codes for the LMD-A240. The monitor reports problems through the power switch indicator on the front panel.",
        "rows": [
            ("Power indicator flashes red",
             "Sony's instructions give the cause as an abnormality with the panel, the power supply or a sensor.",
             _SERVICE),
            ("Power indicator flashes amber once a second",
             "The monitor has lowered its brightness to protect itself from overheating.",
             "Make sure the vents are clear and the room is not hot. If it keeps happening, have the monitor checked."),
            ("Screen goes dark and the monitor turns off",
             "The internal temperature may have risen too high.",
             "Leave it off and have it serviced."),
            ("Buttons do not respond",
             "Key protection is on.",
             "Set Key Inhibit to Off in the Security menu."),
            ("Black bars at the top and bottom, or left and right",
             "The signal's aspect ratio differs from the panel's. Sony says this is not a failure.",
             "No action needed."),
        ],
        "source": "Sony LMD-A240 / LMD-A220 / LMD-A170 Operating Instructions.",
        "faq": [
            ("What does a flashing red power light mean on the Sony LMD-A240?",
             "Sony's operating instructions say a red flashing power indicator means an abnormality with the panel, the power supply or a sensor. The monitor needs service."),
            ("Why is the power light flashing amber on my Sony LMD-A240?",
             "Flashing amber once a second means the monitor has lowered its brightness to protect itself from overheating."),
        ],
    },
    "sony-lmd-2451td": {
        "title": "warning lights and error signals",
        "intro": "Sony's operating instructions for the LMD-2451TD list no numbered error codes. The fault signal they describe is the fan error.",
        "rows": [
            ("RETURN button on the front panel blinks",
             "Fan error. The built-in cooling fan has stopped.",
             "Turn the power off and have the monitor serviced."),
            ("Picture looks green or purple",
             "The input type selected does not match the signal.",
             "Press the RGB or COMPONENT button to select the right one."),
            ("Buttons do not respond",
             "Key lock is on.",
             "Turn it off in the KEY LOCK menu."),
            ("Black bars at the top or bottom",
             "The signal's aspect ratio differs from the panel's. This is not a fault.",
             "No action needed."),
        ],
        "source": "Sony LMD-4251TD / LMD-2451TD Operating Instructions.",
        "faq": [
            ("What does a blinking RETURN button mean on the Sony LMD-2451TD?",
             "It is the fan error signal. Sony's operating instructions say that when the cooling fan stops, the RETURN button on the front panel blinks. Turn the power off and have the monitor serviced."),
        ],
    },
    "sony-bvm-d24e1wu": {
        "title": "warning lamps and error messages",
        "intro": "Sony lists no numbered error codes for the BVM-D24E1WU. The monitor reports its condition through front-panel lamps and on-screen messages.",
        "rows": [
            ("OVER LOAD lamp is lit",
             "The lamp warns of CRT overload.",
             "Sony's manual says to use the monitor with contrast or brightness reduced. If the lamp stays on at normal settings, have the monitor checked."),
            ("STANDBY lamp blinks after the main power is switched on",
             "Internal data is initializing. The monitor cannot go into operation mode until the lamp stays lit.",
             "Wait a few moments."),
            ("“INITIALIZING” on screen",
             "Shown when the monitor is turned on. It does not accept commands from the control unit while this is displayed.",
             "Wait for it to clear."),
            ("“NG” or “ERROR” during menu operation",
             "The menu operation failed.",
             "Sony's manual says to press the MENU button to return to the menu in use."),
        ],
        "source": "Sony BVM-D20F1U / BVM-D24E1WU / BVM-D32E1WU Operation Manual.",
        "facts": [
            ("Viewable picture, 16:9", "482.1 x 271.2 mm (21⅞ inches diagonal)"),
            ("Viewable picture, 4:3", "361.6 x 271.2 mm (17⅞ inches diagonal)"),
        ],
        "faq": [
            ("What does the OVER LOAD lamp mean on the Sony BVM-D24E1WU?",
             "Sony's operation manual says the OVER LOAD lamp lights to warn of CRT overload, and to use the monitor with contrast or brightness reduced."),
            ("Why is the STANDBY lamp blinking on my Sony BVM-D24E1WU?",
             "For a few moments after the main power is switched on, the STANDBY lamp blinks while internal data initializes. The monitor cannot go into operation mode until the lamp stays lit."),
        ],
    },
    "sony-bvm-20f1u": {
        "title": "warning lamps and fault signals",
        "intro": "Sony service bulletins for the BVM-20F1U describe one fault signal: the three front-panel lamps blinking together.",
        "rows": [
            ("OVER LOAD, STANDBY and POWER lamps blink together at power-on (about 2 seconds on, half a second off)",
             "Sony bulletin B96-272: the over-voltage protection on the +B supply has tripped.",
             "Switch the monitor off. It needs bench repair, so do not keep cycling the power."),
            ("OVER LOAD, STANDBY and POWER lamps blink and the monitor will not operate on 200 to 240 V AC",
             "Sony bulletin B96-273: the PFC (power factor compensation) output over-voltage protection is activating.",
             "Switch the monitor off and have it repaired."),
        ],
        "note": "Sony issued the bulletins for early production units: BVM-20F1U serial numbers 2,000,001 to 2,001,230 (B96-272) and 2,000,001 to 2,001,210 (B96-273).",
        "source": "Sony technical bulletins B96-272 and B96-273 for the BVM-20F1U and related BVM-E and BVM-F series monitors.",
        "faq": [
            ("Why are all three lamps blinking on my Sony BVM-20F1U?",
             "Sony service bulletins for the BVM-20F1U describe the OVER LOAD, STANDBY and POWER lamps blinking together when an over-voltage protection circuit has tripped. The monitor will not run in that state and needs bench repair."),
        ],
    },
    "sony-pvm-20m2u": {
        "title": "indicator and error information",
        "intro": "Sony's service manual for the PVM-20M2U and PVM-20M4U has no error code or self-diagnosis section. The front indicator it describes is the POWER indicator, which lights green when the monitor is on.",
        "rows": [],
        "note": "For the DEGAUSS button, Sony's instructions say to wait 10 minutes or more before using it again.",
        "source": "Sony PVM-20M2U / PVM-20M4U Service Manual.",
        "faq": [
            ("Does the Sony PVM-20M2U have error codes?",
             "Sony's service manual for the PVM-20M2U and PVM-20M4U has no error code or self-diagnosis section. The POWER indicator lights green when the monitor is on."),
        ],
    },
}


def monitor_info(slug):
    return MONITOR_INFO.get(slug)


# ------------------------------------------------------------------ lenses

_CANON_BOX = {
    "title": "error messages",
    "intro": "Canon's DIGISUPER operation manual lists no numbered error codes. It documents one error message, shown in words on the lens's information display.",
    "rows": [
        ("“Initialize Error!” on the information display",
         "Canon's manual says this appears when the servo module is not mounted correctly, when the lens is forcibly locked, or for some other reason. It belongs to the initialize operation, where the lens detects its positions after power-on.",
         "Check the lens, clear the problem, then turn the power off and on, as Canon's manual directs. If the message comes back, send the lens in."),
        ("Zoom or focus position reads wrong on the camera or the lens display",
         "Canon's manual says that when position detection fails, the position signal the lens sends to the camera and the reading on the information display will be incorrect.",
         "Turn the power off and on so the lens can initialize again. If the readings stay wrong, send the lens in."),
    ],
    "note": "This applies to DIGISUPER lenses that have the information display.",
    "source": "Canon DIGISUPER 100AF (XJ100x9.3B AF) Operation Manual.",
}

_CANON_PORTABLE = {
    "title": "error messages",
    "intro": "The Canon portable lens manuals reviewed list no numbered error codes. Lenses with the information display on the drive unit can show a start-up error in words.",
    "rows": [
        ("“Initialize Error” on the drive unit display at power-on",
         "The lens did not finish its power-on initialization. Canon's DIGISUPER manual gives the causes of this message as a servo unit that is not mounted correctly, a lens that is forcibly locked, or some other reason.",
         "Turn the camera power off, make sure nothing is holding the zoom, focus or iris, and power on again. If the message returns, send the lens in."),
    ],
    "source": "Canon operation manuals for CJ and KJ portable lenses and for DIGISUPER lenses; owner report on Canon's community forum (HJ22ex7.6B IASE).",
}

_CANON_PORTABLE_S_ROWS = [
    ("Information display goes blank",
     "Normal. Canon's manual says the display turns off after 2 minutes without operation.",
     "No action needed."),
]
_CANON_PORTABLE_S_NOTE = "Power: Canon's manual gives the supply range as 10 to 17 V DC and warns that voltage outside it may damage the drive unit."

_CANON_OTHER = {
    "title": "error messages",
    "intro": "No error codes are listed for this lens in the Canon operation manuals reviewed.",
    "rows": [],
    "source": "Canon BCTV zoom lens operation manuals.",
}

_FUJINON_BOX = {
    "title": "error codes and status signals",
    "intro": "The Fujinon box lens operation manuals reviewed list no numbered error codes. These are the status signals the manuals describe.",
    "rows": [
        ("Lens does not respond right after power-on",
         "Normal. Fujinon's manuals say the lens runs an initial setting for several seconds at power-on, and the optical stabilizer, on lenses that have one, for about ten seconds. Lens controls do not work until it finishes, and the zoom then returns to where it was.",
         "Wait for it to finish, and do not pan or tilt during the stabilizer's initial setting. If the lens never becomes ready, send it in."),
        ("Stabilizer control unit indicator blinks",
         "The stabilizer is running its initial setting.",
         "Wait until it stops."),
        ("LCD panel shows MT-NO",
         "No servo module is connected.",
         "Check that the servo modules are fitted and seated."),
        ("LCD panel shows IDLE",
         "No controller is connected. The lens holds its current position.",
         "Check the zoom and focus demand connections."),
        ("LCD panel shows MEM-NO, HOST-NO or FILE-NO",
         "USB messages: no USB memory is connected, the USB driver is not in HOST mode, or no settings file was found on the USB memory.",
         "Nothing, unless you are saving or loading lens settings by USB."),
        ("Iris hunts in auto mode",
         "Fujinon's manual says the iris may hunt depending on the camera, and provides an iris gain adjustment for it.",
         "Have the iris gain adjusted."),
    ],
    "note": "The LCD panel rows apply to box lenses fitted with Fujinon's LCD panel. For deeper diagnosis, Fujinon's manuals describe an RS-232C connector on the lens used for self-diagnosis with the FUJINON Find System.",
    "source": "Fujinon XA99x8.4BESM, XA55x9.5BESM and UA107x8.4BESM Operation Manuals; Fujinon box lens LCD Panel User Manual.",
}

_FUJINON_UA_HA_PORTABLE = {
    "title": "error codes and status information",
    "intro": "The Fujinon portable lens operation manuals reviewed (UA and HA series) list no error codes and describe no display on the drive unit. These are the checks the manuals give.",
    "rows": [
        ("Lens misbehaves when the camera is controlling it",
         "Fujinon's manuals treat this as a possible serial communication failure between the lens and the camera.",
         "Set the camera communication switch on the drive unit to OFF, as the manuals direct, and test again. If the fault stays, send the lens in."),
        ("Iris hunts (keeps moving) in auto mode",
         "Iris sensitivity is set too high. Fujinon's manuals warn that raising it too far causes hunting.",
         "Turn the iris sensitivity trimmer counterclockwise to lower it."),
    ],
    "source": "Fujinon UA series (BERD-S6, BERD-S10) and HA Premier series (BERD-S6, BERM-M6) Operation Manuals.",
}

_FUJINON_PORTABLE = {
    "title": "error codes and status information",
    "intro": "The Fujinon portable lens operation manuals reviewed (UA and HA series) list no numbered error codes.",
    "rows": [],
    "source": "Fujinon UA series and HA Premier series portable lens Operation Manuals.",
}

_FUJINON_OTHER = {
    "title": "error codes and status information",
    "intro": "No error codes are listed in the Fujinon operation manuals reviewed.",
    "rows": [],
    "source": "Fujinon TV lens operation manuals.",
}

# Specifications taken from the manufacturer's operation manual for that exact model.
LENS_FACTS = {
    "fujinon-xa99x8-4besm": [
        ("Focal length", "8.4 to 832 mm (16.8 to 1664 mm with the 2x extender)"),
        ("Maximum aperture", "F1.7 (8.4 to 341 mm) to F4.15 (832 mm)"),
        ("Minimum object distance", "2.9 m"),
        ("Weight", "About 23.5 kg"),
    ],
    "fujinon-ua107x8-4besm": [
        ("Focal length", "8.4 to 900 mm (16.8 to 1800 mm with the 2x extender)"),
        ("Maximum aperture", "F1.7 (8.4 to 340 mm) to F4.5 (900 mm)"),
        ("Minimum object distance", "3.05 m"),
        ("Weight", "About 23.9 kg"),
    ],
}
LENS_FACTS_SOURCE = "Fujinon operation manual for this model."


def _with_faq(block, name, faq):
    out = dict(block)
    out["faq"] = faq
    return out


def lens_info(brand_slug, model):
    """Return the information block for one lens model."""
    name = model["name"]
    if brand_slug == "canon":
        if re.search(r"DIGISUPER|\b[XU]J\d", name):
            return _with_faq(_CANON_BOX, name, [
                ("What does “Initialize Error!” mean on the " + name + "?",
                 "On Canon DIGISUPER lenses with the information display, Canon's operation manual says the message appears when the servo module is not mounted correctly, when the lens is forcibly locked, or for some other reason. Check the lens, clear the problem, then turn the power off and on. If the message returns, the lens needs service."),
                ("Does the " + name + " have error codes?",
                 "Canon's DIGISUPER operation manual lists no numbered error codes. The error message it documents is “Initialize Error!”, shown on the lens's information display."),
            ])
        if re.search(r"IASE|KASE|HJ40ex", name):
            block = dict(_CANON_PORTABLE)
            if re.search(r"\b[CK]J\d", name) and re.search(r"(IASE|KASE)( II)? S\b", name):
                block["rows"] = block["rows"] + _CANON_PORTABLE_S_ROWS
                block["note"] = _CANON_PORTABLE_S_NOTE
            return _with_faq(block, name, [
                ("What does “Initialize Error” mean on the " + name + "?",
                 "The lens did not finish its power-on initialization. Canon's DIGISUPER manual gives the causes of this message as a servo unit that is not mounted correctly, a lens that is forcibly locked, or some other reason. Turn the power off and on. If the message returns, the lens needs service."),
            ])
        return _with_faq(_CANON_OTHER, name, [])
    if brand_slug == "fujinon":
        if re.search(r"BESM|BES\b", name):
            return _with_faq(_FUJINON_BOX, name, [
                ("Does the " + name + " have error codes?",
                 "The Fujinon box lens operation manuals reviewed list no numbered error codes. The lens shows its condition through its indicators and, on lenses fitted with the LCD panel, status messages such as MT-NO (no servo module connected) and IDLE (no controller connected)."),
                ("Why does the " + name + " not respond right after power-on?",
                 "Fujinon's manuals say the lens runs an initial setting for several seconds at power-on, and the optical stabilizer, on lenses that have one, for about ten seconds. Lens controls do not work until it finishes."),
            ])
        if re.search(r"BERD|BERM", name):
            if re.search(r"\b(UA|HA)\d", name):
                return _with_faq(_FUJINON_UA_HA_PORTABLE, name, [
                    ("Does the " + name + " have error codes?",
                     "The Fujinon portable lens operation manuals reviewed (UA and HA series) list no error codes and describe no display on the drive unit. For a suspected serial communication failure, the manuals say to set the camera communication switch on the drive unit to OFF."),
                ])
            return _with_faq(_FUJINON_PORTABLE, name, [])
        return _with_faq(_FUJINON_OTHER, name, [])
    return None
