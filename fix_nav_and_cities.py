"""
fix_nav_and_cities.py
Two fixes:
1. Standardize promo bar + header across ALL pages to match index.html exactly
   (only the nav active class changes per page)
2. Fix city coverage sections: remove neighbourhood <p> descriptions,
   show just city name + View Details. For pages without city-specific pages,
   replace pill spans with proper linked city cards.
"""
import os, re

FOLDER = r"c:\Users\user\OneDrive\Desktop\designhelp"

# ────────────────────────────────────────────────────────────────
# STANDARD PROMO BAR (identical on all pages)
# ────────────────────────────────────────────────────────────────
PROMO_BAR = """<!-- PROMO BAR -->
<div class="promo-bar">
  <div class="promo-inner">
    <div class="pb-left">
      <span class="pb-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
      <span>4.9 Google Rating</span>
      <span class="pb-sep">&middot;</span>
      <span>500+ Reviews</span>
      <span class="pb-sep">&middot;</span>
      <span>20+ Years Serving GTA</span>
    </div>
    <div class="pb-center">Toronto&rsquo;s #1 Limo &amp; Chauffeur Service &mdash; Flat Rates, No Surge Pricing</div>
    <div class="pb-right">
      <a href="tel:+14164513106">&#9990;&nbsp; 416 451 3106</a>
      <a href="booking.html" class="pb-pill">Book Online</a>
    </div>
  </div>
</div>"""

# ────────────────────────────────────────────────────────────────
# NAV ITEMS — href → display label (order matters for active matching)
# ────────────────────────────────────────────────────────────────
NAV_ITEMS = [
    ("index.html",       "Home"),
    ("AirportHUB.html",  "Airport"),
    ("CorporateHUB.html","Corporate"),
    ("WeddingHUB.html",  "Wedding"),
    ("events.html",      "Events"),
    ("car-service.html", "Chauffeur"),
    ("tours.html",       "Tours"),
    ("sprinter.html",    "Sprinter"),
    ("fleet.html",       "Fleet"),
    ("contact.html",     "Contact"),
]

def build_nav(active_href):
    links = []
    for href, label in NAV_ITEMS:
        cls = ' class="active"' if href == active_href else ''
        links.append(f'      <a href="{href}"{cls}>{label}</a>')
    return "\n".join(links)

def build_header(active_href):
    nav_html = build_nav(active_href)
    return f"""<!-- HEADER -->
<header class="header">
  <div class="header-inner">
    <a href="index.html" class="logo"><img src="assets/logo.jpg" alt="Limo4All" onerror="this.style.display='none';this.nextSibling.style.display='inline'"><span style="display:none">LIMO<span>4ALL</span></span></a>
    <nav class="nav" id="main-nav">
{nav_html}
    </nav>
    <div class="hdr-right">
      <div class="hdr-phone-wrap">
        <span class="hdr-phone-label">Reservations</span>
        <a href="tel:+14164513106" class="hdr-phone">416 451 3106</a>
      </div>
      <a href="booking.html" class="btn-book">Book Online</a>
      <a href="contact.html" class="btn-quote-sm">Get a Quote</a>
      <button class="hamburger" id="hamburger" aria-label="Menu"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>"""

# ────────────────────────────────────────────────────────────────
# Which nav item is "active" for each file?
# ────────────────────────────────────────────────────────────────
def active_for(fname):
    if fname == "index.html":            return "index.html"
    if fname == "AirportHUB.html":       return "AirportHUB.html"
    if fname == "CorporateHUB.html":     return "CorporateHUB.html"
    if fname == "WeddingHUB.html":       return "WeddingHUB.html"
    if fname == "events.html":           return "events.html"
    if fname == "car-service.html":      return "car-service.html"
    if fname == "tours.html":            return "tours.html"
    if fname == "sprinter.html":         return "sprinter.html"
    if fname == "fleet.html":            return "fleet.html"
    if fname in ("contact.html", "about.html", "faq.html",
                 "booking.html", "locations.html", "sitemap.html",
                 "hourly.html", "transfers.html", "wedding.html",
                 "corporate.html"):      return None  # no active
    if fname.endswith("-airport-limo.html"):   return "AirportHUB.html"
    if fname.endswith("-corporate-limo.html"): return "CorporateHUB.html"
    return None

# ────────────────────────────────────────────────────────────────
# Regex to match the promo bar block
# ────────────────────────────────────────────────────────────────
PROMO_RE = re.compile(
    r'(?:<!-- PROMO BAR -->\n?)?<div class="promo-bar">.*?</div>\s*</div>\s*</div>',
    re.DOTALL
)

# Regex to match the header block
HEADER_RE = re.compile(
    r'(?:<!-- HEADER -->\n?)?<header class="header">.*?</header>',
    re.DOTALL
)

