import datetime
import os

from lensdata import BRANDS, CANON_MODELS, FUJINON_MODELS
from flask import Flask, Response, abort, redirect, render_template, send_from_directory

BASE = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(BASE, "public")

app = Flask(__name__, static_folder=None)


@app.context_processor
def inject_year():
    return {"year": datetime.date.today().year}


@app.context_processor
def inject_lens_models():
    return {"fujinon_models": FUJINON_MODELS, "canon_models": CANON_MODELS}


@app.route("/lens-repair/<brand>")
def lens_brand_hub(brand):
    b = BRANDS.get(brand.lower())
    if not b:
        abort(404)
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
    return render_template("lens-model.html", b=b, m=model, prev_m=prev_m, next_m=next_m)


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


@app.route("/robots.txt")
def robots():
    return Response("User-agent: *\nAllow: /\n\nUser-agent: GPTBot\nAllow: /\n\nUser-agent: OAI-SearchBot\nAllow: /\n\nUser-agent: ChatGPT-User\nAllow: /\n\nUser-agent: ClaudeBot\nAllow: /\n\nUser-agent: Claude-User\nAllow: /\n\nUser-agent: Claude-SearchBot\nAllow: /\n\nUser-agent: anthropic-ai\nAllow: /\n\nUser-agent: PerplexityBot\nAllow: /\n\nUser-agent: Google-Extended\nAllow: /\n\nUser-agent: Applebot-Extended\nAllow: /\n\nSitemap: https://tekmg.com/sitemap.xml\n", mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap():
    urls = ["/"] + ["/" + k for k in PAGES if k not in ("", "home")]
    for b in BRANDS.values():
        urls += ["/lens-repair/" + b["slug"]] + ["/lens-repair/" + b["slug"] + "/" + m["slug"] for m in b["models"]]
    body = "".join("<url><loc>https://tekmg.com%s</loc></url>" % u for u in urls)
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
        "- [Fujinon box and studio lens repair, all models](https://tekmg.com/lens-repair/fujinon): one page per Fujinon model, free estimates, 90-day warranty\n"
        "- [Canon box and studio lens repair, all models](https://tekmg.com/lens-repair/canon): one page per Canon model, free estimates, 90-day warranty\n"
        "- [Professional camera and deck repair](https://tekmg.com/camera-repair)\n\n"
        "## Company\n"
        "- [About](https://tekmg.com/about)\n"
        "- [Contact](https://tekmg.com/contact)\n"
        "- [Accessibility](https://tekmg.com/accessibility)\n"
    )
    return Response(txt, mimetype="text/plain")


@app.route("/healthz")
def healthz():
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
