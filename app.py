import datetime
import os

from lensdata import BRANDS, CANON_MODELS, FUJINON_MODELS
from monitordata import PROBLEMS, SERVICES, SONY_BY_SLUG, SONY_MONITORS
from modelinfo import LENS_FACTS, LENS_FACTS_SOURCE, lens_info, monitor_info
from cameradata import (CAMERA_BRANDS, CAMERA_BRAND_NAMES, CAMERA_MODEL_COUNT, DECK_BRANDS,
                        DECK_BRAND_NAMES, DECK_MODEL_COUNT)
from flowcharts import OTHER_BRANDS, OTHER_BY_SLUG, brand_flow, lens_flow
from sitesearch import search as site_search
import ticketlookup
from flask import Flask, Response, abort, jsonify, redirect, render_template, request, send_from_directory

BASE = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(BASE, "public")

app = Flask(__name__, static_folder=None)


@app.context_processor
def inject_year():
    return {"year": datetime.date.today().year}


@app.context_processor
def inject_lens_models():
    return {"fujinon_models": FUJINON_MODELS, "canon_models": CANON_MODELS, "sony_monitors": SONY_MONITORS, "other_brands": OTHER_BRANDS}


@app.context_processor
def inject_camera_models():
    return {"camera_brands": CAMERA_BRANDS, "deck_brands": DECK_BRANDS,
            "camera_brand_names": CAMERA_BRAND_NAMES, "deck_brand_names": DECK_BRAND_NAMES,
            "camera_model_count": CAMERA_MODEL_COUNT, "deck_model_count": DECK_MODEL_COUNT}


@app.route("/lens-repair/<brand>")
def lens_brand_hub(brand):
    key = brand.lower()
    b = BRANDS.get(key)
    if not b:
        ob = OTHER_BY_SLUG.get(key)
        if not ob:
            abort(404)
        if brand != ob["slug"]:
            return redirect("/lens-repair/" + ob["slug"], code=301)
        # brand without model pages: one page with the general flowchart
        return render_template("lens-brand.html", ob=ob, flow=brand_flow(ob["name"]))
    if brand != b["slug"]:
        return redirect("/lens-repair/" + b["slug"], code=301)
    return render_template("lens-hub.html", b=b)


@app.route("/lens-repair/<brand>/<slug>")
def lens_model(brand, slug):
    b = BRANDS.get(brand.lower())
    if not b:
        abort(404)
    key = slug.lower()
    model = b["by_slug"].get(key)
    if not model:
        abort(404)
    if brand != b["slug"] or key != slug:
        return redirect("/lens-repair/" + b["slug"] + "/" + key, code=301)
    models = b["models"]
    i = models.index(model)
    prev_m = models[i - 1] if i > 0 else None
    next_m = models[i + 1] if i + 1 < len(models) else None
    return render_template(
        "lens-model.html", b=b, m=model, prev_m=prev_m, next_m=next_m,
        info=lens_info(b["slug"], model), facts=LENS_FACTS.get(model["slug"]), facts_source=LENS_FACTS_SOURCE,
        flow=lens_flow(b["slug"], model),
    )


@app.route("/monitor-repair/<slug>")
def monitor_model(slug):
    key = slug.lower()
    model = SONY_BY_SLUG.get(key)
    if not model:
        abort(404)
    if key != slug:
        return redirect("/monitor-repair/" + key, code=301)
    i = SONY_MONITORS.index(model)
    prev_m = SONY_MONITORS[i - 1] if i > 0 else None
    next_m = SONY_MONITORS[i + 1] if i + 1 < len(SONY_MONITORS) else None
    return render_template(
        "monitor-model.html", m=model, prev_m=prev_m, next_m=next_m,
        problems=PROBLEMS[model["kind"]], services=SERVICES[model["kind"]],
        info=monitor_info(model["slug"]),
    )


