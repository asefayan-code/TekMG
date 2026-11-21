import datetime
import os

from lensdata import BRANDS, CANON_MODELS, FUJINON_MODELS
from monitordata import PROBLEMS, SERVICES, SONY_BY_SLUG, SONY_MONITORS
from modelinfo import LENS_FACTS, LENS_FACTS_SOURCE, lens_info, monitor_info
from cameradata import (CAMERA_BRANDS, CAMERA_BRAND_NAMES, CAMERA_MODEL_COUNT, DECK_BRANDS,
                        DECK_BRAND_NAMES, DECK_MODEL_COUNT)
from flowcharts import OTHER_BRANDS, OTHER_BY_SLUG, brand_flow, lens_flow
from sitesearch import search as site_search
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
    "contact": "contact.html",
    "accessibility": "accessibility.html",
    "lens-repair": "lens-repair.html",
    "camera-repair": "camera-repair.html",
    "projector-repair": "projector-repair.html",
    "monitor-repair": "monitor-repair.html",
    "reel-to-reel": "reel-to-reel.html",
    "reel-to-reel/studer": "reel-to-reel-studer.html",
    "reel-to-reel/aiwa": "reel-to-reel-aiwa.html",
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
        return send_from_directory(PUBLIC, path)
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
        "- [Bang & Olufsen authorized service](https://tekmg.com/bang-olufsen): warranty and out-of-warranty repair of Beosound, BeoLab, Beocenter, Beogram and Beovision; Beogram 4000, 4002, 4004 and 8000 refurbishing program; California, Nevada and Arizona with nationwide shipping; free estimates\n"
        "- [Beogram turntable shop](https://tekmg.com/bang-olufsen/turntable-shop): Bang & Olufsen authorized classic repair for Beogram 4000, 4002, 4004, 8000, 8002 and TX; 4002-4004 restore program; free estimates; walk-in, ship-in, pickup and delivery\n"
        "- [Beovision TV repair](https://tekmg.com/bang-olufsen/beovision-tv): Bang & Olufsen Beovision TV repair, warranty and non-warranty; Harmony, Eclipse, Avant, Horizon, BeoVision 11, 14, 10, 8, 7, 6 and 4; common faults listed per model; free estimates\n"
        "- [Beosound and Beocenter repair](https://tekmg.com/bang-olufsen/beosound-beocenter): every Bang & Olufsen Beosound and Beocenter model on one page; pick a model to request service; free estimates\n"
        "- [Beosound 9000 repair](https://tekmg.com/bang-olufsen/beosound-9000): Bang & Olufsen Beosound 9000 multi-CD player repair; CD not reading, sledge and glass door stuck, Cleaning Required message, laser replacement, motor and clamp repair; free estimates\n"
        "- [BeoLab and Beovox speaker repair](https://tekmg.com/bang-olufsen/beolab-beovox): every Bang & Olufsen BeoLab and Beovox speaker on one page; pick a model to request service; free estimates\n"
        "- [BeoLab 5 repair](https://tekmg.com/bang-olufsen/beolab-5): BeoLab 5 red protection light, no bass, ICEpower amplifier, acoustic lens and driver repair; free estimates\n"
        "- [Hi-fi audio repair](https://tekmg.com/hifi-audio): McIntosh, Marantz, Mark Levinson, Denon, Luxman, Nakamichi and other high-end and vintage receivers, amplifiers and preamps; free estimates\n"
        "- [Studer reel-to-reel repair](https://tekmg.com/reel-to-reel/studer): Studer J37, A62, C37, A80, A810, A807, A820, A812, A816, A827 and A721 tape machines\n"
        "- [Aiwa reel-to-reel](https://tekmg.com/reel-to-reel/aiwa): Aiwa TPR-10, X-300/X-500/X-700, TPD-10A and AD-1250U/AD-1650U reel-to-reel recorders\n"
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
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
