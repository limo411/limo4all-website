"""
fix_banners_and_misc.py
1. Make promo bar pb-center text page-relevant
2. Standardize ticker text to var(--blue) across all pages
3. Change "Get a Quote" → "View Details" in city-card arrows only
4. Change "Service Areas" → "Areas We Serve" in city coverage section labels
"""
import os, re

FOLDER = r"c:\Users\user\OneDrive\Desktop\designhelp"

# ── Page-specific promo bar center text ───────────────────────────────────────
PROMO_CENTER = {
    "index.html":        "Toronto&rsquo;s #1 Limo &amp; Chauffeur Service &mdash; Flat Rates, No Surge Pricing",
    "AirportHUB.html":   "Airport Limo to Pearson YYZ &amp; Billy Bishop YTZ &mdash; Flat Rates, No Surge Pricing",
    "CorporateHUB.html": "Executive Corporate Car Service Across the GTA &mdash; Professional, Discreet, On-Time",
    "WeddingHUB.html":   "Luxury Wedding Limo Across Ontario &mdash; Make Your Day Unforgettable",
    "events.html":       "Concert, Gala &amp; Event Limo Across the GTA &mdash; No Surge Pricing, Book Tonight",
    "car-service.html":  "Personal Chauffeur by the Hour &mdash; Flexible, Professional, Available 24/7",
    "tours.html":        "Niagara Falls &amp; Wine Country Tours from Toronto &mdash; Book a Custom Day Trip",
    "sprinter.html":     "Sprinter Van for Groups Up to 14 &mdash; GTA &amp; Ontario &mdash; Flat Rates, No Surge",
    "fleet.html":        "Executive Sedans, SUVs &amp; Sprinter Vans &mdash; All Fully Licensed &amp; Insured",
    "contact.html":      "Reach Our Team 24/7 &mdash; Fast Quotes, No Pressure, No Commitment",
    "about.html":        "20+ Years Serving the GTA &mdash; 4.9 Stars &middot; 500+ Reviews &middot; Fully Licensed",
    "booking.html":      "Book Your Ride in Minutes &mdash; Flat Rates, Instant Confirmation, No Surge",
    "hourly.html":       "Hourly Chauffeur Service Across Ontario &mdash; Book by the Hour, Any Occasion",
    "faq.html":          "All Your Questions Answered &mdash; Limo4All Toronto, GTA &amp; Ontario",
    "locations.html":    "We Serve All of the GTA &amp; Southern Ontario &mdash; 16+ Cities, Flat Rates",
    "sitemap.html":      "All Limo4All Services &amp; Pages &mdash; Toronto, GTA &amp; Ontario",
}

PB_CENTER_RE = re.compile(r'<div class="pb-center">.*?</div>', re.DOTALL)

# ── Ticker: old dim-white → var(--blue) ───────────────────────────────────────
OLD_TICKER_COLOR = "color:rgba(255,255,255,0.55)"
NEW_TICKER_COLOR = "color:var(--blue)"

# ── City card arrow: "Get a Quote" → "View Details" ──────────────────────────
OLD_CITY_ARROW = 'class="city-arrow">Get a Quote &rsaquo;</span>'
NEW_CITY_ARROW = 'class="city-arrow">View Details &rsaquo;</span>'

# ── "Service Areas" sec-label → "Areas We Serve" (in city-coverage section) ──
# Only within the CITY COVERAGE block
CITY_COVERAGE_RE = re.compile(r'(<!-- CITY COVERAGE -->.*?</section>)', re.DOTALL)
SERVICE_AREAS_RE = re.compile(r'<span class="sec-label">Service Areas</span>')

def fix_city_coverage_label(content):
    def replacer(m):
        block = m.group(1)
        block = SERVICE_AREAS_RE.sub('<span class="sec-label">Areas We Serve</span>', block)
        return block
    return CITY_COVERAGE_RE.sub(replacer, content)

html_files = [f for f in os.listdir(FOLDER) if f.endswith('.html')]

for fname in sorted(html_files):
    fpath = os.path.join(FOLDER, fname)
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"[SKIP] {fname}: {e}")
        continue

    original = content

    # 1. Promo bar center text
    if fname in PROMO_CENTER and '<div class="pb-center">' in content:
        new_text = f'<div class="pb-center">{PROMO_CENTER[fname]}</div>'
        content = PB_CENTER_RE.sub(new_text, content)

    # For airport & corporate city pages, generate relevant text
    elif fname.endswith('-airport-limo.html') and '<div class="pb-center">' in content:
        city = fname.replace('-airport-limo.html', '').replace('-', ' ').title()
        new_text = f'<div class="pb-center">Flat-Rate Airport Limo from {city} to Pearson YYZ &amp; Billy Bishop YTZ &mdash; No Surge Pricing</div>'
        content = PB_CENTER_RE.sub(new_text, content)

    elif fname.endswith('-corporate-limo.html') and '<div class="pb-center">' in content:
        city = fname.replace('-corporate-limo.html', '').replace('-', ' ').title()
        new_text = f'<div class="pb-center">Corporate Car Service in {city} &mdash; Discreet, Punctual, Professional &mdash; Book Online</div>'
        content = PB_CENTER_RE.sub(new_text, content)

    # 2. Ticker colour
    content = content.replace(OLD_TICKER_COLOR, NEW_TICKER_COLOR)

    # 3. City card "Get a Quote" → "View Details"
    content = content.replace(OLD_CITY_ARROW, NEW_CITY_ARROW)

    # 4. "Service Areas" → "Areas We Serve" in city coverage blocks
    content = fix_city_coverage_label(content)

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[OK]   {fname}")
    else:
        print(f"[SAME] {fname}")

print("\nDone.")
