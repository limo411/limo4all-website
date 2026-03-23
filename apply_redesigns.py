#!/usr/bin/env python3
"""Apply redesigns:
1. WeddingHUB.html - merge service cards into scenario-card design
2. AirportHUB.html - convert airport grid to horizontal slider
3. Update generate_hubs.py wedding_services to match new design
"""
import re, os

BASE = os.path.dirname(os.path.abspath(__file__))

def read(f):
    with open(f, encoding='utf-8') as fh: return fh.read()

def write(f, content):
    with open(f, 'w', encoding='utf-8') as fh: fh.write(content)

# ─────────────────────────────────────────────────────────
# 1. WEDDINGHUB.HTML – unified scenario-card section
# ─────────────────────────────────────────────────────────
print("Patching WeddingHUB.html…")
p = os.path.join(BASE, 'WeddingHUB.html')
html = read(p)

NEW_WEDDING_SECTION = '''<!-- SERVICES COMBINED - WEDDING -->
<section class="airports" id="services">
  <div class="wrap">
    <span class="sec-label">Wedding Transportation Services</span>
    <h2 class="sec-h2">Every Wedding Moment <em>Perfectly Covered</em></h2>
    <p class="sec-sub" style="max-width:580px;margin-bottom:40px">From the bridal limo to the grand exit &mdash; every vehicle, every pickup, every timing milestone coordinated with elegance and precision so you focus entirely on your day.</p>
    <div class="scenario-grid" style="grid-template-columns:repeat(2,1fr)">
      <div class="scenario-card">
        <div class="scenario-cat">Bride &amp; Groom</div>
        <h4 class="scenario-h4">Bridal Limo &amp; Getaway Car</h4>
        <p class="scenario-p">A stretch limousine or luxury SUV dedicated entirely to the couple &mdash; from the getting-ready location to the ceremony, reception, and late-night hotel getaway. Complimentary champagne and red carpet included.</p>
      </div>
      <div class="scenario-card">
        <div class="scenario-cat">Bridal Party</div>
        <h4 class="scenario-h4">Multi-Vehicle Coordination</h4>
        <p class="scenario-p">Three to eight matching vehicles for the bridal party, coordinated from a single contact. Church, venue, and hotel pickups &mdash; every vehicle departs on schedule so the whole party arrives together, looking perfect.</p>
      </div>
      <div class="scenario-card">
        <div class="scenario-cat">Wedding Guests</div>
        <h4 class="scenario-h4">Guest Shuttle Service</h4>
        <p class="scenario-p">Mercedes Sprinter vans looping between hotels and the venue throughout the evening. Up to 14 guests per run &mdash; nobody drives, nobody worries, everyone gets home safely after the celebration.</p>
      </div>
      <div class="scenario-card">
        <div class="scenario-cat">Photography</div>
        <h4 class="scenario-h4">Photo Stop Coordination</h4>
        <p class="scenario-p">Your chauffeur knows Toronto&rsquo;s best photography locations &mdash; Distillery District, Scarborough Bluffs, High Park, the waterfront. Custom stops built into your timeline. Not one minute wasted.</p>
      </div>
    </div>
    <div id="wedding-more" style="display:none">
      <div class="scenario-grid" style="grid-template-columns:repeat(2,1fr);margin-top:20px">
        <div class="scenario-card">
          <div class="scenario-cat">Out-of-Town Guests</div>
          <h4 class="scenario-h4">Airport &amp; Hotel Pickup</h4>
          <p class="scenario-p">We collect your out-of-town guests from Pearson or Billy Bishop and deliver them to your venue on time. They arrive relaxed &mdash; not scrambling for transit after a long flight.</p>
        </div>
        <div class="scenario-card">
          <div class="scenario-cat">End of the Night</div>
          <h4 class="scenario-h4">Late-Night Grand Exit</h4>
          <p class="scenario-p">When the last dance ends, a pristine vehicle and uniformed chauffeur are waiting. The happy couple whisked away in style. Standalone or as part of a full-day wedding package.</p>
        </div>
      </div>
    </div>
    <div style="text-align:center;margin-top:32px;display:flex;align-items:center;justify-content:center;gap:16px;flex-wrap:wrap">
      <button onclick="var m=document.getElementById('wedding-more');m.style.display=m.style.display==='none'?'block':'none';this.textContent=m.style.display==='none'?'See All Services \u2193':'Show Less \u2191'" style="background:none;border:1px solid var(--border);border-radius:50px;padding:10px 24px;font-family:var(--font-sans);font-size:13px;font-weight:600;color:var(--text);cursor:pointer;transition:all 0.2s">See All Services &#8595;</button>
      <a href="contact.html" class="btn-primary" style="padding:11px 32px;font-size:13px">Plan Your Wedding Transport &rarr;</a>
    </div>
  </div>
</section>'''

