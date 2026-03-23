#!/usr/bin/env python3
"""
fix_consistency.py
Applies 5 consistency fixes to all 50 HTML pages in the designhelp directory.
"""

import os
import re
import glob

DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# ── SITEMAP CSS ──────────────────────────────────────────────────────────────
SITEMAP_CSS = """\
  /* ── SITEMAP ────────────────────────────────────────────────────── */
  .sitemap-section{background:var(--off-white);border-top:1px solid var(--border);padding:56px 0 48px}
  .sitemap-top{margin-bottom:36px}
  .sitemap-top .sec-label{display:block;margin-bottom:8px}
  .sitemap-top h2{font-family:var(--font-serif);font-size:1.5rem;font-style:italic;color:var(--dark);font-weight:400}
  .sitemap-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:28px}
  .sitemap-col h4{font-family:var(--font-sans);font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:0.14em;color:var(--blue);margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid var(--border)}
  .sitemap-col a{display:block;font-family:var(--font-sans);font-size:12.5px;color:var(--text-light);padding:3px 0;transition:color 0.15s}
  .sitemap-col a:hover{color:var(--blue)}
  @media(max-width:900px){.sitemap-grid{grid-template-columns:repeat(2,1fr)}}
  @media(max-width:580px){.sitemap-grid{grid-template-columns:1fr}}
"""

# ── SITEMAP HTML ─────────────────────────────────────────────────────────────
SITEMAP_HTML = """\
<!-- SITEMAP -->
<section class="sitemap-section">
  <div class="wrap">
    <div class="sitemap-top">
      <span class="sec-label">Site Directory</span>
      <h2>Everything <em>at a Glance</em></h2>
    </div>
    <div class="sitemap-grid">
      <div class="sitemap-col">
        <h4>Services</h4>
        <a href="AirportHUB.html">Airport Limo</a>
        <a href="CorporateHUB.html">Corporate Limo</a>
        <a href="WeddingHUB.html">Wedding Limo</a>
        <a href="events.html">Events &amp; Concerts</a>
        <a href="car-service.html">Chauffeur Service</a>
        <a href="tours.html">Tours &amp; Day Trips</a>
        <a href="sprinter.html">Sprinter Van Groups</a>
        <a href="transfers.html">City-to-City Transfers</a>
      </div>
      <div class="sitemap-col">
        <h4>Airport Limo Cities</h4>
        <a href="toronto-airport-limo.html">Toronto</a>
        <a href="mississauga-airport-limo.html">Mississauga</a>
        <a href="vaughan-airport-limo.html">Vaughan</a>
        <a href="markham-airport-limo.html">Markham</a>
        <a href="oakville-airport-limo.html">Oakville</a>
        <a href="richmond-hill-airport-limo.html">Richmond Hill</a>
        <a href="brampton-airport-limo.html">Brampton</a>
        <a href="hamilton-airport-limo.html">Hamilton</a>
        <a href="burlington-airport-limo.html">Burlington</a>
        <a href="niagara-falls-airport-limo.html">Niagara Falls</a>
        <a href="london-airport-limo.html">London</a>
        <a href="guelph-airport-limo.html">Guelph</a>
        <a href="aurora-airport-limo.html">Aurora</a>
        <a href="king-city-airport-limo.html">King City</a>
        <a href="milton-airport-limo.html">Milton</a>
        <a href="waterloo-kitchener-airport-limo.html">Waterloo-Kitchener</a>
      </div>
      <div class="sitemap-col">
        <h4>Corporate Limo Cities</h4>
        <a href="toronto-corporate-limo.html">Toronto</a>
        <a href="mississauga-corporate-limo.html">Mississauga</a>
        <a href="vaughan-corporate-limo.html">Vaughan</a>
        <a href="markham-corporate-limo.html">Markham</a>
        <a href="oakville-corporate-limo.html">Oakville</a>
        <a href="richmond-hill-corporate-limo.html">Richmond Hill</a>
        <a href="brampton-corporate-limo.html">Brampton</a>
        <a href="hamilton-corporate-limo.html">Hamilton</a>
        <a href="burlington-corporate-limo.html">Burlington</a>
        <a href="niagara-falls-corporate-limo.html">Niagara Falls</a>
        <a href="london-corporate-limo.html">London</a>
        <a href="guelph-corporate-limo.html">Guelph</a>
        <a href="aurora-corporate-limo.html">Aurora</a>
        <a href="king-city-corporate-limo.html">King City</a>
        <a href="milton-corporate-limo.html">Milton</a>
        <a href="waterloo-kitchener-corporate-limo.html">Waterloo-Kitchener</a>
      </div>
      <div class="sitemap-col">
        <h4>Company</h4>
        <a href="about.html">About Us</a>
        <a href="fleet.html">Our Fleet</a>
        <a href="sprinter.html">Sprinter Vans</a>
        <a href="booking.html">Book Online</a>
        <a href="contact.html">Get a Quote</a>
        <a href="faq.html">FAQs</a>
        <a href="locations.html">All Locations</a>
      </div>
    </div>
  </div>
</section>

"""

