#!/usr/bin/env python3
import sys
sys.stdout.reconfigure(encoding='utf-8')

content = open('AirportHUB.html', encoding='utf-8').read()

# 1. Add CSS for airport card photos
CSS_INSERT = """  /* -- AIRPORT CARD PHOTO ---------------------------------------- */
  .airport-card-photo{height:130px;overflow:hidden;position:relative;border-radius:18px 18px 0 0}
  .airport-card-photo img{width:100%;height:100%;object-fit:cover;filter:brightness(0.82);transition:transform 0.4s ease}
  .airport-card:hover .airport-card-photo img{transform:scale(1.06)}
  .airport-card-photo-badge{position:absolute;bottom:8px;left:14px;background:var(--blue);color:#fff;font-family:var(--font-sans);font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.12em;padding:3px 10px;border-radius:50px}

"""
insert_before = '  .airport-card{'
content = content.replace(insert_before, CSS_INSERT + insert_before, 1)
print("Added CSS")

# 2. Add images to the 4 existing airport cards
airport_images = {
    'YYZ': ('images/pearsonairport.jpg', 'Toronto Pearson International'),
    'YTZ': ('images/billibishop.jpg', 'Billy Bishop Toronto City Airport'),
    'YHM': ('images/hamiltionairport.jpg', 'Hamilton International Airport'),
    'BUF': ('images/buffaloniagra%20airport.jpg', 'Buffalo Niagara International'),
}

for iata, (img_path, alt) in airport_images.items():
    iata_span = f'<span class="airport-iata">{iata}</span>'
    idx = content.find(iata_span)
    if idx == -1:
        print(f"WARN: IATA {iata} not found")
        continue
    # Find airport-card-head before this IATA
    card_head_marker = '<div class="airport-card-head">'
    card_head_idx = content.rfind(card_head_marker, 0, idx)
    if card_head_idx == -1:
        print(f"WARN: airport-card-head not found for {iata}")
        continue
    photo_html = (
        '        <div class="airport-card-photo">\n'
        f'          <img src="{img_path}" alt="{alt}" loading="lazy">\n'
        f'          <span class="airport-card-photo-badge">{iata}</span>\n'
        '        </div>\n'
        '        '
    )
    content = content[:card_head_idx] + photo_html + content[card_head_idx:]
    print(f"Added image for {iata}")

