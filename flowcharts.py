"""Troubleshooting flowcharts for Fujinon lenses.

These flowcharts are Tek Media Group's own. Fujinon's operation manuals contain
no troubleshooting flowchart, so each check below is either a control or caution
described in those manuals, or a plain swap test to isolate the fault.

A flowchart is a dict:
  intro     paragraph shown above the chart
  branches  list of {symptom, steps, end, end_ok}
            step = {q, exit ("no" or "yes": the answer that leaves the path), do}
  note      caveat about control names
  source    the manuals the checks come from
"""
import re

SEND = "Send it in."

_PORTABLE = {
    "intro": "Fujinon's operation manuals for these lenses contain no troubleshooting flowchart, so we built this one from the checks those manuals describe. Pick the symptom, answer each check, and follow the arrow. When a path ends in “Send it in,” stop there.",
    "branches": [
        {"symptom": "Nothing on the lens works",
         "steps": [
             {"q": "Is the lens cable plugged into the camera's lens connector, with the camera switched on?", "exit": "no",
              "do": "Switch the camera off, plug the cable in, then switch on. Fujinon's manuals say to turn the system off before changing any connection."},
             {"q": "Unplug the zoom and focus demands and any other accessory, then try the lens alone. Does it work now?", "exit": "yes",
              "do": "An accessory or its cable is at fault, or the camera cannot power the whole system. Fujinon's manuals warn that the lens system may not work normally if the camera cannot supply enough power. Add the accessories back one at a time to find it."},
             {"q": "Does the lens work on another camera?", "exit": "yes",
              "do": "The fault is in the first camera or its lens connector, not the lens."},
         ],
         "end": SEND},
        {"symptom": "Servo zoom does not move",
         "steps": [
             {"q": "Is the zoom servo/manual select knob set to S?", "exit": "no",
              "do": "Set it to S. At M the zoom only moves by hand."},
             {"q": "Is the limit zoom switch OFF?", "exit": "no",
              "do": "Set it to OFF and try again. With limits on, the servo zoom only moves inside the stored range, and the lens keeps those limits after the power is turned off."},
             {"q": "Is the zoom speed knob turned up?", "exit": "no",
              "do": "Turn it clockwise. It sets the top servo zoom speed, and a low setting makes the zoom slow."},
             {"q": "Does the seesaw lever on the lens grip zoom the lens?", "exit": "yes",
              "do": "The lens drive works. If only the zoom demand fails, the demand, its cable or its settings are at fault. With an analog demand, check the analog zoom demand switch on the drive unit."},
             {"q": "With the knob at M, does the zoom ring turn smoothly by hand through its whole range?", "exit": "no",
              "do": "Stop and do not force it. The fault is mechanical. Send it in."},
         ],
         "end": "The drive unit needs bench service. " + SEND},
        {"symptom": "Zoom stops short of full wide or full tele",
         "steps": [
             {"q": "Is the limit zoom switch OFF?", "exit": "no",
              "do": "Set it to OFF. Stored limits restrict the servo zoom even after the power has been off."},
             {"q": "If you use a zoom demand, is its own zoom limit off?", "exit": "no",
              "do": "Turn it off. Fujinon notes that zoom demands have their own limit function, and with an analog demand both limits are active at once."},
         ],
         "end": SEND},
        {"symptom": "Focus does not respond",
         "steps": [
             {"q": "Is the focus servo/manual select knob in the right position?", "exit": "no",
              "do": "Set S to use a focus demand, or M to focus by hand."},
             {"q": "For servo focus: is a focus demand connected?", "exit": "no",
              "do": "Connect one with the power off. Fujinon's manual says servo focus needs an optional focus demand."},
             {"q": "With the knob at M, does the focus ring turn smoothly by hand?", "exit": "no",
              "do": "Stop and do not force it. Send it in."},
         ],
         "end": "The focus servo needs bench service. " + SEND},
        {"symptom": "Picture goes soft when zooming",
         "steps": [
             {"q": "Is macro off, with the macro ring fully returned?", "exit": "no",
              "do": "Turn the macro ring back until the lever returns to its normal position."},
             {"q": "Adjust the flange focal length (back focus). Set limit zoom OFF, open the iris and aim at a sharp chart about 3 m away. At full wide, loosen the F.f lock knob and set the F.f ring for best focus. At full tele, refocus with the focus ring. Repeat until both ends are sharp, then tighten the lock. Does focus now hold through the zoom?", "exit": "yes",
              "do": "Fixed. Fujinon's manual says to do this adjustment whenever the lens is first mounted or moved to another camera."},
         ],
         "end": "If focus will not hold after the adjustment, the lens needs bench service. " + SEND},
        {"symptom": "Iris does not behave",
         "steps": [
             {"q": "If the iris ignores the camera: is the iris mode switch at A?", "exit": "no",
              "do": "Set it to A. At M the iris only moves by the iris ring, or while the momentary iris button is held. A switch on the drive unit can swap the A and M positions, so check the label."},
             {"q": "Does the iris hunt, opening and closing around the right setting?", "exit": "yes",
              "do": "Iris sensitivity is set too high. Turn the iris sensitivity trimmer counterclockwise to lower it."},
             {"q": "Does the picture only darken when the 2x extender is in?", "exit": "yes",
              "do": "That is the extender, not a fault. With the iris under remote control, the iris compensation switch on the drive unit prevents the darkening."},
         ],
         "end": SEND},
        {"symptom": "Lens misbehaves only when the camera is controlling it",
         "steps": [
             {"q": "Set the camera communication switch on the drive unit to OFF and test again. Is the fault gone?", "exit": "yes",
              "do": "The fault is in the serial link between lens and camera. Fujinon's manual gives this switch for that case. You can keep working with it OFF, and have the lens and camera checked."},
         ],
         "end": SEND},
        {"symptom": "Fog or water",
         "steps": [
             {"q": "Did the lens fog after moving from a cold place to a warm or humid one?", "exit": "yes",
              "do": "Let it come up to room temperature. Fujinon's manual says to let the lens adjust to the surroundings to avoid fogging."},
             {"q": "Did water get into the lens?", "exit": "yes",
              "do": "Shut the power off at once and leave it off. Wipe the lens dry, seal it in a plastic bag with desiccant, and send it in."},
         ],
         "end": "Fog that will not clear needs bench service. " + SEND},
        {"symptom": "Smoke, burning smell or unusual noise",
         "steps": [],
         "end": "Switch the power off at once, take the lens off the camera and do not power it again. " + SEND},
    ],
    "note": "Control names follow Fujinon's manuals for the BERD-S6 and BERD-S10 drive units. On another drive unit a control may be named or placed differently, or not fitted.",
    "source": "Fujinon UA series (BERD-S6, BERD-S10) and HA Premier series (BERD-S6, BERM-M6) Operation Manuals. The flowchart itself is by Tek Media Group.",
}

