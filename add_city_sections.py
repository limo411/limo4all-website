"""
add_city_sections.py
Adds city coverage grid sections to hub pages and city pill bars to other service pages.
"""
import os, re

FOLDER = r"c:\Users\user\OneDrive\Desktop\designhelp"

# ── CSS to inject into each file's <style> block ────────────────────────
CITY_CSS = """
  /* ── CITY GRID ─────────────────────────────────────────────────── */
  .city-coverage{background:var(--off-white);padding:72px 0;border-top:1px solid var(--border)}
  .city-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:40px}
  .city-card{background:var(--white);border:1px solid var(--border);border-radius:var(--radius);padding:22px 20px;transition:all 0.2s;display:block;color:inherit;text-decoration:none}
  .city-card:hover{border-color:var(--blue);box-shadow:0 6px 24px rgba(20,183,244,0.12);transform:translateY(-3px)}
  .city-card h3{font-family:var(--font-sans);font-size:14px;font-weight:700;color:var(--dark);margin-bottom:4px}
  .city-card p{font-size:12px;color:var(--text-light);line-height:1.5;margin-bottom:10px}
  .city-card .city-arrow{font-size:11px;color:var(--blue);font-weight:700;text-transform:uppercase;letter-spacing:0.08em}
  .city-pills-wrap{display:flex;flex-wrap:wrap;gap:10px;margin-top:32px}
  .city-pill{display:inline-flex;align-items:center;gap:6px;background:var(--white);border:1px solid var(--border);border-radius:50px;padding:7px 16px;font-family:var(--font-sans);font-size:12.5px;font-weight:600;color:var(--text);box-shadow:0 2px 8px rgba(0,0,0,0.04);transition:all 0.2s}
  .city-pill:hover{border-color:var(--blue);color:var(--blue);box-shadow:0 4px 16px rgba(20,183,244,0.12)}
  .city-pill::before{content:'';width:6px;height:6px;background:var(--blue);border-radius:50%;flex-shrink:0}
  @media(max-width:1024px){.city-grid{grid-template-columns:repeat(3,1fr)}}
  @media(max-width:768px){.city-grid{grid-template-columns:repeat(2,1fr)}}
  @media(max-width:480px){.city-grid{grid-template-columns:1fr}}
"""

# ── Airport city grid section ────────────────────────────────────────────
AIRPORT_CITY_SECTION = """<!-- CITY COVERAGE -->
<section class="city-coverage" id="service-areas">
  <div class="wrap">
    <span class="sec-label">Service Areas</span>
    <h2 class="sec-h2">Airport Limo Service <em>Near You</em></h2>
    <p class="sec-sub">Flat-rate airport limo service from your city to Toronto Pearson (YYZ), Billy Bishop (YTZ) and all Ontario airports. Click your city for local pricing and details.</p>
    <div class="city-grid">
      <a href="toronto-airport-limo.html" class="city-card"><h3>Toronto</h3><p>Downtown, Etobicoke, North York, Scarborough</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="mississauga-airport-limo.html" class="city-card"><h3>Mississauga</h3><p>Square One, Port Credit, Streetsville</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="vaughan-airport-limo.html" class="city-card"><h3>Vaughan</h3><p>Woodbridge, Maple, Kleinburg, Thornhill</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="markham-airport-limo.html" class="city-card"><h3>Markham</h3><p>Unionville, Cornell, Milliken, Stouffville</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="oakville-airport-limo.html" class="city-card"><h3>Oakville</h3><p>Old Oakville, Glen Abbey, Bronte</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="richmond-hill-airport-limo.html" class="city-card"><h3>Richmond Hill</h3><p>Oak Ridges, Jefferson, Bayview Hill</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="hamilton-airport-limo.html" class="city-card"><h3>Hamilton</h3><p>Downtown, Ancaster, Stoney Creek, Dundas</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="niagara-falls-airport-limo.html" class="city-card"><h3>Niagara Falls</h3><p>Tourist District, Old Town, St. Catharines</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="brampton-airport-limo.html" class="city-card"><h3>Brampton</h3><p>Downtown, Bramalea, Heart Lake, Springdale</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="aurora-airport-limo.html" class="city-card"><h3>Aurora</h3><p>Aurora Village, Bayview, Leslie, Industrial</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="burlington-airport-limo.html" class="city-card"><h3>Burlington</h3><p>Downtown, Alton, Aldershot, Millcroft</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="king-city-airport-limo.html" class="city-card"><h3>King City</h3><p>King City Village, Schomberg, Nobleton</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="london-airport-limo.html" class="city-card"><h3>London</h3><p>Downtown, Old North, Byron, Hyde Park</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="milton-airport-limo.html" class="city-card"><h3>Milton</h3><p>Bronte Meadows, Hawthorne Village, Scott</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="guelph-airport-limo.html" class="city-card"><h3>Guelph</h3><p>Downtown, Kortright Hills, Stone Road</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="waterloo-kitchener-airport-limo.html" class="city-card"><h3>Waterloo-Kitchener</h3><p>Uptown Waterloo, Kitchener Downtown, Elmira</p><span class="city-arrow">View Details &rsaquo;</span></a>
    </div>
  </div>
</section>

"""