# Replace the entire SERVICES COMBINED - WEDDING section
pattern = re.compile(
    r'<!-- SERVICES COMBINED - WEDDING -->.*?</section>',
    re.DOTALL
)
if pattern.search(html):
    html = pattern.sub(NEW_WEDDING_SECTION, html, count=1)
    print("  [OK] Replaced combined section with scenario-card design")
else:
    print("  [FAIL] Could not find SERVICES COMBINED - WEDDING section")

write(p, html)
print("  [OK] WeddingHUB.html saved")


# ─────────────────────────────────────────────────────────
# 2. AIRPORTHUB.HTML – airport card slider
# ─────────────────────────────────────────────────────────
print("\nPatching AirportHUB.html…")
p2 = os.path.join(BASE, 'AirportHUB.html')
html2 = read(p2)

# Add slider CSS before </style>
SLIDER_CSS = '''
  /* ── AIRPORT SLIDER ─────────────────────────────────────────────── */
  .apt-slider-wrap{position:relative;margin-top:48px;overflow:hidden}
  .apt-slider-track{display:flex;gap:20px;transition:transform 0.45s cubic-bezier(0.25,0.46,0.45,0.94);will-change:transform;padding:4px 2px 20px}
  .apt-slide{flex:0 0 calc(33.333% - 14px);background:var(--white);border:1px solid var(--border);border-radius:20px;overflow:hidden;text-decoration:none;color:inherit;display:flex;flex-direction:column;transition:border-color 0.25s,box-shadow 0.25s,transform 0.25s;position:relative;min-width:0}
  .apt-slide::before{content:'';position:absolute;top:0;left:0;right:0;height:4px;background:var(--blue);transform:scaleX(0);transform-origin:left;transition:transform 0.3s ease}
  .apt-slide:hover{border-color:var(--blue);box-shadow:0 12px 40px rgba(20,183,244,0.14);transform:translateY(-4px)}
  .apt-slide:hover::before{transform:scaleX(1)}
  .apt-slide-img{height:200px;overflow:hidden;position:relative;flex-shrink:0}
  .apt-slide-img img{width:100%;height:100%;object-fit:cover;filter:brightness(0.82);transition:transform 0.4s ease}
  .apt-slide:hover .apt-slide-img img{transform:scale(1.06)}
  .apt-slide-iata{position:absolute;top:12px;left:14px;background:var(--dark);color:#fff;font-family:var(--font-sans);font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;padding:4px 12px;border-radius:50px}
  .apt-slide-body{padding:22px 24px;flex:1;display:flex;flex-direction:column;gap:12px}
  .apt-slide-name{font-family:var(--font-sans);font-size:14px;font-weight:700;color:var(--dark);line-height:1.3}
  .apt-slide-loc{font-family:var(--font-sans);font-size:11.5px;color:var(--text-light);line-height:1.45}
  .apt-slide-feats{display:flex;flex-wrap:wrap;gap:6px}
  .apt-slide-feat{display:inline-flex;align-items:center;gap:5px;background:var(--blue-bg);color:var(--blue);font-family:var(--font-sans);font-size:10.5px;font-weight:600;padding:4px 10px;border-radius:50px;white-space:nowrap}
  .apt-slide-feat svg{width:11px;height:11px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
  .apt-slide-foot{margin-top:auto;padding-top:14px;border-top:1px solid var(--border);display:flex;align-items:center;justify-content:space-between}
  .apt-slide-price{font-family:var(--font-serif);font-size:1.6rem;font-style:italic;color:var(--blue);line-height:1}
  .apt-slide-price em{font-family:var(--font-sans);font-size:10.5px;font-style:normal;color:var(--text-light);font-weight:400;margin-left:2px}
  .apt-slide-arrow{font-family:var(--font-sans);font-size:11.5px;font-weight:700;color:var(--blue);text-transform:uppercase;letter-spacing:0.06em;transition:gap 0.15s}
  .apt-nav-row{display:flex;align-items:center;justify-content:center;gap:12px;margin-top:28px}
  .apt-btn{width:42px;height:42px;border-radius:50%;background:var(--white);border:1.5px solid var(--border);display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:18px;color:var(--text);transition:all 0.2s;flex-shrink:0;line-height:1}
  .apt-btn:hover{background:var(--blue);border-color:var(--blue);color:#fff}
  .apt-btn:disabled{opacity:0.35;cursor:default}
  .apt-dots{display:flex;gap:7px;align-items:center}
  .apt-dot{width:8px;height:8px;border-radius:50%;background:var(--border);cursor:pointer;transition:all 0.2s}
  .apt-dot.active{background:var(--blue);transform:scale(1.2)}
  @media(max-width:1024px){.apt-slide{flex:0 0 calc(50% - 10px)}}
  @media(max-width:640px){.apt-slide{flex:0 0 calc(100% - 4px)}}

'''

