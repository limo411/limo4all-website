#!/usr/bin/env python3
"""
Generator script for Limo4All city corporate limo pages.
Uses CorporateHUB.html as template + GitHub markdown content.
Run: python generate_corporate_pages.py
"""

import urllib.request
import re
import os

BASE_RAW = "https://raw.githubusercontent.com/limo411/Replitlimo2/b97691583f5fd908ba76edb7d2545979f1cf73f3/artifacts/limo4all/src/content/corporate-car-service/"

CITIES = [
    ("corporate-01-toronto.md",           "toronto",            "Toronto",            "Greater Toronto Area"),
    ("corporate-02-mississauga.md",        "mississauga",        "Mississauga",        "Peel Region"),
    ("corporate-03-vaughan.md",            "vaughan",            "Vaughan",            "York Region"),
    ("corporate-04-oakville.md",           "oakville",           "Oakville",           "Halton Region"),
    ("corporate-05-markham.md",            "markham",            "Markham",            "York Region"),
    ("corporate-06-hamilton.md",           "hamilton",           "Hamilton",           "Hamilton"),
    ("corporate-07-london.md",             "london",             "London",             "Southwestern Ontario"),
    ("corporate-08-niagara-falls.md",      "niagara-falls",      "Niagara Falls",      "Niagara Region"),
    ("corporate-09-waterloo-kitchener.md", "waterloo-kitchener", "Waterloo-Kitchener", "Waterloo Region"),
    ("corporate-10-richmond-hill.md",      "richmond-hill",      "Richmond Hill",      "York Region"),
    ("corporate-11-brampton.md",           "brampton",           "Brampton",           "Peel Region"),
    ("corporate-12-aurora.md",             "aurora",             "Aurora",             "York Region"),
    ("corporate-13-king-city.md",          "king-city",          "King City",          "King Township"),
    ("corporate-14-burlington.md",         "burlington",         "Burlington",         "Halton Region"),
    ("corporate-15-milton.md",             "milton",             "Milton",             "Halton Region"),
    ("corporate-16-guelph.md",             "guelph",             "Guelph",             "Wellington County"),
]

NEARBY_CITIES = {
    "toronto":            ["mississauga", "brampton", "vaughan", "markham", "oakville"],
    "mississauga":        ["toronto", "brampton", "oakville", "burlington", "vaughan"],
    "vaughan":            ["toronto", "richmond-hill", "markham", "aurora", "king-city"],
    "oakville":           ["mississauga", "burlington", "toronto", "milton", "brampton"],
    "markham":            ["toronto", "richmond-hill", "vaughan", "scarborough", "aurora"],
    "hamilton":           ["burlington", "oakville", "mississauga", "niagara-falls", "toronto"],
    "london":             ["guelph", "waterloo-kitchener", "hamilton", "toronto", "milton"],
    "niagara-falls":      ["hamilton", "burlington", "oakville", "toronto", "mississauga"],
    "waterloo-kitchener": ["guelph", "london", "hamilton", "toronto", "mississauga"],
    "richmond-hill":      ["vaughan", "markham", "aurora", "toronto", "king-city"],
    "brampton":           ["mississauga", "toronto", "vaughan", "oakville", "burlington"],
    "aurora":             ["richmond-hill", "vaughan", "king-city", "markham", "toronto"],
    "king-city":          ["aurora", "vaughan", "richmond-hill", "toronto", "markham"],
    "burlington":         ["oakville", "hamilton", "mississauga", "niagara-falls", "milton"],
    "milton":             ["oakville", "brampton", "burlington", "mississauga", "guelph"],
    "guelph":             ["waterloo-kitchener", "cambridge", "hamilton", "burlington", "london"],
}

CITY_NAMES = {slug: name for _, slug, name, _ in CITIES}
CITY_NAMES["etobicoke"] = "Etobicoke"
CITY_NAMES["scarborough"] = "Scarborough"
CITY_NAMES["cambridge"] = "Cambridge"


