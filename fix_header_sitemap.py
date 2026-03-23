#!/usr/bin/env python3
"""
fix_header_sitemap.py
Batch fixes across all .html files in the designhelp directory.

1. Remove <!-- SITEMAP --> section from HTML body
2. Remove sitemap CSS lines from <style> block
3. Standardize pb-left in promo bar
4. Remove SMS link from pb-right in promo bar
5. Standardize hdr-phone-wrap (remove "Call / Text" + text span)
6. Add sitemap.html link to footer Quick Links (if not already present)
"""

import sys
import os
import re
import glob

sys.stdout.reconfigure(encoding='utf-8')

DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# ── TARGET CONTENT ──────────────────────────────────────────────────────────

PB_LEFT_CANONICAL = '''    <div class="pb-left">
      <span class="pb-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
      <span>4.9 Google Rating</span>
      <span class="pb-sep">&middot;</span>
      <span>500+ Reviews</span>
      <span class="pb-sep">&middot;</span>
      <span>20+ Years Serving GTA</span>
    </div>'''

PB_RIGHT_CANONICAL = '''    <div class="pb-right">
      <a href="tel:+14164513106">&#9990;&nbsp; 416 451 3106</a>
      <a href="booking.html" class="pb-pill">Book Online</a>
    </div>'''

HDR_PHONE_CANONICAL = '''      <div class="hdr-phone-wrap">
        <span class="hdr-phone-label">Reservations</span>
        <a href="tel:+14164513106" class="hdr-phone">416 451 3106</a>
      </div>'''

SITEMAP_FOOTER_LINK = '        <a href="sitemap.html">Sitemap</a>'

# ── REGEX PATTERNS ───────────────────────────────────────────────────────────

# 1. Remove entire <!-- SITEMAP --> ... </section> block
RE_SITEMAP_HTML = re.compile(
    r'\n?[ \t]*<!-- SITEMAP -->\s*\n<section class="sitemap-section">.*?</section>',
    re.DOTALL
)

# 2. Sitemap CSS lines — covers the comment + all sitemap-* rules + responsive lines
#    We match the comment line through the two @media sitemap lines at end of <style>
RE_SITEMAP_CSS = re.compile(
    r'[ \t]*/\* ── SITEMAP ─+\s*\*/\s*\n'
    r'(?:[ \t]*\.sitemap-[^\n]+\n)*'           # .sitemap-* lines
    r'(?:[ \t]*@media\([^)]+\)\{\.sitemap-[^\n]+\n)*',  # @media sitemap lines
    re.DOTALL
)

# 3a. pb-left block — match anything between <div class="pb-left"> and </div>
#     We want to replace the whole div.pb-left block
RE_PB_LEFT = re.compile(
    r'[ \t]*<div class="pb-left">.*?</div>',
    re.DOTALL
)

# 3b. pb-right block with SMS link
#     Only replace if the block contains sms: link
#     Use [^<]* to avoid crossing HTML tag boundaries (safer than DOTALL .*?)
RE_PB_RIGHT_WITH_SMS = re.compile(
    r'[ \t]*<div class="pb-right">[^<]*(?:<[^>]+>[^<]*(?:<[^>]+>[^<]*</[^>]+>[^<]*)*</[^>]+>[^<]*)*</div>',
    re.DOTALL
)

# 4. hdr-phone-wrap with "Call / Text" label (3-line version)
#    Match the entire div block that has Call / Text label + text span
RE_HDR_PHONE_CALLTEXT = re.compile(
    r'[ \t]*<div class="hdr-phone-wrap">\s*\n'
    r'[ \t]*<span class="hdr-phone-label">Call / Text</span>\s*\n'
    r'[ \t]*<a href="tel:\+14164513106" class="hdr-phone">416 451 3106</a>\s*\n'
    r'[ \t]*<span[^>]*>Text:[^<]*</span>\s*\n'
    r'[ \t]*</div>',
    re.DOTALL
)

# 5. Footer Quick Links: detect if sitemap.html already present
RE_SITEMAP_LINK_PRESENT = re.compile(r'href=["\']sitemap\.html["\']')

