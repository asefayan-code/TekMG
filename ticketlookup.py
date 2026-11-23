"""Ticket status lookup against RepairShopr (last name + phone number)."""
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request

SUBDOMAIN = os.environ.get("REPAIRSHOPR_SUBDOMAIN", "techmediagroup")
BASE = "https://%s.repairshopr.com/api/v1" % SUBDOMAIN
OLD_LOOKUP = "https://%s.repairshopr.com/my_profile/login" % SUBDOMAIN
MAX_OPEN = 40
MAX_DONE = 5
_hits = {}


def api_key():
    """The RepairShopr key; tolerant of stray spaces or lower case in the variable name."""
    for name, value in os.environ.items():
        if name.strip().upper() in ("REPAIRSHOPR_API_KEY", "REPAIRSHOPR_KEY") and value.strip():
            return value.strip()
    return ""


def allowed(ip, limit=8, window=600):
    """Simple per-visitor limit so the form cannot be used to guess customers."""
    now = time.time()
    recent = [t for t in _hits.get(ip, []) if now - t < window]
    if len(recent) >= limit:
        _hits[ip] = recent
        return False
    recent.append(now)
    _hits[ip] = recent
    if len(_hits) > 5000:
        _hits.clear()
    return True


def _call(method, path, params=None, body=None):
    url = "%s/%s" % (BASE, path)
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    # RepairShopr refuses Python's default User-Agent, so send a normal one.
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": "Bearer " + api_key(), "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "TekMediaGroup-Website/1.0 (+https://tekmg.com)"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        text = e.read(300).decode("utf-8", "replace")
        raise RuntimeError("RepairShopr %s on %s %s: %s" % (e.code, method, path, " ".join(text.split())[:200]))


def _get(path, **params):
    return _call("GET", path, params=params)


def _post(path, body):
    return _call("POST", path, body=body)


def digits(s):
    d = re.sub(r"\D", "", s or "")
    return d[-10:] if len(d) >= 10 else ""


def _phones(c):
    out = {digits(c.get("phone")), digits(c.get("mobile"))}
    for p in c.get("phones") or []:
        if isinstance(p, dict):
            out.add(digits(p.get("number")))
    out.discard("")
    return out


def _norm(s):
    return re.sub(r"[^a-z]", "", (s or "").lower())


def _last_matches(c, last):
    want = _norm(last)
    names = [_norm(c.get("lastname"))]
    full = (c.get("fullname") or "").split()
    if full:
        names.append(_norm(full[-1]))
    return bool(want) and want in names


def find_customers(last, phone):
    """Customers whose last name AND phone number both match."""
    want = digits(phone)
    found = {}
    searches = [{"lastname": last}, {"query": want},
                {"query": "%s-%s-%s" % (want[:3], want[3:6], want[6:])}]
    for params in searches:
        for page in range(1, 6):
            data = _get("customers", page=page, **params)
            rows = data.get("customers") or []
            for c in rows:
                if want in _phones(c) and _last_matches(c, last):
                    found[c.get("id")] = c
            if page >= int((data.get("meta") or {}).get("total_pages") or 1) or not rows:
                break
        if found:
            break
    return list(found.values())


def _date(s):
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", s or "")
    if not m:
        return ""
    months = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
    return "%s %d, %s" % (months[int(m.group(2)) - 1], int(m.group(3)), m.group(1))


DONE = ("resolved", "invoiced", "closed", "completed", "picked up", "shipped", "delivered")


def is_done(status):
    st = (status or "").lower()
    return any(w in st for w in DONE)


def lookup(last, phone):
    """Return {"open": [...], "done": [...]} (newest first) or None when nothing matches.

    A customer can have several items in the shop, so every open ticket is listed;
    finished tickets are limited to the most recent few."""
    customers = find_customers(last, phone)
    if not customers:
        return None
    seen, tickets = set(), []
    for c in customers[:3]:
        for page in range(1, 4):
            data = _get("tickets", customer_id=c.get("id"), page=page)
            rows = data.get("tickets") or []
            for t in rows:
                if t.get("id", t.get("number")) in seen:
                    continue
                seen.add(t.get("id", t.get("number")))
                tickets.append({"number": t.get("number"), "subject": (t.get("subject") or "").strip(),
                                "status": (t.get("status") or "").strip(),
                                "created": _date(t.get("created_at")), "updated": _date(t.get("updated_at")),
                                "_sort": t.get("created_at") or ""})
            if page >= int((data.get("meta") or {}).get("total_pages") or 1) or not rows:
                break
    tickets.sort(key=lambda t: t["_sort"], reverse=True)
    return {"open": [t for t in tickets if not is_done(t["status"])][:MAX_OPEN],
            "done": [t for t in tickets if is_done(t["status"])][:MAX_DONE]}


# ---- new service ticket -------------------------------------------------

def find_by_email(email, last):
    """Existing customer with this email and last name, if any."""
    data = _get("customers", email=email)
    for c in data.get("customers") or []:
        if (c.get("email") or "").strip().lower() == email.lower() and _last_matches(c, last):
            return c
    return None


def create_tickets(cust, items, service_request, contact):
    """Find or create the customer, then open one ticket per equipment item.

    Returns the list of new ticket numbers."""
    existing = find_customers(cust["lastname"], cust["phone"])
    customer = existing[0] if existing else find_by_email(cust["email"], cust["lastname"])
    if customer is None:
        body = {k: v for k, v in cust.items() if v not in ("", None)}
        body["get_sms"] = "SMS" in contact
        made = _post("customers", body)
        customer = made.get("customer") or made
    cid = customer.get("id")
    if not cid:
        raise RuntimeError("RepairShopr returned no customer id")
    numbers = []
    for it in items:
        subject = ("%s %s - %s" % (it["brand"], it["model"], it["type"]))[:250]
        made = _post("tickets", {"customer_id": cid, "subject": subject,
                                 "problem_type": it["type"], "status": "New"})
        t = made.get("ticket") or made
        if not t.get("id"):
            raise RuntimeError("RepairShopr returned no ticket id")
        lines = ["Website service request", "",
                 "Equipment type: " + it["type"], "Brand: " + it["brand"], "Model: " + it["model"],
                 "Serial number: " + (it["serial"] or "not given"), "",
                 "Issue: " + it["issue"], "",
                 "Service request: " + service_request,
                 "Contact by: " + (", ".join(contact) or "not chosen"),
                 "Referred by: " + (cust.get("referred_by") or "not given")]
        _post("tickets/%s/comment" % t["id"], {"subject": "Initial Issue", "body": "\n".join(lines),
                                               "hidden": True, "do_not_email": True})
        numbers.append(t.get("number") or t["id"])
    return numbers