# Clean URL -> template in /templates
PAGES = {
    "": "home.html",
    "home": "home.html",
    "about": "about.html",
    "terms": "terms.html",
    "how-to": "how-to.html",
    "capacitor-replacement": "capacitor-replacement.html",
    "privacy": "privacy.html",
    "contact": "contact.html",
    "accessibility": "accessibility.html",
    "lens-repair": "lens-repair.html",
    "camera-repair": "camera-repair.html",
    "projector-repair": "projector-repair.html",
    "monitor-repair": "monitor-repair.html",
    "reel-to-reel": "reel-to-reel.html",
    "reel-to-reel/studer": "reel-to-reel-studer.html",
    "reel-to-reel/aiwa": "reel-to-reel-aiwa.html",
    "reel-to-reel/akai": "reel-to-reel-akai.html",
    "reel-to-reel/akai/akai-gx-747": "reel-to-reel-akai-gx-747.html",
    "reel-to-reel/akai/akai-gx-635d": "reel-to-reel-akai-gx-635d.html",
    "reel-to-reel/akai/akai-gx-4000d": "reel-to-reel-akai-gx-4000d.html",
    "reel-to-reel/nakamichi": "reel-to-reel-nakamichi.html",
    "reel-to-reel/revox": "reel-to-reel-revox.html",
    "reel-to-reel/revox/revox-a700": "reel-to-reel-revox-revox-a700.html",
    "reel-to-reel/revox/revox-b77": "reel-to-reel-revox-revox-b77.html",
    "reel-to-reel/revox/revox-a77": "reel-to-reel-revox-revox-a77.html",
    "reel-to-reel/revox/revox-pr99": "reel-to-reel-revox-revox-pr99.html",
    "reel-to-reel/revox/revox-pr77": "reel-to-reel-revox-revox-pr77.html",
    "reel-to-reel/revox/revox-c270": "reel-to-reel-revox-revox-c270.html",
    "reel-to-reel/revox/revox-g36": "reel-to-reel-revox-revox-g36.html",
    "reel-to-reel/revox/revox-f36": "reel-to-reel-revox-revox-f36.html",
    "reel-to-reel/revox/revox-b710": "reel-to-reel-revox-revox-b710.html",
    "reel-to-reel/revox/revox-b760": "reel-to-reel-revox-revox-b760.html",
    "reel-to-reel/revox/revox-b225": "reel-to-reel-revox-revox-b225.html",
    "reel-to-reel/revox/revox-b226": "reel-to-reel-revox-revox-b226.html",
    "reel-to-reel/pioneer": "reel-to-reel-pioneer.html",
    "reel-to-reel/pioneer/pioneer-rt-701": "reel-to-reel-pioneer-pioneer-rt-701.html",
    "reel-to-reel/pioneer/pioneer-rt-707": "reel-to-reel-pioneer-pioneer-rt-707.html",
    "reel-to-reel/pioneer/pioneer-rt-909": "reel-to-reel-pioneer-pioneer-rt-909.html",
    "reel-to-reel/pioneer/pioneer-rt-1011": "reel-to-reel-pioneer-pioneer-rt-1011.html",
    "reel-to-reel/pioneer/pioneer-rt-1020": "reel-to-reel-pioneer-pioneer-rt-1020.html",
    "reel-to-reel/pioneer/pioneer-rt-1050": "reel-to-reel-pioneer-pioneer-rt-1050.html",
    "reel-to-reel/pioneer/pioneer-rt-2022": "reel-to-reel-pioneer-pioneer-rt-2022.html",
    "reel-to-reel/pioneer/pioneer-rt-2024": "reel-to-reel-pioneer-pioneer-rt-2024.html",
    "reel-to-reel/pioneer/pioneer-rt-761": "reel-to-reel-pioneer-pioneer-rt-761.html",
    "reel-to-reel/teac": "reel-to-reel-teac.html",
    "reel-to-reel/teac/teac-td-102": "reel-to-reel-teac-teac-td-102.html",
    "reel-to-reel/teac/teac-a-3300sx": "reel-to-reel-teac-teac-a-3300sx.html",
    "reel-to-reel/teac/teac-a-3440": "reel-to-reel-teac-teac-a-3440.html",
    "reel-to-reel/teac/teac-a-1250": "reel-to-reel-teac-teac-a-1250.html",
    "reel-to-reel/teac/teac-a-4010sl": "reel-to-reel-teac-teac-a-4010sl.html",
    "reel-to-reel/teac/teac-a-7300": "reel-to-reel-teac-teac-a-7300.html",
    "reel-to-reel/teac/teac-x-1000r": "reel-to-reel-teac-teac-x-1000r.html",
    "reel-to-reel/teac/teac-x-2000": "reel-to-reel-teac-teac-x-2000.html",
    "reel-to-reel/tascam": "reel-to-reel-tascam.html",
    "reel-to-reel/tascam/tascam-58": "reel-to-reel-tascam-tascam-58.html",
    "reel-to-reel/tascam/tascam-34": "reel-to-reel-tascam-tascam-34.html",
    "reel-to-reel/tascam/tascam-80-8": "reel-to-reel-tascam-tascam-80-8.html",
    "reel-to-reel/tascam/tascam-38": "reel-to-reel-tascam-tascam-38.html",
    "reel-to-reel/tascam/tascam-atr-60": "reel-to-reel-tascam-tascam-atr-60.html",
    "reel-to-reel/tascam/tascam-86": "reel-to-reel-tascam-tascam-86.html",
    "reel-to-reel/sony": "reel-to-reel-sony.html",
    "reel-to-reel/sony/sony-tc-880-2": "reel-to-reel-sony-sony-tc-880-2.html",
    "reel-to-reel/sony/sony-tc-788-4": "reel-to-reel-sony-sony-tc-788-4.html",
    "reel-to-reel/studer/studer-a62": "reel-to-reel-studer-studer-a62.html",
    "reel-to-reel/studer/studer-a67": "reel-to-reel-studer-studer-a67.html",
    "reel-to-reel/studer/studer-a80": "reel-to-reel-studer-studer-a80.html",
    "reel-to-reel/studer/studer-a721": "reel-to-reel-studer-studer-a721.html",
    "reel-to-reel/studer/studer-a807": "reel-to-reel-studer-studer-a807.html",
    "reel-to-reel/studer/studer-a810": "reel-to-reel-studer-studer-a810.html",
    "reel-to-reel/studer/studer-a812": "reel-to-reel-studer-studer-a812.html",
    "reel-to-reel/studer/studer-a816": "reel-to-reel-studer-studer-a816.html",
    "reel-to-reel/studer/studer-a820": "reel-to-reel-studer-studer-a820.html",
    "reel-to-reel/studer/studer-a827": "reel-to-reel-studer-studer-a827.html",
    "reel-to-reel/studer/studer-c37": "reel-to-reel-studer-studer-c37.html",
    "reel-to-reel/studer/studer-j37": "reel-to-reel-studer-studer-j37.html",
    "reel-to-reel/technics": "reel-to-reel-technics.html",
    "reel-to-reel/wilcox-gay": "reel-to-reel-wilcox-gay.html",
    "reel-to-reel/nagra": "reel-to-reel-nagra.html",
    "reel-to-reel/nagra/nagra-nta-2s": "reel-to-reel-nagra-nta-2s.html",
    "reel-to-reel/nagra/nagra-nta-3tcr": "reel-to-reel-nagra-nta-3tcr.html",
    "reel-to-reel/nagra/nagra-nta-2b": "reel-to-reel-nagra-nta-2b.html",
    "reel-to-reel/nagra/nagra-nts-3tcs": "reel-to-reel-nagra-nts-3tcs.html",
    "reel-to-reel/nagra/nagra-nta-2m": "reel-to-reel-nagra-nta-2m.html",
    "reel-to-reel/nagra/nagra-nta-3tcn": "reel-to-reel-nagra-nta-3tcn.html",
    "hifi-audio": "hifi-audio.html",
    "site-index": "site-index.html",
    "bang-olufsen": "bang-olufsen.html",
    "bang-olufsen/turntable-shop": "bang-olufsen-turntable-shop.html",
    "bang-olufsen/beovision-tv": "bang-olufsen-beovision-tv.html",
    "bang-olufsen/beosound-beocenter": "bang-olufsen-beosound-beocenter.html",
    "bang-olufsen/beosound-9000": "bang-olufsen-beosound-9000.html",
    "bang-olufsen/beolab-beovox": "bang-olufsen-beolab-beovox.html",
    "bang-olufsen/beolab-5": "bang-olufsen-beolab-5.html",
}

