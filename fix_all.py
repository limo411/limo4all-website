#!/usr/bin/env python3
"""
fix_all.py  –  Limo4All website fixer + page generator
"""

import os, re, glob

BASE = os.path.dirname(os.path.abspath(__file__))

# ── helpers ──────────────────────────────────────────────────────────────────

def read(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        return f.read()

def write(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  [OK] wrote {os.path.basename(path)}")

def fix_html(path, content):
    """Apply all Part-1 fixes to a single file's content."""
    fname = os.path.basename(path)

    # nav hub links – airport
    if fname != 'AirportHUB.html':
        content = content.replace('href="airport.html"', 'href="AirportHUB.html"')
    else:
        # in AirportHUB itself fix the self-reference too
        content = content.replace('href="airport.html" class="active"', 'href="AirportHUB.html" class="active"')
        content = content.replace('href="airport.html"', 'href="AirportHUB.html"')

    # nav hub links – corporate
    if fname != 'CorporateHUB.html':
        content = content.replace('href="corporate.html"', 'href="CorporateHUB.html"')
    else:
        content = content.replace('href="corporate.html" class="active"', 'href="CorporateHUB.html" class="active"')
        content = content.replace('href="corporate.html"', 'href="CorporateHUB.html"')

    # phone numbers
    content = content.replace('1-800-XXX-XXXX', '416 451 3106')
    content = content.replace('tel:+18001234567', 'tel:+14164513106')
    content = content.replace('sms:+18001234567', 'sms:+16473131786')
    # schema / ld+json phone if present
    content = content.replace('"telephone":"1-800-XXX-XXXX"', '"telephone":"416 451 3106"')

    # footer city links
    city_map = {
        'toronto': 'toronto-airport-limo.html',
        'mississauga': 'mississauga-airport-limo.html',
        'vaughan': 'vaughan-airport-limo.html',
        'markham': 'markham-airport-limo.html',
        'oakville': 'oakville-airport-limo.html',
        'richmond-hill': 'richmond-hill-airport-limo.html',
        'hamilton': 'hamilton-airport-limo.html',
        'niagara': 'niagara-falls-airport-limo.html',
        'niagara-falls': 'niagara-falls-airport-limo.html',
    }
    for city, target in city_map.items():
        content = content.replace(f'href="locations/{city}.html"', f'href="{target}"')

    return content

# ── extract CSS from AirportHUB.html ─────────────────────────────────────────

hub_path = os.path.join(BASE, 'AirportHUB.html')
hub_src  = read(hub_path)
m = re.search(r'<style>(.*?)</style>', hub_src, re.DOTALL)
CSS = m.group(1) if m else '/* CSS not found */'
print(f"Extracted CSS: {len(CSS)} chars")

# ── Part 1: fix every HTML file ───────────────────────────────────────────────

html_files = glob.glob(os.path.join(BASE, '**', '*.html'), recursive=True)
print(f"\nPART 1: fixing {len(html_files)} HTML files …")
for path in sorted(html_files):
    original = read(path)
    fixed    = fix_html(path, original)
    if fixed != original:
        write(path, fixed)
        print(f"  patched {os.path.relpath(path, BASE)}")
    else:
        print(f"  ok      {os.path.relpath(path, BASE)}")

# ── shared building blocks ────────────────────────────────────────────────────

PROMO_BAR = '''<div class="promo-bar">
  <strong>Flat-Rate Limo Service &mdash; No Surge Pricing Ever.</strong>&nbsp; Toronto from $75 &nbsp;&mdash;&nbsp; <a href="tel:+14164513106">Call 416 451 3106</a>
</div>'''

def header(active=''):
    links = [
        ('index.html',      'Home'),
        ('AirportHUB.html', 'Airport'),
        ('CorporateHUB.html','Corporate'),
        ('wedding.html',    'Wedding'),
        ('events.html',     'Events'),
        ('hourly.html',     'Hourly'),
        ('tours.html',      'Tours'),
        ('fleet.html',      'Fleet'),
        ('locations.html',  'Locations'),
        ('contact.html',    'Contact'),
    ]
    nav_items = ''
    for href, label in links:
        cls = ' class="active"' if label.lower() == active.lower() else ''
        nav_items += f'\n      <a href="{href}"{cls}>{label}</a>'
    return f'''<header class="header">
  <div class="header-inner">
    <a href="index.html" class="logo">
      <img src="assets/logo.jpg" alt="Limo4All" onerror="this.style.display=\'none\';this.nextSibling.style.display=\'block\'">
      <span style="display:none">LIMO<span>4ALL</span></span>
    </a>
    <nav class="nav" id="main-nav">{nav_items}
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
</header>'''

FOOTER = '''<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <h3>LIMO<span>4ALL</span></h3>
        <p>Premium Ground Transportation Across Ontario. Licensed, insured, Canadian-owned and operated.</p>
        <a href="tel:+14164513106" class="footer-phone">416 451 3106</a>
        <span class="footer-email">info@limo4all.ca</span>
      </div>
      <div class="footer-col">
        <h4>Services</h4>
        <a href="AirportHUB.html">Airport Limo</a>
        <a href="CorporateHUB.html">Corporate Car Service</a>
        <a href="wedding.html">Wedding Limo</a>
        <a href="events.html">Events &amp; Concerts</a>
        <a href="hourly.html">Hourly Charter</a>
        <a href="tours.html">Niagara Tours</a>
        <a href="sprinter.html">Sprinter Van Groups</a>
        <a href="transfers.html">City-to-City Transfers</a>
      </div>
      <div class="footer-col">
        <h4>Locations</h4>
        <a href="toronto-airport-limo.html">Toronto</a>
        <a href="mississauga-airport-limo.html">Mississauga</a>
        <a href="vaughan-airport-limo.html">Vaughan</a>
        <a href="markham-airport-limo.html">Markham</a>
        <a href="oakville-airport-limo.html">Oakville</a>
        <a href="richmond-hill-airport-limo.html">Richmond Hill</a>
        <a href="hamilton-airport-limo.html">Hamilton</a>
        <a href="niagara-falls-airport-limo.html">Niagara Falls</a>
      </div>
      <div class="footer-col">
        <h4>Quick Links</h4>
        <a href="booking.html">Book Online</a>
        <a href="contact.html">Get a Quote</a>
        <a href="fleet.html">Fleet Overview</a>
        <a href="faq.html">FAQ</a>
        <a href="about.html">About Us</a>
        <a href="locations.html">All Locations</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 Limo4All. All Rights Reserved. Canadian-owned and operated.</span>
      <span>Serving Toronto, Mississauga, Vaughan and all of Ontario.</span>
    </div>
  </div>
</footer>'''

JS = '''<script>
  document.querySelectorAll('.faq-q').forEach(function(q){
    q.addEventListener('click',function(){
      var item=q.parentElement;
      var isOpen=item.classList.contains('open');
      document.querySelectorAll('.faq-item').forEach(function(i){i.classList.remove('open');var a=i.querySelector('.faq-a');if(a)a.style.display='none';});
      if(!isOpen){item.classList.add('open');var ans=item.querySelector('.faq-a');if(ans)ans.style.display='block';}
    });
  });
  var ham=document.getElementById('hamburger');var nav=document.getElementById('main-nav');
  if(ham&&nav){ham.addEventListener('click',function(){nav.classList.toggle('open');});}
</script>'''

def page(title, meta_desc, active_nav, body_html):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,minimum-scale=1">
  <title>{title}</title>
  <meta name="description" content="{meta_desc}">
  <style>{CSS}
  /* ── page extras ── */
  .loc-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:40px}}
  .loc-card{{background:var(--white);border:1px solid var(--border);border-radius:var(--radius);padding:24px 20px;text-align:center;transition:all .2s;display:block;color:inherit}}
  .loc-card:hover{{border-color:var(--blue);box-shadow:0 6px 24px rgba(20,183,244,.12);transform:translateY(-3px)}}
  .loc-card h3{{font-family:var(--font-sans);font-size:15px;font-weight:700;color:var(--dark);margin-bottom:6px}}
  .loc-card p{{font-size:12px;color:var(--text-light);line-height:1.5;margin-bottom:10px}}
  .loc-card .loc-arrow{{font-size:11px;color:var(--blue);font-weight:700;text-transform:uppercase;letter-spacing:.08em}}
  .about-grid{{display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center;padding:80px 0}}
  .about-stats{{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:32px}}
  .about-stat{{background:var(--blue-bg);border-radius:var(--radius);padding:24px;text-align:center}}
  .about-stat-num{{font-family:var(--font-serif);font-size:2.5rem;font-style:italic;color:var(--blue);display:block;line-height:1}}
  .about-stat-label{{font-family:var(--font-sans);font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.1em;color:var(--text-light);margin-top:6px;display:block}}
  .route-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:40px}}
  .route-card{{background:var(--white);border:1px solid var(--border);border-radius:var(--radius);padding:28px 24px;transition:all .2s}}
  .route-card:hover{{border-color:var(--blue);box-shadow:0 6px 24px rgba(20,183,244,.12);transform:translateY(-3px)}}
  .route-card h3{{font-family:var(--font-serif);font-size:1.15rem;font-style:italic;color:var(--dark);margin-bottom:8px}}
  .route-card .route-price{{font-family:var(--font-serif);font-size:1.7rem;font-style:italic;color:var(--blue);line-height:1;margin-bottom:4px}}
  .route-card p{{font-size:12.5px;color:var(--text-light);line-height:1.6}}
  @media(max-width:1024px){{.loc-grid{{grid-template-columns:repeat(2,1fr)}}.route-grid{{grid-template-columns:repeat(2,1fr)}}.about-grid{{grid-template-columns:1fr;gap:40px}}}}
  @media(max-width:580px){{.loc-grid{{grid-template-columns:1fr}}.route-grid{{grid-template-columns:1fr}}}}
  </style>
