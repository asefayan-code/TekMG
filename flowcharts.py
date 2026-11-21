"""Troubleshooting flowcharts for lenses.

These flowcharts are Tek Media Group's own. The Fujinon and Canon operation manuals
contain no troubleshooting flowchart, so each check in those charts is either a control
or caution described in the manuals, or a plain swap test to isolate the fault.
The chart for other brands is a general checklist and says so on the page.

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


_CANON_INTRO = "Canon's operation manuals for these lenses contain no troubleshooting flowchart, so we built this one from the checks those manuals describe. Pick the symptom, answer each check, and follow the arrow. When a path ends in “Send it in,” stop there."

_CANON_BOX = {
    "intro": _CANON_INTRO,
    "branches": [
        {"symptom": "Lens does not respond at all",
         "steps": [
             {"q": "Is the power low LED on the indicator panel dark?", "exit": "no",
              "do": "A red power low LED means the supply is 10 V or less. Raise it to 10.5 V or above. On a portable camera running servo zoom or focus, Canon's manual says to feed 12 V DC (10 to 17 V) into the external power jack on the lens, because the camera cannot supply enough."},
             {"q": "Has the lens finished initializing?", "exit": "no",
              "do": "Wait for it. Canon's manual says lens operation is disabled during initialization. If the display shows “Initialize Error!”, follow path 2."},
             {"q": "On lenses with the heater option: is the heater switched OFF?", "exit": "no",
              "do": "Switch it off. Canon's manual says the heater uses so much power that servo zoom and servo focus are disabled while it is on."},
         ],
         "end": SEND},
        {"symptom": "“Initialize Error!” on the information display",
         "steps": [
             {"q": "Is the servo module mounted correctly, with nothing locking or blocking the lens?", "exit": "no",
              "do": "Switch off, reseat the servo module or free the lens, then switch on. Canon's manual gives these as the causes of the message."},
             {"q": "Switch the power off and on. Has the message cleared?", "exit": "yes",
              "do": "Fixed. Canon's manual gives this as the remedy once the cause is cleared."},
         ],
         "end": SEND},
        {"symptom": "Zoom or focus does not respond",
         "steps": [
             {"q": "Is the control system complete? Full servo needs a servo module, a zoom servo demand, a focus servo demand and the demand cables. Manual control needs the flexible module, the flexible zoom and focus control units and the flexible cables.", "exit": "no",
              "do": "Fit and connect the missing part with the power off."},
             {"q": "On lenses with the heater option: is the heater switched OFF?", "exit": "no",
              "do": "Switch it off. The heater disables servo zoom and servo focus while it is on."},
             {"q": "Does the lens respond with a different demand or cable?", "exit": "yes",
              "do": "The first demand or its cable is at fault."},
         ],
         "end": SEND},
        {"symptom": "Zoom or focus position reads wrong on the camera or the display",
         "steps": [
             {"q": "Run the zoom and focus slowly through the middle of their travel, then check again. Is the reading right now?", "exit": "yes",
              "do": "Normal with initialization set to OFF, the factory setting. The lens starts at a temporary position and corrects itself when it passes a point near the middle of its travel. To have it detect its position at power-up, set initialization to ON in the information display, then switch off and on."},
         ],
         "end": "Canon's manual says a failed position detection leaves the position signal wrong. " + SEND},
        {"symptom": "Picture goes soft when zooming",
         "steps": [
             {"q": "Adjust the back focus. Aim at a high-contrast object at the distance Canon gives for the lens (10 to 15 m for most models in its UHD-DIGISUPER manual, 3 to 5 m for the UJ27x6.5B). Set 1x and open the iris fully. At full tele, focus. At full wide, loosen the F.B. lock knob and turn the F.B. adjusting knob until sharp. Repeat until both ends are sharp, then tighten the lock knob. Does focus now hold through the zoom?", "exit": "yes",
              "do": "Fixed. If the camera and lens support Remote Back Focus, it can also be adjusted from the camera."},
         ],
         "end": "If focus will not hold after the adjustment, the lens needs bench service. " + SEND},
        {"symptom": "Iris does not behave",
         "steps": [
             {"q": "If the iris ignores the camera: is the iris control select switch (DIP switch SW2, No. 4, under the lens shroud) at OFF, the I.CAMERA position?", "exit": "no",
              "do": "Set it to OFF so the camera controls the iris. ON, the I.LOCAL position, hands the iris to a switch box. Canon's manual gives this check for an iris that is not responding. On the UJ122x8.2B AF the shroud does not come off, so leave this to service."},
             {"q": "Does the iris hunt in auto, opening and closing around the right setting?", "exit": "yes",
              "do": "Iris gain is set too high. Lower it with the iris gain trimmer or the I-Gain setting in the information display until the hunting stops."},
         ],
         "end": SEND},
        {"symptom": "Extender will not switch",
         "steps": [
             {"q": "Does the extender manual control knob on the lens change the extender?", "exit": "yes",
              "do": "The extender itself works, so the fault is in the remote control: the zoom demand, the switch box or the camera. Canon's manual gives the knob for use when remote control fails. With two remote devices fitted, the extender follows the last one operated."},
         ],
         "end": SEND},
        {"symptom": "Autofocus does not hold focus", "needs": "af",
         "steps": [
             {"q": "Is an AF demand connected?", "exit": "no",
              "do": "Connect one. Canon's manual says AF needs an AF demand."},
             {"q": "Is the subject hard for AF: low contrast, fast moving, or a dark scene?", "exit": "yes",
              "do": "Canon's manual lists these as conditions where AF may struggle. Focus by demand for that shot."},
             {"q": "Is the back focus correct?", "exit": "no",
              "do": "Adjust it (path 5). Canon notes that back focus shifts slightly with temperature and should be checked for best AF performance."},
         ],
         "end": SEND},
        {"symptom": "Image stabilizer does not behave (IS models)",
         "steps": [
             {"q": "Is IS switched on?", "exit": "no",
              "do": "Press the IS operation switch and check the IS indicator LED. The direction selector switches must not be at OFF."},
             {"q": "Does the picture only look unnatural on fast pans or tilts?", "exit": "yes",
              "do": "Select STD. Canon's manual says fast moves are read as vibration and corrected, and STD keeps that to a minimum."},
             {"q": "Was the lens only just switched on?", "exit": "yes",
              "do": "Give it time. Canon's manual says IS may not perform fully during warm-up."},
         ],
         "end": SEND},
        {"symptom": "Fog inside the lens",
         "steps": [
             {"q": "Is the lens fitted with the heater option?", "exit": "yes",
              "do": "Switch the heater on to clear the clouding. Servo zoom and servo focus are disabled while it is on, so switch it off again before shooting with servo control."},
         ],
         "end": "Fog that keeps coming back needs bench service. " + SEND},
        {"symptom": "Smoke, burning smell or unusual noise",
         "steps": [],
         "end": "Switch off at once, disconnect the lens from the camera and do not power it again. " + SEND},
    ],
    "note": "Control names follow Canon's operation manual for the UHD-DIGISUPER and DIGISUPER lenses UJ122x8.2B to XJ80x8.8B. Your lens may not have every item listed, such as the image stabilizer, the heater or the information display.",
    "source": "Canon UHD-DIGISUPER and DIGISUPER Operation Manual “Lens” (UJ122x8.2B AF, UJ122x8.2B, UJ111x8.3B, UJ90x9B, UJ86x9.3B, UJ66x9B, UJ27x6.5B, XJ95x12.4B, XJ95x8.6B, XJ80x8.8B). The flowchart itself is by Tek Media Group.",
}

_CANON_PORTABLE = {
    "intro": _CANON_INTRO,
    "branches": [
        {"symptom": "Nothing on the lens works",
         "steps": [
             {"q": "Is the lens cable plugged into the camera's lens connector, with the camera switched on?", "exit": "no",
              "do": "Switch the camera off, plug the cable in, then switch on."},
             {"q": "Is the supply inside 10 to 17 V DC?", "exit": "no",
              "do": "Correct it. Canon's manual rates the lens at 12 V DC with a working range of 10 to 17 V, and warns that voltage outside the range, or reversed polarity, may damage the drive unit."},
             {"q": "Did the lens just come from a cold place into warm, humid air?", "exit": "yes",
              "do": "Let it warm up and dry out. Canon's manual says condensation from a sudden temperature change can stop the lens working for a time."},
             {"q": "Does the lens work on another camera?", "exit": "yes",
              "do": "The fault is in the first camera or its lens connector, not the lens."},
         ],
         "end": SEND},
        {"symptom": "“Initialize Error” on the drive unit display", "needs": "display",
         "steps": [
             {"q": "Switch the camera off, make sure nothing is holding the zoom, focus or iris, then switch on. Has the message cleared?", "exit": "yes",
              "do": "Fixed. In Canon's box lens manuals the same message is traced to a servo unit that is not mounted correctly or a lens that is forcibly locked."},
         ],
         "end": SEND},
        {"symptom": "Servo zoom does not move",
         "steps": [
             {"q": "Is the zoom operation change-over knob at SERVO?", "exit": "no",
              "do": "Set it to SERVO. At MANU the zoom only moves by hand. Canon's manual warns not to force the zoom by hand while the knob is at SERVO."},
             {"q": "Is the max. zoom speed control turned up?", "exit": "no",
              "do": "Turn it up. It sets the top speed of the zoom rocker."},
             {"q": "Does the rocker on the lens grip zoom the lens?", "exit": "yes",
              "do": "The lens drive works. If only the zoom demand fails, the demand or its cable is at fault."},
             {"q": "With the knob at MANU, does the zoom ring turn smoothly by hand through its whole range?", "exit": "no",
              "do": "Stop and do not force it. The fault is mechanical. Send it in."},
         ],
         "end": "The drive unit needs bench service. " + SEND},
        {"symptom": "Focus does not respond",
         "steps": [
             {"q": "Is the focus operation knob in the right position?", "exit": "no",
              "do": "Set SERVO to use a focus demand, or MANU to focus by hand. Canon's manual describes this knob on the IASE S, IASE-C S and KASE S drive units."},
             {"q": "For servo focus: is a focus demand attached?", "exit": "no",
              "do": "Attach one with the power off. Servo focus needs a focus demand."},
             {"q": "With the knob at MANU, does the focus ring turn smoothly by hand?", "exit": "no",
              "do": "Stop and do not force it. Send it in."},
         ],
         "end": "The focus servo needs bench service. " + SEND},
        {"symptom": "Picture goes soft when zooming",
         "steps": [
             {"q": "Adjust the back focus. Set the extender to 1x and open the iris fully. Use a high-contrast object about 2 to 5 m away (Canon gives 1 to 3 m for the CJ15ex and CJ14ex, and 5 to 7 m for the CJ18ex28B). At full tele, focus with the focus ring. At full wide, loosen the flange back lock screw and turn the flange back adjusting ring until sharp. Repeat until both ends are sharp, then tighten the screw. Does focus now hold through the zoom?", "exit": "yes",
              "do": "Fixed. Redo this adjustment whenever the lens moves to another camera."},
         ],
         "end": "If focus will not hold after the adjustment, the lens needs bench service. " + SEND},
        {"symptom": "Iris does not behave",
         "steps": [
             {"q": "If the iris ignores the camera: is the iris switch at A?", "exit": "no",
              "do": "Set it to A. At M the iris only moves by the iris ring, or while the instant auto-iris switch is held."},
             {"q": "Does the iris hunt in auto, opening and closing around the right setting?", "exit": "yes",
              "do": "Iris gain is set too high. Turn the iris gain trimmer counterclockwise until the hunting stops."},
             {"q": "Does the picture only darken when the 2x extender is in?", "exit": "yes",
              "do": "That is the extender, not a fault. Canon's manual says the light drops with the extender in use, depending on the iris correction setting."},
         ],
         "end": SEND},
        {"symptom": "Information display is blank", "needs": "display",
         "steps": [
             {"q": "Press the DISPLAY switch. Does the display come on?", "exit": "yes",
              "do": "Normal. Canon's manual says the display turns itself off after 2 minutes."},
         ],
         "end": SEND},
        {"symptom": "Fog or water",
         "steps": [
             {"q": "Did the lens fog after moving from a cold place to a warm or humid one?", "exit": "yes",
              "do": "Let it come up to room temperature and dry out before use."},
             {"q": "Did water get into the lens?", "exit": "yes",
              "do": "Stop using it at once. Canon's manual says the lens is not waterproof. Wipe it dry, seal it in a bag with desiccant and send it in."},
         ],
         "end": "Fog that will not clear needs bench service. " + SEND},
        {"symptom": "Dropped or knocked",
         "steps": [],
         "end": "Canon's manual warns that striking or dropping the lens may cause a malfunction. Damage inside may not show on the outside. " + SEND},
        {"symptom": "Smoke, burning smell or unusual noise",
         "steps": [],
         "end": "Take the lens off the camera at once and do not power it again. " + SEND},
    ],
    "note": "Control names follow Canon's operation manual for CJ and KJ portable lenses with IASE S, IRSE S and KASE S drive units. On another drive unit a control may be named or placed differently, or not fitted.",
    "source": "Canon Operation Manual “Lens” for CJ and KJ portable lenses with IASE S, IRSE S and KASE S drive units. The flowchart itself is by Tek Media Group.",
}

# Brands in the "Other Brand Studio Lens Repair" selector on /lens-repair
OTHER_BRANDS = [
    {"name": "Sony", "slug": "sony"},
    {"name": "Panasonic", "slug": "panasonic"},
    {"name": "Zeiss", "slug": "zeiss"},
    {"name": "Cooke Optics", "slug": "cooke"},
    {"name": "ARRI", "slug": "arri"},
    {"name": "Angénieux", "slug": "angenieux"},
    {"name": "Leitz", "slug": "leitz"},
    {"name": "Sigma", "slug": "sigma"},
    {"name": "Panavision", "slug": "panavision"},
    {"name": "Atlas Lens Co.", "slug": "atlas"},
    {"name": "Laowa", "slug": "laowa"},
    {"name": "IRIX", "slug": "irix"},
]
OTHER_BY_SLUG = {b["slug"]: b for b in OTHER_BRANDS}

_GENERAL_BRANCHES = [
    {"symptom": "Focus marks are off, or the lens will not reach infinity",
     "steps": [
         {"q": "Is the lens fully seated and locked in the mount, with any adapter tight?", "exit": "no",
          "do": "Reseat and lock it. A loose mount or adapter shifts the focus."},
         {"q": "Is the fault the same on a second camera body?", "exit": "no",
          "do": "The first camera's flange depth or its adapter is out, not the lens."},
     ],
     "end": "The lens needs its back focus reset on the bench. " + SEND},
    {"symptom": "Zoom lens goes soft when zooming",
     "steps": [
         {"q": "If the lens has a back focus adjustment: has it been set for this camera?", "exit": "no",
          "do": "Set it as the lens manual describes. The usual method is to focus at full tele, adjust the back focus at full wide, and repeat until both ends are sharp."},
     ],
     "end": "If focus will not hold through the zoom, the lens needs bench service. " + SEND},
    {"symptom": "Focus, zoom or iris ring is stiff, gritty, loose or stuck",
     "steps": [
         {"q": "Take off the follow focus, lens motors and lens supports. Does the ring turn freely by hand now?", "exit": "yes",
          "do": "The accessory was binding the ring. Refit it so it does not load the lens."},
         {"q": "Was the lens dropped, or used in sand, salt spray or rain?", "exit": "yes",
          "do": "Stop turning the ring. Grit and impact damage get worse with use. Send it in."},
     ],
     "end": "Do not force a ring. " + SEND},
    {"symptom": "Iris blades are slow, sticking or oily",
     "steps": [],
     "end": "A sticking iris or oil on the blades needs the lens opened on the bench. Do not work the ring to free it. " + SEND},
    {"symptom": "Haze, fog, spots or fungus in the picture",
     "steps": [
         {"q": "Is the mark on the front or rear glass surface?", "exit": "yes",
          "do": "Blow or brush the dust off first. Then wipe gently from the center outward with lens tissue and lens cleaning fluid."},
         {"q": "Did the lens just come from a cold place into warm, humid air?", "exit": "yes",
          "do": "Let it reach room temperature. Condensation clears on its own."},
     ],
     "end": "Haze, fungus or dust inside the glass needs bench cleaning. " + SEND},
    {"symptom": "Picture is soft on one side, or the image shifts when focusing",
     "steps": [
         {"q": "Is the lens seated square in the mount, with no support or matte box pushing on it?", "exit": "no",
          "do": "Reseat the lens and reset the supports so nothing loads it."},
     ],
     "end": "The lens needs to be checked and aligned on the bench. " + SEND},
    {"symptom": "Camera shows no lens data, or electronic control fails",
     "steps": [
         {"q": "Are the contacts on the lens and the camera mount clean, with the lens locked fully home?", "exit": "no",
          "do": "Wipe the contacts with a dry, lint-free cloth and reseat the lens."},
         {"q": "Does the camera support this lens's data system, and is it set up for it?", "exit": "no",
          "do": "Set it up as the camera manual describes. Lens data systems such as Cooke /i, ARRI LDS and ZEISS eXtended Data only work with a camera that supports them."},
         {"q": "Does the lens report data on a second camera?", "exit": "yes",
          "do": "The first camera or its mount is at fault, not the lens."},
     ],
     "end": SEND},
    {"symptom": "Servo zoom or autofocus does not work",
     "steps": [
         {"q": "Is the lens getting power from the camera, with its cable or mount contacts connected?", "exit": "no",
          "do": "Connect it with the camera switched off, then switch on."},
         {"q": "Are the servo/manual and auto/manual switches on the lens set for servo or auto operation?", "exit": "no",
          "do": "Set them and try again."},
         {"q": "With the lens set to manual, does the ring turn smoothly by hand?", "exit": "no",
          "do": "Stop and do not force it. Send it in."},
     ],
     "end": SEND},
    {"symptom": "Dropped, or exposed to water, sand or salt",
     "steps": [],
     "end": "Do not power the lens and do not work the rings. A dropped lens can have internal damage with no visible marks, and salt, sand and moisture damage gets worse over time. " + SEND},
]


def brand_flow(brand_name):
    """General studio and cinema lens flowchart for a brand without model pages."""
    return {
        "intro": "This flowchart is Tek Media Group's general checklist for studio and cinema lenses. It is not taken from " + brand_name + " documentation, so follow the manual for your lens where it differs. Pick the symptom, answer each check, and follow the arrow. When a path ends in “Send it in,” stop there.",
        "branches": _GENERAL_BRANCHES,
        "note": "Not every path applies to every lens. A manual prime has no servo or autofocus, for example.",
        "source": "Tek Media Group general lens checklist. Not from " + brand_name + " documentation.",
    }


def _without(flow, *tags):
    """Copy of a flowchart without the branches that need a feature the lens lacks."""
    out = dict(flow)
    out["branches"] = [b for b in flow["branches"] if b.get("needs") not in tags]
    return out


def lens_flow(brand_slug, model):
    """Return the troubleshooting flowchart for one lens model, or None."""
    name = model["name"]
    if brand_slug == "fujinon":
        if re.search(r"BESM|BES\b", name):
            return _BOX
        if re.search(r"BERD|BERM", name):
            return _PORTABLE
        return None
    if brand_slug == "canon":
        if re.search(r"DIGISUPER|\b[XU]J\d", name):
            # the autofocus path only on AF models
            return _CANON_BOX if re.search(r"AF\b", name) else _without(_CANON_BOX, "af")
        if re.search(r"IASE|KASE|HJ40ex", name):
            return _CANON_PORTABLE
        return _without(_CANON_PORTABLE, "display")
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
