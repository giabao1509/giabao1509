"""Build original, self-contained SVG assets using only Python's stdlib."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
DATA = json.loads((ASSETS / "profile-data.json").read_text(encoding="utf-8"))
THEMES = {
    "dark": dict(bg="#0b1220", panel="#111f32", line="#283d54", fg="#edf5ff", muted="#a7bacf", accent="#67e8f9", soft="#102f40"),
    "light": dict(bg="#f3f8fc", panel="#ffffff", line="#cbdce9", fg="#142b40", muted="#4b6479", accent="#087e91", soft="#e2f2f5"),
}


def write(name, body):
    path = ASSETS / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.strip() + "\n", encoding="utf-8")


def svg(width, height, title, body, t):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{title}</title>
<desc id="desc">Original profile artwork. All content is readable without animation.</desc>
<style>text{{font-family:Arial,Helvetica,sans-serif}} .mono{{font-family:Consolas,monospace}} .packet{{animation:pulse 5s ease-in-out infinite}} .second{{animation-delay:1.5s}} @keyframes pulse{{0%,100%{{opacity:.15}}50%{{opacity:1}}}} @media(prefers-reduced-motion:reduce){{.packet{{animation:none;opacity:.65}}}}</style>
<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="20" fill="{t['bg']}" stroke="{t['line']}"/>
{body}
</svg>'''


for mode, t in THEMES.items():
    body = f'''
<path d="M640 1V299" stroke="{t['line']}" stroke-dasharray="3 9"/>
<text x="44" y="48" fill="{t['accent']}" font-size="13" letter-spacing="3" class="mono">HELLO, I'M</text>
<text x="40" y="111" fill="{t['fg']}" font-size="54" font-weight="700" letter-spacing="-2">Nguyen Thanh</text>
<text x="40" y="172" fill="{t['fg']}" font-size="58" font-weight="700" letter-spacing="-2">Gia Bao<tspan fill="{t['accent']}">.</tspan></text>
<text x="44" y="218" fill="{t['muted']}" font-size="18">Backend development</text>
<text x="44" y="245" fill="{t['muted']}" font-size="18">Quality engineering</text>
<rect x="687" y="34" width="306" height="35" rx="17" fill="{t['soft']}"/>
<circle cx="708" cy="51" r="4" fill="{t['accent']}"/>
<text x="723" y="56" fill="{t['accent']}" font-size="12" class="mono" letter-spacing="1">OPEN TO INTERNSHIPS</text>
<text x="696" y="111" fill="{t['muted']}" font-size="13" class="mono">// building the backend</text>
<g fill="{t['panel']}" stroke="{t['line']}" stroke-width="1.5">
<rect x="693" y="136" width="82" height="62" rx="10"/>
<rect x="803" y="136" width="82" height="62" rx="10"/>
<rect x="913" y="136" width="82" height="62" rx="10"/>
<path d="M775 167H803M885 167H913"/>
</g>
<g fill="{t['fg']}" font-size="14" text-anchor="middle" class="mono">
<text x="734" y="173">API</text><text x="844" y="173">LOGIC</text><text x="954" y="173">DATA</text>
</g>
<circle class="packet" cx="788" cy="167" r="3" fill="{t['accent']}"/>
<circle class="packet second" cx="899" cy="167" r="3" fill="{t['accent']}"/>
<text x="696" y="242" fill="{t['muted']}" font-size="13" class="mono">@giabao1509</text>
<path d="M44 276H124" stroke="{t['accent']}" stroke-width="3" stroke-linecap="round"/>
'''
    write(f"header-{mode}.svg", svg(1040, 300, "Nguyen Thanh Gia Bao — Backend Development &amp; Quality Engineering", body, t))
    values = [(DATA["public_repositories"], "PUBLIC REPOSITORIES"), (DATA["featured_team_projects"], "FEATURED TEAM PROJECTS"), (DATA["testing_coursework_branches"], "TESTING BRANCHES")]
    body = ""
    for index, (value, label) in enumerate(values):
        x = 40 + index * 344
        if index:
            body += f'<path d="M{x-20} 28V132" stroke="{t["line"]}"/>\n'
        body += f'<text x="{x}" y="86" fill="{t["accent"]}" font-size="52" font-weight="700">{value:02d}</text>\n'
        body += f'<text x="{x}" y="119" fill="{t["muted"]}" font-size="12" letter-spacing="1" class="mono">{label}</text>\n'
    write(f"statistics-{mode}.svg", svg(1040, 160, f"GitHub and portfolio snapshot {DATA['snapshot_date']}", body, t))

# Custom illustrative glyphs, rather than downloaded brand logos.
icons = {
    "nodejs": ("Node.js", "#7dd3a8", '<path d="M25 10l12 7v14l-12 7-12-7V17z" fill="none" stroke="currentColor" stroke-width="2"/><text x="25" y="29" text-anchor="middle" fill="currentColor" font-size="13" font-weight="700">N</text>'),
    "typescript": ("TypeScript", "#8dc9ff", '<rect x="12" y="11" width="26" height="26" rx="5" fill="currentColor"/><text x="25" y="29" text-anchor="middle" fill="#101b2b" font-size="13" font-weight="700">TS</text>'),
    "javascript": ("JavaScript", "#f4d976", '<rect x="12" y="11" width="26" height="26" rx="5" fill="currentColor"/><text x="25" y="29" text-anchor="middle" fill="#101b2b" font-size="13" font-weight="700">JS</text>'),
    "rest-api": ("REST API", "#95e6ef", '<path d="M20 15l-8 9 8 9m10-18 8 9-8 9m-3-21-4 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'),
    "sql": ("SQL", "#bab2ff", '<g fill="none" stroke="currentColor" stroke-width="2"><ellipse cx="25" cy="15" rx="12" ry="5"/><path d="M13 15v18c0 7 24 7 24 0V15M13 24c0 7 24 7 24 0"/></g>'),
    "git": ("Git", "#f4a78f", '<g fill="none" stroke="currentColor" stroke-width="2"><rect x="14" y="13" width="23" height="23" rx="3" transform="rotate(45 25.5 24.5)"/><path d="M20 13v14l9 7M20 20l11 2"/><circle cx="20" cy="20" r="2.5" fill="currentColor"/><circle cx="31" cy="22" r="2.5" fill="currentColor"/><circle cx="29" cy="34" r="2.5" fill="currentColor"/></g>'),
}
for name, (label, color, shape) in icons.items():
    write(f"icons/{name}.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" width="144" height="52" viewBox="0 0 144 52" role="img" aria-label="{label}">
<title>{label}</title><rect x="1" y="1" width="142" height="50" rx="10" fill="#111f32" stroke="#3c526b"/>
<g color="{color}" font-family="Arial,Helvetica,sans-serif">{shape}</g>
<text x="47" y="31" fill="#edf5ff" font-family="Arial,Helvetica,sans-serif" font-size="13">{label}</text>
</svg>''')

print("Built 4 theme assets and 6 technology icons in assets/.")