</head>
<body>
{PROMO_BAR}
{header(active_nav)}
{body_html}
{FOOTER}
{JS}
</body>
</html>'''

# ══════════════════════════════════════════════════════════════════════════════
# fleet.html
# ══════════════════════════════════════════════════════════════════════════════

fleet_body = '''
<!-- HERO -->
<section class="hero">
  <div class="wrap">
    <div class="hero-breadcrumb">
      <a href="index.html">Home</a><span class="sep">&rsaquo;</span><span>Fleet</span>
    </div>
    <h1 style="font-family:var(--font-serif);font-size:clamp(2.1rem,4.5vw,3.1rem);font-weight:400;font-style:italic;color:var(--dark);line-height:1.15;margin-bottom:16px">
      Our Premium <strong style="color:var(--blue);font-style:normal;font-weight:700;display:block">Fleet</strong>
    </h1>
    <p class="hero-sub">Executive sedans, luxury SUVs, and Sprinter vans &mdash; all professionally maintained and available 24/7 across Ontario.</p>
    <div class="hero-trust">
      <span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
      <span>4.9 Rating</span>
      <span class="sep">&middot;</span>
      <span>All vehicles licensed &amp; insured</span>
      <span class="sep">&middot;</span>
      <span>Professional chauffeurs</span>
    </div>
    <div class="hero-ctas">
      <a href="booking.html" class="btn-primary">Book Online</a>
      <a href="contact.html" class="btn-outline-dark">Get a Quote</a>
    </div>
  </div>
</section>

<!-- FLEET GRID -->
<section class="fleet">
  <div class="wrap">
    <span class="sec-label">Our Vehicles</span>
    <h2 class="sec-h2">Choose Your <em>Perfect Ride</em></h2>
    <p class="sec-sub">Every vehicle is immaculately maintained, GPS-tracked, and driven by a professional chauffeur.</p>
    <div class="fleet-grid" style="margin-top:40px">

      <!-- Sedan -->
      <div class="fleet-card">
        <div class="fleet-img">
          <img src="images/fleet-sedan.png" alt="Executive Sedan" onerror="this.style.background=\'#1c1c20\'">
          <span class="fleet-badge">Most Popular</span>
        </div>
        <div class="fleet-body">
          <h3>Executive Sedan</h3>
          <span class="fleet-model">Lincoln Continental / Mercedes E-Class</span>
          <div class="fleet-specs">
            <span class="fleet-spec">3 Passengers</span>
            <span class="fleet-spec">3 Bags</span>
            <span class="fleet-spec">Climate Control</span>
            <span class="fleet-spec">WiFi</span>
          </div>
          <p>Perfect for solo travellers or couples. Leather seats, tinted windows, complimentary water, and a professional chauffeur.</p>
          <div class="fleet-foot">
            <div class="fleet-price">$75 <span>from / airport run</span></div>
            <a href="booking.html" class="btn-fleet-book">Book Now</a>
          </div>
        </div>
      </div>

      <!-- SUV -->
      <div class="fleet-card">
        <div class="fleet-img">
          <img src="images/fleet-suv.png" alt="Luxury SUV" onerror="this.style.background=\'#1c1c20\'">
          <span class="fleet-badge">Best for Groups</span>
        </div>
        <div class="fleet-body">
          <h3>Luxury SUV</h3>
          <span class="fleet-model">Cadillac Escalade / Lincoln Navigator</span>
          <div class="fleet-specs">
            <span class="fleet-spec">6 Passengers</span>
            <span class="fleet-spec">6 Bags</span>
            <span class="fleet-spec">Premium Sound</span>
            <span class="fleet-spec">WiFi</span>
          </div>
          <p>Ideal for families, corporate groups, or anyone who wants extra space and commanding road presence.</p>
          <div class="fleet-foot">
            <div class="fleet-price">$95 <span>from / airport run</span></div>
            <a href="booking.html" class="btn-fleet-book">Book Now</a>
          </div>
        </div>
      </div>

      <!-- Sprinter -->
      <div class="fleet-card">
        <div class="fleet-img">
          <img src="images/fleet-sprinter.png" alt="Mercedes Sprinter Van" onerror="this.style.background=\'#1c1c20\'">
          <span class="fleet-badge">Large Groups</span>
        </div>
        <div class="fleet-body">
          <h3>Mercedes Sprinter Van</h3>
          <span class="fleet-model">Mercedes-Benz Sprinter 2500</span>
          <div class="fleet-specs">
            <span class="fleet-spec">14 Passengers</span>
            <span class="fleet-spec">Large Cargo</span>
            <span class="fleet-spec">USB Charging</span>
            <span class="fleet-spec">WiFi</span>
          </div>
          <p>The ultimate group transport solution for weddings, corporate events, airport shuttles, and Niagara tours.</p>
          <div class="fleet-foot">
            <div class="fleet-price">$150 <span>from / airport run</span></div>
            <a href="booking.html" class="btn-fleet-book">Book Now</a>
          </div>
        </div>
      </div>

    </div>
  </div>
</section>

<!-- COMPARISON -->
<section class="compare">
  <div class="wrap">
    <div class="center">
      <span class="sec-label">Why Not Rideshare?</span>
      <h2 class="sec-h2">Limo4All vs <em>Rideshare Apps</em></h2>
    </div>
    <div class="compare-wrap">
      <div class="compare-us">
        <h3>Limo4All</h3>
        <ul class="compare-list">
          <li>Flat rate — price locked at booking</li>
          <li>Professional licensed chauffeur</li>
          <li>Real-time flight tracking</li>
          <li>60-min free wait on international arrivals</li>
          <li>Meet &amp; greet inside terminal</li>
          <li>Guaranteed vehicle class</li>
          <li>24/7 live dispatch support</li>
          <li>Canadian-owned &amp; operated</li>
        </ul>
      </div>
      <div class="compare-vs"><div class="vs-badge">VS</div></div>
      <div class="compare-them">
        <h3>Rideshare Apps</h3>
        <ul class="compare-list">
          <li>Surge pricing at peak hours</li>
          <li>Random, unvetted drivers</li>
          <li>No flight tracking</li>
          <li>Extra charges for wait time</li>
          <li>Curbside pickup only</li>
          <li>Vehicle type not guaranteed</li>
          <li>App-only support</li>
          <li>Foreign-owned corporations</li>
        </ul>
      </div>
    </div>
    <div class="compare-ctas">
      <a href="booking.html" class="btn-primary">Book a Flat-Rate Ride</a>
      <a href="contact.html" class="btn-outline-dark">Get a Quote</a>
    </div>
  </div>
</section>

<!-- FAQ -->
<section class="faq">
  <div class="wrap">
    <div class="center">
      <span class="sec-label">Fleet FAQ</span>
      <h2 class="sec-h2">Common <em>Questions</em></h2>
    </div>
    <div class="faq-grid">

      <div class="faq-item">
        <div class="faq-q">How many passengers does each vehicle hold?<svg viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></div>
        <div class="faq-a">The Executive Sedan holds up to 3 passengers, the Luxury SUV up to 6, and the Mercedes Sprinter Van up to 14. Contact us if you need a custom arrangement for larger groups.</div>
      </div>

      <div class="faq-item">
        <div class="faq-q">Are all vehicles professionally maintained?<svg viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></div>
        <div class="faq-a">Yes. Every vehicle in our fleet is serviced on a strict maintenance schedule, cleaned before each trip, and inspected daily. We only operate late-model vehicles.</div>
      </div>

      <div class="faq-item">
        <div class="faq-q">Can I request a specific vehicle model?<svg viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></div>
        <div class="faq-a">You can request a vehicle class (sedan, SUV, Sprinter). Specific model availability depends on scheduling. Call us and we will do our best to accommodate.</div>
      </div>

      <div class="faq-item">
        <div class="faq-q">Do vehicles have WiFi and charging ports?<svg viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></div>
        <div class="faq-a">Yes. All vehicles are equipped with complimentary WiFi and USB charging ports. Water and mints are provided in every vehicle.</div>
      </div>

      <div class="faq-item">
        <div class="faq-q">Are child seats available?<svg viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></div>
        <div class="faq-a">Child seats are available upon request at no extra charge. Please mention this when booking so we can ensure the correct seat type is fitted before your ride.</div>
      </div>

      <div class="faq-item">
        <div class="faq-q">What if I need more than 14 passengers?<svg viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></div>
        <div class="faq-a">We can arrange multiple vehicles travelling together for larger groups. Contact us for a custom group quote and we will coordinate seamlessly.</div>
      </div>

    </div>
    <div class="faq-cta">
      <a href="faq.html" class="btn-faq-more">View All FAQs</a>
    </div>
  </div>
</section>