def fetch_url(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8")
    except Exception as e:
        print(f"  ERROR fetching {url}: {e}")
        return None


def esc(text):
    return (text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
        .replace("\u2014", "&mdash;")
        .replace("\u2013", "&ndash;")
        .replace("\u2019", "&rsquo;")
        .replace("\u2018", "&lsquo;")
        .replace("\u201c", "&ldquo;")
        .replace("\u201d", "&rdquo;")
    )


def extract_section(md, heading):
    level = len(re.match(r'^(#+)', heading.strip()).group(1)) if re.match(r'^(#+)', heading.strip()) else 2
    pattern = re.escape(heading.strip())
    match = re.search(pattern, md, re.IGNORECASE)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r'\n#{1,' + str(level) + r'} ', md[start:])
    if next_heading:
        end = start + next_heading.start()
    else:
        end = len(md)
    return md[start:end].strip()


def extract_bullets(text_block):
    bullets = []
    for line in text_block.split("\n"):
        line = line.strip()
        if line.startswith("- ") or line.startswith("* "):
            bullets.append(line[2:].strip())
    return bullets


def extract_intro_paragraphs(md):
    """Extract intro paras from ### Limo4All Transportation: Providing... section."""
    section = extract_section(md, "### Limo4All Transportation")
    if not section:
        # Try from ## Best Ontario Corporate section
        section = extract_section(md, "## Best Ontario Corporate")
    paras = []
    for block in section.split("\n\n"):
        block = block.strip()
        if block and not block.startswith("#") and not block.startswith("-"):
            lines = [l.strip() for l in block.split("\n") if not l.strip().startswith("#")]
            text = " ".join(l for l in lines if l)
            if len(text) > 60:
                paras.append(text)
        if len(paras) >= 3:
            break
    return paras[:3]


def extract_service_areas(md, city_name):
    """Extract business district bullets from Service Areas section."""
    # Try city-specific heading first
    section = extract_section(md, f"## {city_name} Corporate Limo")
    if not section:
        section = extract_section(md, "## Service Areas")
    if not section:
        # Fallback: search for any ## heading containing "Areas"
        match = re.search(r'## [^\n]*Area[s]?[^\n]*\n', md)
        if match:
            section = extract_section(md, match.group(0).strip())
    bullets = extract_bullets(section)
    return bullets[:10]


def extract_why_body(md):
    section = extract_section(md, "## Why Limo4All Transportation")
    for block in section.split("\n\n"):
        block = block.strip()
        if block and not block.startswith("#") and not block.startswith("-") and len(block) > 60:
            return " ".join(l.strip() for l in block.split("\n") if not l.strip().startswith("#"))
    return ""


def extract_faq(md):
    faq_section = extract_section(md, "## Frequently Asked Questions")
    if not faq_section:
        return []
    pairs = []
    lines = faq_section.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line and not line.startswith("#") and not line.startswith("-") and not line.startswith("*") and len(line) > 20:
            q = line
            i += 1
            answer_lines = []
            while i < len(lines) and lines[i].strip():
                answer_lines.append(lines[i].strip())
                i += 1
            if answer_lines:
                answer = " ".join(answer_lines)
                pairs.append((q, answer))
        else:
            i += 1
    return pairs[:12]


def build_faq_html(pairs):
    items = []
    for q, a in pairs:
        items.append(f'''      <div class="faq-item">
        <div class="faq-q">{esc(q)}<svg viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></div>
        <div class="faq-a">{esc(a)}</div>
      </div>''')
    return "\n".join(items)


def build_areas_html(areas, city_name):
    if not areas:
        areas = [f"{city_name} Downtown", f"{city_name} Business District", f"{city_name} Central",
                 f"{city_name} North", f"{city_name} East", f"{city_name} West"]
    rows = []
    for area in areas[:10]:
        rows.append(f'      <div class="cs-nbhd-card"><div class="cs-nbhd-name">{esc(area)}</div><div class="cs-nbhd-type">{esc(city_name)}</div></div>')
    return "\n".join(rows)