if '/* ── AIRPORT SLIDER' not in html2:
    html2 = html2.replace('</style>', SLIDER_CSS + '</style>', 1)
    print("  [OK] Added slider CSS")

# New AIRPORTS SERVED section with slider
NEW_AIRPORTS_SECTION = '''<!-- AIRPORTS SERVED -->
<section class="airports" id="coverage">
  <div class="wrap">
    <span class="sec-label">GTA &amp; Beyond</span>
    <h2 class="sec-h2">Airport Transfer <em>Routes</em></h2>
    <p class="sec-sub">Flat-rate limo service to every major airport &mdash; wherever you are in the GTA. Every transfer includes real-time flight tracking, inside terminal meet &amp; greet, and 60-minute complimentary wait.</p>
  </div>

  <!-- Slider -->
  <div class="wrap" style="overflow:visible;position:relative">
    <div class="apt-slider-wrap">
      <div class="apt-slider-track" id="aptTrack">

        <!-- YYZ -->
        <a href="airport-pearson-yyz.html" class="apt-slide">
          <div class="apt-slide-img">
            <img src="images/pearsonairport.jpg" alt="Toronto Pearson International" loading="lazy">
            <span class="apt-slide-iata">YYZ</span>
          </div>
          <div class="apt-slide-body">
            <div class="apt-slide-name">Toronto Pearson International Airport</div>
            <div class="apt-slide-loc">Mississauga, Ontario &mdash; Terminal 1 &amp; 3<br>Air Canada &bull; WestJet &bull; All Major Carriers</div>
            <div class="apt-slide-feats">
              <span class="apt-slide-feat"><svg viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>Flight Tracking</span>
              <span class="apt-slide-feat"><svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>Meet &amp; Greet</span>
              <span class="apt-slide-feat"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>60-Min Wait</span>
            </div>
            <div class="apt-slide-foot">
              <div>
                <div style="font-family:var(--font-sans);font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--text-light);margin-bottom:2px">Sedan from</div>
                <span class="apt-slide-price">$75<em>/flat rate</em></span>
              </div>
              <span class="apt-slide-arrow">View YYZ &rarr;</span>
            </div>
          </div>
        </a>

        <!-- YTZ -->
        <a href="airport-billy-bishop-ytz.html" class="apt-slide">
          <div class="apt-slide-img">
            <img src="images/billibishop.jpg" alt="Billy Bishop Toronto City Airport" loading="lazy">
            <span class="apt-slide-iata">YTZ</span>
          </div>
          <div class="apt-slide-body">
            <div class="apt-slide-name">Billy Bishop Toronto City Airport</div>
            <div class="apt-slide-loc">Toronto Island, Ontario<br>Porter Airlines &bull; Air Canada Express</div>
            <div class="apt-slide-feats">
              <span class="apt-slide-feat"><svg viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>Flight Tracking</span>
              <span class="apt-slide-feat"><svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>Curbside Greet</span>
              <span class="apt-slide-feat"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>30-Min Wait</span>
            </div>
            <div class="apt-slide-foot">
              <div>
                <div style="font-family:var(--font-sans);font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--text-light);margin-bottom:2px">Sedan from</div>
                <span class="apt-slide-price">$65<em>/flat rate</em></span>
              </div>
              <span class="apt-slide-arrow">View YTZ &rarr;</span>
            </div>
          </div>
        </a>

        <!-- YHM -->
        <a href="airport-hamilton-yhm.html" class="apt-slide">
          <div class="apt-slide-img">
            <img src="images/hamiltionairport.jpg" alt="Hamilton International Airport" loading="lazy">
            <span class="apt-slide-iata">YHM</span>
          </div>
          <div class="apt-slide-body">
            <div class="apt-slide-name">Hamilton John C. Munro Airport</div>
            <div class="apt-slide-loc">Hamilton, Ontario<br>Cargo, Charter &amp; Seasonal Carriers</div>
            <div class="apt-slide-feats">
              <span class="apt-slide-feat"><svg viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>Flight Tracking</span>
              <span class="apt-slide-feat"><svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>Curbside Pickup</span>
              <span class="apt-slide-feat"><svg viewBox="0 0 24 24"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>Flat Rate</span>
            </div>
            <div class="apt-slide-foot">
              <div>
                <div style="font-family:var(--font-sans);font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--text-light);margin-bottom:2px">Sedan from</div>
                <span class="apt-slide-price">$130<em>/flat rate</em></span>
              </div>
              <span class="apt-slide-arrow">View YHM &rarr;</span>
            </div>
          </div>
        </a>

        <!-- BUF -->
        <a href="airport-buffalo-buf.html" class="apt-slide">
          <div class="apt-slide-img">
            <img src="images/buffaloniagra%20airport.jpg" alt="Buffalo Niagara International" loading="lazy">
            <span class="apt-slide-iata">BUF</span>
          </div>
          <div class="apt-slide-body">
            <div class="apt-slide-name">Buffalo Niagara International Airport</div>
            <div class="apt-slide-loc">Buffalo, New York &mdash; USA<br>Southwest &bull; American &bull; All U.S. Carriers</div>
            <div class="apt-slide-feats">
              <span class="apt-slide-feat"><svg viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>Flight Tracking</span>
              <span class="apt-slide-feat"><svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>Border Crossing</span>
              <span class="apt-slide-feat"><svg viewBox="0 0 24 24"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>Flat Rate</span>
            </div>
            <div class="apt-slide-foot">
              <div>
                <div style="font-family:var(--font-sans);font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--text-light);margin-bottom:2px">Sedan from</div>
                <span class="apt-slide-price">$220<em>/flat rate</em></span>
              </div>
              <span class="apt-slide-arrow">View BUF &rarr;</span>
            </div>
          </div>
        </a>

        <!-- YXU -->
        <a href="AirportHUB.html" class="apt-slide">
          <div class="apt-slide-img">
            <img src="images/londonontarioairport.jpg" alt="London International Airport" loading="lazy">
            <span class="apt-slide-iata">YXU</span>
          </div>
          <div class="apt-slide-body">
            <div class="apt-slide-name">London International Airport</div>
            <div class="apt-slide-loc">London, Ontario<br>Air Canada, WestJet &amp; Charters</div>
            <div class="apt-slide-feats">
              <span class="apt-slide-feat"><svg viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>Flight Tracking</span>
              <span class="apt-slide-feat"><svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>Curbside Pickup</span>
              <span class="apt-slide-feat"><svg viewBox="0 0 24 24"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>Flat Rate</span>
            </div>
            <div class="apt-slide-foot">
              <div>
                <div style="font-family:var(--font-sans);font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--text-light);margin-bottom:2px">Sedan from</div>
                <span class="apt-slide-price">$175<em>/flat rate</em></span>
              </div>
              <span class="apt-slide-arrow">Book YXU &rarr;</span>
            </div>
          </div>
        </a>

        <!-- YOW -->
        <a href="AirportHUB.html" class="apt-slide">
          <div class="apt-slide-img">
            <img src="images/ottawaairport.jpg" alt="Ottawa Macdonald-Cartier International" loading="lazy">
            <span class="apt-slide-iata">YOW</span>
          </div>
          <div class="apt-slide-body">
            <div class="apt-slide-name">Ottawa International Airport</div>
            <div class="apt-slide-loc">Ottawa, Ontario<br>All Major Carriers &bull; Federal Hub</div>
            <div class="apt-slide-feats">
              <span class="apt-slide-feat"><svg viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>Flight Tracking</span>
              <span class="apt-slide-feat"><svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>Curbside Pickup</span>
              <span class="apt-slide-feat"><svg viewBox="0 0 24 24"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>Flat Rate</span>
            </div>
            <div class="apt-slide-foot">
              <div>
                <div style="font-family:var(--font-sans);font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--text-light);margin-bottom:2px">Sedan from</div>
                <span class="apt-slide-price">$420<em>/flat rate</em></span>
              </div>
              <span class="apt-slide-arrow">Book YOW &rarr;</span>
            </div>
          </div>
        </a>

        <!-- YKF -->
        <a href="AirportHUB.html" class="apt-slide">
          <div class="apt-slide-img">
            <img src="images/waterlooairport.jpg" alt="Waterloo International Airport" loading="lazy">
            <span class="apt-slide-iata">YKF</span>
          </div>
          <div class="apt-slide-body">
            <div class="apt-slide-name">Waterloo International Airport</div>
            <div class="apt-slide-loc">Kitchener-Waterloo, Ontario<br>CargoJet &bull; Seasonal &amp; Charter Flights</div>
            <div class="apt-slide-feats">
              <span class="apt-slide-feat"><svg viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>Flight Tracking</span>
              <span class="apt-slide-feat"><svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>Curbside Pickup</span>
              <span class="apt-slide-feat"><svg viewBox="0 0 24 24"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>Flat Rate</span>
            </div>
            <div class="apt-slide-foot">
              <div>
                <div style="font-family:var(--font-sans);font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--text-light);margin-bottom:2px">Sedan from</div>
                <span class="apt-slide-price">$130<em>/flat rate</em></span>
              </div>
              <span class="apt-slide-arrow">Book YKF &rarr;</span>
            </div>
          </div>
        </a>

        <!-- YLS -->
        <a href="AirportHUB.html" class="apt-slide">
          <div class="apt-slide-img">
            <img src="images/lakesimcoeairport.jpg" alt="Lake Simcoe Regional Airport" loading="lazy">
            <span class="apt-slide-iata">YLS</span>
          </div>
          <div class="apt-slide-body">
            <div class="apt-slide-name">Lake Simcoe Regional Airport</div>
            <div class="apt-slide-loc">Barrie-Oro-Medonte, Ontario<br>Charter, Cargo &amp; Private Aviation</div>
            <div class="apt-slide-feats">
              <span class="apt-slide-feat"><svg viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>Flight Tracking</span>
              <span class="apt-slide-feat"><svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>Curbside Pickup</span>
              <span class="apt-slide-feat"><svg viewBox="0 0 24 24"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>Flat Rate</span>
            </div>
            <div class="apt-slide-foot">
              <div>
                <div style="font-family:var(--font-sans);font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--text-light);margin-bottom:2px">Sedan from</div>
                <span class="apt-slide-price">$140<em>/flat rate</em></span>
              </div>
              <span class="apt-slide-arrow">Book YLS &rarr;</span>
            </div>
          </div>
        </a>

      </div><!-- /apt-slider-track -->
    </div><!-- /apt-slider-wrap -->

    <!-- Nav controls -->
    <div class="apt-nav-row">
      <button class="apt-btn" id="aptPrev" aria-label="Previous">&#8249;</button>
      <div class="apt-dots" id="aptDots"></div>
      <button class="apt-btn" id="aptNext" aria-label="Next">&#8250;</button>
    </div>

    <div style="text-align:center;margin-top:32px">
      <a href="contact.html" class="btn-sec-more">Get a Custom Quote for Your City &rarr;</a>
    </div>
  </div>
</section>'''