<!-- CTA -->
<section class="speak">
  <div class="wrap">
    <div class="speak-grid">
      <div>
        <span class="speak-pre">Ready to Ride?</span>
        <h2 class="speak-h2">Book Your <strong>Premium Vehicle</strong> Today</h2>
        <p class="speak-sub">Flat rates, professional chauffeurs, and 24/7 availability across Ontario. No surge pricing — ever.</p>
        <div class="speak-channels">
          <a href="tel:+14164513106" class="speak-channel">
            <div class="speak-ch-icon"><svg viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81 19.79 19.79 0 01.11 1.18 2 2 0 012.11 0h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 14.92z"/></svg></div>
            <div><div class="speak-ch-label">Call Us</div><div class="speak-ch-value">416 451 3106</div><div class="speak-ch-note">24/7 live dispatch</div></div>
          </a>
          <a href="sms:+16473131786" class="speak-channel">
            <div class="speak-ch-icon"><svg viewBox="0 0 24 24"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg></div>
            <div><div class="speak-ch-label">Text / SMS</div><div class="speak-ch-value">647 313 1786</div><div class="speak-ch-note">Fast reply guaranteed</div></div>
          </a>
          <a href="booking.html" class="speak-channel">
            <div class="speak-ch-icon"><svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg></div>
            <div><div class="speak-ch-label">Book Online</div><div class="speak-ch-value">Instant Confirmation</div><div class="speak-ch-note">Secure online booking</div></div>
          </a>
        </div>
      </div>
      <div class="speak-form-card">
        <h4>Request a Fleet Quote</h4>
        <div class="sf-row">
          <input class="sf-field" type="text" placeholder="Your Name">
          <input class="sf-field" type="tel" placeholder="Phone Number">
        </div>
        <input class="sf-field" type="email" placeholder="Email Address" style="width:100%;margin-bottom:10px">
        <select class="sf-field" style="width:100%;margin-bottom:10px">
          <option value="">Select Vehicle Class</option>
          <option>Executive Sedan</option>
          <option>Luxury SUV</option>
          <option>Mercedes Sprinter Van</option>
        </select>
        <textarea class="sf-textarea" placeholder="Trip details (date, pickup, destination, passengers)"></textarea>
        <div class="sf-btns">
          <button class="btn-speak-submit">Send Quote Request</button>
          <a href="tel:+14164513106" class="btn-speak-call">Call Now</a>
        </div>
        <p class="sf-note">We respond within 15 minutes during business hours.</p>
      </div>
    </div>
  </div>
</section>
'''

write(os.path.join(BASE, 'fleet.html'),
      page('Our Fleet – Executive Sedans, SUVs & Sprinter Vans | Limo4All',
           'Browse the Limo4All premium fleet: executive sedans from $75, luxury SUVs from $95, and Mercedes Sprinter vans from $150. Professional chauffeurs, 24/7 across Ontario.',
           'Fleet', fleet_body))

# ══════════════════════════════════════════════════════════════════════════════
# contact.html
# ══════════════════════════════════════════════════════════════════════════════

contact_body = '''
<section class="hero">
  <div class="wrap">
    <div class="hero-breadcrumb">
      <a href="index.html">Home</a><span class="sep">&rsaquo;</span><span>Contact</span>
    </div>
    <h1 style="font-family:var(--font-serif);font-size:clamp(2.1rem,4.5vw,3.1rem);font-weight:400;font-style:italic;color:var(--dark);line-height:1.15;margin-bottom:16px">
      Get in <strong style="color:var(--blue);font-style:normal;font-weight:700;display:block">Touch</strong>
    </h1>
    <p class="hero-sub">Questions, quotes, or custom requests — our 24/7 dispatch team is always ready to help. Call, text, or fill in the form.</p>
    <div class="hero-trust">
      <span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
      <span>4.9 Rating</span>
      <span class="sep">&middot;</span>
      <span>Replies in under 15 minutes</span>
      <span class="sep">&middot;</span>
      <span>24/7 Dispatch</span>
    </div>
  </div>
</section>

<section class="speak">
  <div class="wrap">
    <div class="speak-grid">
      <div>
        <span class="speak-pre">Contact Us</span>
        <h2 class="speak-h2">We&rsquo;re Available <strong>Around the Clock</strong></h2>
        <p class="speak-sub">Licensed, insured, and Canadian-owned. Our dispatchers are available 24 hours a day, 7 days a week.</p>
        <div class="speak-channels">
          <a href="tel:+14164513106" class="speak-channel">
            <div class="speak-ch-icon"><svg viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81 19.79 19.79 0 01.11 1.18 2 2 0 012.11 0h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 14.92z"/></svg></div>
            <div><div class="speak-ch-label">Call Anytime</div><div class="speak-ch-value">416 451 3106</div><div class="speak-ch-note">24/7 live dispatch — no bots</div></div>
          </a>
          <a href="sms:+16473131786" class="speak-channel">
            <div class="speak-ch-icon"><svg viewBox="0 0 24 24"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg></div>
            <div><div class="speak-ch-label">Text / SMS</div><div class="speak-ch-value">647 313 1786</div><div class="speak-ch-note">Send your trip details by text</div></div>
          </a>
          <a href="mailto:info@limo4all.ca" class="speak-channel">
            <div class="speak-ch-icon"><svg viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg></div>
            <div><div class="speak-ch-label">Email</div><div class="speak-ch-value">info@limo4all.ca</div><div class="speak-ch-note">For quotes and partnerships</div></div>
          </a>
          <a href="booking.html" class="speak-channel">
            <div class="speak-ch-icon"><svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg></div>
            <div><div class="speak-ch-label">Book Online</div><div class="speak-ch-value">Instant Confirmation</div><div class="speak-ch-note">Fast, secure online booking</div></div>
          </a>
        </div>
      </div>
      <div class="speak-form-card">
        <h4>Request a Quote or Ask a Question</h4>
        <div class="sf-row">
          <input class="sf-field" type="text" placeholder="Your Name">
          <input class="sf-field" type="tel" placeholder="Phone Number">
        </div>
        <input class="sf-field" type="email" placeholder="Email Address" style="width:100%;margin-bottom:10px">
        <select class="sf-field" style="width:100%;margin-bottom:10px">
          <option value="">Service Type</option>
          <option>Airport Transfer</option>
          <option>Corporate Car</option>
          <option>Wedding Limo</option>
          <option>Hourly Charter</option>
          <option>Niagara Tour</option>
          <option>Sprinter Van</option>
          <option>City-to-City Transfer</option>
          <option>Other</option>
        </select>
        <div class="sf-row">
          <input class="sf-field" type="text" placeholder="Pickup Location">
          <input class="sf-field" type="text" placeholder="Destination">
        </div>
        <textarea class="sf-textarea" placeholder="Additional details (date, time, passengers, special requests)"></textarea>
        <div class="sf-btns">
          <button class="btn-speak-submit">Send My Request</button>
          <a href="tel:+14164513106" class="btn-speak-call">Call Now</a>
        </div>
        <p class="sf-note">We respond within 15 minutes. No obligation. No spam.</p>
      </div>
    </div>
  </div>
</section>

<!-- COVERAGE -->
<section class="why-section" style="padding:70px 0">
  <div class="wrap">
    <div class="center">
      <span class="sec-label">Service Area</span>
      <h2 class="sec-h2">We Cover All of <em>Ontario</em></h2>
      <p class="sec-sub">From Toronto Pearson to Niagara Falls, from the GTA to Ottawa — wherever you need to go, we go there.</p>
    </div>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:40px">
      <div style="background:#fff;border:1px solid var(--border);border-radius:12px;padding:18px;text-align:center">
        <div style="font-weight:700;color:var(--dark);margin-bottom:4px">Toronto</div>
        <div style="font-size:12px;color:var(--text-light)">YYZ &bull; YTZ &bull; Downtown</div>
      </div>
      <div style="background:#fff;border:1px solid var(--border);border-radius:12px;padding:18px;text-align:center">
        <div style="font-weight:700;color:var(--dark);margin-bottom:4px">Mississauga</div>
        <div style="font-size:12px;color:var(--text-light)">Airport &bull; Port Credit</div>
      </div>
      <div style="background:#fff;border:1px solid var(--border);border-radius:12px;padding:18px;text-align:center">
        <div style="font-weight:700;color:var(--dark);margin-bottom:4px">Vaughan</div>
        <div style="font-size:12px;color:var(--text-light)">Woodbridge &bull; Maple</div>
      </div>
      <div style="background:#fff;border:1px solid var(--border);border-radius:12px;padding:18px;text-align:center">
        <div style="font-weight:700;color:var(--dark);margin-bottom:4px">Markham</div>
        <div style="font-size:12px;color:var(--text-light)">Unionville &bull; Cornell</div>
      </div>
      <div style="background:#fff;border:1px solid var(--border);border-radius:12px;padding:18px;text-align:center">
        <div style="font-weight:700;color:var(--dark);margin-bottom:4px">Oakville</div>
        <div style="font-size:12px;color:var(--text-light)">Burlington &bull; Milton</div>
      </div>
      <div style="background:#fff;border:1px solid var(--border);border-radius:12px;padding:18px;text-align:center">
        <div style="font-weight:700;color:var(--dark);margin-bottom:4px">Richmond Hill</div>
        <div style="font-size:12px;color:var(--text-light)">Aurora &bull; Newmarket</div>
      </div>
      <div style="background:#fff;border:1px solid var(--border);border-radius:12px;padding:18px;text-align:center">
        <div style="font-weight:700;color:var(--dark);margin-bottom:4px">Hamilton</div>
        <div style="font-size:12px;color:var(--text-light)">YHM &bull; Stoney Creek</div>
      </div>
      <div style="background:#fff;border:1px solid var(--border);border-radius:12px;padding:18px;text-align:center">
        <div style="font-weight:700;color:var(--dark);margin-bottom:4px">Niagara Falls</div>
        <div style="font-size:12px;color:var(--text-light)">St. Catharines &bull; BUF</div>
      </div>
    </div>
  </div>
