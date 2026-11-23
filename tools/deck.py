"""Build a read-only slide deck page using the same viewer as vm-numeracy/chapter-1.html.

Usage from another script:
    from deck import build_deck
    build_deck(out_path, page_title, toc_heading, slides, extra_css)
where slides is a list of dicts: {html, toc, sec (or None), li (bool), id}
Slide numbers (data-n), the contents list and section anchors (#sec-K) are generated.
"""
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "vm-numeracy" / "chapter-1.html"


def _template():
    src = TEMPLATE.read_text()
    head = src.split('<div id="stage">')[0]
    tail = src.split('</section>\n</div>\n<div class="bar l">')[1]
    return head, '<div class="bar l">' + tail


def build_deck(out_path, page_title, toc_heading, slides, extra_css=""):
    head, tail = _template()
    head = re.sub(r"<title>.*?</title>", f"<title>{page_title}</title>", head)
    head = head.replace("</style></head>", extra_css + "\n</style></head>")
    secs, toc, body = {}, [], []
    for i, s in enumerate(slides, 1):
        html = s["html"].strip()
        cls = "slide dark" if s.get("dark") else "slide"
        body.append(f'<section id="{s["id"]}" class="{cls}" data-n="{i}">\n{html}\n</section>')
        if s.get("sec"):
            secs[s["sec"]] = i
        toc.append({"n": i, "t": s["toc"], "sec": s.get("sec"), "li": bool(s.get("li"))})
    tail = re.sub(r"const SECS=\{.*?\},TOC=\[.*?\];",
                  lambda m: "const SECS=" + json.dumps(secs) + ",TOC=" + json.dumps(toc) + ";",
                  tail, flags=re.S)
    tail = re.sub(r'(<nav id="toc" aria-label=")[^"]*(">\s*<button class="btn close" id="tocclose">Close</button>\s*<h2>)[^<]*(</h2>)',
                  lambda m: m.group(1) + "Contents" + m.group(2) + toc_heading + m.group(3), tail)
    out = head + '<div id="stage">\n' + "\n".join(body) + "\n</div>\n" + tail
    pathlib.Path(out_path).write_text(out)
    return len(slides)