# Replace AIRPORTS SERVED section
apt_pattern = re.compile(
    r'<!-- AIRPORTS SERVED -->.*?(?=<!-- FAQ -->)',
    re.DOTALL
)
if apt_pattern.search(html2):
    html2 = apt_pattern.sub(NEW_AIRPORTS_SECTION + '\n\n', html2, count=1)
    print("  [OK] Replaced AIRPORTS SERVED with slider")
else:
    print("  [FAIL] Could not find AIRPORTS SERVED section")

# Add slider JS before </script> (the last one)
SLIDER_JS = '''
  // ── AIRPORT SLIDER ───────────────────────────────────────────────
  (function() {
    var track = document.getElementById('aptTrack');
    var prevBtn = document.getElementById('aptPrev');
    var nextBtn = document.getElementById('aptNext');
    var dotsWrap = document.getElementById('aptDots');
    if (!track || !prevBtn || !nextBtn) return;

    var slides = track.querySelectorAll('.apt-slide');
    var total = slides.length;
    var current = 0;

    function getVisible() {
      var w = track.parentElement.offsetWidth;
      if (w <= 640) return 1;
      if (w <= 1024) return 2;
      return 3;
    }

    function maxIndex() { return Math.max(0, total - getVisible()); }

    function buildDots() {
      dotsWrap.innerHTML = '';
      var pages = maxIndex() + 1;
      for (var i = 0; i < pages; i++) {
        var d = document.createElement('div');
        d.className = 'apt-dot' + (i === current ? ' active' : '');
        d.setAttribute('data-i', i);
        d.onclick = function() { go(parseInt(this.getAttribute('data-i'))); };
        dotsWrap.appendChild(d);
      }
    }

    function go(idx) {
      current = Math.max(0, Math.min(idx, maxIndex()));
      var visible = getVisible();
      var slideW = slides[0] ? slides[0].offsetWidth : 0;
      var gap = 20;
      track.style.transform = 'translateX(-' + (current * (slideW + gap)) + 'px)';
      prevBtn.disabled = current === 0;
      nextBtn.disabled = current >= maxIndex();
      dotsWrap.querySelectorAll('.apt-dot').forEach(function(d, i) {
        d.classList.toggle('active', i === current);
      });
    }

    prevBtn.onclick = function() { go(current - 1); };
    nextBtn.onclick = function() { go(current + 1); };

    buildDots();
    go(0);

    window.addEventListener('resize', function() { buildDots(); go(Math.min(current, maxIndex())); });

    // Touch/drag support
    var startX = 0, dragging = false;
    track.addEventListener('touchstart', function(e){ startX = e.touches[0].clientX; dragging = true; }, {passive:true});
    track.addEventListener('touchend', function(e){
      if (!dragging) return;
      var dx = e.changedTouches[0].clientX - startX;
      if (Math.abs(dx) > 40) go(dx < 0 ? current + 1 : current - 1);
      dragging = false;
    }, {passive:true});
  })();

'''

