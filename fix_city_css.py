"""
fix_city_css.py
Updates city-card CSS to look clean without neighbourhood <p> text.
Applies only to files that have the city-coverage section.
"""
import os

FOLDER = r"c:\Users\user\OneDrive\Desktop\designhelp"

OLD_CSS = """.city-card h3{font-family:var(--font-sans);font-size:14px;font-weight:700;color:var(--dark);margin-bottom:4px}
  .city-card p{font-size:12px;color:var(--text-light);line-height:1.5;margin-bottom:10px}
  .city-card .city-arrow{font-size:11px;color:var(--blue);font-weight:700;text-transform:uppercase;letter-spacing:0.08em}"""

NEW_CSS = """.city-card{display:flex;flex-direction:column;justify-content:space-between;min-height:72px}
  .city-card h3{font-family:var(--font-sans);font-size:14px;font-weight:700;color:var(--dark);margin-bottom:6px}
  .city-card .city-arrow{font-size:11px;color:var(--blue);font-weight:700;text-transform:uppercase;letter-spacing:0.08em;margin-top:auto}"""

files = [f for f in os.listdir(FOLDER) if f.endswith('.html')]
updated = 0

for fname in sorted(files):
    fpath = os.path.join(FOLDER, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    if OLD_CSS not in content:
        continue
    content = content.replace(OLD_CSS, NEW_CSS)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK]   {fname}")
    updated += 1

print(f"\nDone: {updated} files updated.")