# ── Corporate city grid section ──────────────────────────────────────────
CORPORATE_CITY_SECTION = """<!-- CITY COVERAGE -->
<section class="city-coverage" id="service-areas">
  <div class="wrap">
    <span class="sec-label">Service Areas</span>
    <h2 class="sec-h2">Corporate Car Service <em>Near You</em></h2>
    <p class="sec-sub">Professional corporate limo and car service throughout the GTA and Southern Ontario. Select your city for local availability, business districts, and pricing.</p>
    <div class="city-grid">
      <a href="toronto-corporate-limo.html" class="city-card"><h3>Toronto</h3><p>Financial District, Bay St, King West, Midtown</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="mississauga-corporate-limo.html" class="city-card"><h3>Mississauga</h3><p>Airport Corporate Centre, City Centre, Meadowvale</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="vaughan-corporate-limo.html" class="city-card"><h3>Vaughan</h3><p>Vaughan Corporate Centre, Weston Road, Hwy 400</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="markham-corporate-limo.html" class="city-card"><h3>Markham</h3><p>Enterprise Blvd, Warden, McCowan Tech Park</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="oakville-corporate-limo.html" class="city-card"><h3>Oakville</h3><p>Winston Churchill, Ford Drive Business Park</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="richmond-hill-corporate-limo.html" class="city-card"><h3>Richmond Hill</h3><p>Hwy 7 Corridor, Yonge St, East Beaver Creek</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="hamilton-corporate-limo.html" class="city-card"><h3>Hamilton</h3><p>Downtown Core, McMaster, Ancaster Business</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="niagara-falls-corporate-limo.html" class="city-card"><h3>Niagara Falls</h3><p>Fallsview, Tourism District, St. Catharines</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="brampton-corporate-limo.html" class="city-card"><h3>Brampton</h3><p>Airport Rd Corridor, Queen St, Steeles</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="aurora-corporate-limo.html" class="city-card"><h3>Aurora</h3><p>Industrial Pkwy, St. John&apos;s, Aurora-Wellington</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="burlington-corporate-limo.html" class="city-card"><h3>Burlington</h3><p>Appleby Line, QEW Corridor, Brant St</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="king-city-corporate-limo.html" class="city-card"><h3>King City</h3><p>King Rd, Keele, Nobleton Business Area</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="london-corporate-limo.html" class="city-card"><h3>London</h3><p>Downtown, Western University, Masonville</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="milton-corporate-limo.html" class="city-card"><h3>Milton</h3><p>Commercial Corridor, Main St, Steeles</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="guelph-corporate-limo.html" class="city-card"><h3>Guelph</h3><p>Gordon St, Hwy 6, Innovation District</p><span class="city-arrow">View Details &rsaquo;</span></a>
      <a href="waterloo-kitchener-corporate-limo.html" class="city-card"><h3>Waterloo-Kitchener</h3><p>Tech Triangle, Innovation Mile, King St</p><span class="city-arrow">View Details &rsaquo;</span></a>
    </div>
  </div>
</section>

"""

# ── GTA coverage pills section (for WeddingHUB, events, car-service, tours) ──
def make_pill_section(service_label, service_h2):
    return f"""<!-- CITY COVERAGE -->
<section class="city-coverage" id="service-areas">
  <div class="wrap">
    <span class="sec-label">Service Areas</span>
    <h2 class="sec-h2">{service_h2}</h2>
    <p class="sec-sub">Serving the Greater Toronto Area and all of Southern Ontario. Call or book online for service from your city.</p>
    <div class="city-pills-wrap">
      <span class="city-pill">Toronto</span>
      <span class="city-pill">Mississauga</span>
      <span class="city-pill">Vaughan</span>
      <span class="city-pill">Markham</span>
      <span class="city-pill">Oakville</span>
      <span class="city-pill">Richmond Hill</span>
      <span class="city-pill">Hamilton</span>
      <span class="city-pill">Niagara Falls</span>
      <span class="city-pill">Brampton</span>
      <span class="city-pill">Aurora</span>
      <span class="city-pill">Burlington</span>
      <span class="city-pill">King City</span>
      <span class="city-pill">London</span>
      <span class="city-pill">Milton</span>
      <span class="city-pill">Guelph</span>
      <span class="city-pill">Waterloo-Kitchener</span>
      <span class="city-pill">Barrie</span>
      <span class="city-pill">Cambridge</span>
      <span class="city-pill">St. Catharines</span>
      <span class="city-pill">Windsor</span>
    </div>
  </div>
</section>

"""

def inject_css(content):
    """Add city CSS before closing </style> of the first <style> block."""
    if '/* ── CITY GRID' in content:
        return content  # Already has city CSS
    return content.replace('</style>', CITY_CSS + '\n</style>', 1)

def inject_before_speak(content, section_html):
    """Inject section HTML before <!-- SPEAK WITH US --> comment."""
    marker = '<!-- SPEAK WITH US -->'
    if '<!-- CITY COVERAGE -->' in content:
        return content  # Already has city section
    if marker not in content:
        # Fallback: inject before footer
        marker = '<footer class="footer">'
    return content.replace(marker, section_html + marker, 1)

tasks = [
    ('AirportHUB.html', AIRPORT_CITY_SECTION),
    ('CorporateHUB.html', CORPORATE_CITY_SECTION),
    ('WeddingHUB.html', make_pill_section('Wedding Limo', 'Wedding Limo <em>Across Ontario</em>')),
    ('events.html', make_pill_section('Events & Concerts', 'Events Limo <em>Across the GTA</em>')),
    ('car-service.html', make_pill_section('Chauffeur Service', 'Personal Chauffeur <em>Across Ontario</em>')),
    ('tours.html', make_pill_section('Tour Service', 'Tour Service <em>Across Ontario</em>')),
]

for fname, section_html in tasks:
    fpath = os.path.join(FOLDER, fname)
    if not os.path.exists(fpath):
        print(f'[SKIP] {fname}: not found')
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = inject_css(content)
    content = inject_before_speak(content, section_html)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'[OK]   {fname}')

print('\nDone.')