_BOX = {
    "intro": "Fujinon's operation manuals for these lenses contain no troubleshooting flowchart, so we built this one from the checks those manuals describe. Pick the symptom, answer each check, and follow the arrow. When a path ends in “Send it in,” stop there.",
    "branches": [
        {"symptom": "Lens does not respond at all",
         "steps": [
             {"q": "Have you waited for the power-on initial setting to finish?", "exit": "no",
              "do": "Wait for it. Fujinon's manuals give several seconds for the lens and about ten seconds for the stabilizer. Controls do not work until it finishes, and you should not pan or tilt while the stabilizer sets."},
             {"q": "Is the lens getting power?", "exit": "no",
              "do": "Check the lens connection to the camera with the power off. If the camera cannot supply enough power, use the power connector on the lens. With a lens supporter, Fujinon says power must come from the lens side, or the lens may not operate correctly."},
             {"q": "On lenses with the LCD panel: does the status screen list a servo module and a controller for zoom and focus?", "exit": "no",
              "do": "MT-NO means no servo module is detected. IDLE means no controller is connected. Switch off, then reseat the module or the demand cable."},
         ],
         "end": SEND},
        {"symptom": "Zoom does not respond",
         "steps": [
             {"q": "Is the zoom drive complete? Servo zoom needs a zoom servo module with a zoom rate demand or shot box. Manual zoom needs a manual module with the zoom handle, its flexible cable and the range selector.", "exit": "no",
              "do": "Fit and connect the missing part with the power off. On lenses with the LCD panel, the status screen shows MT-NO for a missing module and IDLE for a missing controller."},
             {"q": "Does the lens zoom with a different zoom demand or cable?", "exit": "yes",
              "do": "The first demand or its cable is at fault."},
         ],
         "end": SEND},
        {"symptom": "Focus does not respond",
         "steps": [
             {"q": "Is the focus drive complete? Servo focus needs a focus servo module with a focus position demand or shot box. Manual focus needs a manual module with the focus grip and its flexible cable.", "exit": "no",
              "do": "Fit and connect the missing part with the power off. On lenses with the LCD panel, the status screen shows MT-NO for a missing module and IDLE for a missing controller."},
             {"q": "Does the lens focus with a different focus demand or cable?", "exit": "yes",
              "do": "The first demand or its cable is at fault."},
         ],
         "end": SEND},
        {"symptom": "Picture goes soft when zooming",
         "steps": [
             {"q": "Is the macro switch OFF, along with the remote macro unit if one is fitted?", "exit": "no",
              "do": "Switch macro off and check again."},
             {"q": "Adjust the flange focal length (back focus). Open the iris and aim at a distant subject (the XA99x8.4BESM manual uses about 7.5 m). Loosen the F.f locking knob. At full wide, focus with the F.f adjusting knob. At full tele, focus with the focus control. Repeat two or three times, then tighten the knob. Does focus now hold through the zoom?", "exit": "yes",
              "do": "Fixed. Fujinon's manual says to do this adjustment whenever the lens is first fitted or moved to another camera."},
         ],
         "end": "If focus will not hold after the adjustment, the lens needs bench service. " + SEND},
        {"symptom": "Iris does not behave",
         "steps": [
             {"q": "Does the iris respond to the camera's iris control?", "exit": "no",
              "do": "The lens takes its iris from the camera's control signal, or from an iris control unit connected to the lens. Check the camera's iris setting and any iris control unit first. If both are right, send it in."},
             {"q": "Does the iris hunt in auto, opening and closing around the right setting?", "exit": "yes",
              "do": "Fujinon's manual gives an iris gain adjustment for this, inside the lens under the shroud. We can set it on the bench."},
         ],
         "end": SEND},
        {"symptom": "2x extender will not switch",
         "steps": [
             {"q": "Is the extender remote/manual switch set for the control you are using?", "exit": "no",
              "do": "Set MANU to use the knob on the lens. Set REMO to use the extender switch on the range selector or other accessory."},
         ],
         "end": SEND},
        {"symptom": "Stabilizer does not steady the picture",
         "steps": [
             {"q": "Is the stabilizer switched on?", "exit": "no",
              "do": "Set the lens switch to H+V or V. If a stabilizer control unit is connected, its own switch takes priority and the lens switch should be OFF."},
             {"q": "After power-on, did you keep the camera still for about ten seconds?", "exit": "no",
              "do": "Switch off and on again, and do not pan or tilt while the stabilizer runs its initial setting."},
             {"q": "Is the mode right for the shot?", "exit": "no",
              "do": "Fujinon's manual gives HIGH for panning and tilting and STD for static shots."},
         ],
         "end": SEND},
        {"symptom": "Indicator or tally lights stay dark",
         "steps": [
             {"q": "Is the indicator switch ON, and the tally switch at HIGH or LOW?", "exit": "no",
              "do": "Switch them on. The indicator switch turns off the zoom, iris and extender LEDs. The tally switch has HIGH, LOW and OFF."},
         ],
         "end": SEND},
        {"symptom": "Lens misbehaves under camera control, or the camera shows no lens data",
         "steps": [
             {"q": "Is the lens's camera serial communication setting right for the camera?", "exit": "no",
              "do": "Fujinon's manual says to turn camera communication OFF when the camera has no serial communication. On lenses with the LCD panel this is the CAMERA-SER menu item. On others it is a switch inside the lens."},
         ],
         "end": SEND},
        {"symptom": "Fog or water",
         "steps": [
             {"q": "Is the lens fogging inside in humid conditions?", "exit": "yes",
              "do": "Fujinon field lenses hold desiccant bags inside, and the manual says to replace them about twice a year in humid areas. We can replace them."},
             {"q": "Did water get into the lens?", "exit": "yes",
              "do": "Shut the power off and leave it off. Wipe the outside, seal the lens in a plastic bag with fresh drying agent for at least three hours, then send it in."},
         ],
         "end": "Fog that will not clear needs bench service. " + SEND},
        {"symptom": "Smoke, burning smell or unusual noise",
         "steps": [],
         "end": "Shut off the power to the lens at once, pull the lens cable and do not power it again. " + SEND},
    ],
    "note": "Control names follow Fujinon's manuals for the XA99x8.4BESM, XA55x9.5BESM and UA107x8.4BESM. Your lens may not have every control listed, such as the stabilizer or the LCD panel.",
    "source": "Fujinon XA99x8.4BESM, XA55x9.5BESM and UA107x8.4BESM Operation Manuals; Fujinon box lens LCD Panel User Manual. The flowchart itself is by Tek Media Group.",
}


def lens_flow(brand_slug, model):
    """Return the troubleshooting flowchart for one lens model, or None."""
    if brand_slug != "fujinon":
        return None
    name = model["name"]
    if re.search(r"BESM|BES\b", name):
        return _BOX
    if re.search(r"BERD|BERM", name):
        return _PORTABLE
    return None


def flow_text(flow):
    """Plain text of a flowchart, for the site search index."""
    if not flow:
        return ""
    bits = ["troubleshooting flowchart"]
    for br in flow["branches"]:
        bits.append(br["symptom"])
        for st in br["steps"]:
            bits.extend([st["q"], st["do"]])
        bits.append(br["end"])
    return " ".join(bits)
