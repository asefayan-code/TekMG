import datetime
import os

from flask import Flask, abort, redirect, render_template, send_from_directory

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


@app.route("/healthz")
def healthz():
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