# Old tekmg.com addresses -> new pages (permanent redirect)
REDIRECTS = {
    "home.html": "/",
    "terms.aspx": "/terms",
    "capacitor-replacement.aspx": "/capacitor-replacement",
    "audio-models/capacitor-replacement.aspx": "/capacitor-replacement",
    "howto.aspx": "/how-to",
    "privacy-policy.aspx": "/privacy",
    "privacypolicy.aspx": "/privacy",
    "privacy.aspx": "/privacy",
    "aboutus.aspx": "/about",
    "aboutus.aspx.html": "/about",
    "contact.aspx": "/contact",
    "contact.html": "/contact",
    "contact.aspx.html": "/contact",
    "lensrepair/lens.aspx": "/lens-repair",
    "projectorrepair/projector_repair.aspx": "/projector-repair",
    "projector_repairs.aspx": "/projector-repair",
    "camcorder-camera-and-deck-repair": "/camera-repair",
    "camcorder-camera-and-deck-repair.aspx": "/camera-repair",
    "camcorder-camera-and-deck-repair.aspx.html": "/camera-repair",
    "bang_and_olufsen/band_and_olufsen_service.aspx": "/bang-olufsen",
    "bang_and_olufsen/bang_and_olufsen_service.aspx": "/bang-olufsen",
    "bang-and-olufsen": "/bang-olufsen",
    "sitemap": "/site-index",
    "reel-to-reel-models/studer/studer.aspx": "/reel-to-reel/studer",
    "reel-to-reel-models/aiwa/aiwa.aspx": "/reel-to-reel/aiwa",
    "reel-to-reel-models/ikai/akai.aspx": "/reel-to-reel/akai",
    "reel-to-reel-models/ikai/akai-akai gx-747.aspx": "/reel-to-reel/akai/akai-gx-747",
    "reel-to-reel-models/ikai/akai-akai_gx-747.aspx": "/reel-to-reel/akai/akai-gx-747",
    "reel-to-reel-models/ikai/akai gx-635d.aspx": "/reel-to-reel/akai/akai-gx-635d",
    "reel-to-reel-models/ikai/akai_gx-635d.aspx": "/reel-to-reel/akai/akai-gx-635d",
    "reel-to-reel-models/ikai/akai-gx-4000.aspx": "/reel-to-reel/akai/akai-gx-4000d",
    "reel-to-reel-models/nakamichi/nakamichi.aspx": "/reel-to-reel/nakamichi",
    "reel-to-reel-models/revox/revox-pages.aspx": "/reel-to-reel/revox",
    "reel-to-reel-models/revox/revox-a700.aspx": "/reel-to-reel/revox/revox-a700",
    "reel-to-reel-models/revox/revox-b77.aspx": "/reel-to-reel/revox/revox-b77",
    "reel-to-reel-models/revox/revox-a77.aspx": "/reel-to-reel/revox/revox-a77",
    "reel-to-reel-models/revox/revox-pr99.aspx": "/reel-to-reel/revox/revox-pr99",
    "reel-to-reel-models/revox/revox-pr77.aspx": "/reel-to-reel/revox/revox-pr77",
    "reel-to-reel-models/revox/revox-c270.aspx": "/reel-to-reel/revox/revox-c270",
    "reel-to-reel-models/revox/revox_c270.aspx": "/reel-to-reel/revox/revox-c270",
    "reel-to-reel-models/revox/revox-g36.aspx": "/reel-to-reel/revox/revox-g36",
    "reel-to-reel-models/revox/revox-f36.aspx": "/reel-to-reel/revox/revox-f36",
    "reel-to-reel-models/revox/revox-b710.aspx": "/reel-to-reel/revox/revox-b710",
    "reel-to-reel-models/revox/revox-b760.aspx": "/reel-to-reel/revox/revox-b760",
    "reel-to-reel-models/revox/revox-b225.aspx": "/reel-to-reel/revox/revox-b225",
    "reel-to-reel-models/revox/revox-b226.aspx": "/reel-to-reel/revox/revox-b226",
    "reel-to-reel-models/pioneer/pioneer.aspx": "/reel-to-reel/pioneer",
    "reel-to-reel-models/pioneer/pioneer-rt-701.aspx": "/reel-to-reel/pioneer/pioneer-rt-701",
    "reel-to-reel-models/pioneer/pioneer-707.aspx": "/reel-to-reel/pioneer/pioneer-rt-707",
    "reel-to-reel-models/pioneer/pioneer-rt-707.aspx": "/reel-to-reel/pioneer/pioneer-rt-707",
    "reel-to-reel-models/pioneer/pioneer-rt-909.aspx": "/reel-to-reel/pioneer/pioneer-rt-909",
    "reel-to-reel-models/pioneer/pioneer-rt-1011.aspx": "/reel-to-reel/pioneer/pioneer-rt-1011",
    "reel-to-reel-models/pioneer/pioneer-rt1020.aspx": "/reel-to-reel/pioneer/pioneer-rt-1020",
    "reel-to-reel-models/pioneer/pioneer-rt-1020.aspx": "/reel-to-reel/pioneer/pioneer-rt-1020",
    "reel-to-reel-models/pioneer/pioneer-rt-1050.aspx": "/reel-to-reel/pioneer/pioneer-rt-1050",
    "reel-to-reel-models/pioneer/pioneer rt-2022.aspx": "/reel-to-reel/pioneer/pioneer-rt-2022",
    "reel-to-reel-models/pioneer/pioneer_rt-2022.aspx": "/reel-to-reel/pioneer/pioneer-rt-2022",
    "reel-to-reel-models/pioneer/pioneer-rt-2022.aspx": "/reel-to-reel/pioneer/pioneer-rt-2022",
    "reel-to-reel-models/pioneer/pioneer-rt-2024.aspx": "/reel-to-reel/pioneer/pioneer-rt-2024",
    "reel-to-reel-models/pioneer/pioneer-rt-761.aspx": "/reel-to-reel/pioneer/pioneer-rt-761",
    "reel-to-reel-models/teac/teac.aspx": "/reel-to-reel/teac",
    "reel-to-reel-models/teac/teac-td-102.aspx": "/reel-to-reel/teac/teac-td-102",
    "reel-to-reel-models/teac/teac-a-3300sx.aspx": "/reel-to-reel/teac/teac-a-3300sx",
    "reel-to-reel-models/teac/teac-a-3440.aspx": "/reel-to-reel/teac/teac-a-3440",
    "reel-to-reel-models/teac/teac-a-1250.aspx": "/reel-to-reel/teac/teac-a-1250",
    "reel-to-reel-models/teac/teac-a-4010sl.aspx": "/reel-to-reel/teac/teac-a-4010sl",
    "reel-to-reel-models/teac/teac-a-7300.aspx": "/reel-to-reel/teac/teac-a-7300",
    "reel-to-reel-models/teac/teac-x-1000r.aspx": "/reel-to-reel/teac/teac-x-1000r",
    "reel-to-reel-models/teac/teac-x-2000.aspx": "/reel-to-reel/teac/teac-x-2000",
    "reel-to-reel-models/tascam/tascam.aspx": "/reel-to-reel/tascam",
    "reel-to-reel-models/tascam/tascam-58.aspx": "/reel-to-reel/tascam/tascam-58",
    "reel-to-reel-models/tascam/tascam-34.aspx": "/reel-to-reel/tascam/tascam-34",
    "reel-to-reel-models/tascam/tascam-80-8.aspx": "/reel-to-reel/tascam/tascam-80-8",
    "reel-to-reel-models/tascam/tascam-38.aspx": "/reel-to-reel/tascam/tascam-38",
    "reel-to-reel-models/tascam/tascam-atr-60.aspx": "/reel-to-reel/tascam/tascam-atr-60",
    "reel-to-reel-models/tascam/tascam-86.aspx": "/reel-to-reel/tascam/tascam-86",
    "reel-to-reel-models/sony/sony.aspx": "/reel-to-reel/sony",
    "reel-to-reel-models/sony/sony-tc-880-2.aspx": "/reel-to-reel/sony/sony-tc-880-2",
    "reel-to-reel-models/sony/sony-tc-788-4.aspx": "/reel-to-reel/sony/sony-tc-788-4",
    "reel-to-reel-models/studer/studer-a62.aspx": "/reel-to-reel/studer/studer-a62",
    "reel-to-reel-models/studer/studer-a67.aspx": "/reel-to-reel/studer/studer-a67",
    "reel-to-reel-models/studer/studer-a80.aspx": "/reel-to-reel/studer/studer-a80",
    "reel-to-reel-models/studer/studer-a721.aspx": "/reel-to-reel/studer/studer-a721",
    "reel-to-reel-models/studer/studer-a807.aspx": "/reel-to-reel/studer/studer-a807",
    "reel-to-reel-models/studer/studer-a810.aspx": "/reel-to-reel/studer/studer-a810",
    "reel-to-reel-models/studer/studer-a812.aspx": "/reel-to-reel/studer/studer-a812",
    "reel-to-reel-models/studer/studer-a816.aspx": "/reel-to-reel/studer/studer-a816",
    "reel-to-reel-models/studer/studer-a820.aspx": "/reel-to-reel/studer/studer-a820",
    "reel-to-reel-models/studer/studer-a827.aspx": "/reel-to-reel/studer/studer-a827",
    "reel-to-reel-models/studer/studer-c37.aspx": "/reel-to-reel/studer/studer-c37",
    "reel-to-reel-models/studer/studer-j37.aspx": "/reel-to-reel/studer/studer-j37",
    "reel-to-reel-models/technics/technics.aspx": "/reel-to-reel/technics",
    "reel-to-reel-models/wilcox-gay/wilcox-gay.aspx": "/reel-to-reel/wilcox-gay",
    "reel-to-reel-models/nagra-t-audio/nagra-t-audio.aspx": "/reel-to-reel/nagra",
    "reel-to-reel-models/nagra-t-audio/nagra-nta-2s.aspx": "/reel-to-reel/nagra/nagra-nta-2s",
    "reel-to-reel-models/nagra-t-audio/nagra-nta-3tcr.aspx": "/reel-to-reel/nagra/nagra-nta-3tcr",
    "reel-to-reel-models/nagra-t-audio/nagra-nta-2b.aspx": "/reel-to-reel/nagra/nagra-nta-2b",
    "reel-to-reel-models/nagra-t-audio/nagra-nts-3tcs.aspx": "/reel-to-reel/nagra/nagra-nts-3tcs",
    "reel-to-reel-models/nagra-t-audio/nagra-nta-2m.aspx": "/reel-to-reel/nagra/nagra-nta-2m",
    "reel-to-reel-models/nagra-t-audio/nagra-nta-3tcn.aspx": "/reel-to-reel/nagra/nagra-nta-3tcn",
    "reel-to-reel-models/nagra-t-audio/nagra-nta2s.aspx": "/reel-to-reel/nagra/nagra-nta-2s",
    "reel-to-reel-models/nagra-t-audio/nagra-nta2b.aspx": "/reel-to-reel/nagra/nagra-nta-2b",
    "reel-to-reel/reel-to-reel.aspx": "/reel-to-reel",
    "sitemap.html": "/site-index",
    "reel_to_reel": "/reel-to-reel",
    "hifi_audio": "/hifi-audio",
    "bang-olufsen/beosound-beosystem": "/bang-olufsen/beosound-beocenter",
    "bang_and_olufsen/turntabe_shop.aspx": "/bang-olufsen/turntable-shop",
    "bang_and_olufsen/turntable_shop.aspx": "/bang-olufsen/turntable-shop",
    "bang_and_olufsen/beosound-9000.aspx": "/bang-olufsen/beosound-9000",
    "bang_and_olufsen/beovisiontv.aspx": "/bang-olufsen/beovision-tv",
    "beovisionrepair/beovisionrepairhome.aspx": "/bang-olufsen/beovision-tv",
}