def build_nearby_corporate_links(slug):
    nearby = NEARBY_CITIES.get(slug, ["toronto", "mississauga", "brampton", "vaughan", "oakville"])
    links = []
    for n in nearby[:8]:
        name = CITY_NAMES.get(n, n.replace("-", " ").title())
        links.append(f'          <a href="{n}-corporate-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>{esc(name)} Corporate Car Service</a>')
    return "\n".join(links)


def build_other_services_html(city_name, slug):
    services = [
        ("airport-limo", "Airport Limo"),
        ("wedding-limo", "Wedding Limo"),
        ("prom-limo", "Prom Limo"),
        ("events-limo", "Events & Concert Limo"),
        ("hourly-limo", "Hourly Limo"),
        ("niagara-tours", "Niagara Falls Tours"),
        ("sprinter-van", "Sprinter Van Service"),
        ("city-transfers", "City-to-City Transfers"),
    ]
    links = []
    for svc_slug, svc_name in services:
        links.append(f'          <a href="{slug}-{svc_slug}.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>{esc(svc_name)} {esc(city_name)}</a>')
    return "\n".join(links)


def generate_page(template, slug, city_name, region, md):
    filename = f"{slug}-corporate-limo.html"
    city_esc = esc(city_name)
    region_esc = esc(region)

    # Parse markdown
    intro_paras = extract_intro_paragraphs(md)
    service_areas = extract_service_areas(md, city_name)
    why_body = extract_why_body(md)
    faq_pairs = extract_faq(md)

    # Fallbacks
    if not intro_paras:
        intro_paras = [
            f"{city_name} businesses rely on Limo4All Transportation for executive ground transportation that is punctual, professional, and discreet. From single airport transfers to full corporate account management with monthly invoicing, we serve every aspect of {city_name}'s corporate travel needs.",
            f"Our chauffeurs understand the demands of {city_name}'s business environment and deliver consistent, polished service for executives, visiting clients, and corporate teams across the region.",
        ]
    if not faq_pairs:
        faq_pairs = [
            (f"Do you offer corporate car service in {city_name}?", f"Yes. Limo4All Transportation provides full corporate car service throughout {city_name} and the surrounding {region}. Services include executive airport transfers, hourly as-directed bookings, client entertainment, and corporate account management with consolidated monthly invoicing."),
            (f"Can {city_name} businesses open a corporate account?", "Yes. Corporate accounts are available to businesses of all sizes. There is no minimum monthly spend. Set up takes under 10 minutes online or by phone. Invoicing is monthly with net-30 terms."),
            (f"How far in advance should I book corporate car service in {city_name}?", "For standard sedan and SUV bookings, 2 hours notice is sufficient for account holders. For Sprinter or multi-vehicle deployments, 4-12 hours notice is recommended. Advance bookings for important events should be placed 24-48 hours ahead."),
            (f"Do you serve all parts of {city_name}?", f"Yes. We serve all business districts, commercial corridors, and residential pickup locations throughout {city_name}. No area surcharge applies within {region}."),
            ("Are your chauffeurs background-checked?", "All Limo4All chauffeurs complete a full criminal background check, clean driving abstract review, and client confidentiality training before their first assignment. NDAs are available for sensitive accounts."),
            (f"What airports do you serve from {city_name}?", "We serve Toronto Pearson International (YYZ), Billy Bishop City Airport (YTZ), Hamilton International (YHM), and Buffalo Niagara (BUF) from all locations in {city_name}."),
        ]

    if not why_body:
        why_body = f"{city_name}'s business community expects the same level of professionalism from their ground transportation provider as they do from every other vendor. Limo4All Transportation delivers that standard consistently, on every booking."

    # Build HTML blocks
    intro_html = "\n      ".join(f'<p style="font-family:var(--font-sans);font-size:14.5px;color:var(--text-light);line-height:1.75;font-weight:300;margin-bottom:16px">{esc(p)}</p>' for p in intro_paras)
    faq_html = build_faq_html(faq_pairs)
    areas_html = build_areas_html(service_areas, city_name)
    nearby_links = build_nearby_corporate_links(slug)
    other_services = build_other_services_html(city_name, slug)

    page = template

    # --- TITLE & META ---
    page = page.replace(
        '<title>Corporate Car Service Toronto &ndash; Executive Chauffeur | Limo4All</title>',
        f'<title>Corporate Car Service {city_esc} &ndash; Executive Chauffeur | Limo4All</title>'
    )
    page = page.replace(
        'content="Premium corporate car service across the GTA. Executive sedans, SUVs, and Sprinters for meetings, airport transfers, and client entertainment. Monthly billing available."',
        f'content="Premium corporate car service in {city_esc} and {region_esc}. Executive sedans, SUVs, and Sprinters for meetings, airport transfers, and client entertainment. Monthly billing available."'
    )

    # --- SCHEMA ---
    page = page.replace(
        '"name":"Corporate Car Service Toronto"',
        f'"name":"Corporate Car Service {city_name}"'
    )
    page = page.replace(
        '"areaServed":"Greater Toronto Area"',
        f'"areaServed":"{region}"'
    )

    # --- TICKER ---
    page = page.replace(
        '<span>Corporate Car Service Toronto</span>',
        f'<span>Corporate Car Service {city_esc}</span>'
    )

    # --- HERO ---
    page = page.replace(
        '<h1>Corporate Car Service<br><strong>Toronto &amp; GTA</strong></h1>',
        f'<h1>Corporate Car Service<br><strong>{city_esc} &amp; {region_esc}</strong></h1>'
    )
    page = page.replace(
        '<p class="hero-sub">Reliable, confidential, and punctual executive ground transportation for businesses across Ontario. From single-ride bookings to full corporate accounts with consolidated monthly invoicing.</p>',
        f'<p class="hero-sub">Reliable, confidential, and punctual executive ground transportation for businesses in {city_esc} and {region_esc}. From single-ride bookings to full corporate accounts with consolidated monthly invoicing.</p>'
    )

    # --- WHY SECTION HEADING ---
    page = page.replace(
        '<span class="wh-pre">Why Businesses Choose Limo4All For</span>',
        f'<span class="wh-pre">Why {city_esc} Businesses Choose Limo4All</span>'
    )

    # --- FAQ HEADING ---
    page = page.replace(
        '<span class="sec-label center" style="display:block;text-align:center">Corporate FAQ</span>',
        f'<span class="sec-label center" style="display:block;text-align:center">{city_esc} Corporate FAQ</span>'
    )
    page = page.replace(
        '<h2 class="sec-h2 center">Frequently Asked <em>Questions</em></h2>',
        f'<h2 class="sec-h2 center">{city_esc} Corporate Car Service <em>FAQs</em></h2>'
    )

    # Replace FAQ grid content
    faq_grid_match = re.search(
        r'(<div class="faq-grid">)(.*?)(</div>\s*<div class="faq-cta">)',
        page, re.DOTALL
    )
    if faq_grid_match:
        page = page[:faq_grid_match.start()] + f'<div class="faq-grid">\n{faq_html}\n    </div>\n    <div class="faq-cta">' + page[faq_grid_match.end():]

    # --- SPEAK SECTION ---
    page = page.replace(
        '<h2 class="speak-h2">Need to Speak With Us About <strong>Corporate Travel?</strong></h2>',
        f'<h2 class="speak-h2">Book {city_esc} Corporate <strong>Car Service</strong></h2>'
    )
    page = page.replace(
        '<p class="speak-sub">Questions about corporate accounts, monthly billing, executive transfers, or multi-vehicle bookings &mdash; our team is available around the clock.</p>',
        f'<p class="speak-sub">Questions about {city_esc} corporate accounts, executive airport transfers from {region_esc}, or multi-vehicle bookings &mdash; our team is available around the clock.</p>'
    )

    # --- FOOTER BOTTOM ---
    page = page.replace(
        '<span>Corporate Car Service Toronto, Mississauga, Vaughan and all of Ontario.</span>',
        f'<span>Corporate Car Service {city_esc}, {region_esc} and all of Ontario.</span>'
    )

    # --- INJECT CITY INTRO SECTION (before WHY CHOOSE) ---
    intro_section = f'''
<!-- CITY INTRO -->
<section style="background:var(--off-white);padding:56px 0;border-top:1px solid var(--border)">
  <div class="wrap">
    <span class="sec-label">{city_esc} Corporate Car Service</span>
    <h2 class="sec-h2">Executive Ground Transportation in <em>{city_esc}</em></h2>
    <div style="max-width:780px;margin:24px 0 0">
      {intro_html}
    </div>
  </div>
</section>

'''
    page = page.replace('<!-- WHY CHOOSE -->', intro_section + '<!-- WHY CHOOSE -->', 1)

    # --- INJECT SERVICE AREAS SECTION (before FAQ) ---
    areas_section = f'''
<!-- CITY SERVICE AREAS -->
<section style="background:var(--off-white);padding:56px 0;border-top:1px solid var(--border)">
  <div class="wrap">
    <span class="sec-label">{city_esc} Coverage</span>
    <h2 class="sec-h2">Corporate Car Service Across <em>{city_esc}</em></h2>
    <p class="sec-sub" style="margin-bottom:28px">We serve all major business districts and commercial areas in {city_esc} with door-to-door executive transportation.</p>
    <div class="cs-nbhd-grid">
{areas_html}
    </div>
  </div>
</section>

'''
    page = page.replace('<!-- FAQ -->', areas_section + '<!-- FAQ -->', 1)

    # --- INJECT INTERNAL LINKS (before FOOTER) ---
    interlink_section = f'''<!-- INTERNAL LINKS -->
<section class="cs-interlink">
  <div class="wrap">
    <p class="cs-interlink-eyebrow">Explore More</p>
    <div class="cs-interlink-grid">
      <div class="cs-interlink-panel">
        <div class="cs-interlink-panel-bar"></div>
        <div class="cs-interlink-panel-body">
          <span class="cs-interlink-panel-label">Corporate Car Service in Nearby Cities</span>
{nearby_links}
        </div>
      </div>
      <div class="cs-interlink-panel">
        <div class="cs-interlink-panel-bar"></div>
        <div class="cs-interlink-panel-body">
          <span class="cs-interlink-panel-label">Other Limo Services in {city_esc}</span>
{other_services}
        </div>
      </div>
    </div>
  </div>
</section>

'''
    page = page.replace('<!-- FOOTER -->', interlink_section + '<!-- FOOTER -->', 1)

    return filename, page


def main():
    print("Loading template (CorporateHUB.html)...")
    with open("CorporateHUB.html", "r", encoding="utf-8") as f:
        template = f.read()

    generated = []
    for md_file, slug, city_name, region in CITIES:
        print(f"Processing {city_name} ({slug})...")
        md_url = BASE_RAW + md_file
        md = fetch_url(md_url)
        if not md:
            print(f"  SKIPPED (could not fetch markdown)")
            continue

        filename, page_html = generate_page(template, slug, city_name, region, md)
        out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(page_html)
        print(f"  Written: {filename}")
        generated.append(filename)

    print(f"\nDone! Generated {len(generated)} pages:")
    for f in generated:
        print(f"  {f}")


if __name__ == "__main__":
    main()
