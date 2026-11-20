import os
from flask import Flask, abort, redirect, send_from_directory

BASE = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(BASE, "pages")
PUBLIC = os.path.join(BASE, "public")

app = Flask(__name__, static_folder=None)

# Clean URL -> page file in /pages
ROUTES = {
    "": "home.html",
    "home": "home.html",
    "about": "aboutUs.aspx.html",
    "contact": "contact.html",
    "accessibility": "accessibility.html",
    "lens-repair": "lens-repair.html",
    "camcorder-camera-and-deck-repair": "Camcorder-Camera-And-Deck-Repair.aspx.html",
}


def page(name):
    return send_from_directory(PAGES, name)


@app.route("/")
def home():
    return page(ROUTES[""])


# Old tekmg.com addresses -> new pages (permanent redirect)
REDIRECTS = {
    "lensrepair/lens.aspx": "/lens-repair",
}


@app.route("/<path:path>")
def serve(path):
    key = path.strip("/").lower()
    if key in REDIRECTS:
        return redirect(REDIRECTS[key], code=301)
    if key in ROUTES:
        return page(ROUTES[key])
    # Old .aspx.html / .html addresses keep working
    if os.path.isfile(os.path.join(PAGES, path)):
        return page(path)
    # Site assets (css, assets/, images, favicon, sitemap...) from /public
    if os.path.isfile(os.path.join(PUBLIC, path)):
        return send_from_directory(PUBLIC, path)
    abort(404)


@app.route("/healthz")
def healthz():
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
