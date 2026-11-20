import datetime
import os

from flask import Flask, Response, abort, redirect, render_template, send_from_directory

BASE = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(BASE, "public")

app = Flask(__name__, static_folder=None)


@app.context_processor
def inject_year():
    return {"year": datetime.date.today().year}


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
    return Response("User-agent: *\nAllow: /\n\nSitemap: https://tekmg.com/sitemap.xml\n", mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap():
    urls = ["/"] + ["/" + k for k in PAGES if k not in ("", "home")]
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
        "- [Professional box, ENG and studio lens repair](https://tekmg.com/lens-repair)\n"
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
