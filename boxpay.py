"""Optional $75.00 Beogram shipping box, paid through Stripe Checkout (cards, Apple Pay, Google Pay, PayPal).

Needs STRIPE_SECRET_KEY on Render. Without it the box option stays hidden on the ticket form."""
import json
import os
import urllib.parse
import urllib.request

PRICE_CENTS = 7500
_done = set()  # Stripe sessions already written to RepairShopr (stops a refresh from posting twice)


def ready():
    return bool(os.environ.get("STRIPE_SECRET_KEY"))


def _call(method, path, data=None):
    req = urllib.request.Request("https://api.stripe.com/v1/" + path,
                                 data=urllib.parse.urlencode(data).encode() if data else None, method=method,
                                 headers={"Authorization": "Bearer " + os.environ["STRIPE_SECRET_KEY"]})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())


def create_session(base, email, ids, numbers):
    return _call("POST", "checkout/sessions", {
        "mode": "payment",
        "line_items[0][quantity]": "1",
        "line_items[0][price_data][currency]": "usd",
        "line_items[0][price_data][unit_amount]": str(PRICE_CENTS),
        "line_items[0][price_data][product_data][name]": "Beogram Turntable Shipping Box",
        "customer_email": email,
        "metadata[ticket_ids]": ",".join(str(i) for i in ids),
        "metadata[ticket_numbers]": ",".join(str(n) for n in numbers),
        "success_url": base + "/start-ticket/box-paid?session_id={CHECKOUT_SESSION_ID}",
        "cancel_url": base + "/start-ticket/box-paid?cancelled=1",
    })


def paid_session(session_id):
    """The Stripe session if it is paid, else None."""
    s = _call("GET", "checkout/sessions/" + urllib.parse.quote(session_id))
    return s if s.get("payment_status") == "paid" else None


def first_time(session_id):
    if session_id in _done:
        return False
    _done.add(session_id)
    return True