# Insert slider JS before the last </script> tag
last_script_pos = html2.rfind('</script>')
if last_script_pos != -1:
    html2 = html2[:last_script_pos] + SLIDER_JS + html2[last_script_pos:]
    print("  [OK] Added slider JS")

write(p2, html2)
print("  [OK] AirportHUB.html saved")


# ─────────────────────────────────────────────────────────
# 3. UPDATE generate_hubs.py wedding_services to new design
# ─────────────────────────────────────────────────────────
print("\nPatching generate_hubs.py…")
p3 = os.path.join(BASE, 'generate_hubs.py')
py = read(p3)

NEW_WEDDING_SERVICES_VAR = """wedding_services = f'''<!-- SERVICES COMBINED - WEDDING -->
<section class="airports" id="services">
  <div class="wrap">
    <span class="sec-label">Wedding Transportation Services</span>
    <h2 class="sec-h2">Every Wedding Moment <em>Perfectly Covered</em></h2>
    <p class="sec-sub" style="max-width:580px;margin-bottom:40px">From the bridal limo to the grand exit &mdash; every vehicle, every pickup, every timing milestone coordinated with elegance and precision so you focus entirely on your day.</p>
    <div class="scenario-grid" style="grid-template-columns:repeat(2,1fr)">
      <div class="scenario-card">
        <div class="scenario-cat">Bride &amp; Groom</div>
        <h4 class="scenario-h4">Bridal Limo &amp; Getaway Car</h4>
        <p class="scenario-p">A stretch limousine or luxury SUV dedicated entirely to the couple &mdash; from the getting-ready location to the ceremony, reception, and late-night hotel getaway. Complimentary champagne and red carpet included.</p>
      </div>
      <div class="scenario-card">
        <div class="scenario-cat">Bridal Party</div>
        <h4 class="scenario-h4">Multi-Vehicle Coordination</h4>
        <p class="scenario-p">Three to eight matching vehicles for the bridal party, coordinated from a single contact. Church, venue, and hotel pickups &mdash; every vehicle departs on schedule so the whole party arrives together, looking perfect.</p>
      </div>
      <div class="scenario-card">
        <div class="scenario-cat">Wedding Guests</div>
        <h4 class="scenario-h4">Guest Shuttle Service</h4>
        <p class="scenario-p">Mercedes Sprinter vans looping between hotels and the venue throughout the evening. Up to 14 guests per run &mdash; nobody drives, nobody worries, everyone gets home safely after the celebration.</p>
      </div>
      <div class="scenario-card">
        <div class="scenario-cat">Photography</div>
        <h4 class="scenario-h4">Photo Stop Coordination</h4>
        <p class="scenario-p">Your chauffeur knows Toronto&rsquo;s best photography locations &mdash; Distillery District, Scarborough Bluffs, High Park, the waterfront. Custom stops built into your timeline. Not one minute wasted.</p>
      </div>
    </div>
    <div id="wedding-more" style="display:none">
      <div class="scenario-grid" style="grid-template-columns:repeat(2,1fr);margin-top:20px">
        <div class="scenario-card">
          <div class="scenario-cat">Out-of-Town Guests</div>
          <h4 class="scenario-h4">Airport &amp; Hotel Pickup</h4>
          <p class="scenario-p">We collect your out-of-town guests from Pearson or Billy Bishop and deliver them to your venue on time. They arrive relaxed &mdash; not scrambling for transit after a long flight.</p>
        </div>
        <div class="scenario-card">
          <div class="scenario-cat">End of the Night</div>
          <h4 class="scenario-h4">Late-Night Grand Exit</h4>
          <p class="scenario-p">When the last dance ends, a pristine vehicle and uniformed chauffeur are waiting. The happy couple whisked away in style. Standalone or as part of a full-day wedding package.</p>
        </div>
      </div>
    </div>
    <div style="text-align:center;margin-top:32px;display:flex;align-items:center;justify-content:center;gap:16px;flex-wrap:wrap">
      <button onclick="var m=document.getElementById(\\'wedding-more\\');m.style.display=m.style.display===\\'none\\'?\\'block\\':\\'none\\';this.textContent=m.style.display===\\'none\\'?\\'See All Services \\u2193\\':\\'Show Less \\u2191\\'" style="background:none;border:1px solid var(--border);border-radius:50px;padding:10px 24px;font-family:var(--font-sans);font-size:13px;font-weight:600;color:var(--text);cursor:pointer;transition:all 0.2s">See All Services &#8595;</button>
      <a href="contact.html" class="btn-primary" style="padding:11px 32px;font-size:13px">Plan Your Wedding Transport &rarr;</a>
    </div>
  </div>
</section>

'''
"""

# Replace old wedding_services variable (use find/split to avoid regex backslash issues)
start_marker = "wedding_services = f'''"
end_marker = "'''\n"
start_pos = py.find(start_marker)
if start_pos != -1:
    end_pos = py.find(end_marker, start_pos + len(start_marker))
    if end_pos != -1:
        end_pos += len(end_marker)
        py = py[:start_pos] + NEW_WEDDING_SERVICES_VAR + '\n' + py[end_pos:]
        print("  [OK] Updated wedding_services in generate_hubs.py")
    else:
        print("  [FAIL] Could not find end of wedding_services block")
else:
    print("  [FAIL] Could not find wedding_services in generate_hubs.py")

write(p3, py)
print("  [OK] generate_hubs.py saved")

print("\nAll redesigns applied successfully.")