# Hi-fi brand and model pages converted from the old site (see hifi_pages.json)
_hifi = os.path.join(BASE, "hifi_pages.json")
if os.path.exists(_hifi):
    import json as _json
    _m = _json.load(open(_hifi, encoding="utf-8"))
    PAGES.update(_m["pages"])
    REDIRECTS.update(_m["redirects"])


BRANDS_BY_TYPE = {
    "Lens (Box, ENG, Studio)": ["Fujinon", "Canon", "Angenieux", "ARRI", "Atlas Lens Co.", "Cooke Optics", "IRIX",
                                "Laowa", "Leitz", "Panasonic", "Panavision", "Rokinon", "Sigma", "Sony", "Zeiss"],
    "Camera or Camcorder": ["Sony", "Panasonic", "JVC", "Canon", "Hitachi", "ARRI", "RED", "Blackmagic"],
    "Deck or Recorder": ["Sony", "Panasonic", "JVC"],
    "Projector": ["Sony", "Epson", "Panasonic", "Barco", "BenQ", "Canon", "Christie", "Eiki", "Hitachi", "InFocus",
                  "JVC", "LG", "Mitsubishi", "NEC", "Optoma", "Sanyo", "Sharp", "ViewSonic"],
    "Monitor": ["Sony", "Panasonic", "Barco", "Canon", "Flanders", "JVC", "LG", "Marshall", "NEC", "TVLogic"],
    "Hi-Fi Audio (Receiver, Amplifier)": ["McIntosh", "Marantz", "Mark Levinson", "Denon", "Luxman", "Anthem",
                                          "Boston Acoustics", "Harman Kardon", "Kenwood", "NAD", "Nakamichi", "Onkyo",
                                          "Sansui", "Scott", "Sony", "Technics", "Yamaha"],
    "Reel-to-Reel": ["Studer", "Revox", "Akai", "Teac", "Tascam", "Aiwa", "Nagra", "Nakamichi", "Pioneer", "Sony",
                     "Technics", "Wilcox-Gay"],
    "Bang & Olufsen": ["Bang & Olufsen"],
    "Other": [],
}
EQUIP_TYPES = list(BRANDS_BY_TYPE)
_PAGE_TYPES = {"lens-repair": "Lens (Box, ENG, Studio)", "camera-repair": "Camera or Camcorder",
               "projector-repair": "Projector", "monitor-repair": "Monitor",
               "hifi-audio": "Hi-Fi Audio (Receiver, Amplifier)", "reel-to-reel": "Reel-to-Reel",
               "bang-olufsen": "Bang & Olufsen"}