</section>
'''

write(os.path.join(BASE, 'contact.html'),
      page('Contact Limo4All – Call, Text or Get a Quote | 416 451 3106',
           'Contact Limo4All 24/7: call 416 451 3106, text 647 313 1786, or email info@limo4all.ca. Get a free quote for airport transfers, corporate car service, weddings and more.',
           'Contact', contact_body))

# ══════════════════════════════════════════════════════════════════════════════
# faq.html
# ══════════════════════════════════════════════════════════════════════════════

def faq_item(q, a):
    return f'''
      <div class="faq-item">
        <div class="faq-q">{q}<svg viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></div>
        <div class="faq-a">{a}</div>
      </div>'''

faq_body = '''
<section class="hero">
  <div class="wrap">
    <div class="hero-breadcrumb">
      <a href="index.html">Home</a><span class="sep">&rsaquo;</span><span>FAQ</span>
    </div>
    <h1 style="font-family:var(--font-serif);font-size:clamp(2.1rem,4.5vw,3.1rem);font-weight:400;font-style:italic;color:var(--dark);line-height:1.15;margin-bottom:16px">
      Frequently Asked <strong style="color:var(--blue);font-style:normal;font-weight:700;display:block">Questions</strong>
    </h1>
    <p class="hero-sub">Everything you need to know about booking a limo with Limo4All. Can&rsquo;t find your answer? Call us 24/7 at 416 451 3106.</p>
  </div>
</section>

<section class="faq" style="padding:60px 0 90px">
  <div class="wrap">

    <span class="sec-label">Airport Transfers</span>
    <h2 class="sec-h2" style="margin-bottom:24px">Airport <em>Questions</em></h2>
    <div class="faq-grid">
      ''' + faq_item('Which airports do you serve?',
        'We serve Toronto Pearson (YYZ), Billy Bishop (YTZ), Hamilton John C. Munro (YHM), and Buffalo Niagara (BUF). We also transfer to/from Ottawa (YOW) and Montreal (YUL) by arrangement.') + \
      faq_item('Do you track my flight?',
        'Yes. We monitor your flight in real-time through aviation tracking services. If your flight is delayed, your driver will adjust automatically — no phone call required.') + \
      faq_item('How long do you wait if my flight is late?',
        'We include 60 minutes of free wait time for international arrivals and 45 minutes for domestic. If you clear customs faster, your driver is already there.') + \
      faq_item('Do you offer meet and greet inside the terminal?',
        'Yes. For arrivals, your chauffeur will meet you inside the terminal at the baggage claim exit holding a name sign. There is no extra charge for this service.') + \
      faq_item('Are rates flat or does pricing change based on time/traffic?',
        'All our airport rates are fully flat — the price you see at booking is the price you pay. No surge pricing, no tolls added after the fact, no surprises.') + \
    '''
    </div>

    <span class="sec-label" style="margin-top:56px;display:block">Corporate Service</span>
    <h2 class="sec-h2" style="margin-bottom:24px">Corporate <em>Questions</em></h2>
    <div class="faq-grid">
      ''' + faq_item('Can we set up a corporate account?',
        'Absolutely. We offer corporate accounts with monthly invoicing, dedicated account managers, and priority dispatch. Contact us to set up your account.') + \
      faq_item('Do you provide executive car service for client entertainment?',
        'Yes. We regularly provide premium chauffeur service for client pickups, roadshows, and executive entertainment. Our drivers are professionally dressed and discreet.') + \
      faq_item('Can we book for multiple employees on different schedules?',
        'Yes. Our corporate dashboard lets you manage multiple bookings across your team. Or simply call our dispatch line and we will coordinate everything for you.') + \
      faq_item('Is billing available for corporate clients?',
        'Yes. Corporate accounts receive consolidated monthly invoices with trip-by-trip breakdown. We accept all major credit cards, wire transfer, and corporate PO.') + \
    '''
    </div>

    <span class="sec-label" style="margin-top:56px;display:block">Weddings &amp; Events</span>
    <h2 class="sec-h2" style="margin-bottom:24px">Wedding &amp; Event <em>Questions</em></h2>
    <div class="faq-grid">
      ''' + faq_item('How far in advance should I book for a wedding?',
        'We recommend booking at least 4–8 weeks in advance for weddings, especially during peak season (May–October). Popular dates fill quickly.') + \
      faq_item('Can you coordinate multiple vehicles for a wedding party?',
        'Yes. We specialize in multi-vehicle wedding coordination. We will create a schedule for the entire bridal party and stay in communication throughout the day.') + \
      faq_item('Do you decorate the vehicles for weddings?',
        'We offer tasteful ribbon and floral decorations on request. Please mention this when booking and we will confirm what is available for your date.') + \
      faq_item('Do you provide service for concerts and sporting events?',
        'Yes. We handle event transportation for concerts, theatre, Blue Jays and Maple Leafs games, and more. Book a point-to-point ride or hourly charter.') + \
    '''
    </div>

    <span class="sec-label" style="margin-top:56px;display:block">Hourly &amp; Tours</span>
    <h2 class="sec-h2" style="margin-bottom:24px">Hourly &amp; Tour <em>Questions</em></h2>
    <div class="faq-grid">
      ''' + faq_item('What is the minimum hourly booking?',
        'Our minimum hourly charter is 3 hours. The vehicle and chauffeur remain with you for the full duration, ready to go wherever you need.') + \
      faq_item('What is included in the Niagara Falls tour?',
        'Our Niagara day tour includes round-trip transport from anywhere in the GTA, stops at the Falls viewpoints, Clifton Hill, and optional winery visits. Duration is flexible.') + \
      faq_item('Can we customize the tour route?',
        'Yes. We love custom itineraries. Tell us what you want to see and we will plan the route. Wineries, Niagara-on-the-Lake, and the Whirlpool are popular additions.') + \
      faq_item('Is the hourly rate all-inclusive?',
        'The hourly rate includes the vehicle, chauffeur, fuel, and standard amenities. Gratuity and any admission fees at attractions are not included.') + \
    '''
    </div>

    <span class="sec-label" style="margin-top:56px;display:block">General</span>
    <h2 class="sec-h2" style="margin-bottom:24px">General <em>Questions</em></h2>
    <div class="faq-grid">
      ''' + faq_item('Is Limo4All licensed and insured?',
        'Yes. Limo4All is fully licensed under the Ontario Ministry of Transportation and carries comprehensive commercial passenger vehicle insurance. All drivers are CVOR certified.') + \
      faq_item('Is there a cancellation policy?',
        'Cancellations made 24+ hours before pickup are fully refunded. Cancellations within 24 hours may incur a 50% fee. No-shows are charged in full. Contact us for exceptional circumstances.') + \
      faq_item('What payment methods are accepted?',
        'We accept all major credit cards (Visa, Mastercard, Amex), e-Transfer, and corporate billing. Payment is collected at time of booking for most services.') + \
      faq_item('Do drivers accept tips?',
        'Gratuity is not included in our rates and is always at your discretion. A 15–20% tip is appreciated if you had an exceptional experience, but never required.') + \
    '''
    </div>

    <div class="faq-cta">
      <p style="font-family:var(--font-sans);font-size:14px;color:var(--text-light);margin-bottom:16px">Still have questions? We are happy to help.</p>
      <a href="tel:+14164513106" class="btn-faq-more">Call 416 451 3106</a>
    </div>
  </div>
