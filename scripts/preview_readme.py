"""Optional local preview: requires Python-Markdown (pip install Markdown).

Does not make network requests. Output embeds SVGs for offline viewing.
"""

import base64
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / "README.md").read_text(encoding="utf-8")


class Images(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("img", "source"):
            self.paths.append(attrs.get("src", attrs.get("srcset")))
        if tag == "img":
            assert attrs.get("alt"), "Missing image alt text"


images = Images()
images.feed(text)
for name in images.paths:
    assert (ROOT / name).is_file(), name
svgs = list((ROOT / "assets").rglob("*.svg"))
for path in svgs:
    doc = ET.parse(path)
    assert not any(n.tag.rsplit("}", 1)[-1] in ("script", "foreignObject", "image") for n in doc.iter()), path
anchors = {re.sub(r"[^a-z0-9 -]", "", title.lower()).replace(" ", "-") for title in re.findall(r"^## (.+)$", text, re.M)}
for target in re.findall(r'href="#([^"]+)"', text):
    assert target in anchors, target
html = markdown.markdown(text, extensions=["tables", "sane_lists", "toc"])
assert html.count("<table>") == 1, "Expected coursework table"

CSS = '''
*{box-sizing:border-box}body{margin:0;font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;background:#0d1117;color:#e6edf3}
main{max-width:1040px;margin:40px auto;padding:32px;border:1px solid #30363d;border-radius:8px}
h2{font-size:24px;border-bottom:1px solid #30363d;padding-bottom:8px;margin-top:32px}h3{font-size:20px;margin-top:28px}
p{margin:16px 0}a{color:#58a6ff;text-decoration:none}a:hover{text-decoration:underline}
img{max-width:100%;vertical-align:middle;height:auto}img[height="52"]{height:52px;width:auto;margin:3px 2px}picture img{display:block}
sub{font-size:13px;vertical-align:baseline}table{display:block;overflow-x:auto;border-collapse:collapse;width:max-content;max-width:100%}
th,td{border:1px solid #30363d;padding:9px 13px}th{background:#161b22}hr{border:0;border-top:1px solid #30363d;margin:30px 0}ul{padding-left:25px}
.light{background:#fff;color:#1f2328}.light main{border-color:#d1d9e0}.light h2,.light td,.light th,.light hr{border-color:#d1d9e0}.light th{background:#f6f8fa}.light a{color:#0969da}
aside{max-width:1040px;margin:20px auto;color:#9aa8b8;font-size:13px}aside a{margin-right:18px}
@media(max-width:650px){main{margin:12px;padding:16px}aside{margin:16px}h2{font-size:22px}}
'''


def themed(mode):
    def picture(match):
        block = match.group(0)
        source = re.search('srcset="([^"]*' + mode + r'\.svg)"', block).group(1)
        alt = re.search('alt="([^"]*)"', block).group(1)
        return f'<img src="{source}" width="100%" alt="{alt}">'

    body = re.sub(r"<picture>.*?</picture>", picture, html, flags=re.S)

    def inline(match):
        content = (ROOT / match.group(1)).read_bytes()
        return 'src="data:image/svg+xml;base64,' + base64.b64encode(content).decode() + '"'

    body = re.sub(r'src="(assets/[^"]+\.svg)"', inline, body)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Gia Bao | README Preview ({mode})</title><style>{CSS}</style></head><body class="{mode}"><aside>Local Markdown preview · GitHub rendering may differ. &nbsp; <a href="preview.html">Dark</a><a href="preview-light.html">Light</a></aside><main>{body}</main></body></html>'''


for mode, filename in [("dark", "preview.html"), ("light", "preview-light.html")]:
    (ROOT / "assets" / filename).write_text(themed(mode), encoding="utf-8")
print(f"PASS: {len(images.paths)} image references, {len(svgs)} SVGs, internal anchors, and coursework table.")
print("Created two self-contained offline HTML previews.")