def _from_page(ref):
    """Equipment type and brand that match the page the customer came from."""
    from urllib.parse import urlparse
    parts = [p for p in urlparse(ref or "").path.lower().split("/") if p]
    if not parts:
        return {}
    etype = next((t for k, t in _PAGE_TYPES.items() if parts[0].startswith(k)), "")
    if not etype:
        return {}
    out = {"type": etype}
    brands = BRANDS_BY_TYPE[etype]
    if len(brands) == 1:
        out["brand"] = brands[0]
    else:
        slug = "-".join(parts)
        hits = [b for b in brands if b.lower().replace(" ", "-").replace(".", "").replace("&", "and") in slug]
        if hits:
            out["brand"] = max(hits, key=len)
    return out


REFERRED = ["ChatGPT", "Claude (Anthropic)", "Google", "Manufacturer", "Friend"]
SERVICE_REQUESTS = ["Shipping", "Pickup and delivery", "Walk-in"]


@app.route("/start-ticket", methods=["GET", "POST"])
def start_ticket():
    """New service ticket form: creates the customer and one ticket per item in RepairShopr."""
    ctx = {"equip_types": EQUIP_TYPES, "brands_by_type": BRANDS_BY_TYPE, "referred": REFERRED, "form": {}, "items": [{}],
           "error": "", "numbers": None, "service_request": "", "returning": False, "contact": [], "today": "", "box": False}
    if request.method == "GET":
        # match the form to the page the customer came from (a lens page shows lens brands, and so on)
        first = _from_page(request.headers.get("Referer"))
        if request.args.get("box"):  # "Request the original shipping box" on the Bang & Olufsen page
            first.update(type="Bang & Olufsen", brand="Bang & Olufsen")
            ctx["box"] = True
        if request.args.get("model"):
            first["model"] = " ".join(request.args.get("model").split())[:80]
        ctx["items"] = [first]
    if request.method == "POST":
        f = request.form

        def val(name, n=120):
            return " ".join((f.get(name) or "").split())[:n]

        cust = {"firstname": val("firstname", 60), "lastname": val("lastname", 60),
                "business_name": val("business_name", 100), "email": val("email", 120),
                "phone": val("phone", 20), "mobile": val("mobile", 20), "address": val("address", 120),
                "city": val("city", 60), "state": val("state", 40), "zip": val("zip", 12),
                "referred_by": val("referred_by", 40)}
        if cust["referred_by"] not in REFERRED:
            cust["referred_by"] = ""
        cols = [f.getlist(k) for k in ("equip_type", "equip_brand", "equip_model", "equip_serial", "equip_issue")]
        items = []
        for row in list(zip(*cols))[:5]:
            t, b, m, sn, issue = [(x or "").strip() for x in row]
            items.append({"type": t if t in EQUIP_TYPES else "", "brand": " ".join(b.split())[:60],
                          "model": " ".join(m.split())[:80], "serial": " ".join(sn.split())[:60],
                          "issue": issue[:1500]})
        service = val("service_request", 30)
        contact = [n for n, k in (("Email", "contact_email"), ("SMS", "contact_sms")) if f.get(k)]
        box = bool(f.get("bo_box")) and any(i["type"] == "Bang & Olufsen" for i in items)
        ctx["box"] = box
        ctx.update(form=dict(cust, contact_email="Email" in contact, contact_sms="SMS" in contact),
                   items=items or [{}], service_request=service)
        ip = (request.headers.get("X-Forwarded-For") or request.remote_addr or "").split(",")[0].strip()
        if f.get("website"):  # hidden field only robots fill in
            ctx["numbers"] = []
        elif not ticketlookup.api_key():
            ctx["error"] = "Online tickets are not available right now. Call us to open a ticket."
        elif not (cust["firstname"] and cust["lastname"] and "@" in cust["email"] and ticketlookup.digits(cust["phone"])):
            ctx["error"] = "Enter your first name, last name, email and full 10-digit phone number."
        elif not items or not all(i["type"] and i["brand"] and i["model"] and i["issue"] for i in items):
            ctx["error"] = "For each item, choose the equipment type and enter the brand, model and issue."
        elif service not in SERVICE_REQUESTS:
            ctx["error"] = "Choose Shipping, Pickup and delivery, or Walk-ins."
        elif not contact:
            ctx["error"] = "Choose Email or SMS so we can contact you."
        elif not ticketlookup.allowed("new:" + ip, limit=4, window=3600):
            ctx["error"] = "Too many requests. Wait a while and try again, or call us."
        else:
            try:
                made = ticketlookup.create_tickets(cust, items, service, contact,
                                                     box_request=box)
                ctx.update(numbers=made["numbers"], returning=made["returning"], contact=contact,
                           today=datetime.date.today().strftime("%B %-d, %Y"))
            except Exception:
                app.logger.exception("new ticket failed")
                ctx["error"] = "We could not open your ticket right now. Try again in a few minutes or call us."
    resp = app.make_response(render_template("start-ticket.html", **ctx))
    resp.headers["Cache-Control"] = "no-store"
    return resp