</section>
'''

write(os.path.join(BASE, 'faq.html'),
      page('FAQ – Limo4All Airport & Limo Service | Ontario',
           'Answers to common questions about Limo4All airport transfers, corporate car service, wedding limos, and tours in Toronto and across Ontario.',
           '', faq_body))

# ══════════════════════════════════════════════════════════════════════════════
# booking.html
# ══════════════════════════════════════════════════════════════════════════════

booking_body = '''
<section class="hero" style="padding:70px 0 80px">
  <div class="wrap hero-grid">
    <div class="hero-content">
      <div class="hero-breadcrumb">
        <a href="index.html">Home</a><span class="sep">&rsaquo;</span><span>Book Online</span>
      </div>
      <h1 style="font-family:var(--font-serif);font-size:clamp(2.1rem,4.5vw,3.1rem);font-weight:400;font-style:italic;color:var(--dark);line-height:1.15;margin-bottom:16px">
        Book Your <strong style="color:var(--blue);font-style:normal;font-weight:700;display:block">Limo Ride</strong>
      </h1>
      <p class="hero-sub">Flat-rate pricing, instant confirmation, and a professional chauffeur waiting for you. Fill in the form or call us directly at 416 451 3106.</p>
      <div class="hero-trust">
        <span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
        <span>4.9 / 5 — 10,000+ rides</span>
        <span class="sep">&middot;</span>
        <span>Instant confirmation</span>
        <span class="sep">&middot;</span>
        <span>Free cancellation 24h+</span>
      </div>
      <!-- Trust badges -->
      <div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:24px">
        <div style="display:flex;align-items:center;gap:8px;background:var(--off-white);border:1px solid var(--border);border-radius:50px;padding:8px 16px;font-family:var(--font-sans);font-size:12px;font-weight:600;color:var(--text-light)">&#9989; Flat Rate Guaranteed</div>
        <div style="display:flex;align-items:center;gap:8px;background:var(--off-white);border:1px solid var(--border);border-radius:50px;padding:8px 16px;font-family:var(--font-sans);font-size:12px;font-weight:600;color:var(--text-light)">&#9989; No Surge Pricing</div>
        <div style="display:flex;align-items:center;gap:8px;background:var(--off-white);border:1px solid var(--border);border-radius:50px;padding:8px 16px;font-family:var(--font-sans);font-size:12px;font-weight:600;color:var(--text-light)">&#9989; Licensed &amp; Insured</div>
        <div style="display:flex;align-items:center;gap:8px;background:var(--off-white);border:1px solid var(--border);border-radius:50px;padding:8px 16px;font-family:var(--font-sans);font-size:12px;font-weight:600;color:var(--text-light)">&#9989; Canadian Owned</div>
      </div>
    </div>
    <!-- BOOKING FORM -->
    <div class="hero-book-card">
      <div class="hbc-top">
        <span class="hbc-label">Booking Request</span>
        <span class="hbc-secure">
          <svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          Secure &amp; Flat Rate
        </span>
      </div>
      <p class="hbc-title">Complete Your Booking</p>

      <div class="hbc-row">
        <div class="hbc-field-wrap">
          <svg class="hbc-field-icon" viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          <input class="hbc-field" type="text" placeholder="Your Full Name">
        </div>
        <div class="hbc-field-wrap">
          <svg class="hbc-field-icon" viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81 19.79 19.79 0 01.11 1.18 2 2 0 012.11 0h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 14.92z"/></svg>
          <input class="hbc-field" type="tel" placeholder="Phone Number">
        </div>
      </div>

      <div class="hbc-field-wrap">
        <svg class="hbc-field-icon" viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
        <input class="hbc-field" type="email" placeholder="Email Address">
      </div>

      <div class="hbc-field-wrap">
        <svg class="hbc-field-icon" viewBox="0 0 24 24"><circle cx="12" cy="10" r="3"/><path d="M12 2a8 8 0 00-8 8c0 5.25 8 14 8 14s8-8.75 8-14a8 8 0 00-8-8z"/></svg>
        <input class="hbc-field" type="text" placeholder="Pickup Address / City">
      </div>

      <div class="hbc-field-wrap">
        <svg class="hbc-field-icon" viewBox="0 0 24 24"><path d="M3 17l7-7 4 4 7-11"/><polyline points="14 3 21 3 21 10"/></svg>
        <input class="hbc-field" type="text" placeholder="Destination / Airport">
      </div>

      <div class="hbc-row">
        <div class="hbc-field-wrap">
          <svg class="hbc-field-icon" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <input class="hbc-field" type="date" placeholder="Date">
        </div>
        <div class="hbc-field-wrap">
          <svg class="hbc-field-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          <input class="hbc-field" type="time" placeholder="Time">
        </div>
      </div>

      <div class="hbc-row">
        <div class="hbc-field-wrap">
          <select class="hbc-field" style="padding-left:14px">
            <option value="">Vehicle Class</option>
            <option>Executive Sedan (3 pax)</option>
            <option>Luxury SUV (6 pax)</option>
            <option>Mercedes Sprinter Van (14 pax)</option>
          </select>
        </div>
        <div class="hbc-field-wrap">
          <select class="hbc-field" style="padding-left:14px">
            <option value="">Passengers</option>
            <option>1</option><option>2</option><option>3</option>
            <option>4</option><option>5</option><option>6</option>
            <option>7–10</option><option>11–14</option>
          </select>
        </div>
      </div>

      <div class="hbc-divider">Additional Info</div>

      <div class="hbc-field-wrap">
        <input class="hbc-field" type="text" placeholder="Flight number (if airport pickup)" style="padding-left:14px">
      </div>

      <button class="btn-hbc-submit">
        <svg viewBox="0 0 24 24"><path d="M22 2L11 13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
        Send Booking Request
      </button>
      <div class="hbc-foot">
        <span class="hbc-foot-item"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>Flat Rate Guaranteed</span>
        <span class="hbc-foot-item"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>No Surge Pricing</span>
        <span class="hbc-foot-item"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>Free 24h Cancellation</span>
      </div>
    </div>
  </div>
</section>

<!-- PHONE CTA -->
<div style="background:var(--dark);padding:40px 0">
  <div class="wrap" style="text-align:center">
    <p style="font-family:var(--font-sans);font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:.12em;color:rgba(255,255,255,.4);margin-bottom:10px">Prefer to speak with someone?</p>
    <a href="tel:+14164513106" style="font-family:var(--font-serif);font-size:2.4rem;font-weight:700;font-style:italic;color:var(--blue);display:block;margin-bottom:6px">416 451 3106</a>
    <p style="font-family:var(--font-sans);font-size:13px;color:rgba(255,255,255,.35)">24/7 live dispatch &mdash; or text us at <a href="sms:+16473131786" style="color:var(--blue)">647 313 1786</a></p>
  </div>
</div>
'''

write(os.path.join(BASE, 'booking.html'),
      page('Book Your Limo Online – Flat Rate Airport & Limo Service | Limo4All',
           'Book your limo online with Limo4All. Flat-rate airport transfers, corporate car service, wedding limos and more. Instant confirmation. Call 416 451 3106.',
           '', booking_body))

# ══════════════════════════════════════════════════════════════════════════════
# locations.html
# ══════════════════════════════════════════════════════════════════════════════

locations_body = '''
<section class="hero">
  <div class="wrap">
    <div class="hero-breadcrumb">
      <a href="index.html">Home</a><span class="sep">&rsaquo;</span><span>Locations</span>
    </div>
    <h1 style="font-family:var(--font-serif);font-size:clamp(2.1rem,4.5vw,3.1rem);font-weight:400;font-style:italic;color:var(--dark);line-height:1.15;margin-bottom:16px">
      Service Areas Across <strong style="color:var(--blue);font-style:normal;font-weight:700;display:block">Ontario</strong>
    </h1>
    <p class="hero-sub">From the GTA to Niagara Falls, from Hamilton to Ottawa — Limo4All provides premium ground transportation to every corner of Ontario.</p>
    <div class="hero-ctas">
      <a href="booking.html" class="btn-primary">Book a Ride</a>
      <a href="contact.html" class="btn-outline-dark">Get a Quote</a>
    </div>
  </div>
</section>

<section style="background:var(--off-white);padding:80px 0">
  <div class="wrap">
    <span class="sec-label">Airport Limo Cities</span>
    <h2 class="sec-h2">Airport Transfer <em>Locations</em></h2>
    <p class="sec-sub">Flat-rate airport pickups and drop-offs from across the GTA and Ontario. Flight tracking and meet &amp; greet included.</p>
    <div class="loc-grid">
      <a href="toronto-airport-limo.html" class="loc-card">
        <h3>Toronto</h3>
        <p>YYZ Pearson &bull; Billy Bishop YTZ &bull; Downtown Toronto</p>
        <span class="loc-arrow">View &rarr;</span>
      </a>
      <a href="mississauga-airport-limo.html" class="loc-card">
        <h3>Mississauga</h3>
        <p>Airport District &bull; Port Credit &bull; Streetsville</p>
        <span class="loc-arrow">View &rarr;</span>
      </a>
      <a href="vaughan-airport-limo.html" class="loc-card">
        <h3>Vaughan</h3>
        <p>Woodbridge &bull; Maple &bull; Kleinburg &bull; Concord</p>
        <span class="loc-arrow">View &rarr;</span>
      </a>
      <a href="markham-airport-limo.html" class="loc-card">
        <h3>Markham</h3>
        <p>Unionville &bull; Cornell &bull; Milliken &bull; Thornhill</p>
        <span class="loc-arrow">View &rarr;</span>
      </a>
      <a href="oakville-airport-limo.html" class="loc-card">
        <h3>Oakville</h3>
        <p>Downtown Oakville &bull; Bronte &bull; Glen Abbey</p>
        <span class="loc-arrow">View &rarr;</span>
      </a>
      <a href="richmond-hill-airport-limo.html" class="loc-card">
        <h3>Richmond Hill</h3>
        <p>Jefferson &bull; Langstaff &bull; Oak Ridges</p>
        <span class="loc-arrow">View &rarr;</span>
      </a>
      <a href="hamilton-airport-limo.html" class="loc-card">
        <h3>Hamilton</h3>
        <p>YHM Airport &bull; Downtown &bull; Dundas &bull; Ancaster</p>
        <span class="loc-arrow">View &rarr;</span>
      </a>
      <a href="niagara-falls-airport-limo.html" class="loc-card">
        <h3>Niagara Falls</h3>
        <p>Clifton Hill &bull; Niagara-on-the-Lake &bull; BUF Airport</p>
        <span class="loc-arrow">View &rarr;</span>
      </a>
      <a href="brampton-airport-limo.html" class="loc-card">
        <h3>Brampton</h3>
        <p>Downtown &bull; Bramalea &bull; Heart Lake</p>
        <span class="loc-arrow">View &rarr;</span>
      </a>
      <a href="burlington-airport-limo.html" class="loc-card">
        <h3>Burlington</h3>
        <p>Downtown &bull; Aldershot &bull; Waterdown</p>
        <span class="loc-arrow">View &rarr;</span>
      </a>
      <a href="aurora-airport-limo.html" class="loc-card">
        <h3>Aurora</h3>
        <p>Aurora Village &bull; Bayview Wellington</p>
        <span class="loc-arrow">View &rarr;</span>
      </a>
      <a href="guelph-airport-limo.html" class="loc-card">
        <h3>Guelph</h3>
        <p>Downtown &bull; University District &bull; Kortright</p>
        <span class="loc-arrow">View &rarr;</span>
      </a>
    </div>
  </div>
