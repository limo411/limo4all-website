#!/usr/bin/env python3
"""
Generator for Limo4All corporate car service city pages.
Uses toronto-airport-limo.html as design template + GitHub markdown content.
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
    "markham":            ["toronto", "richmond-hill", "vaughan", "aurora", "scarborough"],
    "hamilton":           ["burlington", "oakville", "mississauga", "niagara-falls", "toronto"],
    "london":             ["guelph", "waterloo-kitchener", "hamilton", "toronto", "mississauga"],
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
    end = start + next_heading.start() if next_heading else len(md)
    return md[start:end].strip()


def extract_bullets(text_block):
    bullets = []
    for line in text_block.split("\n"):
        line = line.strip()
        if line.startswith("- ") or line.startswith("* "):
            bullets.append(line[2:].strip())
    return bullets


def extract_card_body(md, heading):
    section = extract_section(md, heading)
    paras = []
    for block in section.split("\n\n"):
        block = block.strip()
        if block and not block.startswith("#") and not block.startswith("-") and not block.startswith("*"):
            lines = [l.strip() for l in block.split("\n") if not l.strip().startswith("#") and not l.strip().startswith("-")]
            text = " ".join(l for l in lines if l)
            if len(text) > 40:
                paras.append(text)
        if len(paras) >= 2:
            break
    return paras[:2]


def extract_intro_paragraphs(md):
    section = extract_section(md, "### Limo4All Transportation")
    if not section:
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


def extract_service_areas(md):
    section = extract_section(md, "## Service Areas")
    if not section:
        match = re.search(r'## [^\n]*Area[s]?[^\n]*\n', md)
        if match:
            section = extract_section(md, match.group(0).strip())
    return extract_bullets(section)[:10]


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
                pairs.append((q, " ".join(answer_lines)))
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


def build_card1_aside_bullets_html(districts, city_name):
    bullets = []
    for d in districts[:5]:
        bullets.append(f'              <li class="cs-svc-card-bullet">{esc(d)}</li>')
    bullets.append('              <li class="cs-svc-card-bullet">Corporate accounts with monthly invoicing</li>')
    bullets.append('              <li class="cs-svc-card-bullet">Flat rates &mdash; no surge pricing</li>')
    return "\n".join(bullets)


def build_nearby_links_html(slug):
    nearby = NEARBY_CITIES.get(slug, ["toronto", "mississauga", "brampton", "vaughan", "oakville"])
    links = []
    for n in nearby[:5]:
        name = CITY_NAMES.get(n, n.replace("-", " ").title())
        links.append(f'          <a href="{n}-corporate-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>{esc(name)} Corporate Car Service</a>')
    return "\n".join(links)


def build_other_services_html(city_name, slug):
    services = [
        ("airport-limo", "Airport Limo"),
        ("wedding-limo", "Wedding Limo"),
        ("events-limo", "Events & Concert Limo"),
        ("hourly-limo", "Hourly Limo"),
        ("prom-limo", "Prom Limo"),
    ]
    links = []
    for svc_slug, svc_name in services:
        links.append(f'          <a href="{slug}-{svc_slug}.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>{esc(svc_name)} {esc(city_name)}</a>')
    return "\n".join(links)


def build_nbhd_html(districts, city_name):
    if not districts:
        districts = [f"{city_name} Downtown", f"{city_name} Business District",
                     f"{city_name} Financial Core", f"{city_name} North", f"{city_name} East"]
    rows = []
    for d in districts[:10]:
        rows.append(f'      <div class="cs-nbhd-card"><div class="cs-nbhd-name">{esc(d)}</div><div class="cs-nbhd-type">{esc(city_name)}</div></div>')
    return "\n".join(rows)


def generate_page(template, slug, city_name, region, md):
    filename = f"{slug}-corporate-limo.html"
    city_esc = esc(city_name)
    region_esc = esc(region)

    # Parse markdown
    intro_paras = extract_intro_paragraphs(md)
    card1_paras = extract_card_body(md, "### Corporate Car Service Near Me")
    card2_paras = extract_card_body(md, "### Executive Airport Transfers")
    card2_bullets = extract_bullets(extract_section(md, "### Executive Airport Transfers"))[:7]
    card3_paras = extract_card_body(md, "### Corporate Events")
    card3_bullets = extract_bullets(extract_section(md, "### Corporate Events"))[:6]
    districts = extract_service_areas(md)
    why_body = extract_why_body(md)
    faq_pairs = extract_faq(md)

    # Fallbacks
    if not intro_paras:
        intro_paras = [
            f"{city_name} businesses rely on Limo4All Transportation for executive ground transportation that is punctual, professional, and discreet. From single airport transfers to full corporate account management with monthly invoicing, we serve every aspect of {city_name}'s corporate travel needs.",
            f"Our chauffeurs understand the demands of {city_name}'s business environment and deliver consistent, polished service for executives, visiting clients, and corporate teams across the region.",
        ]
    if not card1_paras:
        card1_paras = [
            f"Finding reliable corporate car service in {city_name} should not be a challenge. Limo4All Transportation offers door-to-door executive transportation with a fleet of immaculate sedans, SUVs, and Sprinter vans, driven by professional chauffeurs who understand discretion and punctuality.",
            f"We handle every detail including meet-and-greet at offices and hotels, luggage assistance, and the fastest routes through {city_name}'s business corridors. Flat-rate pricing and corporate account billing make expensing effortless.",
        ]
    if not card2_paras:
        card2_paras = [
            f"Executive airport transfers from {city_name} are among our most requested services. Our chauffeurs track incoming flights in real time, adjusting automatically for delays or early arrivals, so your executive never waits at the terminal.",
            "Meet-and-greet service inside the terminal, luggage handling, and 60 minutes of complimentary wait time on international flights are all standard. Vehicles are equipped with Wi-Fi and charging ports for productive transit.",
        ]
    if not card3_paras:
        card3_paras = [
            f"Corporate events and conferences require precise ground transportation logistics. Limo4All Transportation coordinates multi-vehicle deployments across {city_name} venues, handling group pickups, delegate transfers, and VIP arrivals with equal professionalism.",
            "From annual general meetings to trade shows, product launches, and corporate retreats, our event transportation team manages timing, routing, and vehicle allocation so your event runs seamlessly.",
        ]
    if not card2_bullets:
        card2_bullets = ["Toronto Pearson International (YYZ)", "Billy Bishop City Airport (YTZ)", "Hamilton International (YHM)", "Buffalo Niagara (BUF)", "Real-time flight tracking included", "60-minute complimentary wait on international arrivals", "Meet and greet inside terminal with name board"]
    if not card3_bullets:
        card3_bullets = ["Annual general meetings & shareholder events", "Conferences and trade shows", "Client entertainment and corporate retreats", "VIP and board member transfers", "Multi-vehicle delegate shuttles", "Product launches and galas"]
    if not districts:
        districts = [f"{city_name} Downtown", f"{city_name} Business District", f"{city_name} Financial Core", f"{city_name} North", f"{city_name} East"]
    if not why_body:
        why_body = f"{city_name}'s business community expects the same level of professionalism from their ground transportation provider as they do from every other vendor. Limo4All Transportation delivers that standard consistently, on every booking."
    if not faq_pairs:
        faq_pairs = [
            (f"Do you offer corporate car service in {city_name}?", f"Yes. Limo4All Transportation provides full corporate car service throughout {city_name} and the surrounding {region}. Services include executive airport transfers, hourly as-directed bookings, client entertainment, and corporate account management with consolidated monthly invoicing."),
            (f"Can {city_name} businesses open a corporate account?", "Yes. Corporate accounts are available to businesses of all sizes. Set up takes under 10 minutes online or by phone. Invoicing is monthly with net-30 terms available."),
            (f"How far in advance should I book corporate car service in {city_name}?", "For standard bookings, 2 hours notice is sufficient for account holders. For Sprinter or multi-vehicle deployments, 4-12 hours notice is recommended."),
            (f"Do you serve all parts of {city_name}?", f"Yes. We serve all business districts, commercial corridors, and residential pickup locations throughout {city_name}. No area surcharge applies within {region}."),
            ("Are your chauffeurs background-checked?", "All Limo4All chauffeurs complete a full criminal background check, clean driving abstract review, and client confidentiality training before their first assignment."),
            (f"What airports do you serve from {city_name}?", f"We serve Toronto Pearson International (YYZ), Billy Bishop City Airport (YTZ), Hamilton International (YHM), and Buffalo Niagara (BUF) from all locations in {city_name}."),
        ]

    # Build HTML blocks
    intro_html = "\n          ".join(f"<p>{esc(p)}</p>" for p in intro_paras)
    c1_paras_html = "\n            ".join(f'<p class="cs-svc-card-text">{esc(p)}</p>' for p in card1_paras)
    c2_paras_html = "\n            ".join(f'<p class="cs-svc-card-text">{esc(p)}</p>' for p in card2_paras)
    c3_paras_html = "\n            ".join(f'<p class="cs-svc-card-text">{esc(p)}</p>' for p in card3_paras)
    c2_bullets_html = "\n              ".join(f'<li class="cs-svc-card-bullet">{esc(b)}</li>' for b in card2_bullets)
    c3_bullets_html = "\n              ".join(f'<li class="cs-svc-card-bullet">{esc(b)}</li>' for b in card3_bullets)
    card1_aside_bullets = build_card1_aside_bullets_html(districts, city_name)
    nbhd_html = build_nbhd_html(districts, city_name)
    faq_html = build_faq_html(faq_pairs)
    nearby_links = build_nearby_links_html(slug)
    other_services = build_other_services_html(city_name, slug)

    page = template

    # ── META / HEAD ────────────────────────────────────────────────────
    page = page.replace(
        '<title>Airport Limo &amp; Transfers Toronto | Flat Rate | Limo4All</title>',
        f'<title>Corporate Car Service {city_esc} &ndash; Executive Chauffeur | Limo4All</title>'
    )
    page = page.replace(
        'content="Toronto\'s #1 airport limo service. Professional chauffeurs, flat rates, 24/7 availability. Serving YYZ, YTZ, YHM and BUF airports across the GTA. Book online or call 416-451-3106."',
        f'content="Premium corporate car service in {city_esc} and {region_esc}. Executive sedans, SUVs, and Sprinters for meetings, airport transfers, and client entertainment. Monthly billing available."'
    )
    page = page.replace(
        'href="https://www.limo4all.ca/toronto-airport-limo.html"',
        f'href="https://www.limo4all.ca/{slug}-corporate-limo.html"'
    )
    # Schema
    page = page.replace('"name":"Airport Limo & Transfers Toronto"', f'"name":"Corporate Car Service {city_name}"')
    page = page.replace(
        '"description":"Professional airport limo and chauffeur service in Toronto and the GTA. Flat rates, 24/7 availability, serving YYZ, YTZ, YHM and BUF airports."',
        f'"description":"Professional corporate car service in {city_name} and {region}. Executive vehicles, flat rates, 24/7 availability, corporate account billing."'
    )
    page = page.replace('"name":"Toronto"}}', f'"name":"{city_name}"}}')
    page = page.replace('"name":"Toronto"},"serviceType"', f'"name":"{city_name}"' + '},"serviceType"')
    page = page.replace('"serviceType":"Airport Transfer"', '"serviceType":"Corporate Car Service"')
    page = page.replace(
        '"description":"Flat rate airport transfers starting from $75"',
        '"description":"Corporate car service with flat rates and monthly billing available"'
    )
    page = page.replace(
        '"name":"Airport Limo","item":"https://www.limo4all.ca/airport.html"',
        '"name":"Corporate Car Service","item":"https://www.limo4all.ca/corporate.html"'
    )
    page = page.replace(
        f'"name":"Toronto Airport Limo","item":"https://www.limo4all.ca/toronto-airport-limo.html"',
        f'"name":"{city_name} Corporate Car Service","item":"https://www.limo4all.ca/{slug}-corporate-limo.html"'
    )

    # ── NAV active ─────────────────────────────────────────────────────
    page = page.replace('<a href="AirportHUB.html" class="active">Airport</a>', '<a href="AirportHUB.html">Airport</a>')
    page = page.replace('<a href="CorporateHUB.html">Corporate</a>', '<a href="CorporateHUB.html" class="active">Corporate</a>')

    # ── TICKER ─────────────────────────────────────────────────────────
    ticker_toronto = (
        '<span>Toronto Airport Limo from $75</span>\n    <span>Pearson Airport (YYZ) Transfers</span>\n'
        '    <span>Billy Bishop Airport (YTZ) Service</span>\n    <span>Flat Rate &mdash; No Surge Pricing</span>\n'
        '    <span>24/7 Live Dispatch</span>\n    <span>Flight Tracking Included</span>\n'
        '    <span>Meet &amp; Greet Inside Terminal</span>\n    <span>60 Min Free Wait &mdash; International Arrivals</span>\n'
        '    <span>Toronto Airport Limo from $75</span>\n    <span>Pearson Airport (YYZ) Transfers</span>\n'
        '    <span>Billy Bishop Airport (YTZ) Service</span>\n    <span>Flat Rate &mdash; No Surge Pricing</span>\n'
        '    <span>24/7 Live Dispatch</span>\n    <span>Flight Tracking Included</span>\n'
        '    <span>Meet &amp; Greet Inside Terminal</span>\n    <span>60 Min Free Wait &mdash; International Arrivals</span>'
    )
    ticker_corp = (
        f'<span>Corporate Car Service {city_esc}</span>\n    <span>Executive Airport Transfers</span>\n'
        '    <span>Corporate Account Billing Available</span>\n    <span>Flat Rate &mdash; No Surge Pricing</span>\n'
        '    <span>24/7 Live Dispatch</span>\n    <span>Uniformed Professional Chauffeurs</span>\n'
        '    <span>Monthly Invoicing for Businesses</span>\n    <span>Multi-Vehicle Corporate Events</span>\n'
        f'    <span>Corporate Car Service {city_esc}</span>\n    <span>Executive Airport Transfers</span>\n'
        '    <span>Corporate Account Billing Available</span>\n    <span>Flat Rate &mdash; No Surge Pricing</span>\n'
        '    <span>24/7 Live Dispatch</span>\n    <span>Uniformed Professional Chauffeurs</span>\n'
        '    <span>Monthly Invoicing for Businesses</span>\n    <span>Multi-Vehicle Corporate Events</span>'
    )
    page = page.replace(ticker_toronto, ticker_corp)

    # ── BREADCRUMB ─────────────────────────────────────────────────────
    page = page.replace('<a href="airport.html">Airport Limo</a>', '<a href="corporate.html">Corporate Car Service</a>')
    page = page.replace('<span class="bc-current">Toronto</span>', f'<span class="bc-current">{city_esc}</span>')
    page = page.replace("<span>Toronto&rsquo;s #1 Airport Limo</span>", f"<span>{city_esc}&rsquo;s #1 Corporate Car Service</span>")
    page = page.replace('<span>Serving GTA Since 2003</span>', '<span>Serving Ontario Since 2003</span>')
    page = page.replace('<span>99.8% On-Time Rate</span>', '<span>Corporate Accounts Available</span>')
    page = page.replace('<span>Flat Rate Guaranteed</span>', '<span>Monthly Invoicing Available</span>')

    # ── HERO ───────────────────────────────────────────────────────────
    page = page.replace(
        f'<span class="cs-eyebrow"><span class="cs-eyebrow-dot"></span> Toronto Airport Transfer</span>',
        f'<span class="cs-eyebrow"><span class="cs-eyebrow-dot"></span> {city_esc} Corporate Car Service</span>'
    )
    page = page.replace(
        '<h1 class="cs-h1">Airport Limo &amp; Transfers<strong>in Toronto</strong></h1>',
        f'<h1 class="cs-h1">Corporate Car Service<strong>in {city_esc}</strong></h1>'
    )
    page = page.replace(
        '<p class="cs-sub">Professional, flat-rate airport limo service serving all of Toronto and the GTA. Available 24/7 &mdash; never miss a flight, never wait at arrivals.</p>',
        f'<p class="cs-sub">Reliable, confidential, and punctual executive ground transportation for businesses in {city_esc} and {region_esc}. Corporate accounts, monthly billing, and 24/7 availability.</p>'
    )
    page = page.replace(
        '<span class="cs-pill">Flat Rate &mdash; No Surge</span>\n          <span class="cs-pill">Flight Tracked</span>\n          <span class="cs-pill">Meet &amp; Greet</span>\n          <span class="cs-pill">24/7 Dispatch</span>',
        '<span class="cs-pill">Flat Rate &mdash; No Surge</span>\n          <span class="cs-pill">Corporate Accounts</span>\n          <span class="cs-pill">Monthly Invoicing</span>\n          <span class="cs-pill">24/7 Dispatch</span>'
    )
    page = page.replace('<a href="booking.html" class="btn-primary">Book Your Transfer</a>', '<a href="booking.html" class="btn-primary">Book Corporate Car Service</a>')
    page = page.replace('<div class="cs-book-title">Get an Instant Quote</div>', '<div class="cs-book-title">Get a Corporate Quote</div>')
    page = page.replace('<div class="cs-book-sub">Flat rate confirmed &mdash; no hidden fees</div>', '<div class="cs-book-sub">Corporate rates &mdash; monthly billing available</div>')
    page = page.replace('<button class="cs-btn-submit" style="margin-top:12px">Get My Quote &rarr;</button>', '<button class="cs-btn-submit" style="margin-top:12px">Get Corporate Quote &rarr;</button>')
    page = page.replace(
        '<span>Flat Rate</span>\n          <span>No Surge</span>\n          <span>24/7 Support</span>',
        '<span>Flat Rate</span>\n          <span>Corp. Accounts</span>\n          <span>24/7 Support</span>'
    )

    # ── INTRO SECTION ──────────────────────────────────────────────────
    page = page.replace(
        '<span class="section-eyebrow">Best Ontario Airport Limo &amp; Transfer Service</span>',
        f'<span class="section-eyebrow">Best {city_esc} Corporate Car Service</span>'
    )
    page = page.replace(
        '<h2 class="section-h2">Limo4All Transportation:<strong>Providing Luxury Airport Limo &amp; Transfers</strong></h2>',
        f'<h2 class="section-h2">Limo4All Transportation:<strong>Executive Corporate Car Service in {city_esc}</strong></h2>'
    )
    page = page.replace(
        '<p>Toronto is one of Canada&rsquo;s most vibrant and fast-moving cities, and getting to or from the airport should never add stress to your journey. Limo4All Transportation provides premium airport limousine and transfer services across Toronto, connecting passengers reliably to Toronto Pearson International Airport, Billy Bishop Toronto City Airport, and beyond.</p>\n          <p>Our professional chauffeurs arrive on time, handle your luggage, and take the most efficient route so you never have to think twice about making your flight. We track your flight in real time and adjust pickups for delays or early arrivals, giving you one less thing to worry about.</p>\n          <p>From the moment you book to the moment you arrive, every detail is taken care of &mdash; because that is what true luxury transportation looks like in Toronto.</p>',
        intro_html
    )
    page = page.replace('<div class="cs-stat-label">Years serving Toronto &amp; the GTA</div>', '<div class="cs-stat-label">Years serving Ontario businesses</div>')
    # "Airports We Serve" tags → "Corporate Services"
    page = page.replace(
        '<span class="sub-label">Airports We Serve</span>\n        <div class="cs-airport-tags">\n          <span class="cs-airport-tag"><span class="cs-airport-tag-code">YYZ</span> Pearson International</span>\n          <span class="cs-airport-tag"><span class="cs-airport-tag-code">YTZ</span> Billy Bishop City Airport</span>\n          <span class="cs-airport-tag"><span class="cs-airport-tag-code">YHM</span> Hamilton International</span>\n          <span class="cs-airport-tag"><span class="cs-airport-tag-code">BUF</span> Buffalo Niagara</span>\n        </div>',
        f'<span class="sub-label">{city_esc} Corporate Services</span>\n        <div class="cs-airport-tags">\n          <span class="cs-airport-tag"><span class="cs-airport-tag-code">Exec</span> Executive Transfers</span>\n          <span class="cs-airport-tag"><span class="cs-airport-tag-code">Corp</span> Corporate Accounts</span>\n          <span class="cs-airport-tag"><span class="cs-airport-tag-code">Event</span> Events &amp; Conferences</span>\n          <span class="cs-airport-tag"><span class="cs-airport-tag-code">Hrly</span> Hourly As-Directed</span>\n        </div>'
    )
    # "Every Transfer Includes" → "Every Corporate Booking Includes"
    page = page.replace(
        '<span class="sub-label">Every Transfer Includes</span>\n          <ul class="cs-includes-list">\n            <li>Professional uniformed chauffeur</li>\n            <li>Real-time flight monitoring &amp; auto-adjustment</li>\n            <li>Meet &amp; greet inside the terminal with name board</li>\n            <li>60-min complimentary wait for international flights</li>\n            <li>Full luggage loading and unloading assistance</li>\n            <li>24/7 live dispatch &mdash; always a real person on the line</li>\n          </ul>',
        '<span class="sub-label">Every Corporate Booking Includes</span>\n          <ul class="cs-includes-list">\n            <li>Professional uniformed chauffeur</li>\n            <li>Flat-rate pricing locked at booking</li>\n            <li>Flight tracking for airport transfers</li>\n            <li>Corporate account invoicing available</li>\n            <li>Full luggage loading and unloading assistance</li>\n            <li>24/7 live dispatch &mdash; always a real person on the line</li>\n          </ul>'
    )

    # ── SERVICES SECTION ───────────────────────────────────────────────
    page = page.replace(
        '<span class="section-eyebrow">Our Airport Limo &amp; Transfer Services</span>',
        f'<span class="section-eyebrow">Our {city_esc} Corporate Car Services</span>'
    )
    page = page.replace(
        '<h2 class="section-h2" style="text-align:center">What We Offer<strong>for Your Journey</strong></h2>',
        '<h2 class="section-h2" style="text-align:center">What We Offer<strong>for Your Business</strong></h2>'
    )
    page = page.replace(
        'Every service includes real-time flight tracking, flat-rate pricing, and a professional uniformed chauffeur.',
        'Every service includes flat-rate pricing, corporate account billing, and a professional uniformed chauffeur.'
    )

    # Card 1
    page = page.replace('<span class="cs-svc-service-tag">GTA-Wide Coverage</span>', f'<span class="cs-svc-service-tag">{city_esc} Coverage</span>')
    page = page.replace('<h3 class="cs-svc-card-title">Airport Limo &amp; Transfer Service</h3>', '<h3 class="cs-svc-card-title">Corporate Car Service Near Me</h3>')
    page = page.replace(
        '<p class="cs-svc-card-text">Finding a reliable airport limo near you in Toronto should not be a hassle. Limo4All Transportation offers door-to-door service with a fleet of immaculate vehicles and professional chauffeurs who know the city inside and out.</p>\n            <p class="cs-svc-card-text">We handle everything including meet-and-greet at arrivals, luggage assistance, real-time flight monitoring, and the fastest routes through Toronto&rsquo;s busy corridors. Our flat-rate pricing means you always know what you are paying before you book, with no surge pricing or hidden fees.</p>\n            <p class="cs-svc-card-text">Whether you are travelling from downtown Toronto, Yorkville, the Distillery District, or anywhere across the city, we come to you and get you there in comfort and style.</p>',
        c1_paras_html
    )
    page = page.replace('<a href="booking.html" class="cs-svc-card-cta">Book Your Pickup &rarr;</a>', '<a href="booking.html" class="cs-svc-card-cta">Book Corporate Car Service &rarr;</a>')
    page = page.replace(
        '<span class="cs-svc-card-bottom-item">Flat Rate Locked</span>\n              <span class="cs-svc-card-bottom-item">Real-Time Tracking</span>\n              <span class="cs-svc-card-bottom-item">60 Min Free Wait</span>\n              <span class="cs-svc-card-bottom-item">Luggage Assistance</span>',
        '<span class="cs-svc-card-bottom-item">Flat Rate Locked</span>\n              <span class="cs-svc-card-bottom-item">Corp. Accounts</span>\n              <span class="cs-svc-card-bottom-item">Monthly Billing</span>\n              <span class="cs-svc-card-bottom-item">Discreet Service</span>'
    )
    page = page.replace('<span class="sub-label">Toronto Neighborhoods We Serve</span>', f'<span class="sub-label">{city_esc} Business Districts We Serve</span>')
    page = page.replace(
        '<li class="cs-svc-card-bullet">Downtown Core &amp; Financial District</li>\n              <li class="cs-svc-card-bullet">Yorkville, Rosedale &amp; Forest Hill</li>\n              <li class="cs-svc-card-bullet">North York &amp; Scarborough</li>\n              <li class="cs-svc-card-bullet">Etobicoke &amp; West Toronto</li>\n              <li class="cs-svc-card-bullet">East York &amp; The Beaches</li>\n              <li class="cs-svc-card-bullet">Real-time flight tracking for every booking</li>\n              <li class="cs-svc-card-bullet">Flat rates &mdash; no surge pricing</li>',
        card1_aside_bullets
    )
    page = page.replace(
        '<span class="cs-svc-callout-num">60 min</span>\n                <span class="cs-svc-callout-label">Free wait on international arrivals</span>',
        '<span class="cs-svc-callout-num">Corp.</span>\n                <span class="cs-svc-callout-label">Account billing &amp; monthly invoicing</span>'
    )
    page = page.replace('Starting flat rate from Toronto', f'Starting rate from {city_name}')
    page = page.replace(
        '<span>Flat Rate</span><span>Flight Tracked</span><span>24/7 Dispatch</span><span>Meet &amp; Greet</span>',
        '<span>Flat Rate</span><span>Corp. Accounts</span><span>24/7 Dispatch</span><span>Discreet</span>'
    )

    # Card 2
    page = page.replace('<span class="cs-svc-service-tag">Solo &amp; Family Transfers</span>', '<span class="cs-svc-service-tag">Executive Transfers</span>')
    page = page.replace('<h3 class="cs-svc-card-title">Personal Travel</h3>', '<h3 class="cs-svc-card-title">Executive Airport Transfers</h3>')
    page = page.replace(
        '<p class="cs-svc-card-text">Your personal trips deserve more than a standard cab or rideshare. Whether you are jetting off on a vacation, heading home for the holidays, or welcoming family at the airport, Limo4All Transportation makes every personal transfer feel special.</p>\n            <p class="cs-svc-card-text">Our chauffeurs are patient, attentive, and happy to assist with extra luggage, young children, or elderly passengers. Child car seats are available upon request so your youngest travellers are always safe and comfortable. You will arrive at Toronto Pearson relaxed and on time, with no parking headaches or last-minute scrambles.</p>',
        c2_paras_html
    )
    page = page.replace('<a href="booking.html" class="cs-svc-card-cta">Book Personal Transfer &rarr;</a>', '<a href="booking.html" class="cs-svc-card-cta">Book Executive Transfer &rarr;</a>')
    page = page.replace(
        '<span class="cs-svc-card-bottom-item">Child Seats Available</span>\n              <span class="cs-svc-card-bottom-item">Family-Friendly</span>\n              <span class="cs-svc-card-bottom-item">Door-to-Door</span>\n              <span class="cs-svc-card-bottom-item">Flat Rate</span>',
        '<span class="cs-svc-card-bottom-item">Flight Tracked</span>\n              <span class="cs-svc-card-bottom-item">Meet &amp; Greet</span>\n              <span class="cs-svc-card-bottom-item">60 Min Free Wait</span>\n              <span class="cs-svc-card-bottom-item">Wi-Fi Equipped</span>'
    )
    page = page.replace('<span class="sub-label">We Are the Perfect Ride For</span>', '<span class="sub-label">Airports We Serve</span>')
    page = page.replace(
        '<li class="cs-svc-card-bullet">Vacations and getaways</li>\n              <li class="cs-svc-card-bullet">Family visits and reunions</li>\n              <li class="cs-svc-card-bullet">Holiday travel</li>\n              <li class="cs-svc-card-bullet">Moving trips</li>\n              <li class="cs-svc-card-bullet">Special occasions and celebrations</li>\n              <li class="cs-svc-card-bullet">Toronto Maple Leafs, Raptors, and Blue Jays game day transportation</li>\n              <li class="cs-svc-card-bullet">TIFF and cultural event travel across the city</li>',
        c2_bullets_html
    )
    page = page.replace(
        '<span class="cs-svc-callout-num">Family</span>\n                <span class="cs-svc-callout-label">Child seats available on request</span>',
        '<span class="cs-svc-callout-num">60 min</span>\n                <span class="cs-svc-callout-label">Free wait on international arrivals</span>'
    )
    page = page.replace(
        '<span>Child Seats</span><span>Luggage Help</span><span>Family-Friendly</span><span>Flat Rate</span>',
        '<span>Flight Tracked</span><span>Meet &amp; Greet</span><span>60 Min Wait</span><span>Wi-Fi</span>'
    )

    # Card 3
    page = page.replace('<span class="cs-svc-service-tag">Corporate &amp; Executive</span>', '<span class="cs-svc-service-tag">Events &amp; Conferences</span>')
    page = page.replace('<h3 class="cs-svc-card-title">Business Travel</h3>', '<h3 class="cs-svc-card-title">Corporate Events &amp; Conferences</h3>')
    page = page.replace(
        '<p class="cs-svc-card-text">Toronto&rsquo;s corporate community moves fast, and your airport transfer should keep up. Limo4All Transportation&rsquo;s business travel service is built around punctuality, professionalism, and discretion. Our chauffeurs are formally dressed, well-mannered, and familiar with the city&rsquo;s key business corridors.</p>\n            <p class="cs-svc-card-text">Vehicles are equipped with Wi-Fi and charging ports so you can stay connected and productive on the way to or from Toronto Pearson. We also accommodate recurring bookings and multi-passenger corporate accounts, making us the preferred transfer partner for companies across the GTA.</p>',
        c3_paras_html
    )
    page = page.replace('<a href="corporate.html" class="cs-svc-card-cta">Learn About Corporate &rarr;</a>', '<a href="booking.html" class="cs-svc-card-cta">Book Event Transportation &rarr;</a>')
    page = page.replace(
        '<span class="cs-svc-card-bottom-item">Wi-Fi Equipped</span>\n              <span class="cs-svc-card-bottom-item">Corp. Accounts</span>\n              <span class="cs-svc-card-bottom-item">Discreet Service</span>\n              <span class="cs-svc-card-bottom-item">Priority Booking</span>',
        '<span class="cs-svc-card-bottom-item">Multi-Vehicle</span>\n              <span class="cs-svc-card-bottom-item">VIP Service</span>\n              <span class="cs-svc-card-bottom-item">Event Logistics</span>\n              <span class="cs-svc-card-bottom-item">Sprinter Vans</span>'
    )
    page = page.replace('<span class="sub-label">Ideal For</span>', '<span class="sub-label">We Handle</span>')
    page = page.replace(
        '<li class="cs-svc-card-bullet">Business trips and executive travel</li>\n              <li class="cs-svc-card-bullet">Professional seminars</li>\n              <li class="cs-svc-card-bullet">Conferences and trade shows</li>\n              <li class="cs-svc-card-bullet">Corporate retreats</li>\n              <li class="cs-svc-card-bullet">Client pickups and drop-offs</li>\n              <li class="cs-svc-card-bullet">Bay Street financial district and TIFF industry event travel</li>',
        c3_bullets_html
    )
    page = page.replace(
        '<span class="cs-svc-callout-num">Wi-Fi</span>\n                <span class="cs-svc-callout-label">All executive vehicles equipped</span>',
        '<span class="cs-svc-callout-num">Multi</span>\n                <span class="cs-svc-callout-label">Multi-vehicle deployments available</span>'
    )
    page = page.replace(
        '<span class="cs-svc-callout-num">Corp.</span>\n                <span class="cs-svc-callout-label">Account billing &amp; recurring bookings</span>',
        '<span class="cs-svc-callout-num">VIP</span>\n                <span class="cs-svc-callout-label">Dedicated event coordinator on request</span>'
    )
    page = page.replace(
        '<span>Wi-Fi Equipped</span><span>Corp. Accounts</span><span>Priority Booking</span><span>Professional</span>',
        '<span>Multi-Vehicle</span><span>Sprinter Vans</span><span>Event Logistics</span><span>VIP Service</span>'
    )

    # ── BENEFITS ───────────────────────────────────────────────────────
    page = page.replace(
        '<span class="section-eyebrow">Toronto Airport Limo &amp; Transfer Benefits</span>',
        f'<span class="section-eyebrow">{city_esc} Corporate Car Service Benefits</span>'
    )
    page = page.replace(
        '<h2 class="section-h2" style="text-align:center">The Advantages of<strong>Airport Limo &amp; Transfers</strong></h2>',
        f'<h2 class="section-h2" style="text-align:center">The Advantages of<strong>Corporate Car Service in {city_esc}</strong></h2>'
    )
    page = page.replace('<a href="booking.html" class="btn-primary">Book Your Transfer Now</a>', '<a href="booking.html" class="btn-primary">Book Corporate Car Service</a>')

    # ── WHY SECTION ────────────────────────────────────────────────────
    page = page.replace(
        '<span class="cs-why-pre">Best Airport Limo &amp; Transfer Service Near Me</span>',
        f'<span class="cs-why-pre">Best Corporate Car Service in {city_esc}</span>'
    )
    page = page.replace(
        '<h2 class="cs-why-h2">Why Limo4All Transportation<strong>Stands Apart</strong></h2>',
        '<h2 class="cs-why-h2">Why Limo4All Transportation<strong>For Corporate Travel</strong></h2>'
    )
    page = page.replace(
        '<p class="cs-why-body">Toronto has no shortage of transportation options, but Limo4All Transportation stands apart through consistent quality, genuine professionalism, and a team that truly cares about your experience. We have built our reputation one ride at a time, and every booking reflects our commitment to getting it right.</p>\n        <p class="cs-why-body">Do not leave your airport transfer to chance. Limo4All Transportation is available around the clock to get you to Toronto Pearson International Airport, Billy Bishop, or Hamilton International safely, comfortably, and on time.</p>',
        f'<p class="cs-why-body">{esc(why_body)}</p>\n        <p class="cs-why-body">Do not leave your corporate travel to chance. Limo4All Transportation is available around the clock to provide executive ground transportation throughout {city_esc} and {region_esc}.</p>'
    )
    why_toronto_items = (
        '        <div class="cs-why-item">\n'
        '          <div class="cs-why-item-text"><strong>Deep Toronto Market Familiarity</strong>'
        'Deep familiarity with Toronto&rsquo;s Financial District, Yorkville, North York, Etobicoke, Scarborough, '
        'and every GTA corridor connecting to Toronto Pearson and Billy Bishop airports.</div>\n'
        '        </div>\n'
        '        <div class="cs-why-item">\n'
        '          <div class="cs-why-item-text"><strong>A Luxury Fleet for Every Group</strong>'
        'A luxury fleet including sedans, SUVs, and stretch limousines, maintained to the highest standards for comfort and reliability.</div>\n'
        '        </div>\n'
        '        <div class="cs-why-item">\n'
        '          <div class="cs-why-item-text"><strong>Proven On-Time Record</strong>'
        'A proven on-time record on the DVP, Gardiner Expressway, and Highway 401 &mdash; Toronto&rsquo;s most demanding routes, day and night.</div>\n'
        '        </div>\n'
        '        <div class="cs-why-item">\n'
        '          <div class="cs-why-item-text"><strong>Professional Background-Checked Chauffeurs</strong>'
        'Professional, background-checked chauffeurs trained in Toronto&rsquo;s complex terminal and urban pickup logistics.</div>\n'
        '        </div>\n'
        '        <div class="cs-why-item">\n'
        '          <div class="cs-why-item-text"><strong>Easy Online Booking, Transparent Pricing</strong>'
        'Easy online booking with instant confirmation and transparent flat-rate pricing. Lock in your fare today and travel without surprises.</div>\n'
        '        </div>'
    )
    corp_why_items = (
        f'        <div class="cs-why-item">\n'
        f'          <div class="cs-why-item-text"><strong>Deep {city_esc} Market Familiarity</strong>'
        f'Deep familiarity with {city_esc}&rsquo;s business districts, commercial corridors, and routes connecting to Toronto Pearson and surrounding airports.</div>\n'
        '        </div>\n'
        '        <div class="cs-why-item">\n'
        '          <div class="cs-why-item-text"><strong>A Luxury Fleet for Every Group</strong>'
        'A luxury fleet including executive sedans, SUVs, and Mercedes Sprinter vans, maintained to the highest standards for corporate comfort and reliability.</div>\n'
        '        </div>\n'
        '        <div class="cs-why-item">\n'
        '          <div class="cs-why-item-text"><strong>Corporate Accounts &amp; Monthly Billing</strong>'
        'Simplified corporate accounts with consolidated monthly invoicing and net-30 terms. Expensing made effortless for your team.</div>\n'
        '        </div>\n'
        '        <div class="cs-why-item">\n'
        '          <div class="cs-why-item-text"><strong>Professional Background-Checked Chauffeurs</strong>'
        'Every chauffeur completes a criminal background check, driving abstract review, and confidentiality training before their first corporate booking.</div>\n'
        '        </div>\n'
        '        <div class="cs-why-item">\n'
        '          <div class="cs-why-item-text"><strong>Easy Online Booking, Transparent Pricing</strong>'
        'Easy online booking with instant confirmation and transparent flat-rate pricing. No surge charges, no surprises &mdash; ever.</div>\n'
        '        </div>'
    )
    page = page.replace(why_toronto_items, corp_why_items)
    page = page.replace('<a href="booking.html" class="cs-why-cta">Book Your Transfer</a>', '<a href="booking.html" class="cs-why-cta">Book Corporate Service</a>')

    # ── COMPARE ────────────────────────────────────────────────────────
    page = page.replace(
        'See why thousands of Toronto passengers trust Limo4All over rideshare apps for every airport run.',
        f'See why {city_esc} businesses trust Limo4All over rideshare apps for every executive transfer.'
    )

    # ── SERVICE AREAS ──────────────────────────────────────────────────
    page = page.replace('<span class="section-eyebrow">Coverage</span>', f'<span class="section-eyebrow">{city_esc} Corporate Coverage</span>')
    page = page.replace(
        '<h2 class="section-h2" style="text-align:center">Toronto Airport Limo<strong>&amp; Transfer Service Areas</strong></h2>',
        f'<h2 class="section-h2" style="text-align:center">{city_esc} Corporate Car Service<strong>Coverage Areas</strong></h2>'
    )
    page = page.replace(
        'Limo4All Transportation serves all major Toronto neighbourhoods and communities throughout the Greater Toronto Area. No matter where you are located, we will come to your door and get you to your airport on time.',
        f'Limo4All Transportation serves all major business districts and commercial areas throughout {city_name} and {region}. No matter where your office or hotel is located, we provide door-to-door executive transportation.'
    )
    page = page.replace(
        '<span class="sub-label">Airport Limo Services in Nearby Cities</span>',
        f'<span class="sub-label">{city_esc} Business Districts &amp; Nearby Areas</span>'
    )
    # Replace neighbourhood grid
    toronto_nbhd_block = (
        '      <a href="mississauga-airport-limo.html" class="cs-nbhd-card"><div class="cs-nbhd-name">Mississauga Airport Limo</div><div class="cs-nbhd-type">Peel Region</div></a>\n'
        '      <a href="brampton-airport-limo.html" class="cs-nbhd-card"><div class="cs-nbhd-name">Brampton Airport Limo</div><div class="cs-nbhd-type">Peel Region</div></a>\n'
        '      <a href="vaughan-airport-limo.html" class="cs-nbhd-card"><div class="cs-nbhd-name">Vaughan Airport Limo</div><div class="cs-nbhd-type">York Region</div></a>\n'
        '      <a href="markham-airport-limo.html" class="cs-nbhd-card"><div class="cs-nbhd-name">Markham Airport Limo</div><div class="cs-nbhd-type">York Region</div></a>\n'
        '      <a href="oakville-airport-limo.html" class="cs-nbhd-card"><div class="cs-nbhd-name">Oakville Airport Limo</div><div class="cs-nbhd-type">Halton Region</div></a>\n'
        '      <a href="richmond-hill-airport-limo.html" class="cs-nbhd-card"><div class="cs-nbhd-name">Richmond Hill Airport Limo</div><div class="cs-nbhd-type">York Region</div></a>\n'
        '      <a href="scarborough-airport-limo.html" class="cs-nbhd-card"><div class="cs-nbhd-name">Scarborough Airport Limo</div><div class="cs-nbhd-type">East Toronto</div></a>\n'
        '      <a href="north-york-airport-limo.html" class="cs-nbhd-card"><div class="cs-nbhd-name">North York Airport Limo</div><div class="cs-nbhd-type">Central Toronto</div></a>\n'
        '      <a href="etobicoke-airport-limo.html" class="cs-nbhd-card"><div class="cs-nbhd-name">Etobicoke Airport Limo</div><div class="cs-nbhd-type">West Toronto</div></a>\n'
        '      <a href="hamilton-airport-limo.html" class="cs-nbhd-card"><div class="cs-nbhd-name">Hamilton Airport Limo</div><div class="cs-nbhd-type">Hamilton Area</div></a>'
    )
    page = page.replace(toronto_nbhd_block, nbhd_html)
    # Replace airports grid → corporate services grid
    airports_grid = (
        '<span class="sub-label" style="margin-top:32px;display:block">Airports We Service</span>\n'
        '    <div class="cs-airports-grid">\n'
        '      <div class="cs-airport-card">\n'
        '        <div class="cs-airport-iata">YYZ</div>\n'
        '        <div class="cs-airport-full">Toronto Pearson International Airport</div>\n'
        '        <div class="cs-airport-note">All terminals &middot; T1 &amp; T3 &middot; International &amp; Domestic</div>\n'
        '      </div>\n'
        '      <div class="cs-airport-card">\n'
        '        <div class="cs-airport-iata">YTZ</div>\n'
        '        <div class="cs-airport-full">Billy Bishop Toronto City Airport</div>\n'
        '        <div class="cs-airport-note">Downtown Toronto &middot; Porter &amp; Air Canada routes</div>\n'
        '      </div>\n'
        '      <div class="cs-airport-card">\n'
        '        <div class="cs-airport-iata">YHM</div>\n'
        '        <div class="cs-airport-full">Hamilton International Airport</div>\n'
        '        <div class="cs-airport-note">Approx. 60 min from Toronto &middot; Budget carriers</div>\n'
        '      </div>\n'
        '      <div class="cs-airport-card">\n'
        '        <div class="cs-airport-iata">BUF</div>\n'
        '        <div class="cs-airport-full">Buffalo Niagara International Airport</div>\n'
        '        <div class="cs-airport-note">Cross-border transfers &middot; US flights &middot; ~90 min</div>\n'
        '      </div>\n'
        '    </div>'
    )
    corp_services_grid = (
        f'<span class="sub-label" style="margin-top:32px;display:block">Corporate Services Available in {city_esc}</span>\n'
        '    <div class="cs-airports-grid">\n'
        '      <div class="cs-airport-card">\n'
        '        <div class="cs-airport-iata">Exec</div>\n'
        '        <div class="cs-airport-full">Executive Airport Transfers</div>\n'
        '        <div class="cs-airport-note">YYZ, YTZ, YHM &amp; BUF &middot; Flight tracked &middot; Meet &amp; greet</div>\n'
        '      </div>\n'
        '      <div class="cs-airport-card">\n'
        '        <div class="cs-airport-iata">Corp</div>\n'
        '        <div class="cs-airport-full">Corporate Accounts</div>\n'
        '        <div class="cs-airport-note">Monthly invoicing &middot; Net-30 terms &middot; No minimum spend</div>\n'
        '      </div>\n'
        '      <div class="cs-airport-card">\n'
        '        <div class="cs-airport-iata">Event</div>\n'
        '        <div class="cs-airport-full">Events &amp; Conferences</div>\n'
        '        <div class="cs-airport-note">Multi-vehicle &middot; VIP transfers &middot; Delegate shuttles</div>\n'
        '      </div>\n'
        '      <div class="cs-airport-card">\n'
        '        <div class="cs-airport-iata">Hrly</div>\n'
        '        <div class="cs-airport-full">Hourly As-Directed</div>\n'
        '        <div class="cs-airport-note">Full-day bookings &middot; Road shows &middot; Client entertainment</div>\n'
        '      </div>\n'
        '    </div>'
    )
    page = page.replace(airports_grid, corp_services_grid)

    # ── SPEAK SECTION ──────────────────────────────────────────────────
    page = page.replace(
        '<span class="speak-pre">Contact Us for Toronto Airport Limo &amp; Transfers</span>',
        f'<span class="speak-pre">Contact Us for {city_esc} Corporate Car Service</span>'
    )
    page = page.replace(
        '<h2 class="speak-h2">Need to Speak With Us<strong>About Your Airport Transfer?</strong></h2>',
        f'<h2 class="speak-h2">Book {city_esc} Corporate<strong>Car Service</strong></h2>'
    )
    page = page.replace(
        "Toronto's most trusted airport limo service is ready when you are",
        f"{city_name}'s most trusted corporate car service is ready when you are"
    )
    page = page.replace(
        'Booking is quick and easy. Lock in your flat rate online or give us a call and we will handle the rest.',
        'Booking is quick and easy. Set up a corporate account or book individual rides online &mdash; our team is ready to handle your travel program.'
    )
    page = page.replace(
        '<textarea class="sf-textarea" placeholder="Tell us about your transfer — flight number, date, pickup location..."></textarea>',
        '<textarea class="sf-textarea" placeholder="Tell us about your corporate travel needs — company name, booking frequency, account billing..."></textarea>'
    )
    page = page.replace(
        '<div class="sf-note">Flat rate confirmed instantly &middot; No credit card to quote &middot; 24/7 dispatch</div>',
        '<div class="sf-note">Corporate rates confirmed instantly &middot; Account billing available &middot; 24/7 dispatch</div>'
    )

    # ── FAQ ────────────────────────────────────────────────────────────
    faq_grid_match = re.search(r'(<div class="faq-grid">)(.*?)(</div>\s*<div class="faq-cta">)', page, re.DOTALL)
    if faq_grid_match:
        page = page[:faq_grid_match.start()] + f'<div class="faq-grid">\n{faq_html}\n    </div>\n    <div class="faq-cta">' + page[faq_grid_match.end():]
    page = page.replace('<span class="section-eyebrow">Common Questions</span>', f'<span class="section-eyebrow">{city_esc} Corporate FAQ</span>')
    page = page.replace(
        '<h2 class="section-h2" style="text-align:center">Frequently Asked <em>Questions</em></h2>',
        f'<h2 class="section-h2" style="text-align:center">{city_esc} Corporate Car Service <em>FAQs</em></h2>'
    )

    # ── INTERNAL LINKS ─────────────────────────────────────────────────
    toronto_nearby = (
        '          <a href="mississauga-airport-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Mississauga Airport Limo</a>\n'
        '          <a href="brampton-airport-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Brampton Airport Limo</a>\n'
        '          <a href="vaughan-airport-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Vaughan Airport Limo</a>\n'
        '          <a href="markham-airport-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Markham Airport Limo</a>\n'
        '          <a href="oakville-airport-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Oakville Airport Limo</a>\n'
        '          <a href="richmond-hill-airport-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Richmond Hill Airport Limo</a>\n'
        '          <a href="scarborough-airport-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Scarborough Airport Limo</a>\n'
        '          <a href="hamilton-airport-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Hamilton Airport Limo</a>'
    )
    page = page.replace(toronto_nearby, nearby_links)

    toronto_services = (
        '          <a href="toronto-corporate-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Corporate Car Service Toronto</a>\n'
        '          <a href="toronto-wedding-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Wedding Limo Toronto</a>\n'
        '          <a href="toronto-events-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Events &amp; Concert Limo Toronto</a>\n'
        '          <a href="toronto-hourly-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Hourly Limo Toronto</a>\n'
        '          <a href="toronto-prom-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Prom Limo Toronto</a>'
    )
    page = page.replace(toronto_services, other_services)

    page = page.replace(
        '<span class="cs-interlink-panel-label">Airport Limo Services in Nearby Cities</span>',
        '<span class="cs-interlink-panel-label">Corporate Car Service in Nearby Cities</span>'
    )
    page = page.replace(
        '<span class="cs-interlink-panel-label">Other Limo Services in Toronto</span>',
        f'<span class="cs-interlink-panel-label">Other Limo Services in {city_esc}</span>'
    )

    # ── FLOAT CTA ──────────────────────────────────────────────────────
    page = page.replace(
        '<div class="float-cta-title">Book Your Toronto Airport Transfer</div>',
        f'<div class="float-cta-title">Book {city_esc} Corporate Car Service</div>'
    )
    page = page.replace(
        '<div class="float-cta-sub">Flat rate &middot; No surge &middot; 24/7 dispatch &middot; Flight tracked</div>',
        '<div class="float-cta-sub">Flat rate &middot; Corp. accounts &middot; 24/7 dispatch &middot; Professional</div>'
    )

    # ── FOOTER ─────────────────────────────────────────────────────────
    page = page.replace(
        '<span>Serving Toronto, Mississauga, Vaughan, Oakville and all of Ontario.</span>',
        f'<span>Corporate Car Service {city_esc}, {region_esc} and all of Ontario.</span>'
    )

    return filename, page


def main():
    print("Loading template (toronto-airport-limo.html)...")
    with open("toronto-airport-limo.html", "r", encoding="utf-8") as f:
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
