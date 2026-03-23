#!/usr/bin/env python3
"""Comprehensive site cleanup: fix broken links, consistency, footer refs."""
import glob, re, sys
sys.stdout.reconfigure(encoding='utf-8')

changes = {}

def fix(fname, old, new, desc=""):
    global changes
    content = open(fname, encoding='utf-8').read()
    if old in content:
        content = content.replace(old, new)
        open(fname, 'w', encoding='utf-8').write(content)
        changes[fname] = changes.get(fname, [])
        changes[fname].append(desc or old[:50])
        return True
    return False

files = sorted(glob.glob('*.html'))

for f in files:
    content = open(f, encoding='utf-8').read()
    new_content = content

    # 1. Remove fifa-world-cup-2026.html footer links (page doesn't exist)
    new_content = re.sub(r'\s*<a href="fifa-world-cup-2026\.html"[^>]*>.*?</a>', '', new_content)

    # 2. Remove locations.html footer links (removed from nav, page not useful in footer)
    # Keep locations.html page itself but remove footer nav references
    # Actually locations.html exists so keep links to it - just remove from TOP nav done earlier

    # 3. Fix any remaining href="locations/city.html" style links
    new_content = re.sub(r'href="locations/([^"]+)\.html"', r'href="\1-airport-limo.html"', new_content)

    # 4. Ensure all "Get a Quote" buttons go to contact.html
    new_content = new_content.replace('href="quote.html"', 'href="contact.html"')

    # 5. Fix any airport.html or corporate.html nav refs that may have snuck in
    new_content = new_content.replace('href="airport.html"', 'href="AirportHUB.html"')
    new_content = new_content.replace('href="corporate.html"', 'href="CorporateHUB.html"')

    if new_content != content:
        open(f, 'w', encoding='utf-8').write(new_content)
        changes[f] = changes.get(f, [])
        changes[f].append('cleanup fixes')

print(f"Fixed {len(changes)} files:")
for f, c in sorted(changes.items()):
    print(f"  {f}: {', '.join(set(c))}")