</section>

<section style="background:var(--white);padding:80px 0">
  <div class="wrap">
    <span class="sec-label">Corporate Limo Cities</span>
    <h2 class="sec-h2">Corporate Car <em>Locations</em></h2>
    <p class="sec-sub">Executive car service for business travel, client pickups, and corporate events across Ontario.</p>
    <div class="loc-grid">
      <a href="toronto-corporate-limo.html" class="loc-card">
        <h3>Toronto</h3>
        <p>Financial District &bull; Bay St &bull; King West</p>
        <span class="loc-arrow">View &rarr;</span>
      </a>
      <a href="mississauga-corporate-limo.html" class="loc-card">
        <h3>Mississauga</h3>
        <p>City Centre &bull; Airport Corporate Park</p>
        <span class="loc-arrow">View &rarr;</span>
      </a>
      <a href="vaughan-corporate-limo.html" class="loc-card">
        <h3>Vaughan</h3>
        <p>VMC &bull; Highway 400 Corridor</p>
        <span class="loc-arrow">View &rarr;</span>
      </a>
      <a href="markham-corporate-limo.html" class="loc-card">
        <h3>Markham</h3>
        <p>Tech Park &bull; IBM &bull; IBM Canada HQ</p>
        <span class="loc-arrow">View &rarr;</span>
      </a>
      <a href="oakville-corporate-limo.html" class="loc-card">
        <h3>Oakville</h3>
        <p>Corporate Campus &bull; Ford Canada &bull; QEW</p>
        <span class="loc-arrow">View &rarr;</span>
      </a>
      <a href="richmond-hill-corporate-limo.html" class="loc-card">
        <h3>Richmond Hill</h3>
        <p>High Tech Road &bull; Hwy 7 Corridor</p>
        <span class="loc-arrow">View &rarr;</span>
      </a>
      <a href="hamilton-corporate-limo.html" class="loc-card">
        <h3>Hamilton</h3>
        <p>Innovation District &bull; McMaster &bull; Steel City</p>
        <span class="loc-arrow">View &rarr;</span>
      </a>
      <a href="niagara-falls-corporate-limo.html" class="loc-card">
        <h3>Niagara Falls</h3>
        <p>Casino Niagara &bull; Convention Centre</p>
        <span class="loc-arrow">View &rarr;</span>
      </a>
    </div>
  </div>
</section>

<!-- CTA -->
<section class="stats-strip">
  <div class="stats-inner">
    <div class="stat-block"><span class="stat-num">25+</span><span class="stat-label">Cities Served</span></div>
    <div class="stat-block"><span class="stat-num">10k+</span><span class="stat-label">Rides Completed</span></div>
    <div class="stat-block"><span class="stat-num">4.9</span><span class="stat-label">Average Rating</span></div>
    <div class="stat-block"><span class="stat-num">24/7</span><span class="stat-label">Availability</span></div>
  </div>
</section>
'''

write(os.path.join(BASE, 'locations.html'),
      page('Limo Service Locations Across Ontario | Limo4All',
           'Limo4All serves 25+ cities across Ontario including Toronto, Mississauga, Vaughan, Markham, Oakville, Hamilton and Niagara Falls. Airport and corporate limo available.',
           'Locations', locations_body))

# ══════════════════════════════════════════════════════════════════════════════
# about.html
# ══════════════════════════════════════════════════════════════════════════════

about_body = '''
<section class="hero">
  <div class="wrap">
    <div class="hero-breadcrumb">
      <a href="index.html">Home</a><span class="sep">&rsaquo;</span><span>About Us</span>
    </div>
    <h1 style="font-family:var(--font-serif);font-size:clamp(2.1rem,4.5vw,3.1rem);font-weight:400;font-style:italic;color:var(--dark);line-height:1.15;margin-bottom:16px">
      About <strong style="color:var(--blue);font-style:normal;font-weight:700;display:block">Limo4All</strong>
    </h1>
    <p class="hero-sub">Ontario&rsquo;s trusted, Canadian-owned limo service. Over two decades of premium ground transportation across the Greater Toronto Area and beyond.</p>
  </div>
</section>

<section style="background:var(--off-white);padding:0 0 80px">
  <div class="wrap">
    <div class="about-grid">
      <div>
        <span class="sec-label">Our Story</span>
        <h2 class="sec-h2">Built on <em>Trust &amp; Service</em></h2>
        <p class="sec-sub" style="margin-bottom:20px">Limo4All was founded in the Greater Toronto Area by a Canadian entrepreneur who believed that professional ground transportation should be reliable, transparent, and accessible to everyone — not just executives.</p>
        <p class="sec-sub" style="margin-bottom:20px">Over 20 years later, we have completed over 10,000 rides across Ontario, serving individual travellers, families, corporations, wedding parties, and tour groups with the same unwavering commitment to quality.</p>
        <p class="sec-sub">We are fully licensed under the Ontario Ministry of Transportation, fully insured with commercial passenger vehicle coverage, and proudly 100% Canadian-owned and operated.</p>
        <div class="about-stats">
          <div class="about-stat"><span class="about-stat-num">20+</span><span class="about-stat-label">Years in Business</span></div>
          <div class="about-stat"><span class="about-stat-num">10k+</span><span class="about-stat-label">Rides Completed</span></div>
          <div class="about-stat"><span class="about-stat-num">4.9</span><span class="about-stat-label">Average Rating</span></div>
          <div class="about-stat"><span class="about-stat-num">25+</span><span class="about-stat-label">Ontario Cities</span></div>
        </div>
      </div>
      <div>
        <div style="background:var(--dark);border-radius:var(--radius);padding:48px 40px;color:#fff">
          <span style="font-family:var(--font-sans);font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.18em;color:var(--blue);display:block;margin-bottom:14px">Our Values</span>
          <h3 style="font-family:var(--font-serif);font-size:1.6rem;font-style:italic;color:#fff;margin-bottom:24px;line-height:1.3">Why Clients Choose Us</h3>
          <div style="display:flex;flex-direction:column;gap:16px">
            <div style="display:flex;gap:14px;align-items:flex-start">
              <div style="width:36px;height:36px;background:var(--blue);border-radius:10px;display:flex;align-items:center;justify-content:center;flex-shrink:0">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
              </div>
              <div><div style="font-weight:700;color:#fff;margin-bottom:4px">Flat-Rate Transparency</div><div style="font-size:13px;color:rgba(255,255,255,.5);line-height:1.6">The price you see is the price you pay. No surge pricing, no hidden fees.</div></div>
            </div>
            <div style="display:flex;gap:14px;align-items:flex-start">
              <div style="width:36px;height:36px;background:var(--blue);border-radius:10px;display:flex;align-items:center;justify-content:center;flex-shrink:0">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
              </div>
              <div><div style="font-weight:700;color:#fff;margin-bottom:4px">Punctuality Guaranteed</div><div style="font-size:13px;color:rgba(255,255,255,.5);line-height:1.6">We track your flight and ensure your driver is always there on time.</div></div>
            </div>
            <div style="display:flex;gap:14px;align-items:flex-start">
              <div style="width:36px;height:36px;background:var(--blue);border-radius:10px;display:flex;align-items:center;justify-content:center;flex-shrink:0">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
              </div>
              <div><div style="font-weight:700;color:#fff;margin-bottom:4px">Fully Licensed &amp; Insured</div><div style="font-size:13px;color:rgba(255,255,255,.5);line-height:1.6">CVOR certified drivers, Ontario MTO licensed, and fully insured for your peace of mind.</div></div>
            </div>
            <div style="display:flex;gap:14px;align-items:flex-start">
              <div style="width:36px;height:36px;background:var(--blue);border-radius:10px;display:flex;align-items:center;justify-content:center;flex-shrink:0">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87"/><path d="M16 3.13a4 4 0 010 7.75"/></svg>
              </div>
              <div><div style="font-weight:700;color:#fff;margin-bottom:4px">Canadian-Owned</div><div style="font-size:13px;color:rgba(255,255,255,.5);line-height:1.6">Proudly local. Your fare supports a Canadian business and Canadian jobs.</div></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- STATS STRIP -->
<section class="stats-strip">
  <div class="stats-inner">
    <div class="stat-block"><span class="stat-num">20+</span><span class="stat-label">Years Experience</span></div>
    <div class="stat-block"><span class="stat-num">10k+</span><span class="stat-label">Happy Clients</span></div>
    <div class="stat-block"><span class="stat-num">4.9★</span><span class="stat-label">Google Rating</span></div>
    <div class="stat-block"><span class="stat-num">24/7</span><span class="stat-label">Live Dispatch</span></div>
  </div>
</section>

