#!/usr/bin/env python3
"""
Batch update standalone HTML pages:
- Replace simple promo bar CSS with 3-column version
- Replace simple promo bar HTML with 3-column version
- Update nav: hourly.html -> car-service.html, remove transfers.html
Run: python fix_all.py
"""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

def read(name):
    with open(os.path.join(BASE, name), encoding="utf-8") as f:
        return f.read()

def write(name, content):
    with open(os.path.join(BASE, name), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Written: {name}")

# ── New 3-column promo bar CSS ────────────────────────────────
NEW_PROMO_CSS = """  /* ── PROMO BAR ──────────────────────────────────────────────────── */
  .promo-bar{background:var(--blue);color:#fff;padding:7px 0;font-family:var(--font-sans)}
  .promo-inner{max-width:var(--max-w);margin:0 auto;padding:0 28px;display:flex;align-items:center;justify-content:space-between;gap:16px}
  .pb-left{display:flex;align-items:center;gap:7px;font-size:11.5px;font-weight:600;opacity:0.92;white-space:nowrap;flex-shrink:0}
  .pb-stars{letter-spacing:1.5px;font-size:10.5px}
  .pb-sep{opacity:0.4;font-size:11px}
  .pb-center{font-size:12.5px;font-weight:700;text-align:center;flex:1}
  .pb-right{display:flex;align-items:center;gap:14px;font-size:11.5px;font-weight:700;white-space:nowrap;flex-shrink:0}
  .pb-right a{color:#fff;opacity:0.95}
  .pb-right a:hover{opacity:1;text-decoration:underline}
  .pb-pill{background:rgba(255,255,255,0.2);border-radius:50px;padding:3px 10px;font-size:11px;font-weight:700}
  @media(max-width:768px){.pb-left{display:none}.pb-center{text-align:left}}"""

# ── Old promo bar CSS patterns to replace ────────────────────
OLD_PROMO_CSS_1 = """  /* ── PROMO BAR ──────────────────────────────────────────────────── */
  .promo-bar{background:var(--blue);color:#fff;text-align:center;padding:8px 16px;font-family:var(--font-sans);font-size:13px;font-weight:600;letter-spacing:0.02em}
  .promo-bar a{color:#fff;text-decoration:underline}"""

def make_promo_html(center_text):
    return f"""<div class="promo-bar">
  <div class="promo-inner">
    <div class="pb-left">
      <span class="pb-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
      <span>4.9 Rating</span>
      <span class="pb-sep">&middot;</span>
      <span>500+ Reviews</span>
      <span class="pb-sep">&middot;</span>
      <span>&#127809; Canadian Owned</span>
    </div>
    <div class="pb-center">{center_text}</div>
    <div class="pb-right">
      <a href="tel:+14164513106">&#9990;&nbsp; 416 451 3106</a>
      <a href="sms:+16473131786">&#128172;&nbsp; 647 313 1786</a>
      <a href="booking.html" class="pb-pill">Book Online</a>
    </div>
  </div>
</div>"""

# ── Pages and their center texts ─────────────────────────────
pages = {
    "about.html":     "About Limo4All &mdash; Ontario&rsquo;s Premier Limo &amp; Chauffeur Service",
    "booking.html":   "Book Your Limo &mdash; Instant Confirmation, Flat Rates Guaranteed",
    "contact.html":   "Contact Limo4All &mdash; 24/7 Dispatch, Real People, Local Toronto Team",
    "faq.html":       "Limo4All FAQ &mdash; Everything You Need to Know",
    "fleet.html":     "Our Premium Fleet &mdash; Sedans, SUVs, Sprinters &amp; Stretch Limos",
    "locations.html": "Serving All of Ontario &mdash; Toronto, GTA &amp; Beyond",
    "sprinter.html":  "Mercedes Sprinter Van Service &mdash; Group Transport Across Ontario",
    "transfers.html": "City-to-City Limo Transfers &mdash; Toronto to Niagara, Ottawa &amp; Beyond",
    "corporate.html": "Corporate Car Service &mdash; Executive Chauffeurs, Monthly Billing Available",
}

for filename, center_text in pages.items():
    filepath = os.path.join(BASE, filename)
    if not os.path.exists(filepath):
        print(f"  SKIP (not found): {filename}")
        continue

    print(f"\nProcessing {filename}...")
    content = read(filename)

    # 1) Replace promo bar CSS
    if OLD_PROMO_CSS_1 in content:
        content = content.replace(OLD_PROMO_CSS_1, NEW_PROMO_CSS)
        print(f"  Updated promo bar CSS")
    else:
        print(f"  WARN: old promo CSS not found in {filename}")

    # 2) Replace promo bar HTML
    # Match the opening div and its content (single-line strong format)
    # Pattern: <div class="promo-bar">\n  <strong>...</strong>...\n</div>
    old_promo_pattern = re.compile(
        r'<div class="promo-bar">\s*\n\s*<strong>[^<]*</strong>[^\n]*\n</div>',
        re.DOTALL
    )
    new_promo = make_promo_html(center_text)
    if old_promo_pattern.search(content):
        content = old_promo_pattern.sub(new_promo, content, count=1)
        print(f"  Updated promo bar HTML")
    else:
        # Try alternate pattern without leading newline
        old_promo_pattern2 = re.compile(
            r'<div class="promo-bar">\s*<strong>[^<]*</strong>[^\n]*\n?</div>',
            re.DOTALL
        )
        if old_promo_pattern2.search(content):
            content = old_promo_pattern2.sub(new_promo, content, count=1)
            print(f"  Updated promo bar HTML (alt pattern)")
        else:
            print(f"  WARN: old promo HTML not found in {filename}")

    # 3) Update nav: hourly.html -> car-service.html
    if '<a href="hourly.html">Hourly</a>' in content:
        content = content.replace('<a href="hourly.html">Hourly</a>', '<a href="car-service.html">Car Service</a>')
        print(f"  Updated nav: hourly -> car-service")
    else:
        print(f"  WARN: hourly.html nav link not found in {filename}")

    # 4) Remove transfers.html nav link
    if '<a href="transfers.html">Transfers</a>\n' in content:
        content = content.replace('<a href="transfers.html">Transfers</a>\n', '')
        print(f"  Removed transfers nav link")
    elif '<a href="transfers.html">Transfers</a>' in content:
        content = content.replace('<a href="transfers.html">Transfers</a>', '')
        print(f"  Removed transfers nav link (inline)")
    else:
        print(f"  WARN: transfers.html nav link not found in {filename}")

    write(filename, content)

print("\nAll standalone pages updated!")