@app.route("/ticket-status", methods=["GET", "POST"])
def ticket_status():
    """Customer ticket lookup: last name + phone number, answered from RepairShopr."""
    if not ticketlookup.api_key():
        return redirect(ticketlookup.OLD_LOOKUP, code=302)
    ctx = {"tickets": None, "error": "", "last": "", "phone": ""}
    if request.method == "POST":
        last = " ".join((request.form.get("last_name") or "").split())[:60]
        phone = (request.form.get("phone") or "").strip()[:20]
        ctx.update(last=last, phone=phone)
        ip = (request.headers.get("X-Forwarded-For") or request.remote_addr or "").split(",")[0].strip()
        if not last or not ticketlookup.digits(phone):
            ctx["error"] = "Enter your last name and your full 10-digit phone number."
        elif not ticketlookup.allowed(ip):
            ctx["error"] = "Too many tries. Wait a few minutes and try again."
        else:
            try:
                found = ticketlookup.lookup(last, phone)
                if found is None:
                    ctx["error"] = ("No match. Use the last name and phone number you gave us "
                                    "when you opened the ticket, or call us.")
                else:
                    ctx["tickets"] = found
            except Exception:
                app.logger.exception("ticket lookup failed")
                ctx["error"] = "The lookup is not available right now. Try again in a few minutes or call us."
    resp = app.make_response(render_template("ticket-status.html", **ctx))
    resp.headers["Cache-Control"] = "no-store"
    return resp


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    key = path.strip("/").lower()
    if key in REDIRECTS:
        return redirect(REDIRECTS[key], code=301)
    if key in PAGES:
        return render_template(PAGES[key])
    # Site files (images, favicon, sitemap...) from /public
    if path and os.path.isfile(os.path.join(PUBLIC, path)):
        # let browsers keep images and other site files for a day
        return send_from_directory(PUBLIC, path, max_age=86400)
    abort(404)


