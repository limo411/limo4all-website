#!/usr/bin/env python3
"""
Generate all hub pages from AirportHUB.html as the design base.
Run: python generate_hubs.py
"""
import re, os

BASE = os.path.dirname(os.path.abspath(__file__))

def read(name):
    with open(os.path.join(BASE, name), encoding="utf-8") as f:
        return f.read()

def write(name, content):
    with open(os.path.join(BASE, name), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Written: {name}")

def r(page, old, new):
    if old in page:
        return page.replace(old, new)
    print(f"  WARN: pattern not found — {old[:80]!r}")
    return page

# ─────────────────────────────────────────────────────────────
# Base for new hubs
# ─────────────────────────────────────────────────────────────
base = read("AirportHUB.html")
base = base.replace("1-800-XXX-XXXX", "416 451 3106")
base = base.replace("tel:+18001234567", "tel:+14164513106")
base = base.replace("sms:+18001234567", "sms:+16473131786")
base = base.replace("<" + "\\strong>", "</strong>")

# ─────────────────────────────────────────────────────────────
# Helper: build service cards HTML using airport-card CSS
# ─────────────────────────────────────────────────────────────
def svc_card(icon_svg, title, subtitle, features, price_label, price_val, link_text):
    feats_html = "".join(
        f'<span class="airport-feat">{f}</span>' for f in features
    )
    return f'''      <div class="airport-card" style="cursor:auto">
        <div class="airport-card-head">
          <div class="airport-iata-wrap">
            <div style="width:52px;height:52px;display:flex;align-items:center;justify-content:center">{icon_svg}</div>
          </div>
          <div class="airport-head-info">
            <div class="airport-name">{title}</div>
            <div class="airport-location">{subtitle}</div>
          </div>
        </div>
        <div class="airport-card-body">
          <div class="airport-features">{feats_html}</div>
          <div class="airport-pricing">
            <span class="airport-from">{price_label}</span>
            <span class="airport-price-val">{price_val}</span>
            <a href="booking.html" class="airport-arrow">{link_text} &rarr;</a>
          </div>
        </div>
      </div>'''


# ─────────────────────────────────────────────────────────────
# Core make_hub() function
# ─────────────────────────────────────────────────────────────
def make_hub(
    filename, active_nav,
    title, meta_desc, schema_name, schema_type,
    promo_bar_content,
    ticker_items,
    breadcrumb_label, hero_pills, hero_h1_line1, hero_h1_line2, hero_sub,
    hbc_title, hbc_select_options,
    stats_bar_no1_text, stats_bar_label,
    why_pre, why_h2,
    why_tabs,        # list of (h4, p) tuples — 5 items
    why_panels,      # list of (h3, p, [bullets], proof) tuples — 5 items
    why_cta_text,
    seamless_h2, seamless_sub,
    fleet_h2, fleet_sub,
    services_section_html,   # replaces <!-- AIRPORTS SERVED --> to <!-- REVIEWS SPOTLIGHT -->
    faq_label, faq_h2, faq_items,
    speak_pre, speak_h2_html, speak_sub,
    float_badge, float_title, float_sub, float_trust,
):
    page = base

    # ── Nav active ──────────────────────────────────────────────
    page = page.replace('href="AirportHUB.html" class="active"', 'href="AirportHUB.html"')
    page = r(page, f'href="{active_nav}"', f'href="{active_nav}" class="active"')

    # ── Title / meta / schema ───────────────────────────────────
    page = r(page,
        'Airport Limo Toronto &ndash; Flat Rates from $75 | Limo4All',
        title)
    page = r(page,
        'Professional airport limo service to Toronto Pearson (YYZ), Billy Bishop (YTZ) and all GTA airports. Flat rates, real-time flight tracking, meet-and-greet. Book online or call.',
        meta_desc)
    page = r(page, '"name":"Airport Limo Toronto"', f'"name":"{schema_name}"')
    page = r(page, '"serviceType":"Airport Limousine Transfer"', f'"serviceType":"{schema_type}"')

    # ── Promo bar ────────────────────────────────────────────────
    page = r(page,
        '<strong>Flat-Rate Airport Transfers &mdash; No Surge Pricing Ever.</strong>&nbsp; Toronto from $75 &nbsp;&mdash;&nbsp; <a href="tel:+14164513106">Call 416 451 3106</a>',
        promo_bar_content)

    # ── Ticker ───────────────────────────────────────────────────
    doubled = ticker_items + ticker_items
    new_ticker_spans = "\n    ".join(f"<span>{t}</span>" for t in doubled)
    page = re.sub(
        r'<div class="ticker-track">.*?</div>(?=\s*</div>)',
        f'<div class="ticker-track">\n    {new_ticker_spans}\n  </div>',
        page, count=1, flags=re.DOTALL)

    # ── Hero breadcrumb ─────────────────────────────────────────
    page = r(page, '        <span>Airport Limo</span>', f'        <span>{breadcrumb_label}</span>')

    # ── Hero airport pills ──────────────────────────────────────
    old_pills = ('      <div class="hero-airports">\n'
                 '        <span>YYZ</span>\n'
                 '        <span>YTZ</span>\n'
                 '        <span>YHM</span>\n'
                 '        <span>BUF</span>\n'
                 '      </div>')
    new_pills = ('      <div class="hero-airports">\n'
                 + ''.join(f'        <span>{p}</span>\n' for p in hero_pills)
                 + '      </div>')
    page = r(page, old_pills, new_pills)

    # ── Hero h1 ─────────────────────────────────────────────────
    page = r(page,
        '<h1>Airport Transportation<br><strong>Toronto &amp; GTA</strong></h1>',
        f'<h1>{hero_h1_line1}<br><strong>{hero_h1_line2}</strong></h1>')

    # ── Hero sub ─────────────────────────────────────────────────
    page = r(page,
        'Your trusted airport pickup and drop-off partner serving Toronto Pearson (YYZ), Billy Bishop (YTZ), Hamilton (YHM), and Buffalo Niagara (BUF). Flat rates, flight tracking, meet &amp; greet.',
        hero_sub)

    # ── Hero booking card ─────────────────────────────────────────
    page = r(page, '<p class="hbc-title">Book Your Airport Transfer</p>',
             f'<p class="hbc-title">{hbc_title}</p>')
    old_select = ('          <option value="">Select Airport</option>\n'
                  '          <option>Toronto Pearson \u2014 YYZ</option>\n'
                  '          <option>Billy Bishop \u2014 YTZ</option>\n'
                  '          <option>Hamilton \u2014 YHM</option>\n'
                  '          <option>Buffalo Niagara \u2014 BUF</option>')
    page = r(page, old_select, hbc_select_options)

    # ── Stats bar ────────────────────────────────────────────────
    page = r(page,
        '<span class="hs-no1-text">Airport<br>Transfer<br>Service</span>',
        f'<span class="hs-no1-text">{stats_bar_no1_text}</span>')
    # Update "Cheaper Than Taxis" to service-relevant stat
    page = r(page, '40<sup style="font-size:1rem">%</sup></span>\n        <span class="hs-stat-label">Cheaper Than Taxis</span>',
             f'40<sup style="font-size:1rem">%</sup></span>\n        <span class="hs-stat-label">{stats_bar_label}</span>')

    # ── Why section header ───────────────────────────────────────
    page = r(page, '<span class="wh-pre">Why Choose Limo4All For</span>',
             f'<span class="wh-pre">{why_pre}</span>')
    page = r(page, '<h2><em>Airport Transportation Services</em></h2>',
             f'<h2><em>{why_h2}</em></h2>')

    # ── Why tabs (5 items) ───────────────────────────────────────
    airport_why_tabs = [
        ("Real-Time Flight Tracking", "Auto-adjusts for delays \u2014 no calls needed from you."),
        ("Flat Rate. Locked at Booking.", "No surge pricing \u2014 ever. Price confirmed instantly."),
        ("Meet &amp; Greet Inside Terminal", "Name board inside arrivals \u2014 60 min complimentary wait."),
        ("24/7 Live Local Support", "Real people answer at 2am \u2014 no chatbots."),
        ("Vetted, Professional Chauffeurs", "Background checked, licensed, and trained \u2014 not gig workers."),
    ]
    for i, ((old_h4, old_p), (new_h4, new_p)) in enumerate(zip(airport_why_tabs, why_tabs)):
        page = r(page, f'<h4>{old_h4}</h4>', f'<h4>{new_h4}</h4>')
        page = r(page, f'<p>{old_p}</p>', f'<p>{new_p}</p>')

    # ── Why panels (5 items) ─────────────────────────────────────
    airport_why_panels = [
        ("We Monitor Every Flight, Live",
         "Our dispatch system pulls live ADS-B flight data \u2014 not your scheduled arrival time. Delayed two hours? Your driver adjusts automatically. You land, you walk out.",
         ["Automatic adjustment for any delay length", "Driver alerted before you even touch down", "No calls or messages required from you"],
         "10,000+ Flights Tracked"),
        ("Your Rate Is Guaranteed at Booking",
         "The price you see when booking is the price you pay \u2014 regardless of traffic, time of day, fuel costs, or demand spikes. Tolls, airport fees, and gratuity are all included.",
         ["No surge pricing during peak hours", "All-in rate includes tolls and airport fees", "Confirmed by email and SMS at time of booking"],
         "Zero Hidden Fees &mdash; Ever"),
        ("Greeted at the Arrivals Hall, Not the Curb",
         "Your uniformed chauffeur stands inside the terminal with a personalized name board. No navigating outdoor pickup lanes, no searching for a car. Just walk out of customs and you are on your way.",
         ["Inside arrivals hall \u2014 Terminal 1 &amp; 3 at YYZ", "60 minutes complimentary wait (international)", "Luggage loading and unloading included"],
         "Inside Pickup &mdash; Not Curbside"),
        ("Toronto Dispatch &mdash; Always Reachable",
         "Real people pick up the phone at 2am. Local Toronto dispatch handles any situation before, during, or after your ride. No queues, no bots, no offshore call centres.",
         ["Local GTA dispatchers \u2014 not a call centre", "Available by phone, text, and email 24/7", "Rebooking assistance for cancelled flights"],
         "Local Dispatch 24/7 &middot; 365"),
        ("Every Driver Is Fully Vetted",
         "Every chauffeur passes a criminal background check, a clean driving abstract review, and a professional conduct assessment before their first ride. These are career professionals \u2014 not gig workers.",
         ["Criminal background check required", "Clean driving abstract \u2014 reviewed annually", "Uniformed, trained, and punctuality-rated"],
         "100% Professionally Vetted Drivers"),
    ]
    for i, ((old_h3, old_p, old_bullets, old_proof), (new_h3, new_p, new_bullets, new_proof)) in enumerate(zip(airport_why_panels, why_panels)):
        page = r(page, f'<h3>{old_h3}</h3>', f'<h3>{new_h3}</h3>')
        page = r(page, f'<p>{old_p}</p>', f'<p>{new_p}</p>')
        for old_b, new_b in zip(old_bullets, new_bullets):
            page = r(page, f'<li class="why-panel-bullet">{old_b}</li>', f'<li class="why-panel-bullet">{new_b}</li>')
        page = r(page, f'>{old_proof}</div>', f'>{new_proof}</div>')

    # Why CTA button
    page = r(page,
        '<a href="booking.html" class="btn-sec-more">Book Your Airport Transfer &rarr;</a>',
        f'<a href="booking.html" class="btn-sec-more">{why_cta_text} &rarr;</a>')

    # ── Seamless section heading ──────────────────────────────────
    page = r(page, 'A Seamless <em>Travel Experience</em>', seamless_h2)
    page = r(page,
        '<span class="sec-label">How It Works</span>',
        f'<span class="sec-label">{seamless_sub}</span>')

    # ── Fleet section ─────────────────────────────────────────────
    page = r(page, 'Upscale <em>Airport Vehicles</em>', fleet_h2)
    page = r(page,
        'Choose the vehicle that fits your group size, luggage needs, and travel style. All vehicles include the same premium service standard.',
        fleet_sub)

    # ── Step 1 panel (update call number reference) ───────────────
    page = r(page,
        'Book online or call 416 451 3106. Provide your pickup address, airport, flight number, and passengers.',
        'Book online or call 416 451 3106. Provide your pickup location, service type, date, and passenger count.')

    # ── Seamless step 2 — replace airport flight tracking content ─
    page = r(page, '<h4>We Track Your Flight</h4>',
             '<h4>Your Booking Is Confirmed</h4>')
    page = r(page,
        '<p>Live flight data adjusts your driver automatically. Delayed 3 hours? No call needed from you.</p>',
        '<p>A confirmation email and SMS arrive instantly with all your booking details locked in.</p>')
    page = r(page, '<span class="s-panel-tag">Step 2 &mdash; Track</span>',
             '<span class="s-panel-tag">Step 2 &mdash; Confirm</span>')
    page = r(page, '<h5>We Monitor Every Flight, Live</h5>',
             '<h5>Booking Confirmed Instantly</h5>')
    page = r(page,
        "Our dispatch pulls real-time flight data. Delayed two hours? Your driver adjusts automatically \u2014 you don't need to call. You just land and walk out.",
        'The moment you complete your booking, a full confirmation arrives by email and SMS. Your chauffeur is assigned, briefed on your itinerary, and ready.')
    page = r(page,
        '<li class="s-panel-bullet">Live ADS-B flight tracking system</li>',
        '<li class="s-panel-bullet">Confirmation by email and SMS instantly</li>')
    page = r(page,
        '<li class="s-panel-bullet">Automatic driver adjustment \u2014 no calls needed</li>',
        '<li class="s-panel-bullet">Chauffeur assigned and briefed</li>')
    page = r(page,
        '<li class="s-panel-bullet">Delay notification sent to your phone</li>',
        '<li class="s-panel-bullet">All details locked \u2014 no changes to your rate</li>')
    page = r(page,
        '<a href="#services" class="s-panel-link">How It Works &rarr;</a>',
        '<a href="booking.html" class="s-panel-link">Book Now &rarr;</a>')

    # ── Seamless step 3 — replace terminal meet content ───────────
    page = r(page, '<h4>Meet Inside the Terminal</h4>',
             '<h4>Your Chauffeur Arrives Early</h4>')
    page = r(page,
        '<p>Your chauffeur waits inside arrivals with a name board \u2014 not outside at the curb chaos.</p>',
        '<p>Your uniformed driver arrives at your location ahead of schedule \u2014 always punctual, always professional.</p>')
    page = r(page, '<h5>Greeted Inside the Arrivals Hall</h5>',
             '<h5>Your Chauffeur Arrives Before You</h5>')
    page = r(page,
        'Your uniformed chauffeur stands inside the terminal with a personalized name board. No curbside confusion, no searching. Just clear customs and you are on your way.',
        'Your uniformed chauffeur arrives at the scheduled pickup location 5\u201310 minutes early. The vehicle is pre-inspected, climate-controlled, and ready for your journey.')
    page = r(page,
        '<li class="s-panel-bullet">Inside Terminal 1 &amp; Terminal 3 at YYZ</li>',
        '<li class="s-panel-bullet">Arrives 5\u201310 minutes before your pickup time</li>')
    page = r(page,
        '<li class="s-panel-bullet">60 minutes complimentary wait \u2014 international</li>',
        '<li class="s-panel-bullet">Full vehicle pre-inspection before every trip</li>')
    page = r(page,
        '<li class="s-panel-bullet">Name board with passenger name displayed</li>',
        '<li class="s-panel-bullet">Direct contact with your driver on the day</li>')
    page = r(page,
        '<a href="#coverage" class="s-panel-link">View Airports &rarr;</a>',
        '<a href="fleet.html" class="s-panel-link">View Our Fleet &rarr;</a>')

    # ── Seamless step 4 — remove airport departure reference ──────
    page = r(page,
        '<li class="s-panel-bullet">15-min courtesy call before departure pickups</li>',
        '<li class="s-panel-bullet">Courtesy confirmation call before your pickup</li>')

    # ── Fleet description — remove Pearson/Billy Bishop ref ───────
    page = r(page,
        'The ideal choice for solo travellers and couples heading to Pearson or Billy Bishop. Spacious rear seating, premium leather, and a smooth ride through downtown traffic.',
        'The ideal choice for solo travellers and couples. Spacious rear seating, premium leather, and a smooth ride to any destination across Toronto and the GTA.')

    # ── FIFA section — remove from non-airport pages ──────────────
    fifa_pattern = re.compile(
        r'<!-- FIFA WORLD CUP 2026 -->.*?(?=<!-- REVIEWS SPOTLIGHT -->)',
        re.DOTALL)
    if fifa_pattern.search(page):
        page = fifa_pattern.sub('', page, count=1)

    # ── Fleet footer note — remove airport-specific text ─────────
    page = r(page,
        'All vehicles include flight tracking &middot; Meet &amp; greet &middot; Flat rate',
        'All vehicles include professional chauffeur &middot; White-glove service &middot; Flat rate')

    # ── Comparison section — replace airport-specific bullets ─────
    page = r(page,
        '<li>Real-time flight tracking and automatic adjustment</li>',
        '<li>On-time guarantee &mdash; chauffeur arrives early</li>')
    page = r(page,
        '<li>Meet and greet inside the terminal, not curbside</li>',
        '<li>Door-to-door white-glove service</li>')
    page = r(page,
        '<li>60 minutes complimentary wait time</li>',
        '<li>Generous wait time included &mdash; no rush</li>')
    page = r(page,
        "<li>No flight tracking \u2014 driver won't wait for delays</li>",
        '<li>No on-time guarantee &mdash; driver may not wait</li>')
    page = r(page,
        '<li>Curbside pickup only, often causing confusion</li>',
        '<li>No door-to-door service &mdash; you find the car</li>')
    page = r(page,
        '<li>Only 5 minutes free wait time</li>',
        '<li>Minimal wait time &mdash; extra charges after 5 minutes</li>')

    # ── Airports section → services section ──────────────────────
    # Replace from <!-- AIRPORTS SERVED --> to <!-- FAQ -->
    airports_pattern = re.compile(
        r'<!-- AIRPORTS SERVED -->.*?(?=<!-- FAQ -->)',
        re.DOTALL)
    if airports_pattern.search(page):
        page = airports_pattern.sub(services_section_html + '\n\n', page, count=1)
    else:
        print("  WARN: could not find <!-- AIRPORTS SERVED --> section")

    # ── FAQ ───────────────────────────────────────────────────────
    page = r(page, 'Airport Limo FAQ', faq_label)
    page = r(page, 'Frequently Asked <em>Questions</em>', f'{faq_h2}')
    # Build new FAQ items HTML
    faq_svg = '<svg viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg>'
    new_faq_items = "\n".join(
        f'      <div class="faq-item">\n'
        f'        <div class="faq-q">{q}{faq_svg}</div>\n'
        f'        <div class="faq-a">{a}</div>\n'
        f'      </div>'
        for q, a in faq_items
    )
    faq_grid_pattern = re.compile(r'<div class="faq-grid">.*?</div>(?=\s*<div class="faq-cta">)', re.DOTALL)
    if faq_grid_pattern.search(page):
        page = faq_grid_pattern.sub(f'<div class="faq-grid">\n{new_faq_items}\n    </div>', page, count=1)
    else:
        print("  WARN: could not find <div class=\"faq-grid\">")

    # ── Speak section ─────────────────────────────────────────────
    page = r(page, "We&rsquo;re Here For You", speak_pre)
    page = r(page,
        'Need to Speak With Us About <strong>Your Airport Transfer?</strong>',
        speak_h2_html)
    page = r(page,
        'Questions about your flight, pickup location, wait time, or group rates &mdash; our GTA dispatch team handles airport transfers 24 hours a day.',
        speak_sub)

    # ── Float CTA ─────────────────────────────────────────────────
    page = r(page, '✈&nbsp; Airport Transfer', float_badge)
    page = r(page, 'Ready to book your ride?', float_title)
    page = r(page,
        'Flat rates &middot; Flight tracking &middot; Meet &amp; greet inside terminal',
        float_sub)
    # Float trust pills
    old_trust = ('<div class="float-cta-trust">\n'
                 '    <span>Flat rate guaranteed</span>\n'
                 '    <span>No credit card</span>\n'
                 '    <span>24/7 dispatch</span>\n'
                 '  </div>')
    new_trust = ('<div class="float-cta-trust">\n'
                 + ''.join(f'    <span>{t}</span>\n' for t in float_trust)
                 + '  </div>')
    page = r(page, old_trust, new_trust)

    write(filename, page)
    return True


# ═══════════════════════════════════════════════════════════════
# WEDDING HUB
# ═══════════════════════════════════════════════════════════════
print("\nGenerating wedding.html...")

wedding_services = f'''<!-- SERVICES OVERVIEW - WEDDING -->
<section class="airports" id="services">
  <div class="wrap">
    <span class="sec-label">Wedding Transportation Services</span>
    <h2 class="sec-h2">Everything You Need <em>for Your Perfect Day</em></h2>
    <p class="sec-sub">From the bridal limo to the guest shuttle, Limo4All handles every wedding transport detail with elegance and precision.</p>
    <div class="airport-cards">
{svc_card('<svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="var(--blue)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>',
          "Bridal Limo &amp; Getaway Car",
          "Stretch Lincoln Town Car &bull; Luxury SUV &bull; Complimentary Champagne",
          ["Red Carpet Service", "Photo Stop Coordination", "Decorated Vehicle Available"],
          "Included", "Champagne<em> &amp; Red Carpet</em>", "Book Bridal Limo")}
{svc_card('<svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="var(--blue)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
          "Bridal Party Transport",
          "Multi-vehicle coordination &bull; SUVs &amp; Sprinters &bull; Full party covered",
          ["Church, Venue &amp; Hotel Pickups", "Coordinated Timing", "Formally Dressed Chauffeurs"],
          "From", "$95<em> per vehicle</em>", "Book Party Transport")}
{svc_card('<svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="var(--blue)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>',
          "Wedding Guest Shuttle",
          "Mercedes Sprinter &bull; Up to 14 guests &bull; Hotel-to-venue loops",
          ["Airport Pickups for Out-of-Town Guests", "Custom Schedule", "Flat Hourly Rate"],
          "Flat", "Hourly<em> rate</em>", "Book Guest Shuttle")}
    </div>
  </div>
</section>

'''

make_hub(
    "WeddingHUB.html", "WeddingHUB.html",
    title="Wedding Limo &amp; Chauffeur Service Ontario | Limo4All",
    meta_desc="Luxury wedding limo service across Ontario. Stretch limousines, SUVs, and Sprinters for bridal parties, guests, and getaway cars. Complimentary champagne. Book online.",
    schema_name="Wedding Limo Service Ontario",
    schema_type="Wedding Limousine Service",
    promo_bar_content='<strong>Ontario&rsquo;s Premier Wedding Limo Service &mdash; Stretch Limos, SUVs &amp; Sprinters.</strong>&nbsp; Complimentary champagne &nbsp;&mdash;&nbsp; <a href="tel:+14164513106">Call 416 451 3106</a>',
    ticker_items=["Wedding Limo Toronto", "Stretch Limousine Rentals", "Bridal Party Transport", "Red Carpet Arrival", "Complimentary Champagne", "White Glove Chauffeur Service", "Wedding Guest Shuttle", "Getaway Car Service"],
    breadcrumb_label="Wedding Limo",
    hero_pills=["Stretch Limousines", "Bridal Packages", "Complimentary Champagne", "Red Carpet Service"],
    hero_h1_line1="Wedding Limo &amp; Chauffeur",
    hero_h1_line2="Service Across Ontario",
    hero_sub="Make your wedding day unforgettable with Limo4All&rsquo;s premium wedding limo service. Stretch limousines, luxury SUVs, and Sprinters for the bridal party, guests, and getaway car. Complimentary champagne included.",
    hbc_title="Get a Wedding Quote",
    hbc_select_options=('          <option value="">Select Service</option>\n'
                        '          <option>Stretch Limousine &mdash; Bridal</option>\n'
                        '          <option>Luxury SUV &mdash; Bridal Party</option>\n'
                        '          <option>Sprinter Van &mdash; Guest Shuttle</option>\n'
                        '          <option>Full-Day Wedding Package</option>'),
    stats_bar_no1_text="Wedding<br>Limo<br>Service",
    stats_bar_label="Less Than Hiring Separately",
    why_pre="Ontario&rsquo;s Most Trusted Wedding Limo Service",
    why_h2="Wedding Transportation Services",
    why_tabs=[
        ("Complimentary Champagne &amp; Red Carpet", "Included as standard in every bridal booking &mdash; because your arrival matters."),
        ("Flat Rate. Locked at Booking.", "No hidden fees &mdash; ever. Package price confirmed instantly."),
        ("Photo Stop Coordination", "Custom stops planned into your schedule &mdash; chauffeur knows every location."),
        ("24/7 Wedding Support Line", "Real people answer on your wedding day &mdash; no chatbots ever."),
        ("Vetted, Formally Dressed Chauffeurs", "Background checked, licensed, and trained in wedding-day protocol."),
    ],
    why_panels=[
        ("Arriving in the Style You Deserve",
         "Our stretch limousines and luxury SUVs arrive immaculately presented for your wedding day. Red carpet, complimentary champagne, and a uniformed chauffeur ensure your arrival is unforgettable.",
         ["Stretch Lincoln Town Car Limousine available", "Complimentary champagne on arrival", "Vehicle ribbon decoration included"],
         "Champagne &amp; Red Carpet Included"),
        ("Your Package Price Never Changes",
         "The price you confirm at booking is the price you pay &mdash; full stop. No surprise charges for overtime, decorations, or extra stops within your agreed package.",
         ["No surprise charges day-of", "All-in rate includes gratuity and fuel", "Confirmed by email and SMS at booking"],
         "Zero Hidden Fees &mdash; Ever"),
        ("Every Photo Stop Perfectly Timed",
         "Your chauffeur plans the most efficient routing through your photo stop locations while keeping you on time for every ceremony and reception commitment.",
         ["Custom photo stop list built into schedule", "Chauffeur knows all major GTA venues", "Flexible timing for the unexpected"],
         "Flawless Timing &mdash; Every Stop"),
        ("Your Wedding Day Support Team",
         "Our wedding coordination team is available directly by phone on your big day. Real local dispatchers &mdash; not a call centre &mdash; handle any situation calmly and quickly.",
         ["Local GTA dispatchers &mdash; not a call centre", "Available by phone, text, and email on your day", "Multi-vehicle coordination from one contact"],
         "Dedicated Wedding Day Support"),
        ("Every Driver Is Formally Trained",
         "Every chauffeur passes a criminal background check, a professional conduct review, and wedding-day protocol training before serving a bridal booking.",
         ["Criminal background check required", "Clean driving abstract &mdash; reviewed annually", "Uniformed, trained in wedding-day etiquette"],
         "100% Professionally Vetted Drivers"),
    ],
    why_cta_text="Book Your Wedding Limo",
    seamless_h2='A <em>Flawless Wedding Day</em>',
    seamless_sub="Wedding Day Timeline",
    fleet_h2='Elegant <em>Wedding Vehicles</em>',
    fleet_sub="Choose the vehicle that perfectly suits your wedding style and party size. All vehicles include uniformed chauffeur, complimentary champagne, and red carpet service.",
    services_section_html=wedding_services,
    faq_label="Wedding Limo FAQ",
    faq_h2='Frequently Asked <em>Wedding Questions</em>',
    faq_items=[
        ("How far in advance should I book a wedding limo?", "We recommend booking at least 3&ndash;6 months in advance, especially for peak season (May&ndash;October). Popular dates fill quickly. A deposit secures your booking."),
        ("Do you decorate the wedding vehicles?", "Yes. Ribbon and bow decoration is available at no extra charge for bridal vehicles. Custom decorations can be arranged with advance notice."),
        ("What does the bridal limo package include?", "Our standard bridal limo package includes: professional uniformed chauffeur, complimentary champagne, red carpet service, vehicle decoration, and flexibility for photo stops."),
        ("Can you coordinate multiple vehicles for our wedding party?", "Absolutely. We regularly coordinate 3&ndash;8 vehicles for large weddings. A dedicated coordinator manages timing across all vehicles on your day."),
        ("What is the capacity of your stretch limousine?", "Our stretch Lincoln Town Car limousine comfortably seats up to 10 passengers. For larger groups, we recommend a Mercedes Sprinter van (up to 14 passengers)."),
        ("Do you offer a getaway car for the end of the night?", "Yes. Late-night getaway car service to take the happy couple from the reception to their hotel in style. Can be booked as a standalone or added to a full-day package."),
        ("Can we make photo stops during our wedding day?", "Of course. We build your photo stop locations into the schedule. Let us know the spots in advance and your chauffeur will plan the most efficient routing."),
        ("Do you serve wedding venues outside Toronto?", "Yes. We serve all of Ontario &mdash; including Niagara-on-the-Lake, Muskoka, Hamilton, Collingwood, and all Ontario wedding destinations."),
        ("Is there a minimum booking time?", "For stretch limousines, our minimum booking is 3 hours. For SUVs and Sprinters, a 2-hour minimum applies. Full-day wedding packages are available at a preferred rate."),
        ("What happens if there is a delay on our wedding day?", "We build flexibility into every wedding booking. Your chauffeur is on standby for the duration of your package and accommodates reasonable delays."),
    ],
    speak_pre="Book Your Ontario Wedding Limo",
    speak_h2_html='Ready to Plan Your <strong>Wedding Transportation?</strong>',
    speak_sub="Tell us your wedding date, venue, and party size and we will build a custom transportation plan for your day. Our wedding team responds within the hour.",
    float_badge="&#128141;&nbsp; Wedding Limo",
    float_title="Book Your Wedding Limo",
    float_sub="Complimentary champagne &middot; Red carpet &middot; Uniformed chauffeur",
    float_trust=["Champagne Included", "Red Carpet", "White Glove"],
)


# ═══════════════════════════════════════════════════════════════
# EVENTS HUB
# ═══════════════════════════════════════════════════════════════
print("\nGenerating events.html...")

events_services = f'''<!-- SERVICES OVERVIEW - EVENTS -->
<section class="airports" id="services">
  <div class="wrap">
    <span class="sec-label">Event &amp; Concert Limo Services</span>
    <h2 class="sec-h2">The Right Ride <em>for Every Occasion</em></h2>
    <p class="sec-sub">From concerts and sports games to galas and bachelorette parties &mdash; flat rates, no surge pricing, group packages available.</p>
    <div class="airport-cards">
{svc_card('<svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="var(--blue)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>',
          "Concert &amp; Festival Transport",
          "Scotiabank Arena &bull; Rogers Centre &bull; Budweiser Stage",
          ["Pre-Show Pickup &amp; Post-Show Return", "Group Packages: 2&ndash;14 pax", "Flat Rate &mdash; No Surge Ever"],
          "Flat", "Rate<em> locked at booking</em>", "Book Concert Limo")}
{svc_card('<svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="var(--blue)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="8 21 12 17 16 21"/><path d="M17 4H7L5 8v4a7 7 0 0 0 14 0V8L17 4z"/><path d="M5 10H3a2 2 0 0 0 0 4h2"/><path d="M19 10h2a2 2 0 0 1 0 4h-2"/><line x1="12" y1="17" x2="12" y2="21"/></svg>',
          "Sports Games &amp; Events",
          "Maple Leafs &bull; Raptors &bull; Blue Jays &bull; TFC",
          ["Game Day Group Packages", "Out-of-Town Game Transport", "Post-Game Return Included"],
          "From", "$75<em> per trip</em>", "Book Sports Limo")}
{svc_card('<svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="var(--blue)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
          "Galas, Nightlife &amp; VIP",
          "TIFF &bull; Black-Tie Galas &bull; Bachelorette Parties",
          ["Stretch Limo &amp; Luxury SUV Options", "Bachelor &amp; Bachelorette Packages", "VIP Arrival Service"],
          "Custom", "VIP<em> package</em>", "Book VIP Transport")}
    </div>
  </div>
</section>

'''

make_hub(
    "events.html", "events.html",
    title="Events &amp; Concert Limo Service Toronto | Limo4All",
    meta_desc="VIP limo and group transportation for concerts, sports games, galas, and events across Toronto and Ontario. Flat rates, no surge pricing. Book online.",
    schema_name="Events & Concert Limo Toronto",
    schema_type="Event Transportation Service",
    promo_bar_content='<strong>VIP Events &amp; Concert Limo &mdash; Flat Rates, No Surge on Event Nights.</strong>&nbsp; Groups welcome &nbsp;&mdash;&nbsp; <a href="tel:+14164513106">Call 416 451 3106</a>',
    ticker_items=["Events &amp; Concert Limo", "Scotiabank Arena &amp; Rogers Centre", "Sports Game Transportation", "Group Packages Available", "Flat Rate &mdash; No Surge Pricing", "TIFF &amp; Gala Transportation", "Bachelorette &amp; Bachelor Parties", "Safe Ride Home After the Show"],
    breadcrumb_label="Events Limo",
    hero_pills=["Concert &amp; Event Rides", "Group Packages", "Flat Rate No Surge", "Post-Show Pickup"],
    hero_h1_line1="Events &amp; Concert Limo",
    hero_h1_line2="VIP Transportation for Any Occasion",
    hero_sub="Arrive in style at any event &mdash; concerts, sports games, festivals, galas, and more. Limo4All provides premium group transportation across Ontario with flat rates and no surge pricing ever.",
    hbc_title="Get an Event Quote",
    hbc_select_options=('          <option value="">Select Event Type</option>\n'
                        '          <option>Concert or Festival</option>\n'
                        '          <option>Sports Game</option>\n'
                        '          <option>Gala or Award Show</option>\n'
                        '          <option>Bachelorette / Bachelor Party</option>'),
    stats_bar_no1_text="Events<br>Limo<br>Service",
    stats_bar_label="Lower Than Surge Pricing",
    why_pre="Toronto&rsquo;s #1 Events &amp; Concert Limo Service",
    why_h2="Events &amp; Concert Transportation",
    why_tabs=[
        ("Flat Rate &mdash; Never Surge Pricing", "Lock in your rate at booking &mdash; never changes on event nights."),
        ("Flat Rate. Locked at Booking.", "No surge pricing &mdash; ever. Price confirmed instantly."),
        ("Post-Show Pickup Included", "Your chauffeur tracks the event &mdash; ready at the door when you exit."),
        ("24/7 Live Local Support", "Real people answer at 2am &mdash; no chatbots."),
        ("Vetted, Professional Chauffeurs", "Background checked, licensed, and trained &mdash; not gig workers."),
    ],
    why_panels=[
        ("Flat Rate &mdash; Even on the Busiest Nights",
         "We never apply surge pricing on concert nights, playoff games, or New Year&rsquo;s Eve. Your rate is locked at booking regardless of demand.",
         ["No surge on high-demand event nights", "Rate confirmed by email at booking", "Same price for return trip included"],
         "Flat Rate &mdash; Always"),
        ("Your Rate Is Guaranteed at Booking",
         "The price you confirm when booking is the price you pay. No add-ons, no surprises, no post-event receipt shock.",
         ["No surge pricing during peak hours", "All-in rate &mdash; no hidden fees", "Confirmed by email and SMS at booking"],
         "Zero Hidden Fees &mdash; Ever"),
        ("Post-Show Pickup &mdash; We Wait for You",
         "Your chauffeur monitors the event and is ready at the designated pickup point when the final buzzer sounds or the curtain drops. No scrambling for a ride.",
         ["Driver tracks event end time", "Curbside pickup at venue exit", "No waiting in the cold"],
         "Post-Show Pickup Included"),
        ("Toronto Dispatch &mdash; Always Reachable",
         "Real people pick up the phone at 2am. Local Toronto dispatch handles any situation before, during, or after your event.",
         ["Local GTA dispatchers &mdash; not a call centre", "Available by phone, text, and email 24/7", "Group coordination handled seamlessly"],
         "Local Dispatch 24/7 &middot; 365"),
        ("Every Driver Is Fully Vetted",
         "Every chauffeur passes a criminal background check, a clean driving abstract review, and a professional conduct assessment before their first ride.",
         ["Criminal background check required", "Clean driving abstract &mdash; reviewed annually", "Uniformed, trained, and punctuality-rated"],
         "100% Professionally Vetted Drivers"),
    ],
    why_cta_text="Book Event Transportation",
    seamless_h2='A <em>Night to Remember</em>',
    seamless_sub="How It Works",
    fleet_h2='Premium <em>Event Vehicles</em>',
    fleet_sub="The right vehicle for your group size and style. From luxury sedans for couples to Sprinter vans for the full crew &mdash; all at flat rates with no surge pricing.",
    services_section_html=events_services,
    faq_label="Events Limo FAQ",
    faq_h2='Frequently Asked <em>Event Questions</em>',
    faq_items=[
        ("Do you offer flat rates for concert and event nights?", "Yes. All Limo4All event bookings are at a flat rate confirmed at booking. We never apply surge pricing on high-demand event nights &mdash; the price you see is the price you pay."),
        ("Do you serve Scotiabank Arena and Rogers Centre?", "Yes. We provide pickup and drop-off at all major Toronto venues including Scotiabank Arena, Rogers Centre, Budweiser Stage, History, and all venues across the GTA."),
        ("Can you accommodate a large group for a sports game?", "Absolutely. Our Sprinter vans seat up to 14 passengers and are perfect for group game days. For larger groups, we coordinate multiple vehicles under one booking."),
        ("Can you pick us up after the event?", "Yes. All event bookings include a return trip. We monitor event end times and coordinate pickup at a designated meeting point near the venue."),
        ("Do you serve events outside Toronto?", "Yes. We serve all GTA and major Ontario venues including Niagara Falls Casino, Barrie, Hamilton, and Kitchener-Waterloo venues."),
        ("Can I book a limo for a bachelorette or bachelor party?", "Absolutely. Bachelorette and bachelor party transport is one of our most popular bookings. Stretch limos, luxury SUVs, or Sprinters &mdash; add champagne and plan your venue route."),
        ("Is there a minimum booking for event transportation?", "Our minimum for event rides is 2 hours. Full-evening packages covering pre-event pickup through post-event return are available at preferred rates."),
        ("Do you offer TIFF film festival transportation?", "Yes. During TIFF, we provide VIP transportation to screenings, galas, and industry events. Advance booking is strongly recommended."),
    ],
    speak_pre="Book Your Events &amp; Concert Limo",
    speak_h2_html='Ready to Book Your <strong>Event Transportation?</strong>',
    speak_sub="Tell us your event, venue, date, and group size and we will confirm your flat rate instantly. Available for all Toronto and Ontario venues.",
    float_badge="&#127926;&nbsp; Event Limo",
    float_title="Book Your Event Limo",
    float_sub="Flat rate &middot; No surge &middot; Group packages available",
    float_trust=["Flat Rate", "No Surge", "Groups Welcome"],
)


# ═══════════════════════════════════════════════════════════════
# HOURLY HUB
# ═══════════════════════════════════════════════════════════════
print("\nGenerating hourly.html...")

hourly_services = f'''<!-- SERVICES OVERVIEW - HOURLY -->
<section class="airports" id="services">
  <div class="wrap">
    <span class="sec-label">Hourly Charter Services</span>
    <h2 class="sec-h2">A Vehicle &amp; Chauffeur <em>Ready for Anything</em></h2>
    <p class="sec-sub">Business meetings, personal errands, sightseeing, or all of the above. Hourly charter puts you in control of your schedule with a flat hourly rate and no hidden fees.</p>
    <div class="airport-cards">
{svc_card('<svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="var(--blue)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/><line x1="12" y1="12" x2="12" y2="16"/><line x1="10" y1="14" x2="14" y2="14"/></svg>',
          "Business &amp; Corporate Charter",
          "Full-day &amp; half-day executive charter &bull; Multiple meetings",
          ["Road Shows &amp; Investor Presentations", "Corporate Account Billing", "Wi-Fi Ready Vehicles"],
          "Flat", "Hourly<em> rate</em>", "Book Business Charter")}
{svc_card('<svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="var(--blue)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>',
          "Shopping, Errands &amp; Personal",
          "As-directed &bull; Multiple stops &bull; Chauffeur waits at each",
          ["High-End Shopping &amp; Yorkdale Runs", "Medical Appointments", "No Limit on Stops"],
          "2-hr", "Minimum<em> booking</em>", "Book Hourly Charter")}
{svc_card('<svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="var(--blue)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/></svg>',
          "City Tours &amp; Sightseeing",
          "Toronto city tours &bull; Custom Ontario day trips",
          ["Distillery, CN Tower &amp; Waterfront", "Niagara Falls Day Trip Option", "Flexible Itinerary"],
          "Custom", "Itinerary<em> built for you</em>", "Book City Tour")}
    </div>
  </div>
</section>

'''

make_hub(
    "hourly.html", "hourly.html",
    title="Hourly Limo Charter &amp; As-Directed Service | Limo4All",
    meta_desc="Hourly limo and chauffeur service across Ontario. As-directed bookings for business, shopping, tours, and personal use. Flat hourly rates, 2-hour minimum. Book online.",
    schema_name="Hourly Limo Charter Ontario",
    schema_type="Hourly Limousine Charter",
    promo_bar_content='<strong>Hourly Limo Charter &mdash; As-Directed Service Across Ontario.</strong>&nbsp; Flat hourly rates &nbsp;&mdash;&nbsp; <a href="tel:+14164513106">Call 416 451 3106</a>',
    ticker_items=["Hourly Limo Charter", "As-Directed Chauffeur Service", "Business Day Use", "Shopping &amp; Errands", "City Tours &amp; Sightseeing", "Corporate Road Shows", "Flat Hourly Rate", "2-Hour Minimum"],
    breadcrumb_label="Hourly Charter",
    hero_pills=["Flat Hourly Rates", "As-Directed", "Multiple Stops", "2-Hour Minimum"],
    hero_h1_line1="Hourly Limo Charter",
    hero_h1_line2="As-Directed Chauffeur Service",
    hero_sub="Book a professional chauffeur for as many hours as you need. Perfect for business meetings, shopping trips, city tours, or any as-directed use across Ontario. Flat hourly rates, no hidden fees.",
    hbc_title="Get an Hourly Quote",
    hbc_select_options=('          <option value="">Select Charter Type</option>\n'
                        '          <option>Business &amp; Corporate Charter</option>\n'
                        '          <option>Shopping &amp; Personal Errands</option>\n'
                        '          <option>City Tour &amp; Sightseeing</option>\n'
                        '          <option>Medical Appointments</option>'),
    stats_bar_no1_text="Hourly<br>Charter<br>Service",
    stats_bar_label="More Productive Than Driving",
    why_pre="Ontario&rsquo;s Most Flexible Hourly Limo Service",
    why_h2="Hourly Charter &amp; As-Directed Service",
    why_tabs=[
        ("Flat Hourly Rate &mdash; No Meter Surprises", "Confirmed at booking &mdash; no changes regardless of stops or detours."),
        ("Flat Rate. Locked at Booking.", "No surge pricing &mdash; ever. Price confirmed instantly."),
        ("Chauffeur Waits at Every Stop", "Vehicle and driver stay with you through every appointment &mdash; always ready."),
        ("24/7 Live Local Support", "Real people answer at 2am &mdash; no chatbots."),
        ("Vetted, Professional Chauffeurs", "Background checked, licensed, and trained &mdash; not gig workers."),
    ],
    why_panels=[
        ("One Rate. Unlimited Stops.",
         "Your flat hourly rate is confirmed at booking. Whether you make 1 stop or 12, the rate never changes. The meter does not run while you are inside your meeting.",
         ["Rate confirmed at booking &mdash; no changes", "Waiting time built into your hourly block", "No per-kilometer charges ever"],
         "Flat Hourly Rate &mdash; Always"),
        ("Your Rate Is Guaranteed at Booking",
         "The price you confirm when booking is the price you pay. No add-ons at the end of the trip, regardless of traffic, extra stops, or schedule changes.",
         ["No surprise charges at the end", "All-in rate &mdash; tolls and fuel included", "Confirmed by email and SMS at booking"],
         "Zero Hidden Fees &mdash; Ever"),
        ("Your Vehicle Stays With You",
         "During your hourly charter, your chauffeur and vehicle remain exclusively yours. No disappearing between stops, no sharing &mdash; the vehicle is at your disposal for the full booked time.",
         ["No sharing &mdash; exclusively yours", "Driver waits at every stop", "Ready to depart the moment you are"],
         "Your Vehicle &mdash; Exclusively"),
        ("Toronto Dispatch &mdash; Always Reachable",
         "Our local dispatch team handles last-minute schedule changes, route adjustments, and any situation that arises during your charter. Available 24/7 by phone or text.",
         ["Local GTA dispatchers &mdash; not a call centre", "Available by phone, text, and email 24/7", "Last-minute changes handled seamlessly"],
         "Local Dispatch 24/7 &middot; 365"),
        ("Every Driver Is Fully Vetted",
         "Every chauffeur passes a criminal background check, a clean driving abstract review, and a professional conduct assessment before their first ride.",
         ["Criminal background check required", "Clean driving abstract &mdash; reviewed annually", "Uniformed, trained, and punctuality-rated"],
         "100% Professionally Vetted Drivers"),
    ],
    why_cta_text="Book Hourly Charter",
    seamless_h2='A <em>Seamless Charter Experience</em>',
    seamless_sub="How It Works",
    fleet_h2='Premium <em>Charter Vehicles</em>',
    fleet_sub="Executive sedans, full-size SUVs, and Mercedes Sprinter vans &mdash; all Wi-Fi equipped for business productivity. Choose the right vehicle for your needs.",
    services_section_html=hourly_services,
    faq_label="Hourly Charter FAQ",
    faq_h2='Frequently Asked <em>Hourly Charter Questions</em>',
    faq_items=[
        ("What is the minimum booking for hourly charter?", "Our minimum is 2 hours for sedans and SUVs. Sprinter van hourly bookings have a 3-hour minimum. There is no maximum &mdash; full-day and multi-day charters are available."),
        ("Can I add extra hours during my booking?", "Yes. If you need more time during your charter, simply let your chauffeur know. Additional hours are billed at the same hourly rate and added to your final invoice."),
        ("Does the chauffeur wait at each stop?", "Yes. During your hourly charter, your chauffeur stays with the vehicle at every stop and is ready whenever you are. There is no limit to the number of stops within your booked time."),
        ("What vehicles are available for hourly charter?", "We offer executive sedans (Lincoln Continental, Mercedes E-Class), full-size SUVs (Cadillac Escalade, Lincoln Navigator), and Mercedes Sprinter vans for groups. All vehicles are Wi-Fi equipped."),
        ("Is hourly charter available for business road shows?", "Yes. Hourly as-directed service is ideal for investor road shows, multi-site client meetings, and all-day business travel. Corporate account billing with monthly invoicing is available."),
        ("Can I book an hourly charter for a day trip to Niagara Falls?", "Yes. Many clients book our hourly service for Niagara Falls day trips. We offer flexible itineraries including the falls, Niagara-on-the-Lake wine country, and the casinos. Typical round trip is 6&ndash;8 hours."),
        ("What is the difference between hourly charter and point-to-point?", "A point-to-point booking is a direct transfer at a flat rate. Hourly charter gives you a chauffeur and vehicle at your disposal for a set number of hours with unlimited stops."),
        ("Do you offer hourly charter for medical appointments?", "Yes. We regularly provide hourly charter for medical appointments and hospital visits. Our chauffeurs are patient, assist with mobility needs, and will wait for the full duration of your appointment."),
    ],
    speak_pre="Book Your Hourly Limo Charter",
    speak_h2_html='Ready to Book <strong>Your Hourly Charter?</strong>',
    speak_sub="Tell us your date, vehicle preference, approximate hours, and intended use. We will confirm your flat hourly rate and have a chauffeur ready for you.",
    float_badge="&#9200;&nbsp; Hourly Charter",
    float_title="Book Hourly Charter",
    float_sub="As-directed &middot; Flat rate &middot; 2-hour minimum",
    float_trust=["As-Directed", "Flat Rate", "Multiple Stops"],
)


# ═══════════════════════════════════════════════════════════════
# TOURS HUB
# ═══════════════════════════════════════════════════════════════
print("\nGenerating tours.html...")

tours_services = f'''<!-- SERVICES OVERVIEW - TOURS -->
<section class="airports" id="services">
  <div class="wrap">
    <span class="sec-label">Private Ontario Tours</span>
    <h2 class="sec-h2">Explore Ontario <em>in Luxury &amp; Comfort</em></h2>
    <p class="sec-sub">Private chauffeured day trips to Niagara Falls, wine country, Muskoka, and beyond &mdash; your itinerary, your pace, zero group rush.</p>
    <div class="airport-cards">
{svc_card('<svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="var(--blue)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 22 12 2 21 22"/><polyline points="7.5 15 12 7 16.5 15"/></svg>',
          "Niagara Falls Day Trip",
          "Private door-to-door &bull; Full day at the falls",
          ["Clifton Hill &amp; Fallsview Area", "Casino Niagara &amp; Boat Tour Stops", "Flexible Timing &mdash; Your Pace"],
          "From", "$350<em> per trip</em>", "Book Niagara Trip")}
{svc_card('<svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="var(--blue)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M8 22h8"/><path d="M12 11v11"/><path d="M7 2v5a5 5 0 0 0 10 0V2"/></svg>',
          "Wine Country &amp; NOTL Tour",
          "Niagara-on-the-Lake &bull; 3&ndash;5 Winery Visits",
          ["Inniskillin, Peller &amp; Wayne Gretzky Estates", "Safe Designated Driver", "Shaw Festival &amp; Old Town Stops"],
          "Custom", "Itinerary<em> built for you</em>", "Book Wine Tour")}
{svc_card('<svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="var(--blue)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>',
          "Custom Ontario Tours",
          "Muskoka &bull; Stratford &bull; Prince Edward County",
          ["Blue Mountains &amp; Collingwood", "Stratford Festival Transport", "Any Ontario Destination"],
          "Custom", "Day trip<em> pricing</em>", "Book Custom Tour")}
    </div>
  </div>
</section>

'''

make_hub(
    "tours.html", "tours.html",
    title="Niagara Falls &amp; Ontario Private Tours | Limo4All",
    meta_desc="Private chauffeured tours to Niagara Falls, wine country, Muskoka, and across Ontario. Fully custom itineraries, luxury vehicles, door-to-door service. Book online.",
    schema_name="Niagara Falls & Ontario Private Tours",
    schema_type="Tour Operator",
    promo_bar_content='<strong>Private Niagara Falls &amp; Ontario Tours &mdash; Luxury Vehicles, Your Itinerary.</strong>&nbsp; Door-to-door &nbsp;&mdash;&nbsp; <a href="tel:+14164513106">Call 416 451 3106</a>',
    ticker_items=["Niagara Falls Day Trips", "Wine Country &amp; NOTL Tours", "Muskoka Lake Country", "Private Ontario Tours", "Stratford Festival Transport", "Casino Niagara &amp; Fallsview", "Custom Itinerary Built Around You", "Door-to-Door from the GTA"],
    breadcrumb_label="Ontario Tours",
    hero_pills=["Niagara Falls Day Trips", "Wine Country Tours", "Custom Ontario Tours", "Private Group Tours"],
    hero_h1_line1="Niagara Falls &amp; Ontario",
    hero_h1_line2="Private Chauffeured Tours",
    hero_sub="Explore Ontario&rsquo;s most iconic destinations in luxury and comfort. Private Niagara Falls day trips, wine country tours, Muskoka excursions, and fully custom Ontario tours &mdash; all with a professional chauffeur and no group rush.",
    hbc_title="Get a Tour Quote",
    hbc_select_options=('          <option value="">Select Tour Type</option>\n'
                        '          <option>Niagara Falls Day Trip</option>\n'
                        '          <option>Wine Country &amp; NOTL Tour</option>\n'
                        '          <option>Muskoka Day Trip</option>\n'
                        '          <option>Custom Ontario Tour</option>'),
    stats_bar_no1_text="Private<br>Tour<br>Service",
    stats_bar_label="vs. Group Bus Tours",
    why_pre="Ontario&rsquo;s Premier Private Tour Service",
    why_h2="Private Chauffeured Ontario Tours",
    why_tabs=[
        ("Private &mdash; No Group Rush", "Your tour, your pace &mdash; no waiting for other guests, ever."),
        ("Flat Rate. Locked at Booking.", "No hidden fees &mdash; ever. Tour price confirmed at booking."),
        ("Door-to-Door Service", "Picked up from home, hotel, or office &mdash; returned at day&rsquo;s end."),
        ("24/7 Live Local Support", "Real people answer at 2am &mdash; no chatbots."),
        ("Vetted, Knowledgeable Chauffeurs", "Background checked, licensed, and familiar with Ontario&rsquo;s top destinations."),
    ],
    why_panels=[
        ("Your Tour. Your Pace. No Group Rush.",
         "Unlike group bus tours with rigid schedules and 30-person lineups, our private tours put you in complete control. Stay longer at a winery, skip an attraction you don&rsquo;t want &mdash; it&rsquo;s your day.",
         ["No waiting for other guests", "Adjust itinerary on the fly", "Stay as long as you like at each stop"],
         "Completely Private &mdash; Just Your Group"),
        ("Your Tour Price Is Confirmed at Booking",
         "The price you confirm is the price you pay. No surcharges for waiting time at wineries, extra stops, or schedule changes. One all-in rate, locked at booking.",
         ["No surprise charges at end of day", "All-in rate includes fuel and tolls", "Confirmed by email at booking"],
         "Zero Hidden Fees &mdash; Ever"),
        ("Picked Up from Your Door",
         "We pick you up from your home, hotel, or office and return you at the end of the day. No need to find a departure point or arrange separate transfers to a tour bus pickup.",
         ["Home, hotel, or office pickup", "Return drop-off at end of day", "No transit connections needed"],
         "True Door-to-Door Service"),
        ("Ontario Experts &mdash; Always Reachable",
         "Our chauffeurs know Ontario&rsquo;s top destinations inside and out. They can recommend the best spots for photos, the best restaurants in NOTL, and the most efficient Niagara route.",
         ["Local knowledge of all Ontario destinations", "Restaurant and attraction recommendations", "Optimal routing for your itinerary"],
         "Local Expertise Included"),
        ("Every Driver Is Fully Vetted",
         "Every chauffeur passes a criminal background check, a clean driving abstract review, and a professional conduct assessment. These are career professionals who represent Limo4All on every tour.",
         ["Criminal background check required", "Clean driving abstract &mdash; reviewed annually", "Uniformed, trained, and punctuality-rated"],
         "100% Professionally Vetted Drivers"),
    ],
    why_cta_text="Book a Private Tour",
    seamless_h2='A <em>Perfect Day Trip</em>',
    seamless_sub="How It Works",
    fleet_h2='Comfortable <em>Tour Vehicles</em>',
    fleet_sub="Luxury sedans for intimate tours, SUVs for small groups, and Sprinter vans for larger parties &mdash; all with a professional chauffeur who knows Ontario&rsquo;s best routes.",
    services_section_html=tours_services,
    faq_label="Ontario Tours FAQ",
    faq_h2='Frequently Asked <em>Tour Questions</em>',
    faq_items=[
        ("How long is the Niagara Falls day trip from Toronto?", "The drive from Toronto to Niagara Falls is approximately 90 minutes each way. A typical day trip is 7&ndash;9 hours total, giving you 4&ndash;5 hours at the Falls and surrounding attractions."),
        ("What is included in the Niagara Falls private tour?", "Our private Niagara Falls tours include door-to-door transportation, a dedicated chauffeur for the full day, and a completely flexible itinerary. Attraction admission tickets are not included but can be arranged."),
        ("Can you take us to multiple wineries in Niagara-on-the-Lake?", "Yes. Our wine country tours typically include 3&ndash;5 winery stops of your choice. We recommend Inniskillin, Peller Estates, and Wayne Gretzky Estates for first-time visitors."),
        ("How many passengers can you accommodate for a group tour?", "For groups of 2&ndash;6, we recommend a luxury SUV. Groups of 7&ndash;14 should book our Mercedes Sprinter van. For larger groups, multiple vehicles can be coordinated."),
        ("Do you offer Muskoka day trips from Toronto?", "Yes. Muskoka day trips are approximately 2 hours from Toronto. We arrange custom day tours including Bracebridge, Gravenhurst, Port Carling, and the Muskoka Lakes."),
        ("Can we visit Casino Niagara or Fallsview Casino?", "Yes. Casino Niagara and Fallsview Casino Resort are popular stops on our Niagara Falls day trip. We drop you at the casino entrance and pick you up whenever you are ready."),
        ("Can you arrange a Stratford Festival tour?", "Yes. We provide private transportation to the Stratford Festival for matinee and evening performances. Book transport to match your show times and explore Stratford before or after."),
        ("How far in advance should I book a tour?", "We recommend booking at least 1&ndash;2 weeks in advance for weekend tours. For custom multi-stop tours, 2&ndash;3 weeks notice allows us to plan the ideal itinerary. Same-week bookings are accommodated based on availability."),
    ],
    speak_pre="Book Your Private Ontario Tour",
    speak_h2_html='Ready to Plan Your <strong>Ontario Day Trip?</strong>',
    speak_sub="Tell us your preferred destination, date, group size, and any must-see stops. We will build a custom private tour itinerary and confirm your all-in flat rate.",
    float_badge="&#127758;&nbsp; Ontario Tours",
    float_title="Book a Private Tour",
    float_sub="Niagara Falls &middot; Wine country &middot; Custom Ontario tours",
    float_trust=["Fully Private", "Door-to-Door", "Custom Route"],
)

print("\nAll hub pages generated successfully!")
