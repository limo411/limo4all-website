"""
update_footer.py
Replaces the footer in all HTML files with the new structured footer:
  Services | Vehicles | Company  (no Employment, no Technology)
"""
import os, re

FOLDER = r"c:\Users\user\OneDrive\Desktop\designhelp"

NEW_FOOTER = """<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <h3>LIMO<span>4ALL</span></h3>
        <p>Premium Ground Transportation Across Ontario. Licensed, insured and trusted by thousands of GTA passengers since 2003.</p>
        <a href="tel:+14164513106" class="footer-phone">416 451 3106</a>
        <span class="footer-email"><a href="mailto:info@limo4all.ca" style="color:rgba(255,255,255,0.35)">info@limo4all.ca</a></span>
      </div>
      <div class="footer-col">
        <h4>Services</h4>
        <a href="AirportHUB.html">Airport Limo</a>
        <a href="CorporateHUB.html">Corporate Car Service</a>
        <a href="WeddingHUB.html">Wedding Limo</a>
        <a href="car-service.html">Personal Chauffeur</a>
        <a href="events.html">Events &amp; Concerts</a>
        <a href="tours.html">Niagara Tours</a>
      </div>
      <div class="footer-col">
        <h4>Vehicles</h4>
        <a href="fleet.html#sedan">Executive Sedan</a>
        <a href="fleet.html#suv">Luxury SUV</a>
        <a href="sprinter.html">Mercedes Sprinter Van</a>
        <a href="fleet.html">Full Fleet Overview</a>
      </div>
      <div class="footer-col">
        <h4>Company</h4>
        <a href="contact.html">Contact Us</a>
        <a href="about.html">About Limo4All</a>
        <a href="faq.html">FAQ</a>
        <a href="booking.html">Book Online</a>
        <a href="privacy.html">Privacy Statement</a>
        <a href="terms.html">Terms &amp; Conditions</a>
        <a href="sitemap.html">Sitemap</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 Limo4All. All Rights Reserved.</span>
      <span>Serving Toronto, Mississauga, Vaughan, Oakville and all of Ontario.</span>
    </div>
  </div>
</footer>"""

# Regex to match from <footer class="footer"> to </footer> (including any newlines)
FOOTER_RE = re.compile(r'<footer\s+class="footer">.*?</footer>', re.DOTALL)

html_files = [f for f in os.listdir(FOLDER) if f.endswith('.html') and f != 'update_footer.py']

updated = 0
skipped = 0

for fname in sorted(html_files):
    fpath = os.path.join(FOLDER, fname)
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"[SKIP] {fname}: {e}")
        skipped += 1
        continue

    if '<footer class="footer">' not in content:
        print(f"[SKIP] {fname}: no footer found")
        skipped += 1
        continue

    new_content = FOOTER_RE.sub(NEW_FOOTER, content)

    if new_content == content:
        print(f"[SAME] {fname}: no change")
        continue

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"[OK]   {fname}")
    updated += 1

print(f"\nDone: {updated} updated, {skipped} skipped.")