def _query():
    return " ".join((request.args.get("q") or "").split())[:80]


@app.route("/search")
def search_page():
    q = _query()
    results, total, exact = site_search(q, PAGES) if q else ([], 0, None)
    if exact:
        # the query names exactly one model: go straight to its page
        return redirect(exact, code=302)
    return render_template("search.html", q=q, results=results, total=total)


@app.route("/search.json")
def search_json():
    q = _query()
    results, total, _ = site_search(q, PAGES, limit=8) if q else ([], 0, None)
    resp = jsonify({"q": q, "total": total, "results": [{"title": r["title"], "url": r["url"], "kind": r["kind"]} for r in results]})
    resp.headers["X-Robots-Tag"] = "noindex"
    return resp


@app.route("/robots.txt")
def robots():
    return Response("User-agent: *\nAllow: /\n\nUser-agent: GPTBot\nAllow: /\n\nUser-agent: OAI-SearchBot\nAllow: /\n\nUser-agent: ChatGPT-User\nAllow: /\n\nUser-agent: ClaudeBot\nAllow: /\n\nUser-agent: Claude-User\nAllow: /\n\nUser-agent: Claude-SearchBot\nAllow: /\n\nUser-agent: anthropic-ai\nAllow: /\n\nUser-agent: PerplexityBot\nAllow: /\n\nUser-agent: Google-Extended\nAllow: /\n\nUser-agent: Applebot-Extended\nAllow: /\n\nSitemap: https://tekmg.com/sitemap.xml\n", mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap():
    urls = ["/"] + ["/" + k for k in PAGES if k not in ("", "home")]
    urls += ["/monitor-repair/" + m["slug"] for m in SONY_MONITORS]
    for b in BRANDS.values():
        urls += ["/lens-repair/" + b["slug"]] + ["/lens-repair/" + b["slug"] + "/" + m["slug"] for m in b["models"]]
    urls += ["/lens-repair/" + ob["slug"] for ob in OTHER_BRANDS]
    body = "".join("<url><loc>https://tekmg.com%s</loc><lastmod>2026-11-21</lastmod></url>" % u for u in dict.fromkeys(urls) if u != "/site-index" or True)
    xml = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + body + "</urlset>"
    return Response(xml, mimetype="application/xml")


@app.route("/llms.txt")
def llms():
    txt = (
        "# Tek Media Group\n\n"
        "> Electronics repair shop at 711 South Victory Blvd, Burbank, CA 91502. Phone (818) 244-4440. "
        "Hours: Mon-Fri 8:30 AM-5:00 PM; weekends, holidays and after hours by appointment only. Estimates are free; repairs carry a 90-day warranty.\n\n"
        "## Services\n"
        "- [Projector repair](https://tekmg.com/projector-repair): LCD, DLP, LED and 4K projectors; Epson warranty service provider only\n"
        "- [Professional box, ENG and studio lens repair](https://tekmg.com/lens-repair): Box, ENG, EFP, studio and cinema lenses from Canon, Fujinon, Sony, Zeiss and others; clean room service; free estimates; 90-day warranty\n"
        "- [Fujinon box and studio lens repair, all models](https://tekmg.com/lens-repair/fujinon): one page per Fujinon model with a troubleshooting flowchart and the error codes and status signals from Fujinon's manuals; free estimates; 90-day warranty\n"
        "- [Canon box and studio lens repair, all models](https://tekmg.com/lens-repair/canon): one page per Canon model with a troubleshooting flowchart and the error messages from Canon's manuals, such as Initialize Error; free estimates; 90-day warranty\n"
        "- Other lens brands, each with a general troubleshooting flowchart: " + ", ".join("[%s](https://tekmg.com/lens-repair/%s)" % (ob["name"], ob["slug"]) for ob in OTHER_BRANDS) + "\n"
        "- [Professional and medical monitor repair](https://tekmg.com/monitor-repair): Sony PVM, BVM and LMD, Panasonic, JVC, Eizo, NEC and Barco; one page per Sony model with its warning lights and error signals from Sony's manuals; free estimates; 90-day warranty\n"
        "- [Professional camera, camcorder and deck repair](https://tekmg.com/camera-repair): cameras and camcorders from " + ", ".join(CAMERA_BRAND_NAMES) + "; video decks and recorders from " + ", ".join(DECK_BRAND_NAMES) + "; model list for each manufacturer, and equipment that is not listed is not ruled out; free estimates; 90-day warranty\n"
        "- [Bang & Olufsen authorized service](https://tekmg.com/bang-olufsen): warranty and out-of-warranty repair of Beosound, BeoLab, Beovox, Beocenter, Beosystem, Beomaster, Beogram, Beovision, Beoplay and BeoCom phones; Beogram 4000, 4002, 4004 and 8000 refurbishing program; California, Nevada and Arizona with nationwide shipping; free estimates\n"
        "- [Beogram turntable shop](https://tekmg.com/bang-olufsen/turntable-shop): Bang & Olufsen authorized classic repair for Beogram 4000, 4002, 4004, 8000, 8002 and TX; 4002-4004 restore program; free estimates; walk-in, ship-in, pickup and delivery\n"
        "- [Beovision TV repair](https://tekmg.com/bang-olufsen/beovision-tv): Bang & Olufsen Beovision TV repair, warranty and non-warranty; Harmony, Eclipse, Avant, Horizon, BeoVision 11, 14, 10, 8, 7, 6 and 4; common faults listed per model; free estimates\n"
        "- [Beosound and Beocenter repair](https://tekmg.com/bang-olufsen/beosound-beocenter): every Bang & Olufsen Beosound and Beocenter model on one page; pick a model to request service; free estimates\n"
        "- [Beosound 9000 repair](https://tekmg.com/bang-olufsen/beosound-9000): Bang & Olufsen Beosound 9000 multi-CD player repair; CD not reading, sledge and glass door stuck, Cleaning Required message, laser replacement, motor and clamp repair; free estimates\n"
        "- [BeoLab and Beovox speaker repair](https://tekmg.com/bang-olufsen/beolab-beovox): every Bang & Olufsen BeoLab and Beovox speaker on one page; pick a model to request service; free estimates\n"
        "- [BeoLab 5 repair](https://tekmg.com/bang-olufsen/beolab-5): BeoLab 5 red protection light, no bass, ICEpower amplifier, acoustic lens and driver repair; free estimates\n"
        "- [Hi-fi audio repair](https://tekmg.com/hifi-audio): McIntosh, Marantz, Mark Levinson, Denon, Luxman, Nakamichi and other high-end and vintage receivers, amplifiers and preamps; free estimates\n"
        "- [Studer reel-to-reel repair](https://tekmg.com/reel-to-reel/studer): Studer J37, A62, C37, A80, A810, A807, A820, A812, A816, A827 and A721 tape machines\n"
        "- [Aiwa reel-to-reel](https://tekmg.com/reel-to-reel/aiwa): Aiwa TPR-10, X-300/X-500/X-700, TPD-10A and AD-1250U/AD-1650U reel-to-reel recorders\n"
        "- [Akai reel-to-reel](https://tekmg.com/reel-to-reel/akai): Akai GX-747, GX-635D and GX-4000D repair guides and top Akai models\n"
        "- [Nakamichi reel-to-reel](https://tekmg.com/reel-to-reel/nakamichi): Nakamichi 1000ZXL, 700ZXL, 680ZX, 581 and 582 repair and restoration\n"
        "- [Revox reel-to-reel](https://tekmg.com/reel-to-reel/revox): Revox A700, B77, A77, PR99, PR77, C270, G36, F36, B710, B760, B225 and B226 repair guides\n"
        "- [Pioneer reel-to-reel](https://tekmg.com/reel-to-reel/pioneer): Pioneer RT-701, RT-707, RT-909, RT-1011, RT-1020, RT-1050, RT-761, RT-2022 and RT-2024 repair\n"
        "- [TEAC reel-to-reel](https://tekmg.com/reel-to-reel/teac): TEAC TD-102, A-3300SX, A-3440, A-1250, A-4010SL, A-7300, X-1000R and X-2000 repair\n"
        "- [TASCAM reel-to-reel](https://tekmg.com/reel-to-reel/tascam): TASCAM 58, 34, 80-8, 38, ATR-60 and 85 series repair\n"
        "- [Sony reel-to-reel](https://tekmg.com/reel-to-reel/sony): Sony TC-880-2, TC-788-4 and other Sony tape machines\n"
        "- [Technics reel-to-reel](https://tekmg.com/reel-to-reel/technics): Technics reel-to-reel repair and restoration\n"
        "- [Wilcox-Gay reel-to-reel](https://tekmg.com/reel-to-reel/wilcox-gay): Wilcox-Gay recorder repair and restoration\n"
        "- [Nagra T-Audio reel-to-reel](https://tekmg.com/reel-to-reel/nagra): Nagra NTA-2S, NTA-3TCR, NTA-2B, NTS-3TCS, NTA-2M and NTA-3TCN restoration and repair\n"
        "- [Reel-to-reel repair](https://tekmg.com/reel-to-reel): vintage and professional reel-to-reel recorders from Studer, Akai, Teac, Tascam, Revox and Ampex; free estimates\n\n"
        "## Company\n"
        "- [Site index](https://tekmg.com/site-index): every page on the site\n"
        "- [About](https://tekmg.com/about)\n"
        "- [Contact](https://tekmg.com/contact)\n"
        "- [Accessibility](https://tekmg.com/accessibility)\n"
        "- [Site search](https://tekmg.com/search): find a model or service page; JSON results at https://tekmg.com/search.json?q=MODEL\n"
    )
    return Response(txt, mimetype="text/plain")


@app.route("/healthz")
def healthz():
    return "ok tickets:%s" % ("on" if ticketlookup.api_key() else "off")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