# Pattern to find "All Locations" line in footer quick links col
RE_ALL_LOCATIONS_FOOTER = re.compile(
    r'([ \t]*<a href="locations\.html">All Locations</a>)'
)


def fix_file(filepath):
    filename = os.path.basename(filepath)
    changes = []

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # ── 1. Remove SITEMAP HTML section ────────────────────────────────────────
    new_content, count = RE_SITEMAP_HTML.subn('', content)
    if count:
        changes.append(f'  [1] Removed {count} SITEMAP HTML section(s)')
        content = new_content

    # ── 2. Remove SITEMAP CSS ─────────────────────────────────────────────────
    # Approach: find the comment line and remove from there through end of sitemap rules
    # We handle this with a more targeted line-based approach for robustness
    style_start = content.find('<style>')
    style_end = content.find('</style>', style_start)

    if style_start != -1 and style_end != -1:
        style_block = content[style_start:style_end]
        new_style = RE_SITEMAP_CSS.sub('', style_block)

        # Fallback: if regex didn't catch it, do a line-by-line removal
        if new_style == style_block and '/* ── SITEMAP' in style_block:
            lines = style_block.split('\n')
            out_lines = []
            in_sitemap = False
            for line in lines:
                stripped = line.strip()
                if '/* ── SITEMAP' in stripped:
                    in_sitemap = True
                if in_sitemap:
                    # Stop removing after the last sitemap @media rule
                    if stripped.startswith('@media') and '.sitemap-grid' in stripped:
                        in_sitemap = False
                        # skip this line too
                        continue
                    elif stripped.startswith('.sitemap-') or '/* ── SITEMAP' in stripped:
                        continue
                    else:
                        # If we hit a non-sitemap line after the comment but before the
                        # closing @media, still skip if it's in the sitemap block
                        if in_sitemap:
                            continue
                out_lines.append(line)
            new_style = '\n'.join(out_lines)

        if new_style != style_block:
            content = content[:style_start] + new_style + content[style_end:]
            changes.append('  [2] Removed SITEMAP CSS rules')

    # ── 3a. Standardize pb-left ────────────────────────────────────────────────
    # Check current pb-left content
    pb_left_match = RE_PB_LEFT.search(content)
    if pb_left_match:
        current_pb_left = pb_left_match.group(0).strip()
        canonical_stripped = PB_LEFT_CANONICAL.strip()
        if current_pb_left != canonical_stripped:
            new_content = RE_PB_LEFT.sub(PB_LEFT_CANONICAL, content, count=1)
            if new_content != content:
                content = new_content
                changes.append('  [3a] Standardized pb-left content')
        # else: already correct, skip

    # ── 3b. Remove SMS from pb-right ──────────────────────────────────────────
    # Find the pb-right div by character position to avoid DOTALL spanning too far
    pb_right_start = content.find('<div class="pb-right">')
    if pb_right_start != -1:
        pb_right_end = content.find('</div>', pb_right_start)
        if pb_right_end != -1:
            pb_right_end += len('</div>')
            pb_right_block = content[pb_right_start:pb_right_end]
            if 'sms:' in pb_right_block:
                # Replace only this block
                canonical = PB_RIGHT_CANONICAL.lstrip()  # remove leading spaces for inline replacement
                new_content = content[:pb_right_start] + canonical + content[pb_right_end:]
                if new_content != content:
                    content = new_content
                    changes.append('  [3b] Removed SMS link from pb-right, standardized')

    # ── 4. Standardize hdr-phone-wrap ─────────────────────────────────────────
    if RE_HDR_PHONE_CALLTEXT.search(content):
        new_content = RE_HDR_PHONE_CALLTEXT.sub(HDR_PHONE_CANONICAL, content, count=1)
        if new_content != content:
            content = new_content
            changes.append('  [4] Standardized hdr-phone-wrap (removed Call/Text + text span)')

    # ── 5. Add sitemap.html to footer Quick Links ──────────────────────────────
    if not RE_SITEMAP_LINK_PRESENT.search(content):
        # Find footer section first, then look for any footer-col with All Locations
        footer_start = content.find('<footer')
        if footer_start == -1:
            footer_start = 0

        footer_content = content[footer_start:]

        # Strategy 1: find "Quick Links" h4 column block
        ql_block_match = re.search(
            r'(<h4>Quick Links</h4>.*?</div>)',
            footer_content,
            re.DOTALL
        )
        # Strategy 2: fallback — find any footer-col that has locations.html
        if not ql_block_match:
            ql_block_match = re.search(
                r'(<h4>[^<]+</h4>[^<]*(?:<a[^>]+>[^<]*</a>[^<]*)*<a href="locations\.html">All Locations</a>[^<]*(?:<a[^>]+>[^<]*</a>[^<]*)*</div>)',
                footer_content,
                re.DOTALL
            )

        if ql_block_match:
            ql_block = ql_block_match.group(1)
            if 'locations.html' in ql_block and 'sitemap.html' not in ql_block:
                new_ql_block = RE_ALL_LOCATIONS_FOOTER.sub(
                    r'\1\n' + SITEMAP_FOOTER_LINK,
                    ql_block,
                    count=1
                )
                if new_ql_block != ql_block:
                    abs_start = footer_start + ql_block_match.start(1)
                    abs_end = footer_start + ql_block_match.end(1)
                    content = content[:abs_start] + new_ql_block + content[abs_end:]
                    changes.append('  [5] Added sitemap.html link to footer Quick Links')

    # ── Write if changed ───────────────────────────────────────────────────────
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'UPDATED: {filename}')
        for c in changes:
            print(c)
    else:
        print(f'NO CHANGE: {filename}')