# 3. Add new airport cards before closing of airports section
new_cards = """
      <a href="AirportHUB.html" class="airport-card">
        <div class="airport-card-photo">
          <img src="images/londonontarioairport.jpg" alt="London International Airport" loading="lazy">
          <span class="airport-card-photo-badge">YXU</span>
        </div>
        <div class="airport-card-head">
          <div class="airport-iata-wrap">
            <span class="airport-iata">YXU</span>
            <span class="airport-iata-sub">Regional</span>
          </div>
          <div class="airport-head-info">
            <div class="airport-name">London International Airport</div>
            <div class="airport-location">London, Ontario<br>Air Canada, WestJet &amp; Charters</div>
          </div>
        </div>
        <div class="airport-card-body">
          <div class="airport-features">
            <span class="airport-feat"><svg viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>Flight Tracking</span>
            <span class="airport-feat"><svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>Curbside Pickup</span>
            <span class="airport-feat"><svg viewBox="0 0 24 24"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>Flat Rate</span>
          </div>
          <div class="airport-pricing">
            <div>
              <span class="airport-from">Sedan from</span>
              <span class="airport-price-val">$175<em>/flat rate</em></span>
            </div>
            <span class="airport-arrow">Book YXU Transfer &rarr;</span>
          </div>
        </div>
      </a>

      <a href="AirportHUB.html" class="airport-card">
        <div class="airport-card-photo">
          <img src="images/ottawaairport.jpg" alt="Ottawa Macdonald-Cartier International Airport" loading="lazy">
          <span class="airport-card-photo-badge">YOW</span>
        </div>
        <div class="airport-card-head">
          <div class="airport-iata-wrap">
            <span class="airport-iata">YOW</span>
            <span class="airport-iata-sub">International</span>
          </div>
          <div class="airport-head-info">
            <div class="airport-name">Ottawa International Airport</div>
            <div class="airport-location">Ottawa, Ontario<br>All Major Carriers &bull; Federal Hub</div>
          </div>
        </div>
        <div class="airport-card-body">
          <div class="airport-features">
            <span class="airport-feat"><svg viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>Flight Tracking</span>
            <span class="airport-feat"><svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>Curbside Pickup</span>
            <span class="airport-feat"><svg viewBox="0 0 24 24"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>Flat Rate</span>
          </div>
          <div class="airport-pricing">
            <div>
              <span class="airport-from">Sedan from</span>
              <span class="airport-price-val">$420<em>/flat rate</em></span>
            </div>
            <span class="airport-arrow">Book YOW Transfer &rarr;</span>
          </div>
        </div>
      </a>

      <a href="AirportHUB.html" class="airport-card">
        <div class="airport-card-photo">
          <img src="images/waterlooairport.jpg" alt="Region of Waterloo International Airport" loading="lazy">
          <span class="airport-card-photo-badge">YKF</span>
        </div>
        <div class="airport-card-head">
          <div class="airport-iata-wrap">
            <span class="airport-iata">YKF</span>
            <span class="airport-iata-sub">Regional</span>
          </div>
          <div class="airport-head-info">
            <div class="airport-name">Waterloo International Airport</div>
            <div class="airport-location">Kitchener-Waterloo, Ontario<br>CargoJet &bull; Seasonal &amp; Charter Flights</div>
          </div>
        </div>
        <div class="airport-card-body">
          <div class="airport-features">
            <span class="airport-feat"><svg viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>Flight Tracking</span>
            <span class="airport-feat"><svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>Curbside Pickup</span>
            <span class="airport-feat"><svg viewBox="0 0 24 24"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>Flat Rate</span>
          </div>
          <div class="airport-pricing">
            <div>
              <span class="airport-from">Sedan from</span>
              <span class="airport-price-val">$130<em>/flat rate</em></span>
            </div>
            <span class="airport-arrow">Book YKF Transfer &rarr;</span>
          </div>
        </div>
      </a>

      <a href="AirportHUB.html" class="airport-card">
        <div class="airport-card-photo">
          <img src="images/lakesimcoeairport.jpg" alt="Lake Simcoe Regional Airport" loading="lazy">
          <span class="airport-card-photo-badge">YLS</span>
        </div>
        <div class="airport-card-head">
          <div class="airport-iata-wrap">
            <span class="airport-iata">YLS</span>
            <span class="airport-iata-sub">Regional</span>
          </div>
          <div class="airport-head-info">
            <div class="airport-name">Lake Simcoe Regional Airport</div>
            <div class="airport-location">Barrie-Oro-Medonte, Ontario<br>Charter, Cargo &amp; Private Aviation</div>
          </div>
        </div>
        <div class="airport-card-body">
          <div class="airport-features">
            <span class="airport-feat"><svg viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>Flight Tracking</span>
            <span class="airport-feat"><svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>Curbside Pickup</span>
            <span class="airport-feat"><svg viewBox="0 0 24 24"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>Flat Rate</span>
          </div>
          <div class="airport-pricing">
            <div>
              <span class="airport-from">Sedan from</span>
              <span class="airport-price-val">$140<em>/flat rate</em></span>
            </div>
            <span class="airport-arrow">Book YLS Transfer &rarr;</span>
          </div>
        </div>
      </a>
"""

close_airports = '    </div>\n  </div>\n</section>\n\n<!-- FAQ -->'
airports_start = content.find('<!-- AIRPORTS SERVED -->')
airports_section = content[airports_start:]
close_idx = airports_section.find(close_airports)
if close_idx != -1:
    abs_idx = airports_start + close_idx
    content = content[:abs_idx] + new_cards + '\n' + content[abs_idx:]
    print("Added 4 new airport cards")
else:
    print("WARN: closing div not found")

open('AirportHUB.html', 'w', encoding='utf-8').write(content)
print("Done: AirportHUB.html updated with airport images")
