"""Writes the Chapter 1 worked examples from ch1_we.py into the slides
(vm-numeracy/chapter-1.html) and into ch1_content.py (worksheets), and turns
every typed fraction on the slides into a stacked fraction.

Run from tools/:  python3 apply_we.py [fit.json]
fit.json (optional) maps a slide id to a step font size in px.
Then rebuild worksheets with build_worksheets.py."""
import re, sys, json, html, pathlib
from ch1_we import WE

ROOT = pathlib.Path(__file__).resolve().parent.parent
DECK = ROOT / "vm-numeracy" / "chapter-1.html"
CONTENT = ROOT / "tools" / "ch1_content.py"
I, A, E, C = "Identify the maths:", "Act on and use maths:", "Evaluate and reflect:", "Communicate &amp; report:"

FR = r'<span class="fr"><span>\1</span><span>\2</span></span>'


def inline(t):
    t = re.sub(r"\{(\d+)/(\d+)\}", FR, t)
    t = re.sub(r"\[\[(.+?)\]\]", r'<span class="note">(\1)</span>', t)
    return t


def col_html(op, nums, res):
    rows = "".join(f'<tr><td class="op">{op if i == len(nums) - 1 else ""}</td><td>{n}</td></tr>'
                   for i, n in enumerate(nums))
    return f'<table class="col">{rows}<tr class="res"><td class="op"></td><td>{res}</td></tr></table>'


def ul(items):
    return "<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>"


def act_item(x):
    return col_html(*x[1:]) if isinstance(x, tuple) else inline(x)


# ---------------------------------------------------------------- slides
def slide_steps(w):
    out = [f'<div class="step"><b>1 {I}</b>{ul(w["identify"])}</div>']
    first, *rest = w["act"]
    out.append(f'<p class="step"><b>2 {A}</b> {act_item(first)}</p>')
    for x in rest:
        out.append(f'<div class="step">{act_item(x)}</div>' if isinstance(x, tuple) else f'<p class="step">{act_item(x)}</p>')
    out.append(f'<div class="step"><b>3 {E}</b>{ul(w["evaluate"])}</div>')
    out.append(f'<p class="step"><b>4 {C}</b> {inline(w["comm"])}</p>')
    return '<div class="stages">\n' + "\n".join(out) + "\n</div>\n"


CSS = """
/* worked examples: 4-stage cycle, stacked sums, stacked fractions */
.we .step{font-size:var(--fs,30px);line-height:1.28;margin:0 0 4px}
.we .step ul{margin:2px 0 4px;padding-left:1.3em}
.we .step li{margin:0;font-size:1em;line-height:1.28}
.we[style*="--fs"]{padding:28px 40px 26px}
.we[style*="--fs"] .tag{font-size:24px;margin:0 0 6px}
.we[style*="--fs"] .q{font-size:28px;line-height:1.25;margin:0 0 10px}
.we[style*="--fs"] .ans{font-size:30px;margin:6px 0 0;padding-top:8px}
.slide:has(.we[style*="--fs"]) h2{font-size:56px;margin:0 0 20px}
.slide:has(.we[style*="--fs"]) .we{flex:1.65}
.slide:has(.we[style*="--fs"]) .yt .q{font-size:30px}
.we .stages{column-count:2;column-gap:34px;column-fill:balance}
.we .stages .step{break-inside:avoid}
/* end worked examples */
.note{color:#80878c;font-size:.86em}
.col{border-collapse:collapse;font-variant-numeric:tabular-nums;margin:2px 0 6px 1.2em;font-size:1.08em}
.col td{text-align:right;padding:0 .2em;line-height:1.2}
.col td.op{padding-right:.6em;font-weight:700}
.col tr.res td{border-top:3px solid currentColor;font-weight:700}
.fr{display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;line-height:1.02;font-size:.82em;margin:0 .12em}
.fr>span:first-child{border-bottom:.09em solid currentColor;padding:0 .12em}
"""


def fractions_in_text(s):
    """Typed fractions (3/8, 1 1/4) outside tags and scripts become stacked fractions."""
    parts = re.split(r"(<script\b.*?</script>|<[^>]+>)", s, flags=re.S)
    for i, p in enumerate(parts):
        if i % 2 or not p:
            continue
        p = re.sub(r"(?<![\w./])(\d+)/(\d+)(?![\w/])", FR, p)
        parts[i] = p
    return "".join(parts)


def patch_deck(fit):
    s = DECK.read_text()
    s = re.sub(r"\n/\* worked examples: 4-stage cycle.*?(?:/\* end worked examples \*/|(?=</style>))\n?", "\n", s, count=1, flags=re.S)
    s = s.replace("</style>", CSS + "</style>", 1)
    for sid, w in WE.items():
        m = re.search(r'<section id="%s"[^>]*>.*?</section>' % re.escape(sid), s, re.S)
        sec = m.group(0)
        wm = re.search(r'<div class="we"[^>]*>', sec)
        start = wm.end()
        first = re.search(r'<div class="stages">|<(p|div) class="step"', sec[start:])
        cue = sec.index('<p class="cue">', start)
        a = start + first.start()
        new = sec[:a] + slide_steps(w) + sec[cue:]
        new = re.sub(r'<p class="ans"([^>]*)>.*?</p>', lambda mm: f'<p class="ans"{mm.group(1)}>{inline(w["ans"])}</p>', new, count=1)
        fs = fit.get(sid, 26)
        new = re.sub(r'<div class="we"[^>]*>', f'<div class="we" style="--fs:{fs}px">', new, count=1)
        s = s.replace(sec, new)
    s = fractions_in_text(s)
    DECK.write_text(s)


# ---------------------------------------------------------------- worksheets
def ws_steps(w):
    out = [f"<b>1 {I}</b>{ul(w['identify'])}"]
    first, *rest = w["act"]
    out.append(f"<b>2 {A}</b> {act_item(first)}")
    out += [act_item(x) for x in rest]
    out.append(f"<b>3 {E}</b>{ul(w['evaluate'])}")
    return out


def patch_content():
    c = CONTENT.read_text()
    for sid, w in WE.items():
        pat = re.compile(r'(we=dict\(q="%s.*?steps=)\[.*?\](,\s*ans=)(".*?")' % re.escape(w["ws"]), re.S)
        assert pat.search(c), sid
        steps = json.dumps(ws_steps(w), ensure_ascii=False)
        ans = json.dumps(f"<b>4 {C}</b> {inline(w['comm'])}", ensure_ascii=False)
        c = pat.sub(lambda m: m.group(1) + steps + m.group(2) + ans, c, count=1)
    CONTENT.write_text(c)


if __name__ == "__main__":
    fj = [a for a in sys.argv[1:] if a.endswith(".json")]
    fit = json.load(open(fj[0])) if fj else {}
    patch_deck(fit)
    if "--deck-only" not in sys.argv:
        patch_content()
    print("applied", len(WE), "worked examples")