def main():
    html_files = sorted(glob.glob(os.path.join(DIRECTORY, '*.html')))
    print(f'Processing {len(html_files)} HTML files in: {DIRECTORY}')
    print('=' * 60)

    updated = 0
    unchanged = 0

    for filepath in html_files:
        try:
            before = open(filepath, 'r', encoding='utf-8').read()
            fix_file(filepath)
            after = open(filepath, 'r', encoding='utf-8').read()
            if before != after:
                updated += 1
            else:
                unchanged += 1
        except Exception as e:
            print(f'ERROR: {os.path.basename(filepath)}: {e}')

    print('=' * 60)
    print(f'Done. Updated: {updated}, Unchanged: {unchanged}, Total: {len(html_files)}')

    # ── Verification spot-check ────────────────────────────────────────────────
    print()
    print('── Verification spot-check ──────────────────────────────────')
    for fname in ['index.html', 'toronto-airport-limo.html']:
        fpath = os.path.join(DIRECTORY, fname)
        content = open(fpath, 'r', encoding='utf-8').read()
        print(f'\n{fname}:')

        # Check sitemap HTML removed
        has_sitemap_html = bool(re.search(r'<!-- SITEMAP -->', content))
        print(f'  SITEMAP HTML present: {has_sitemap_html} (should be False)')

        # Check sitemap CSS removed
        has_sitemap_css = bool(re.search(r'sitemap-section|sitemap-grid', content))
        print(f'  SITEMAP CSS present:  {has_sitemap_css} (should be False)')

        # Check pb-left content
        pb_left_m = re.search(r'<div class="pb-left">.*?</div>', content, re.DOTALL)
        if pb_left_m:
            pb_text = ' '.join(pb_left_m.group(0).split())
            print(f'  pb-left: {pb_text[:120]}')

        # Check pb-right — no SMS
        pb_right_m = re.search(r'<div class="pb-right">.*?</div>', content, re.DOTALL)
        if pb_right_m:
            has_sms = 'sms:' in pb_right_m.group(0)
            print(f'  pb-right has SMS: {has_sms} (should be False)')

        # Check hdr-phone-wrap
        hdr_m = re.search(r'<div class="hdr-phone-wrap">.*?</div>', content, re.DOTALL)
        if hdr_m:
            hdr_text = ' '.join(hdr_m.group(0).split())
            print(f'  hdr-phone-wrap: {hdr_text[:120]}')

        # Check footer sitemap link
        has_sitemap_link = bool(re.search(r'href=["\']sitemap\.html["\']', content))
        print(f'  Footer sitemap.html link: {has_sitemap_link} (should be True)')


if __name__ == '__main__':
    main()
