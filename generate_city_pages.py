#!/usr/bin/env python3
"""
Generator script for Limo4All city airport limo pages.
Uses toronto-airport-limo.html as template + GitHub markdown content.
Run: python generate_city_pages.py
"""

import urllib.request
import re
import os
import html as html_module

BASE_RAW = "https://raw.githubusercontent.com/limo411/Replitlimo2/b97691583f5fd908ba76edb7d2545979f1cf73f3/artifacts/limo4all/src/content/airport-limo/"

CITIES = [
    ("02-mississauga.md",      "mississauga",        "Mississauga",        "Peel Region"),
    ("03-vaughan.md",          "vaughan",             "Vaughan",            "York Region"),
    ("04-oakville.md",         "oakville",            "Oakville",           "Halton Region"),
    ("05-markham.md",          "markham",             "Markham",            "York Region"),
    ("06-hamilton.md",         "hamilton",            "Hamilton",           "Hamilton"),
    ("07-london.md",           "london",              "London",             "Southwestern Ontario"),
    ("08-niagara-falls.md",    "niagara-falls",       "Niagara Falls",      "Niagara Region"),
    ("09-waterloo-kitchener.md","waterloo-kitchener", "Waterloo-Kitchener", "Waterloo Region"),
    ("10-richmond-hill.md",    "richmond-hill",       "Richmond Hill",      "York Region"),
    ("11-brampton.md",         "brampton",            "Brampton",           "Peel Region"),
    ("12-aurora.md",           "aurora",              "Aurora",             "York Region"),
    ("13-king-city.md",        "king-city",           "King City",          "King Township"),
    ("14-burlington.md",       "burlington",          "Burlington",         "Halton Region"),
    ("15-milton.md",           "milton",              "Milton",             "Halton Region"),
    ("16-guelph.md",           "guelph",              "Guelph",             "Wellington County"),
]

# Internal link data per city: [nearby_same_service, other_services_same_city]
NEARBY_CITIES = {
    "mississauga":        ["toronto", "brampton", "oakville", "etobicoke", "burlington"],
    "vaughan":            ["toronto", "richmond-hill", "markham", "aurora", "king-city"],
    "oakville":           ["mississauga", "burlington", "toronto", "milton", "brampton"],
    "markham":            ["toronto", "richmond-hill", "vaughan", "scarborough", "aurora"],
    "hamilton":           ["burlington", "oakville", "mississauga", "niagara-falls", "toronto"],
    "london":             ["guelph", "waterloo-kitchener", "hamilton", "toronto", "milton"],
    "niagara-falls":      ["hamilton", "burlington", "oakville", "toronto", "mississauga"],
    "waterloo-kitchener": ["guelph", "london", "hamilton", "toronto", "mississauga"],
    "richmond-hill":      ["vaughan", "markham", "aurora", "toronto", "king-city"],
    "brampton":           ["mississauga", "toronto", "vaughan", "etobicoke", "oakville"],
    "aurora":             ["richmond-hill", "vaughan", "king-city", "markham", "toronto"],
    "king-city":          ["aurora", "vaughan", "richmond-hill", "toronto", "markham"],
    "burlington":         ["oakville", "hamilton", "mississauga", "niagara-falls", "milton"],
    "milton":             ["oakville", "brampton", "burlington", "mississauga", "guelph"],
    "guelph":             ["waterloo-kitchener", "cambridge", "hamilton", "burlington", "london"],
}

CITY_NAMES = {slug: name for _, slug, name, _ in CITIES}
CITY_NAMES["toronto"] = "Toronto"
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
    """Escape text for HTML."""
    return (text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
        .replace("—", "&mdash;")
        .replace("–", "&ndash;")
        .replace("'", "&rsquo;")
        .replace("'", "&lsquo;")
        .replace(""", "&ldquo;")
        .replace(""", "&rdquo;")
    )

def paragraphs_to_html(text_block):
    """Convert plain text paragraphs to <p> tags."""
    paras = [p.strip() for p in text_block.strip().split("\n\n") if p.strip()]
    result = []
    for p in paras:
        # Skip lines that are headings or bullet lists
        if p.startswith("#") or p.startswith("-") or p.startswith("*"):
            continue
        # Join multi-line paragraph
        p_clean = " ".join(l.strip() for l in p.split("\n") if not l.strip().startswith("#"))
        if p_clean:
            result.append(f'<p class="cs-svc-card-text">{esc(p_clean)}</p>')
    return "\n            ".join(result)

def extract_bullets(text_block):
    """Extract bullet list items from markdown block."""
    bullets = []
    for line in text_block.split("\n"):
        line = line.strip()
        if line.startswith("- ") or line.startswith("* "):
            bullets.append(line[2:].strip())
    return bullets