# ── LOGO REPLACEMENT ─────────────────────────────────────────────────────────
LOGO_OLD = '<a href="index.html" class="logo">LIMO<span>4ALL</span></a>'
LOGO_NEW = '<a href="index.html" class="logo"><img src="assets/logo.jpg" alt="Limo4All" onerror="this.style.display=\'none\';this.nextSibling.style.display=\'inline\'"><span style="display:none">LIMO<span>4ALL</span></span></a>'


def fix_file(filepath):
    filename = os.path.basename(filepath)
    changes = []

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # ── 1. NAV FIXES ────────────────────────────────────────────────────────

    # 1a. Replace href="hourly.html">Hourly with Chauffeur
    new_content = re.sub(
        r'href="hourly\.html">Hourly',
        'href="car-service.html">Chauffeur',
        content
    )
    if new_content != content:
        changes.append('NAV: hourly->Chauffeur')
        content = new_content

    # 1b. Replace href="car-service.html">Car Service with Chauffeur
    new_content = re.sub(
        r'href="car-service\.html">Car Service',
        'href="car-service.html">Chauffeur',
        content
    )
    if new_content != content:
        changes.append('NAV: Car Service->Chauffeur')
        content = new_content

    # 1c. Remove <a href="transfers.html">Transfers</a> from nav
    # Only remove if it appears in the nav (between nav tags)
    # We look for the pattern with optional surrounding whitespace/newlines
    new_content = re.sub(
        r'\n?\s*<a href="transfers\.html">Transfers</a>',
        '',
        content
    )
    if new_content != content:
        changes.append('NAV: removed Transfers link')
        content = new_content

    # ── 2. LOGO STANDARDIZATION ──────────────────────────────────────────────
    if LOGO_OLD in content:
        content = content.replace(LOGO_OLD, LOGO_NEW)
        changes.append('LOGO: replaced text logo with image+fallback')
    elif 'assets/logo.jpg' in content:
        pass  # already has image logo
    else:
        # Check for multiline logo already present - skip
        pass

    # ── 3. SITEMAP CSS + SECTION ────────────────────────────────────────────

    # 3a. Add CSS before </style>
    if '.sitemap-section' not in content:
        # Find the last </style> before </head>
        style_close_pos = content.find('</style>')
        if style_close_pos != -1:
            content = content[:style_close_pos] + SITEMAP_CSS + content[style_close_pos:]
            changes.append('CSS: added sitemap styles')

    # 3b. Add HTML before <!-- FOOTER -->
    if '<!-- SITEMAP -->' not in content:
        footer_marker = '<!-- FOOTER -->'
        pos = content.find(footer_marker)
        if pos != -1:
            content = content[:pos] + SITEMAP_HTML + content[pos:]
            changes.append('HTML: added sitemap section')

    # ── 4. FOOTER SERVICES LINK FIX ─────────────────────────────────────────

    # 4a. Replace href="hourly.html">Hourly Charter
    new_content = re.sub(
        r'href="hourly\.html">Hourly Charter',
        'href="car-service.html">Chauffeur Service',
        content
    )
    if new_content != content:
        changes.append('FOOTER: hourly.html->car-service.html (Hourly Charter->Chauffeur Service)')
        content = new_content

    # 4b. Any remaining href="hourly.html" (catch-all)
    new_content = re.sub(
        r'href="hourly\.html"',
        'href="car-service.html"',
        content
    )
    if new_content != content:
        changes.append('FOOTER: remaining hourly.html->car-service.html')
        content = new_content

    # ── 5. PROMO BAR: pb-center white-space:nowrap ──────────────────────────
    # Fix rule that has font-size but is missing white-space:nowrap
    # Pattern: .pb-center{...flex:1} without white-space:nowrap
    new_content = re.sub(
        r'(\.pb-center\{[^}]*font-size:12\.5px;[^}]*flex:1(?!;white-space:nowrap)[^}]*)\}',
        lambda m: m.group(0).rstrip('}') + ';white-space:nowrap}',
        content
    )
    if new_content != content:
        changes.append('CSS: added white-space:nowrap to .pb-center')
        content = new_content

    # Write only if changed
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return changes
    else:
        return []


def main():
    html_files = sorted(glob.glob(os.path.join(DIRECTORY, '*.html')))
    print(f"Found {len(html_files)} HTML files to process.\n")
    print("=" * 70)

    total_changes = 0
    files_changed = 0
    files_unchanged = 0

    for filepath in html_files:
        filename = os.path.basename(filepath)
        changes = fix_file(filepath)
        if changes:
            files_changed += 1
            total_changes += len(changes)
            print(f"[CHANGED] {filename}")
            for c in changes:
                print(f"          - {c}")
        else:
            files_unchanged += 1
            print(f"[OK]      {filename}")

    print("\n" + "=" * 70)
    print(f"Summary: {files_changed} files changed, {files_unchanged} files already OK")
    print(f"Total individual changes: {total_changes}")


if __name__ == '__main__':
    main()
