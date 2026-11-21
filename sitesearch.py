"""Site search: a small in-memory index of every page on the site.

The index is built once, on the first search, from the same data and templates
that serve the pages, so it never goes out of date with the site.
"""
import html
import re
import threading

from flask import render_template

from lensdata import BRANDS
from flowcharts import flow_text, lens_flow
from modelinfo import lens_info, monitor_info
from monitordata import PROBLEMS, SONY_MONITORS

_lock = threading.Lock()
_index = None


def norm(text):
    """Lowercase, join model-number punctuation (PVM-A250 -> pvma250, 9.3 -> 93)."""
    s = (text or "").lower().replace("×", "x")
    s = re.sub(r"(?<=[a-z0-9])[.\-/](?=[a-z0-9])", "", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return s.strip()


def compact(text):
    return norm(text).replace(" ", "")


def _strip_tags(fragment):
    s = re.sub(r"<(script|style)\b.*?</\1>", " ", fragment, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def _doc(url, title, kind, desc, body, boost=0, aliases=()):
    return {
        "url": url, "title": title, "kind": kind, "desc": desc,
        "t": " " + norm(title), "b": " " + norm(body),
        "aliases": {a for a in aliases if a}, "boost": boost,
    }


def _page_doc(url, page_html, kind):
    m = re.search(r"<title>(.*?)</title>", page_html, flags=re.S)
    title = html.unescape(m.group(1)).strip() if m else url
    title = re.sub(r"\s*\|\s*Tek Media Group.*$", "", title).strip() or title
    m = re.search(r'<meta name="description" content="(.*?)"', page_html, flags=re.S)
    desc = html.unescape(m.group(1)).strip() if m else ""
    m = re.search(r"<main\b[^>]*>(.*?)</main>", page_html, flags=re.S)
    body = _strip_tags(m.group(1) if m else page_html)
    return _doc(url, title, kind, desc, desc + " " + body, boost=3)


def _aliases(name, brand):
    base = name[len(brand) + 1:] if name.lower().startswith(brand.lower() + " ") else name
    parts = [name, base, re.sub(r"\s*\([^)]*\)", "", base)] + re.findall(r"\(([^)]*)\)", base)
    return {compact(p) for p in parts if p.strip()}


def _info_text(info):
    if not info:
        return ""
    bits = [info.get("title", ""), info.get("intro", ""), info.get("note") or ""]
    for row in info.get("rows", []):
        bits.extend(row)
    return " ".join(bits)


def _build(pages):
    docs = []
    seen = set()
    for key, template in pages.items():
        if template in seen:
            continue
        seen.add(template)
        url = "/" + key if key not in ("", "home") else "/"
        docs.append(_page_doc(url, render_template(template), "Service page" if "repair" in key else "Page"))
    for slug, b in BRANDS.items():
        url = "/lens-repair/" + slug
        docs.append(_page_doc(url, render_template("lens-hub.html", b=b), "Brand page"))
        for m in b["models"]:
            info = lens_info(slug, m)
            docs.append(_doc(
                url + "/" + m["slug"], m["name"] + " lens repair", "Lens model",
                b["name"] + " broadcast lens. Repair, " + (info["title"] if info else "service") + ".",
                b["name"] + " box ENG studio broadcast lens repair " + _info_text(info) + " " + flow_text(lens_flow(slug, m)),
                aliases=_aliases(m["name"], b["name"]),
            ))
    for m in SONY_MONITORS:
        info = monitor_info(m["slug"])
        size = (m["size"] + " ") if m.get("size") else ""
        docs.append(_doc(
            "/monitor-repair/" + m["slug"], m["name"] + " monitor repair", "Monitor model",
            size + m["display"] + " professional monitor. Repair" + (", " + info["title"] if info else "") + ".",
            "Sony professional monitor repair " + m["display"] + " " + size + " ".join(PROBLEMS[m["kind"]]) + " " + _info_text(info),
            aliases=_aliases(m["name"], "Sony"),
        ))
    return docs


def get_index(pages):
    global _index
    if _index is None:
        with _lock:
            if _index is None:
                _index = _build(pages)
    return _index


def _count(tok, text, title=False):
    """Occurrences of a query word. Short plain words must start a word, and
    one- and two-letter words only count in titles; model fragments match anywhere."""
    if tok.isalpha() and len(tok) <= 3:
        if len(tok) <= 2 and not title:
            return 0
        return text.count(" " + tok)
    return text.count(tok)


def search(query, pages, limit=60):
    """Return (results, total, exact_url). exact_url is set when the query names exactly one model."""
    tokens = norm(query).split()
    if not tokens:
        return [], 0, None
    cq = "".join(tokens)
    scored = []
    exact = []
    for pos, d in enumerate(get_index(pages)):
        s = 0
        for tok in tokens:
            in_title = _count(tok, d["t"], title=True)
            in_body = _count(tok, d["b"])
            if not (in_title or in_body):
                s = 0
                break
            s += (10 if in_title else 0) + min(in_body, 6)
        if not s:
            continue
        if cq in d["aliases"]:
            s += 100
            exact.append(d["url"])
        scored.append((-(s + d["boost"]), pos, d))
    scored.sort(key=lambda x: (x[0], x[1]))
    results = [{"title": d["title"], "url": d["url"], "kind": d["kind"], "desc": d["desc"]} for _, _, d in scored[:limit]]
    return results, len(scored), (exact[0] if len(exact) == 1 else None)