def extract_section(md, heading):
    """Extract text between a heading and the next same-level or higher heading."""
    # Match from heading to next ## or ### or end
    level = len(re.match(r'^(#+)', heading.strip()).group(1)) if re.match(r'^(#+)', heading.strip()) else 2
    pattern = re.escape(heading.strip())
    # Find heading position
    match = re.search(pattern, md, re.IGNORECASE)
    if not match:
        return ""
    start = match.end()
    # Find next heading of same or higher level
    next_heading = re.search(r'\n#{1,' + str(level) + r'} ', md[start:])
    if next_heading:
        end = start + next_heading.start()
    else:
        end = len(md)
    return md[start:end].strip()

def extract_faq(md):
    """Extract FAQ Q&A pairs from markdown."""
    faq_section = extract_section(md, "## Frequently Asked Questions")
    if not faq_section:
        return []
    pairs = []
    lines = faq_section.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line and not line.startswith("#") and not line.startswith("-") and not line.startswith("*") and len(line) > 20:
            # Could be a question
            q = line
            # Next non-empty line(s) are the answer
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
    return pairs[:12]  # max 12 FAQs

def extract_intro_paragraphs(md):
    """Extract intro paragraphs after the H3 subtitle."""
    # After "### Limo4All Transportation: Providing Luxury..."
    section = extract_section(md, "### Limo4All Transportation")
    if not section:
        # Try after H1
        section = extract_section(md, "# Airport Limo")
    paras = []
    for block in section.split("\n\n"):
        block = block.strip()
        if block and not block.startswith("#") and not block.startswith("-"):
            lines = [l.strip() for l in block.split("\n") if not l.strip().startswith("#")]
            text = " ".join(l for l in lines if l)
            if len(text) > 50:
                paras.append(text)
        if len(paras) >= 3:
            break
    return paras[:3]

def extract_card_body(md, heading):
    """Extract the body text for a service card."""
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

def extract_neighborhoods(md):
    """Extract neighborhood list from service areas section."""
    section = extract_section(md, "## " + "Airport Limo & Transfer Service Areas") or \
              extract_section(md, "## Hamilton Airport Limo") or ""
    # Try to find "Neighbourhoods" bullet list
    nbhd_match = re.search(r'Neighbourhood[s]? and areas[^:]*:(.*?)(?:Airports we service|$)', section, re.DOTALL | re.IGNORECASE)
    if nbhd_match:
        return extract_bullets(nbhd_match.group(1))
    # Fallback: just get all bullets
    return extract_bullets(section)[:10]

def extract_why_items(md):
    """Extract why-section bullet items."""
    section = extract_section(md, "## Why Limo4All Transportation")
    # Find "Here is what you get" list
    list_match = re.search(r'Here is what you get[^:]*:(.*?)$', section, re.DOTALL | re.IGNORECASE)
    if list_match:
        bullets = extract_bullets(list_match.group(1))
    else:
        bullets = extract_bullets(section)
    return bullets[:5]

def extract_why_body(md):
    """Extract why section intro paragraph."""
    section = extract_section(md, "## Why Limo4All Transportation")
    for block in section.split("\n\n"):
        block = block.strip()
        if block and not block.startswith("#") and not block.startswith("-") and len(block) > 60:
            return " ".join(l.strip() for l in block.split("\n") if not l.strip().startswith("#"))
    return ""

def build_faq_html(pairs):
    items = []
    for i, (q, a) in enumerate(pairs):
        items.append(f'''      <div class="faq-item">
        <div class="faq-q">{esc(q)}<svg viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></div>
        <div class="faq-a">{esc(a)}</div>
      </div>''')
    return "\n".join(items)

def build_nbhd_html(neighborhoods, slug):
    """Build the neighborhoods/cities area grid."""
    if not neighborhoods:
        neighborhoods = [f"{slug.replace('-', ' ').title()} Downtown", f"{slug.replace('-', ' ').title()} Central", "Greater Area"]
    rows = []
    for nbhd in neighborhoods[:10]:
        rows.append(f'      <div class="cs-nbhd-card"><div class="cs-nbhd-name">{esc(nbhd)}</div><div class="cs-nbhd-type">Service Area</div></div>')
    return "\n".join(rows)

def build_card1_aside_bullets_html(neighborhoods, city_name):
    """Build Card 1 aside bullets: city neighborhoods + 2 fixed service bullets."""
    bullets = []
    for nbhd in neighborhoods[:5]:
        bullets.append(f'              <li class="cs-svc-card-bullet">{esc(nbhd)}</li>')
    bullets.append('              <li class="cs-svc-card-bullet">Real-time flight tracking for every booking</li>')
    bullets.append('              <li class="cs-svc-card-bullet">Flat rates &mdash; no surge pricing</li>')
    return "\n".join(bullets)