# ────────────────────────────────────────────────────────────────
# City data — same 16 cities, airport and corporate slugs
# ────────────────────────────────────────────────────────────────
AIRPORT_CITIES = [
    ("toronto",                "Toronto"),
    ("mississauga",            "Mississauga"),
    ("vaughan",                "Vaughan"),
    ("markham",                "Markham"),
    ("oakville",               "Oakville"),
    ("richmond-hill",          "Richmond Hill"),
    ("hamilton",               "Hamilton"),
    ("niagara-falls",          "Niagara Falls"),
    ("brampton",               "Brampton"),
    ("aurora",                 "Aurora"),
    ("burlington",             "Burlington"),
    ("king-city",              "King City"),
    ("london",                 "London"),
    ("milton",                 "Milton"),
    ("guelph",                 "Guelph"),
    ("waterloo-kitchener",     "Waterloo-Kitchener"),
]

def city_card(slug_suffix, city_name, service):
    href = f"{slug_suffix}-{service}.html"
    return (f'      <a href="{href}" class="city-card">'
            f'<h3>{city_name}</h3>'
            f'<span class="city-arrow">View Details &rsaquo;</span></a>')

def make_airport_grid():
    cards = "\n".join(city_card(s, n, "airport-limo") for s, n in AIRPORT_CITIES)
    return f"""<!-- CITY COVERAGE -->
<section class="city-coverage" id="service-areas">
  <div class="wrap">
    <span class="sec-label">Service Areas</span>
    <h2 class="sec-h2">Airport Limo Service <em>Near You</em></h2>
    <p class="sec-sub">Flat-rate airport limo from your city to Toronto Pearson (YYZ), Billy Bishop (YTZ) and all Ontario airports. Select your city for local pricing.</p>
    <div class="city-grid">
{cards}
    </div>
  </div>
</section>"""

def make_corporate_grid():
    cards = "\n".join(city_card(s, n, "corporate-limo") for s, n in AIRPORT_CITIES)
    return f"""<!-- CITY COVERAGE -->
<section class="city-coverage" id="service-areas">
  <div class="wrap">
    <span class="sec-label">Service Areas</span>
    <h2 class="sec-h2">Corporate Car Service <em>Near You</em></h2>
    <p class="sec-sub">Professional corporate limo and car service throughout the GTA and Southern Ontario. Select your city for local pricing and availability.</p>
    <div class="city-grid">
{cards}
    </div>
  </div>
</section>"""

def make_generic_grid(h2_text, desc):
    cards = "\n".join(
        f'      <a href="contact.html" class="city-card"><h3>{n}</h3><span class="city-arrow">Get a Quote &rsaquo;</span></a>'
        for _, n in AIRPORT_CITIES
    )
    return f"""<!-- CITY COVERAGE -->
<section class="city-coverage" id="service-areas">
  <div class="wrap">
    <span class="sec-label">Service Areas</span>
    <h2 class="sec-h2">{h2_text}</h2>
    <p class="sec-sub">{desc}</p>
    <div class="city-grid">
{cards}
    </div>
  </div>
</section>"""

CITY_SECTION_MAP = {
    "AirportHUB.html":   make_airport_grid(),
    "CorporateHUB.html": make_corporate_grid(),
    "WeddingHUB.html":   make_generic_grid(
        "Wedding Limo <em>Across Ontario</em>",
        "Premium wedding limo service across the GTA and Southern Ontario. Contact us to plan your complete wedding day transport."),
    "events.html":       make_generic_grid(
        "Events Limo <em>Across the GTA</em>",
        "Concert, sports, gala, and special event transport throughout Ontario. Call or request a quote for your date."),
    "car-service.html":  make_generic_grid(
        "Personal Chauffeur <em>Across Ontario</em>",
        "Hourly chauffeur and personal car service available across the GTA and Southern Ontario. Book by the hour, no minimum fuss."),
    "tours.html":        make_generic_grid(
        "Tour Service <em>Across Ontario</em>",
        "Niagara Falls, wine country, and custom day tours departing from anywhere in Ontario. Contact us to plan your itinerary."),
}

CITY_SECTION_RE = re.compile(
    r'<!-- CITY COVERAGE -->.*?</section>',
    re.DOTALL
)

# ────────────────────────────────────────────────────────────────
# MAIN LOOP
# ────────────────────────────────────────────────────────────────
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
    changed = False

    # ── 1. Fix promo bar ─────────────────────────────────────────
    if '<div class="promo-bar">' in content:
        new_content = PROMO_RE.sub(PROMO_BAR, content)
        if new_content != content:
            content = new_content
            changed = True

    # ── 2. Fix header ────────────────────────────────────────────
    if '<header class="header">' in content:
        active = active_for(fname)
        new_header = build_header(active)
        new_content = HEADER_RE.sub(new_header, content)
        if new_content != content:
            content = new_content
            changed = True

    # ── 3. Fix city coverage section ─────────────────────────────
    if fname in CITY_SECTION_MAP and '<!-- CITY COVERAGE -->' in content:
        new_section = CITY_SECTION_MAP[fname]
        new_content = CITY_SECTION_RE.sub(new_section, content)
        if new_content != content:
            content = new_content
            changed = True

    if changed:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[OK]   {fname}")
    else:
        print(f"[SAME] {fname}")

print("\nDone.")