<!-- CTA -->
<section class="speak">
  <div class="wrap" style="text-align:center">
    <span class="speak-pre">Ready to Ride with Us?</span>
    <h2 class="speak-h2" style="margin:0 auto 16px;max-width:500px">Experience the <strong>Limo4All Difference</strong></h2>
    <p class="speak-sub" style="margin:0 auto 32px;max-width:460px">Join 10,000+ satisfied customers. Book online in minutes or call our 24/7 dispatch team.</p>
    <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap">
      <a href="booking.html" class="btn-primary">Book Online Now</a>
      <a href="tel:+14164513106" style="display:inline-flex;align-items:center;gap:8px;background:transparent;color:rgba(255,255,255,.8);font-family:var(--font-sans);font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;padding:12px 28px;border-radius:50px;border:2px solid rgba(255,255,255,.25)">Call 416 451 3106</a>
    </div>
  </div>
</section>
'''

write(os.path.join(BASE, 'about.html'),
      page('About Limo4All – Canadian-Owned Limo Service, Ontario',
           'Limo4All is a Canadian-owned premium limo and ground transportation company serving Ontario for over 20 years. Licensed, insured, 24/7 dispatch. Learn our story.',
           '', about_body))

# ══════════════════════════════════════════════════════════════════════════════
# sprinter.html
# ══════════════════════════════════════════════════════════════════════════════

sprinter_body = '''
<section class="hero">
  <div class="wrap">
    <div class="hero-breadcrumb">
      <a href="index.html">Home</a><span class="sep">&rsaquo;</span><a href="fleet.html">Fleet</a><span class="sep">&rsaquo;</span><span>Sprinter Van</span>
    </div>
    <h1 style="font-family:var(--font-serif);font-size:clamp(2.1rem,4.5vw,3.1rem);font-weight:400;font-style:italic;color:var(--dark);line-height:1.15;margin-bottom:16px">
      Mercedes Sprinter <strong style="color:var(--blue);font-style:normal;font-weight:700;display:block">Van Service</strong>
    </h1>
    <p class="hero-sub">The ultimate group transport solution for 7 to 14 passengers. Perfect for weddings, corporate groups, airport shuttles, and Niagara tours across Ontario.</p>
    <div class="hero-trust">
      <span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
      <span>4.9 Rating</span>
      <span class="sep">&middot;</span>
      <span>Up to 14 Passengers</span>
      <span class="sep">&middot;</span>
      <span>From $150 / trip</span>
    </div>
    <div class="hero-ctas">
      <a href="booking.html" class="btn-primary">Book a Sprinter</a>
      <a href="contact.html" class="btn-outline-dark">Get a Group Quote</a>
    </div>
  </div>
</section>

<!-- FLEET CARD -->
<section class="fleet">
  <div class="wrap">
    <span class="sec-label">The Vehicle</span>
    <h2 class="sec-h2">Mercedes-Benz <em>Sprinter 2500</em></h2>
    <div class="fleet-grid" style="margin-top:32px;grid-template-columns:1fr 1fr">
      <div class="fleet-card">
        <div class="fleet-img">
          <img src="images/fleet-sprinter.png" alt="Mercedes Sprinter Van" onerror="this.style.background=\'#1c1c20\'">
          <span class="fleet-badge">Up to 14 Passengers</span>
        </div>
        <div class="fleet-body">
          <h3>Mercedes Sprinter Van</h3>
          <span class="fleet-model">Mercedes-Benz Sprinter 2500 — Late Model</span>
          <div class="fleet-specs">
            <span class="fleet-spec">14 Passengers</span>
            <span class="fleet-spec">Large Luggage Bay</span>
            <span class="fleet-spec">WiFi Onboard</span>
            <span class="fleet-spec">USB Charging</span>
            <span class="fleet-spec">Climate Control</span>
            <span class="fleet-spec">Tinted Windows</span>
          </div>
          <p>Premium leather seating, panoramic windows, ample headroom, and a separate luggage bay. Your group travels together in comfort and style.</p>
          <div class="fleet-foot">
            <div class="fleet-price">$150 <span>from / airport</span></div>
            <a href="booking.html" class="btn-fleet-book">Book Now</a>
          </div>
        </div>
      </div>
      <div style="padding:40px 0">
        <span class="sec-label">Perfect For</span>
        <h3 style="font-family:var(--font-serif);font-size:1.5rem;font-style:italic;color:#fff;margin-bottom:24px">Every Group <em>Occasion</em></h3>
        <div style="display:flex;flex-direction:column;gap:14px">
          <div style="display:flex;align-items:flex-start;gap:14px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:16px 18px">
            <div style="font-size:1.4rem;flex-shrink:0">&#9992;</div>
            <div><div style="font-weight:700;color:#fff;margin-bottom:3px">Airport Group Shuttles</div><div style="font-size:12.5px;color:rgba(255,255,255,.45);line-height:1.6">One vehicle for the whole team. Flat airport rate, flight tracking, meet &amp; greet.</div></div>
          </div>
          <div style="display:flex;align-items:flex-start;gap:14px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:16px 18px">
            <div style="font-size:1.4rem;flex-shrink:0">&#128141;</div>
            <div><div style="font-weight:700;color:#fff;margin-bottom:3px">Wedding Party Transport</div><div style="font-size:12.5px;color:rgba(255,255,255,.45);line-height:1.6">Move the entire bridal party together. Ribbons and decorations available.</div></div>
          </div>
          <div style="display:flex;align-items:flex-start;gap:14px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:16px 18px">
            <div style="font-size:1.4rem;flex-shrink:0">&#127970;</div>
            <div><div style="font-weight:700;color:#fff;margin-bottom:3px">Corporate Off-Sites &amp; Events</div><div style="font-size:12.5px;color:rgba(255,255,255,.45);line-height:1.6">Team building trips, conferences, and executive group transport.</div></div>
          </div>
          <div style="display:flex;align-items:flex-start;gap:14px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:16px 18px">
            <div style="font-size:1.4rem;flex-shrink:0">&#127966;</div>
            <div><div style="font-weight:700;color:#fff;margin-bottom:3px">Niagara Falls Tours</div><div style="font-size:12.5px;color:rgba(255,255,255,.45);line-height:1.6">Day tours from the GTA. Falls, wineries, Niagara-on-the-Lake.</div></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- FAQ -->
<section class="faq">
  <div class="wrap">
    <div class="center">
      <span class="sec-label">Sprinter FAQ</span>
      <h2 class="sec-h2">Common <em>Questions</em></h2>
    </div>
    <div class="faq-grid">
      <div class="faq-item">
        <div class="faq-q">How many passengers does the Sprinter hold?<svg viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></div>
        <div class="faq-a">Our Mercedes Sprinter 2500 comfortably seats up to 14 passengers with luggage space in the rear bay. For groups larger than 14, we can arrange multiple vehicles.</div>
      </div>
      <div class="faq-item">
        <div class="faq-q">Is WiFi available in the Sprinter?<svg viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></div>
        <div class="faq-a">Yes. All our Sprinter vans include complimentary WiFi, USB charging ports at every seat, climate control, and tinted privacy glass.</div>
      </div>
      <div class="faq-item">
        <div class="faq-q">What is the minimum booking for a Sprinter?<svg viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></div>
        <div class="faq-a">For point-to-point transfers there is no minimum. For hourly charters the minimum is 3 hours. Airport runs are booked as flat-rate single trips.</div>
      </div>
      <div class="faq-item">
        <div class="faq-q">Can we decorate the Sprinter for a wedding?<svg viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></div>
        <div class="faq-a">Yes. We offer tasteful floral and ribbon decoration for weddings. Please mention this when booking and confirm specifics with our team.</div>
      </div>
      <div class="faq-item">
        <div class="faq-q">How far in advance should we book?<svg viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></div>
        <div class="faq-a">We recommend booking at least 2–3 weeks in advance for weekend events and 1 week for weekday trips. Popular summer and holiday dates fill quickly.</div>
      </div>
      <div class="faq-item">
        <div class="faq-q">Do you provide Sprinter service outside the GTA?<svg viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></div>
        <div class="faq-a">Yes. Our Sprinter operates across all of Ontario including Niagara, Hamilton, London, Ottawa, and beyond. Contact us for a custom long-distance quote.</div>
      </div>
    </div>
  </div>
</section>

<!-- CTA -->
<section class="speak">
  <div class="wrap" style="text-align:center">
    <span class="speak-pre">Ready to Book?</span>
    <h2 class="speak-h2" style="margin:0 auto 16px;max-width:500px">Book Your <strong>Group Sprinter</strong> Today</h2>
    <p class="speak-sub" style="margin:0 auto 32px;max-width:460px">Call or text for an instant group quote. Flat rates, professional chauffeur, and 24/7 dispatch.</p>
    <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap">
      <a href="booking.html" class="btn-primary">Book Online</a>
      <a href="tel:+14164513106" style="display:inline-flex;align-items:center;gap:8px;background:transparent;color:rgba(255,255,255,.8);font-family:var(--font-sans);font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;padding:12px 28px;border-radius:50px;border:2px solid rgba(255,255,255,.25)">Call 416 451 3106</a>
    </div>
  </div>