def build_nearby_links_html(slug):
    """Build nearby same-service city links."""
    nearby = NEARBY_CITIES.get(slug, ["toronto", "mississauga", "brampton", "vaughan", "oakville"])
    links = []
    for n in nearby[:8]:
        name = CITY_NAMES.get(n, n.replace("-", " ").title())
        links.append(f'          <a href="{n}-airport-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>{esc(name)} Airport Limo</a>')
    return "\n".join(links)

def build_other_services_html(city_name, slug):
    """Build other services in the same city links."""
    services = [
        ("wedding-limo", "Wedding Limo"),
        ("corporate-limo", "Corporate Limo"),
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

def build_why_items_html(bullets):
    items = []
    for b in bullets[:5]:
        # First bold phrase (up to first period or comma)
        parts = b.split(" ", 4)
        if len(parts) >= 3:
            # Try to identify a strong lead phrase
            strong_end = b.find(" — ")
            if strong_end > 0:
                strong = b[:strong_end]
                rest = b[strong_end+3:]
            elif "," in b[:50]:
                comma = b.index(",")
                strong = b[:comma]
                rest = b[comma+1:].strip()
            else:
                words = b.split()
                strong = " ".join(words[:3])
                rest = " ".join(words[3:])
        else:
            strong = b
            rest = ""
        items.append(f'''        <div class="cs-why-item">
          <div class="cs-why-item-text"><strong>{esc(strong.strip())}</strong>{esc(rest.strip())}</div>
        </div>''')
    return "\n".join(items)

def build_intro_paras_html(paras):
    return "\n          ".join(f"<p>{esc(p)}</p>" for p in paras)

def build_svc_card_paras(paras):
    return "\n            ".join(f'<p class="cs-svc-card-text">{esc(p)}</p>' for p in paras)

def generate_page(template, slug, city_name, region, md):
    city_slug_html = slug  # e.g. "mississauga"
    filename = f"{slug}-airport-limo.html"
    city_name_esc = esc(city_name)
    region_esc = esc(region)

    # Parse markdown content
    intro_paras = extract_intro_paragraphs(md)
    card1_paras = extract_card_body(md, "### Airport Limo & Transfer Service Near Me")
    card2_paras = extract_card_body(md, "### Personal Travel")
    card2_bullets = extract_bullets(extract_section(md, "### Personal Travel"))[:7]
    card3_paras = extract_card_body(md, "### Business Travel")
    card3_bullets = extract_bullets(extract_section(md, "### Business Travel"))[:6]
    neighborhoods = extract_neighborhoods(md)
    why_body = extract_why_body(md)
    why_items = extract_why_items(md)
    faq_pairs = extract_faq(md)

    # Ensure minimum content
    if not intro_paras:
        intro_paras = [
            f"{city_name} residents and visitors deserve premium airport transportation that is reliable, professional, and stress-free. Limo4All Transportation provides luxury airport limo and transfer services throughout {city_name}, connecting passengers to Toronto Pearson International Airport and beyond.",
            f"Our professional chauffeurs arrive on time, assist with luggage, and take the most efficient route so you never have to worry about making your flight. Real-time flight tracking ensures every pickup is perfectly timed to your actual arrival.",
            f"From the moment you book to the moment you arrive, every detail is handled — because that is what true luxury transportation looks like in {city_name}.",
        ]
    if not card1_paras:
        card1_paras = [
            f"Finding a reliable airport limo near you in {city_name} should not be a hassle. Limo4All Transportation offers door-to-door service with a fleet of immaculate vehicles and professional chauffeurs who know the region inside and out.",
            f"We handle meet-and-greet at arrivals, luggage assistance, real-time flight monitoring, and the fastest routes through the GTA. Our flat-rate pricing means you always know what you are paying before you book.",
        ]
    if not card2_paras:
        card2_paras = [
            f"Your personal trips deserve more than a standard cab or rideshare. Whether you are jetting off on a vacation, heading home for the holidays, or welcoming family at the airport, Limo4All Transportation makes every personal transfer feel special.",
            f"Our chauffeurs are patient and attentive. Child car seats are available upon request so your youngest travellers are always safe and comfortable. You will arrive at Toronto Pearson relaxed and on time.",
        ]
    if not card3_paras:
        card3_paras = [
            f"{city_name}'s business community moves fast, and your airport transfer should keep up. Limo4All Transportation's corporate transfer service is built around punctuality, professionalism, and discretion.",
            f"Vehicles are equipped with Wi-Fi and charging ports so you can stay connected on the way to or from Toronto Pearson. We support corporate accounts and recurring bookings for businesses across the region.",
        ]
    if not card2_bullets:
        card2_bullets = ["Vacations and getaways", "Family visits and reunions", "Holiday travel", "Moving trips", "Special occasions and celebrations", "Sporting and cultural events", "Airport pickup and drop-off"]
    if not card3_bullets:
        card3_bullets = ["Business trips and executive travel", "Professional seminars", "Conferences and trade shows", "Corporate retreats", "Client pickups and drop-offs", "Local business corridors"]
    if not neighborhoods:
        neighborhoods = [f"{city_name} Downtown", f"{city_name} Central", f"{city_name} East", f"{city_name} West", f"{city_name} North", f"{city_name} South"]
    if not why_items:
        why_items = [
            f"Deep {city_name} Market Familiarity — deep familiarity with {city_name}'s communities and the key corridors connecting to Toronto Pearson Airport.",
            "A Luxury Fleet for Every Group — sedans, SUVs, and stretch limousines maintained to the highest standards.",
            "Proven On-Time Record — on-time performance on the GTA's most demanding routes, day and night.",
            "Professional Background-Checked Chauffeurs — trained in the complex terminal and urban pickup logistics.",
            "Easy Online Booking, Transparent Pricing — instant confirmation and flat-rate pricing with no surprises.",
        ]
    if not faq_pairs:
        faq_pairs = [
            (f"How far in advance should I book an airport limo in {city_name}?", f"We recommend booking at least 24 hours in advance to secure your preferred vehicle. Limo4All Transportation also accommodates last-minute bookings based on availability."),
            (f"Do you offer flat-rate airport limo pricing from {city_name}?", f"Yes. All Limo4All Transportation airport transfers from {city_name} are priced at a flat rate confirmed at booking. No surge charges, no hidden fees."),
            (f"What if my flight is delayed?", f"We monitor all flights in real time. If your flight is delayed, your chauffeur automatically adjusts the pickup time at no extra charge."),
            (f"Do you serve all areas of {city_name}?", f"Yes. Limo4All Transportation provides airport limo service throughout all {city_name} neighbourhoods and communities. We come to your door."),
            (f"What vehicles do you offer?", f"Our fleet includes executive sedans, luxury SUVs, and Mercedes Sprinter vans. All vehicles are fully licensed, insured, and maintained."),
            (f"How do I find my driver at Toronto Pearson?", f"Your chauffeur will be in the arrivals area with a name sign. You will also receive your driver's contact details and vehicle information before landing."),
        ]
    if not why_body:
        why_body = f"{city_name} has no shortage of transportation options, but Limo4All Transportation stands apart through consistent quality, genuine professionalism, and a team that truly cares about your experience."

    # Build HTML blocks
    intro_html = "\n          ".join(f"<p>{esc(p)}</p>" for p in intro_paras)
    c1_paras_html = "\n            ".join(f'<p class="cs-svc-card-text">{esc(p)}</p>' for p in card1_paras)
    c2_paras_html = "\n            ".join(f'<p class="cs-svc-card-text">{esc(p)}</p>' for p in card2_paras)
    c3_paras_html = "\n            ".join(f'<p class="cs-svc-card-text">{esc(p)}</p>' for p in card3_paras)
    c2_bullets_html = "\n              ".join(f'<li class="cs-svc-card-bullet">{esc(b)}</li>' for b in card2_bullets)
    c3_bullets_html = "\n              ".join(f'<li class="cs-svc-card-bullet">{esc(b)}</li>' for b in card3_bullets)
    card1_aside_bullets = build_card1_aside_bullets_html(neighborhoods, city_name)
    nbhd_html = build_nbhd_html(neighborhoods, slug)
    why_items_html = build_why_items_html(why_items)
    faq_html = build_faq_html(faq_pairs)
    nearby_links = build_nearby_links_html(slug)
    other_services = build_other_services_html(city_name, slug)

    # Now do substitutions on the template
    page = template

    # --- META / HEAD ---
    page = page.replace(
        '<title>Airport Limo &amp; Transfers Toronto | Flat Rate | Limo4All</title>',
        f'<title>Airport Limo &amp; Transfers {city_name_esc} | Flat Rate | Limo4All</title>'
    )
    page = page.replace(
        'content="Toronto\'s #1 airport limo service. Professional chauffeurs, flat rates, 24/7 availability. Serving YYZ, YTZ, YHM and BUF airports across the GTA. Book online or call 1-800-XXX-XXXX."',
        f'content="{city_name_esc}\'s #1 airport limo service. Professional chauffeurs, flat rates, 24/7 availability. Serving YYZ, YTZ, YHM and BUF airports from {city_name_esc} and the GTA. Book online or call 1-800-XXX-XXXX."'
    )
    page = page.replace(
        'href="https://www.limo4all.ca/toronto-airport-limo.html"',
        f'href="https://www.limo4all.ca/{slug}-airport-limo.html"'
    )

    # Schema JSON-LD
    page = page.replace(
        '"name":"Airport Limo & Transfers Toronto"',
        f'"name":"Airport Limo & Transfers {city_name}"'
    )
    page = page.replace(
        '"description":"Professional airport limo and chauffeur service in Toronto and the GTA. Flat rates, 24/7 availability, serving YYZ, YTZ, YHM and BUF airports."',
        f'"description":"Professional airport limo and chauffeur service in {city_name} and the GTA. Flat rates, 24/7 availability, serving YYZ, YTZ, YHM and BUF airports."'
    )
    page = page.replace(
        '"name":"Toronto"}}',
        f'"name":"{city_name}"}}'
    )
    city_schema_name = city_name
    page = page.replace(
        '"name":"Toronto"},"serviceType"',
        '"name":"' + city_schema_name + '"},"serviceType"'
    )
    # Breadcrumb schema
    page = page.replace(
        '"name":"Toronto Airport Limo","item":"https://www.limo4all.ca/toronto-airport-limo.html"',
        f'"name":"{city_name} Airport Limo","item":"https://www.limo4all.ca/{slug}-airport-limo.html"'
    )

    # --- BREADCRUMB ---
    page = page.replace(
        '<span class="bc-current">Toronto</span>',
        f'<span class="bc-current">{city_name_esc}</span>'
    )
    page = page.replace(
        "<span>Toronto&rsquo;s #1 Airport Limo</span>",
        f"<span>{city_name_esc}&rsquo;s #1 Airport Limo</span>"
    )

    # --- HERO ---
    page = page.replace(
        '<span class="cs-eyebrow"><span class="cs-eyebrow-dot"></span> Toronto Airport Transfer</span>',
        f'<span class="cs-eyebrow"><span class="cs-eyebrow-dot"></span> {city_name_esc} Airport Transfer</span>'
    )
    page = page.replace(
        '<h1 class="cs-h1">Airport Limo &amp; Transfers<strong>in Toronto</strong></h1>',
        f'<h1 class="cs-h1">Airport Limo &amp; Transfers<strong>in {city_name_esc}</strong></h1>'
    )
    page = page.replace(
        '<p class="cs-sub">Professional, flat-rate airport limo service serving all of Toronto and the GTA. Available 24/7 &mdash; never miss a flight, never wait at arrivals.</p>',
        f'<p class="cs-sub">Professional, flat-rate airport limo service serving all of {city_name_esc} and the GTA. Available 24/7 &mdash; never miss a flight, never wait at arrivals.</p>'
    )

    # --- INTRO ---
    page = page.replace(
        '<span class="section-eyebrow">Best Ontario Airport Limo &amp; Transfer Service</span>',
        f'<span class="section-eyebrow">Best {city_name_esc} Airport Limo &amp; Transfer Service</span>'
    )
    page = page.replace(
        '<p>Toronto is one of Canada&rsquo;s most vibrant and fast-moving cities, and getting to or from the airport should never add stress to your journey. Limo4All Transportation provides premium airport limousine and transfer services across Toronto, connecting passengers reliably to Toronto Pearson International Airport, Billy Bishop Toronto City Airport, and beyond.</p>\n          <p>Our professional chauffeurs arrive on time, handle your luggage, and take the most efficient route so you never have to think twice about making your flight. We track your flight in real time and adjust pickups for delays or early arrivals, giving you one less thing to worry about.</p>\n          <p>From the moment you book to the moment you arrive, every detail is taken care of &mdash; because that is what true luxury transportation looks like in Toronto.</p>',
        intro_html
    )

    # --- SERVICES ---
    # Card 1 body paragraphs
    page = page.replace(
        '<p class="cs-svc-card-text">Finding a reliable airport limo near you in Toronto should not be a hassle. Limo4All Transportation offers door-to-door service with a fleet of immaculate vehicles and professional chauffeurs who know the city inside and out.</p>\n            <p class="cs-svc-card-text">We handle everything including meet-and-greet at arrivals, luggage assistance, real-time flight monitoring, and the fastest routes through Toronto&rsquo;s busy corridors. Our flat-rate pricing means you always know what you are paying before you book, with no surge pricing or hidden fees.</p>\n            <p class="cs-svc-card-text">Whether you are travelling from downtown Toronto, Yorkville, the Distillery District, or anywhere across the city, we come to you and get you there in comfort and style.</p>',
        c1_paras_html
    )
    # Card 2 body paragraphs
    page = page.replace(
        '<p class="cs-svc-card-text">Your personal trips deserve more than a standard cab or rideshare. Whether you are jetting off on a vacation, heading home for the holidays, or welcoming family at the airport, Limo4All Transportation makes every personal transfer feel special.</p>\n            <p class="cs-svc-card-text">Our chauffeurs are patient, attentive, and happy to assist with extra luggage, young children, or elderly passengers. Child car seats are available upon request so your youngest travellers are always safe and comfortable. You will arrive at Toronto Pearson relaxed and on time, with no parking headaches or last-minute scrambles.</p>',
        c2_paras_html
    )
    # Card 1 aside sub-label
    page = page.replace(
        '<span class="sub-label">Toronto Neighborhoods We Serve</span>',
        f'<span class="sub-label">{city_name_esc} Neighborhoods We Serve</span>'
    )
    # Card 1 aside bullets
    page = page.replace(
        '''<li class="cs-svc-card-bullet">Downtown Core &amp; Financial District</li>
              <li class="cs-svc-card-bullet">Yorkville, Rosedale &amp; Forest Hill</li>
              <li class="cs-svc-card-bullet">North York &amp; Scarborough</li>
              <li class="cs-svc-card-bullet">Etobicoke &amp; West Toronto</li>
              <li class="cs-svc-card-bullet">East York &amp; The Beaches</li>
              <li class="cs-svc-card-bullet">Real-time flight tracking for every booking</li>
              <li class="cs-svc-card-bullet">Flat rates &mdash; no surge pricing</li>''',
        card1_aside_bullets
    )
    # Card 1 callout: flat rate city name
    page = page.replace(
        'Starting flat rate from Toronto',
        f'Starting flat rate from {city_name}'
    )

    # Card 2 aside bullets
    page = page.replace(
        '''<li class="cs-svc-card-bullet">Vacations and getaways</li>
              <li class="cs-svc-card-bullet">Family visits and reunions</li>
              <li class="cs-svc-card-bullet">Holiday travel</li>
              <li class="cs-svc-card-bullet">Moving trips</li>
              <li class="cs-svc-card-bullet">Special occasions and celebrations</li>
              <li class="cs-svc-card-bullet">Toronto Maple Leafs, Raptors, and Blue Jays game day transportation</li>
              <li class="cs-svc-card-bullet">TIFF and cultural event travel across the city</li>''',
        c2_bullets_html
    )
    # Card 3 body paragraphs
    page = page.replace(
        '<p class="cs-svc-card-text">Toronto&rsquo;s corporate community moves fast, and your airport transfer should keep up. Limo4All Transportation&rsquo;s business travel service is built around punctuality, professionalism, and discretion. Our chauffeurs are formally dressed, well-mannered, and familiar with the city&rsquo;s key business corridors.</p>\n            <p class="cs-svc-card-text">Vehicles are equipped with Wi-Fi and charging ports so you can stay connected and productive on the way to or from Toronto Pearson. We also accommodate recurring bookings and multi-passenger corporate accounts, making us the preferred transfer partner for companies across the GTA.</p>',
        c3_paras_html
    )
    # Card 3 aside bullets
    page = page.replace(
        '''<li class="cs-svc-card-bullet">Business trips and executive travel</li>
              <li class="cs-svc-card-bullet">Professional seminars</li>
              <li class="cs-svc-card-bullet">Conferences and trade shows</li>
              <li class="cs-svc-card-bullet">Corporate retreats</li>
              <li class="cs-svc-card-bullet">Client pickups and drop-offs</li>
              <li class="cs-svc-card-bullet">Bay Street financial district and TIFF industry event travel</li>''',
        c3_bullets_html
    )

    # --- BENEFITS heading ---
    page = page.replace(
        '<span class="section-eyebrow">Toronto Airport Limo &amp; Transfer Benefits</span>',
        f'<span class="section-eyebrow">{city_name_esc} Airport Limo &amp; Transfer Benefits</span>'
    )
    page = page.replace(
        '<h2 class="section-h2" style="text-align:center">The Advantages of<strong>Airport Limo &amp; Transfers</strong></h2>',
        f'<h2 class="section-h2" style="text-align:center">The Advantages of<strong>{city_name_esc} Airport Limo &amp; Transfers</strong></h2>'
    )

    # --- WHY SECTION ---
    page = page.replace(
        '<span class="cs-why-pre">Best Airport Limo &amp; Transfer Service Near Me</span>',
        f'<span class="cs-why-pre">Best {city_name_esc} Airport Limo &amp; Transfer Service</span>'
    )
    page = page.replace(
        '<p class="cs-why-body">Toronto has no shortage of transportation options, but Limo4All Transportation stands apart through consistent quality, genuine professionalism, and a team that truly cares about your experience. We have built our reputation one ride at a time, and every booking reflects our commitment to getting it right.</p>\n        <p class="cs-why-body">Do not leave your airport transfer to chance. Limo4All Transportation is available around the clock to get you to Toronto Pearson International Airport, Billy Bishop, or Hamilton International safely, comfortably, and on time.</p>',
        f'<p class="cs-why-body">{esc(why_body)}</p>\n        <p class="cs-why-body">Do not leave your airport transfer to chance. Limo4All Transportation is available around the clock to get you to Toronto Pearson International Airport and beyond safely, comfortably, and on time.</p>'
    )
    # Why list items
    why_toronto_items = '''        <div class="cs-why-item">
          <div class="cs-why-item-text"><strong>Deep Toronto Market Familiarity</strong>Deep familiarity with Toronto&rsquo;s Financial District, Yorkville, North York, Etobicoke, Scarborough, and every GTA corridor connecting to Toronto Pearson and Billy Bishop airports.</div>
        </div>
        <div class="cs-why-item">
          <div class="cs-why-item-text"><strong>A Luxury Fleet for Every Group</strong>A luxury fleet including sedans, SUVs, and stretch limousines, maintained to the highest standards for comfort and reliability.</div>
        </div>
        <div class="cs-why-item">
          <div class="cs-why-item-text"><strong>Proven On-Time Record</strong>A proven on-time record on the DVP, Gardiner Expressway, and Highway 401 &mdash; Toronto&rsquo;s most demanding routes, day and night.</div>
        </div>
        <div class="cs-why-item">
          <div class="cs-why-item-text"><strong>Professional Background-Checked Chauffeurs</strong>Professional, background-checked chauffeurs trained in Toronto&rsquo;s complex terminal and urban pickup logistics.</div>
        </div>
        <div class="cs-why-item">
          <div class="cs-why-item-text"><strong>Easy Online Booking, Transparent Pricing</strong>Easy online booking with instant confirmation and transparent flat-rate pricing. Lock in your fare today and travel without surprises.</div>
        </div>'''
    page = page.replace(why_toronto_items, why_items_html)

    # --- SERVICE AREAS ---
    page = page.replace(
        '<span class="section-eyebrow">Coverage</span>',
        f'<span class="section-eyebrow">{city_name_esc} Coverage</span>'
    )
    page = page.replace(
        '<h2 class="section-h2" style="text-align:center">Toronto Airport Limo<strong>&amp; Transfer Service Areas</strong></h2>',
        f'<h2 class="section-h2" style="text-align:center">{city_name_esc} Airport Limo<strong>&amp; Transfer Service Areas</strong></h2>'
    )
    page = page.replace(
        'Limo4All Transportation serves all major Toronto neighbourhoods and communities throughout the Greater Toronto Area. No matter where you are located, we will come to your door and get you to your airport on time.',
        f'Limo4All Transportation serves all major {city_name} neighbourhoods and communities throughout {region}. No matter where you are located, we will come to your door and get you to your airport on time.'
    )
    page = page.replace(
        '<span class="sub-label">Airport Limo Services in Nearby Cities</span>',
        f'<span class="sub-label">Airport Limo Services in {city_name_esc} &amp; Nearby Cities</span>'
    )
    # Replace neighborhood grid
    toronto_nbhd = '''      <a href="mississauga-airport-limo.html" class="cs-nbhd-card"><div class="cs-nbhd-name">Mississauga Airport Limo</div><div class="cs-nbhd-type">Peel Region</div></a>
      <a href="brampton-airport-limo.html" class="cs-nbhd-card"><div class="cs-nbhd-name">Brampton Airport Limo</div><div class="cs-nbhd-type">Peel Region</div></a>
      <a href="vaughan-airport-limo.html" class="cs-nbhd-card"><div class="cs-nbhd-name">Vaughan Airport Limo</div><div class="cs-nbhd-type">York Region</div></a>
      <a href="markham-airport-limo.html" class="cs-nbhd-card"><div class="cs-nbhd-name">Markham Airport Limo</div><div class="cs-nbhd-type">York Region</div></a>
      <a href="oakville-airport-limo.html" class="cs-nbhd-card"><div class="cs-nbhd-name">Oakville Airport Limo</div><div class="cs-nbhd-type">Halton Region</div></a>
      <a href="richmond-hill-airport-limo.html" class="cs-nbhd-card"><div class="cs-nbhd-name">Richmond Hill Airport Limo</div><div class="cs-nbhd-type">York Region</div></a>
      <a href="scarborough-airport-limo.html" class="cs-nbhd-card"><div class="cs-nbhd-name">Scarborough Airport Limo</div><div class="cs-nbhd-type">East Toronto</div></a>
      <a href="north-york-airport-limo.html" class="cs-nbhd-card"><div class="cs-nbhd-name">North York Airport Limo</div><div class="cs-nbhd-type">Central Toronto</div></a>
      <a href="etobicoke-airport-limo.html" class="cs-nbhd-card"><div class="cs-nbhd-name">Etobicoke Airport Limo</div><div class="cs-nbhd-type">West Toronto</div></a>
      <a href="hamilton-airport-limo.html" class="cs-nbhd-card"><div class="cs-nbhd-name">Hamilton Airport Limo</div><div class="cs-nbhd-type">Hamilton Area</div></a>'''
    nearby = NEARBY_CITIES.get(slug, ["toronto", "mississauga", "brampton", "vaughan", "oakville"])
    new_nbhd_rows = []
    for nb in nearby[:5]:
        nb_name = CITY_NAMES.get(nb, nb.replace("-", " ").title())
        new_nbhd_rows.append(f'      <a href="{nb}-airport-limo.html" class="cs-nbhd-card"><div class="cs-nbhd-name">{esc(nb_name)} Airport Limo</div><div class="cs-nbhd-type">Airport Limo Service</div></a>')
    # Also add local neighborhoods (non-linked)
    for nbhd in neighborhoods[:5]:
        new_nbhd_rows.append(f'      <div class="cs-nbhd-card"><div class="cs-nbhd-name">{esc(nbhd)}</div><div class="cs-nbhd-type">{city_name_esc}</div></div>')
    page = page.replace(toronto_nbhd, "\n".join(new_nbhd_rows))

    # --- SPEAK SECTION ---
    page = page.replace(
        '<span class="speak-pre">Contact Us for Toronto Airport Limo &amp; Transfers</span>',
        f'<span class="speak-pre">Contact Us for {city_name_esc} Airport Limo &amp; Transfers</span>'
    )
    page = page.replace(
        "Toronto's most trusted airport limo service is ready when you are",
        f"{city_name}'s most trusted airport limo service is ready when you are"
    )

    # --- FAQ ---
    # Replace FAQ section content
    toronto_faq_start = '    <div class="faq-grid">\n      <div class="faq-item">\n        <div class="faq-q">How far in advance should I book an airport limo in Toronto?'
    city_faq_start = f'    <div class="faq-grid">\n{faq_html}'
    # Find and replace FAQ grid content
    faq_grid_match = re.search(
        r'(<div class="faq-grid">)(.*?)(</div>\s*<div class="faq-cta">)',
        page, re.DOTALL
    )
    if faq_grid_match:
        page = page[:faq_grid_match.start()] + f'<div class="faq-grid">\n{faq_html}\n    </div>\n    <div class="faq-cta">' + page[faq_grid_match.end():]

    # FAQ heading
    page = page.replace(
        '<h2 class="section-h2" style="text-align:center">Frequently Asked <em>Questions</em></h2>',
        f'<h2 class="section-h2" style="text-align:center">{city_name_esc} Airport Limo <em>FAQs</em></h2>'
    )

    # --- INTERNAL LINKS ---
    # Replace nearby cities links
    toronto_nearby = '''          <a href="mississauga-airport-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Mississauga Airport Limo</a>
          <a href="brampton-airport-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Brampton Airport Limo</a>
          <a href="vaughan-airport-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Vaughan Airport Limo</a>
          <a href="markham-airport-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Markham Airport Limo</a>
          <a href="oakville-airport-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Oakville Airport Limo</a>
          <a href="richmond-hill-airport-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Richmond Hill Airport Limo</a>
          <a href="scarborough-airport-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Scarborough Airport Limo</a>
          <a href="hamilton-airport-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Hamilton Airport Limo</a>'''
    page = page.replace(toronto_nearby, nearby_links)

    toronto_services = '''          <a href="toronto-wedding-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Wedding Limo Toronto</a>
          <a href="toronto-corporate-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Corporate Limo Toronto</a>
          <a href="toronto-prom-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Prom Limo Toronto</a>
          <a href="toronto-events-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Events &amp; Concert Limo Toronto</a>
          <a href="toronto-hourly-limo.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Hourly Limo Toronto</a>
          <a href="toronto-niagara-tours.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Niagara Falls Tours from Toronto</a>
          <a href="toronto-sprinter-van.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>Sprinter Van Service Toronto</a>
          <a href="toronto-city-transfers.html" class="cs-interlink-link"><span class="cs-interlink-link-arrow">\u2192</span>City-to-City Transfers Toronto</a>'''
    page = page.replace(toronto_services, other_services)

    # Update interlink panel label for services
    page = page.replace(
        '<span class="cs-interlink-panel-label">Other Limo Services in Toronto</span>',
        f'<span class="cs-interlink-panel-label">Other Limo Services in {city_name_esc}</span>'
    )
    # Update nearby cities panel label
    page = page.replace(
        '<span class="cs-interlink-panel-label">Airport Limo Services in Nearby Cities</span>',
        f'<span class="cs-interlink-panel-label">Airport Limo Services Near {city_name_esc}</span>'
    )

    # --- FLOAT CTA ---
    page = page.replace(
        '<div class="float-cta-title">Book Your Toronto Airport Transfer</div>',
        f'<div class="float-cta-title">Book Your {city_name_esc} Airport Transfer</div>'
    )

    # --- CANONICAL URL in breadcrumb href (booking) ---
    # airport.html nav active link (keep as-is since toronto page had it active)

    return filename, page


def main():
    print("Loading template...")
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