</section>
'''

write(os.path.join(BASE, 'sprinter.html'),
      page('Mercedes Sprinter Van Service – Group Transport Ontario | Limo4All',
           'Book a Mercedes Sprinter van for groups of 7–14. Perfect for airport shuttles, weddings, corporate events, and Niagara tours. Flat rates across Ontario. Call 416 451 3106.',
           '', sprinter_body))

# ══════════════════════════════════════════════════════════════════════════════
# transfers.html
# ══════════════════════════════════════════════════════════════════════════════

transfers_body = '''
<section class="hero">
  <div class="wrap">
    <div class="hero-breadcrumb">
      <a href="index.html">Home</a><span class="sep">&rsaquo;</span><span>City-to-City Transfers</span>
    </div>
    <h1 style="font-family:var(--font-serif);font-size:clamp(2.1rem,4.5vw,3.1rem);font-weight:400;font-style:italic;color:var(--dark);line-height:1.15;margin-bottom:16px">
      City-to-City <strong style="color:var(--blue);font-style:normal;font-weight:700;display:block">Transfers</strong>
    </h1>
    <p class="hero-sub">Flat-rate intercity limo service across Ontario and beyond. Toronto to Niagara, Ottawa, Montreal, and every city in between — door to door in comfort.</p>
    <div class="hero-trust">
      <span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
      <span>4.9 Rating</span>
      <span class="sep">&middot;</span>
      <span>Flat-rate pricing</span>
      <span class="sep">&middot;</span>
      <span>Door-to-door service</span>
    </div>
    <div class="hero-ctas">
      <a href="booking.html" class="btn-primary">Book a Transfer</a>
      <a href="contact.html" class="btn-outline-dark">Get a Route Quote</a>
    </div>
  </div>
</section>

<!-- POPULAR ROUTES -->
<section style="background:var(--off-white);padding:80px 0">
  <div class="wrap">
    <span class="sec-label">Popular Routes</span>
    <h2 class="sec-h2">Most Booked <em>City Transfers</em></h2>
    <p class="sec-sub">All prices are flat rates per vehicle. No tolls or fuel surcharges added after booking.</p>
    <div class="route-grid">
      <div class="route-card">
        <div style="font-family:var(--font-sans);font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--blue);margin-bottom:8px">Most Popular</div>
        <h3>Toronto &rarr; Niagara Falls</h3>
        <div class="route-price">$199</div>
        <p style="font-size:11px;color:var(--text-light);margin-bottom:12px">per vehicle / flat rate</p>
        <p>1.5 hour scenic drive from downtown Toronto to Clifton Hill or any Niagara address. Includes Niagara-on-the-Lake stops on request.</p>
        <a href="booking.html" class="btn-primary" style="font-size:12px;padding:10px 22px;margin-top:16px">Book This Route</a>
      </div>
      <div class="route-card">
        <h3>Toronto &rarr; Ottawa</h3>
        <div class="route-price">$499</div>
        <p style="font-size:11px;color:var(--text-light);margin-bottom:12px">per vehicle / flat rate</p>
        <p>4.5 hour comfort ride from GTA to the nation&rsquo;s capital. Ideal for government officials, business travellers, and families.</p>
        <a href="booking.html" class="btn-primary" style="font-size:12px;padding:10px 22px;margin-top:16px">Book This Route</a>
      </div>
      <div class="route-card">
        <h3>Toronto &rarr; Montreal</h3>
        <div class="route-price">$699</div>
        <p style="font-size:11px;color:var(--text-light);margin-bottom:12px">per vehicle / flat rate</p>
        <p>5.5 hour door-to-door luxury transfer. Skip the airport hassle for shorter business trips or family visits.</p>
        <a href="booking.html" class="btn-primary" style="font-size:12px;padding:10px 22px;margin-top:16px">Book This Route</a>
      </div>
      <div class="route-card">
        <h3>Toronto &rarr; Hamilton</h3>
        <div class="route-price">$99</div>
        <p style="font-size:11px;color:var(--text-light);margin-bottom:12px">per vehicle / flat rate</p>
        <p>45-minute flat-rate transfer between Toronto and Hamilton (including YHM airport). Fast, reliable, no surge pricing.</p>
        <a href="booking.html" class="btn-primary" style="font-size:12px;padding:10px 22px;margin-top:16px">Book This Route</a>
      </div>
      <div class="route-card">
        <h3>Toronto &rarr; London, ON</h3>
        <div class="route-price">$299</div>
        <p style="font-size:11px;color:var(--text-light);margin-bottom:12px">per vehicle / flat rate</p>
        <p>2-hour transfer from the GTA to London, Ontario. Ideal for Western University visits, business trips, and family travel.</p>
        <a href="booking.html" class="btn-primary" style="font-size:12px;padding:10px 22px;margin-top:16px">Book This Route</a>
      </div>
      <div class="route-card">
        <h3>Toronto &rarr; Buffalo, NY</h3>
        <div class="route-price">$249</div>
        <p style="font-size:11px;color:var(--text-light);margin-bottom:12px">per vehicle / flat rate</p>
        <p>Cross-border transfer to Buffalo Niagara International (BUF). Stress-free border crossing with a professional driver.</p>
        <a href="booking.html" class="btn-primary" style="font-size:12px;padding:10px 22px;margin-top:16px">Book This Route</a>
      </div>
    </div>
    <p style="text-align:center;margin-top:32px;font-family:var(--font-sans);font-size:13px;color:var(--text-light)">Don&rsquo;t see your route? <a href="contact.html" style="color:var(--blue);font-weight:600">Contact us for a custom quote &rarr;</a></p>
  </div>
</section>

<!-- WHY CHOOSE -->
<section class="why-section" style="padding:70px 0">
  <div class="wrap">
    <div class="center">
      <span class="sec-label">Why Book With Us</span>
      <h2 class="sec-h2">The Smarter Way to <em>Travel Between Cities</em></h2>
      <p class="sec-sub">No airports, no delays, no luggage fees. Just a professional chauffeur and a comfortable ride, door to door.</p>
    </div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:48px">
      <div style="background:#fff;border:1px solid var(--border);border-radius:var(--radius);padding:32px 28px">
        <div style="width:48px;height:48px;background:var(--blue-bg);border-radius:12px;display:flex;align-items:center;justify-content:center;margin-bottom:18px">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="var(--blue)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
        </div>
        <h4 style="font-family:var(--font-sans);font-size:14px;font-weight:700;color:var(--dark);margin-bottom:8px">Flat Rate Pricing</h4>
        <p style="font-size:13px;color:var(--text-light);line-height:1.65">The price we quote is the price you pay. No fuel surcharges, no tolls added, no surprises on your receipt.</p>
      </div>
      <div style="background:#fff;border:1px solid var(--border);border-radius:var(--radius);padding:32px 28px">
        <div style="width:48px;height:48px;background:var(--blue-bg);border-radius:12px;display:flex;align-items:center;justify-content:center;margin-bottom:18px">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="var(--blue)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        </div>
        <h4 style="font-family:var(--font-sans);font-size:14px;font-weight:700;color:var(--dark);margin-bottom:8px">Always On Time</h4>
        <p style="font-size:13px;color:var(--text-light);line-height:1.65">Your driver will be at your door before the scheduled pickup time — every time. We track traffic and route in real-time.</p>
      </div>
      <div style="background:#fff;border:1px solid var(--border);border-radius:var(--radius);padding:32px 28px">
        <div style="width:48px;height:48px;background:var(--blue-bg);border-radius:12px;display:flex;align-items:center;justify-content:center;margin-bottom:18px">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="var(--blue)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></svg>
        </div>
        <h4 style="font-family:var(--font-sans);font-size:14px;font-weight:700;color:var(--dark);margin-bottom:8px">Comfort &amp; Privacy</h4>
        <p style="font-size:13px;color:var(--text-light);line-height:1.65">Work, relax, or sleep in a premium vehicle. Tinted windows, WiFi, charging ports, and complimentary water onboard.</p>
      </div>
    </div>
  </div>
</section>

<!-- FAQ -->
<section class="faq">
  <div class="wrap">
    <div class="center">
      <span class="sec-label">Transfers FAQ</span>
      <h2 class="sec-h2">Common <em>Questions</em></h2>
    </div>
    <div class="faq-grid">
      <div class="faq-item">
        <div class="faq-q">Do prices include tolls and fuel?<svg viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></div>
        <div class="faq-a">Yes. All quoted prices are fully inclusive of fuel, driver time, and highway tolls. You will never see extra charges on your receipt beyond the agreed fare.</div>
      </div>
      <div class="faq-item">
        <div class="faq-q">Can I book a return trip at the same time?<svg viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></div>
        <div class="faq-a">Yes. We offer a small discount for round-trip bookings made at the same time. Mention this when booking and we will apply the discount automatically.</div>
      </div>
      <div class="faq-item">
        <div class="faq-q">Do you cross the US border?<svg viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></div>
        <div class="faq-a">Yes. We regularly transfer clients to Buffalo Niagara (BUF) and can arrange other US destinations by request. Please ensure you have valid travel documents for border crossing.</div>
      </div>
      <div class="faq-item">
        <div class="faq-q">Can I make multiple stops on a city-to-city transfer?<svg viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg></div>
        <div class="faq-a">Yes. We accommodate en-route stops (e.g., winery visits on the Niagara run). Let us know your stops when booking and we will adjust the itinerary and pricing accordingly.</div>
      </div>
    </div>
  </div>
</section>
'''

write(os.path.join(BASE, 'transfers.html'),
      page('City-to-City Transfers – Ontario Intercity Limo Service | Limo4All',
           'Flat-rate city-to-city limo transfers across Ontario. Toronto to Niagara $199, Ottawa $499, Montreal $699, Hamilton $99, Buffalo $249. Door-to-door. Call 416 451 3106.',
           '', transfers_body))

print("\nDone! All fixes applied and all pages created.")
