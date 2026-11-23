"""Builds the Chapter 1 diagnostic, worksheets 1.1-1.6 and the teacher answer key
from ch1_content.py into vm-numeracy/. Run: python3 build_worksheets.py"""
import re, html, pathlib
from ch1_content import DIAGNOSTIC, WORKSHEETS

OUT = pathlib.Path(__file__).resolve().parent.parent / "vm-numeracy"
KEY_FILE = "teacher-key-ch1-k7q2xw.html"   # unlinked from student pages
LETTERS = "ABCDEFGH"


def fmt(t):
    t = re.sub(r"\{(\d+)/(\d+)\}", r'<span class="fr"><span>\1</span><span>\2</span></span>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return t


FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600&family=Nunito+Sans:wght@400;700;800&display=swap" rel="stylesheet">')

CSS = r"""
/* VOICE: a worksheet a student works through at their own pace, on screen or printed.
   IDEA: the slide's worked example, slowed down: reveal one step at a time, then try your own.
   PICTURE: a paper sheet on the site's charcoal-and-tape-yellow theme; teal for worked examples, yellow for your turn.
   COLOUR and TYPE: charcoal #1f2326, paper #f4f2ec, tape yellow #f6c21a, teal #1f7a6e, rust #a84b16; Oswald + Nunito Sans.
   LAYOUT: header with learning intention, then Parts A-D (worked example over your turn), then a self-check. */
:root{color-scheme:light;--ink:#1f2326;--paper:#f4f2ec;--card:#fffdf8;--soft:#4a5157;--line:#dcd7cc;--y:#f6c21a;--teal:#1f7a6e;--rust:#a84b16}
*{box-sizing:border-box;min-width:0}
body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.55 'Nunito Sans',system-ui,sans-serif}
a{color:inherit}
.wrap{max-width:920px;margin:0 auto;padding:0 max(4vw,16px)}
h1,h2,h3{font-family:Oswald,'Arial Narrow',sans-serif;font-weight:600;margin:0;text-wrap:balance}
.top{background:var(--ink);color:var(--paper);padding:28px 0 30px}
.eye{font-size:13px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--y);margin:0 0 8px}
.top h1{font-size:clamp(30px,5vw,44px);line-height:1.08}
.top h1 small{display:block;font-size:.5em;color:#c9cfd3;font-weight:500;letter-spacing:.02em;margin-bottom:4px}
.lisc{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:20px}
.lisc div{background:#2c3236;border-radius:12px;padding:14px 18px}
.lisc h3{font-size:17px;color:var(--y);margin-bottom:4px;font-weight:500;letter-spacing:.04em;text-transform:uppercase}
.lisc p,.lisc li{margin:0;color:#e6e3dc;font-size:15.5px}
.lisc ul{margin:0;padding-left:20px}
.links{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px}
.links a,.links button{display:inline-flex;align-items:center;min-height:44px;padding:0 16px;border-radius:10px;background:#2c3236;color:var(--paper);font:800 15px 'Nunito Sans',sans-serif;text-decoration:none;border:0;cursor:pointer}
.links a.hl{background:var(--y);color:var(--ink)}
.links a:hover,.links button:hover{filter:brightness(1.15)}
:focus-visible{outline:3px solid var(--teal);outline-offset:2px}
.how{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 20px;margin:26px 0 8px;font-size:15.5px}
.how ol{margin:6px 0 0;padding-left:22px}
.part{margin:34px 0 0}
.phead{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;border-bottom:3px solid var(--ink);padding-bottom:6px;margin-bottom:14px}
.pl{font:600 15px Oswald,sans-serif;letter-spacing:.08em;text-transform:uppercase;background:var(--ink);color:var(--y);padding:3px 10px;border-radius:6px}
.phead h2{font-size:26px;line-height:1.15;flex:1}
.phead a{font-size:14px;font-weight:700;color:var(--teal)}
.we,.yt{background:var(--card);border-radius:14px;padding:18px 22px 20px;margin-bottom:14px}
.we{border-top:8px solid var(--teal)} .yt{border-top:8px solid var(--y)}
.tag{font:600 16px Oswald,sans-serif;letter-spacing:.06em;text-transform:uppercase;margin:0 0 6px}
.we .tag{color:var(--teal)} .yt .tag{color:var(--rust)}
.we .q{font-weight:800;font-size:18px;margin:0 0 10px}
.steps{margin:0;padding-left:24px;color:var(--soft)}
.steps li{margin:4px 0}
.ans{font-weight:800;color:var(--teal);font-size:18px;border-top:2px solid var(--line);padding-top:8px;margin:10px 0 0}
.ctrl{display:flex;gap:10px;margin-top:12px;flex-wrap:wrap}
.ctrl button{min-height:44px;padding:0 16px;border-radius:10px;border:2px solid var(--teal);background:#fff;color:var(--teal);font:800 15px 'Nunito Sans',sans-serif;cursor:pointer}
.ctrl button.main{background:var(--teal);color:#fff}
.js .steps li.hid,.js .ans.hid{display:none}
.no-js-note{display:none}
.tip{font-size:15px;color:var(--soft);background:#fff6d6;border-left:6px solid var(--y);border-radius:8px;padding:8px 14px;margin:0 0 14px}
.qq{display:grid;grid-template-columns:34px 1fr;gap:0 6px;padding:10px 0;border-top:1px solid var(--line)}
.qq:first-of-type{border-top:0}
.qn{font:600 20px Oswald,sans-serif;color:var(--rust);line-height:1.3}
.qq p{margin:0}
.parts{list-style:none;margin:8px 0 0;padding:0;display:grid;gap:6px 18px}
.c1{grid-template-columns:1fr}.c2{grid-template-columns:repeat(2,1fr)}.c3{grid-template-columns:repeat(3,1fr)}.c4{grid-template-columns:repeat(4,1fr)}
.parts li{display:flex;gap:6px}
.parts b{color:var(--soft);font-weight:800}
.sp{display:none}
table.fill{border-collapse:collapse;margin-top:8px;width:100%;max-width:520px}
table.fill th,table.fill td{border:1.5px solid #b9b3a6;padding:6px 10px;text-align:center;height:34px}
table.fill th{background:#efebe2;font-weight:800}
.fr{display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;line-height:1.05;font-size:.86em;margin:0 2px}
.fr span:first-child{border-bottom:1.5px solid currentColor;padding:0 2px}
.reflect{margin:34px 0 10px;background:var(--card);border-radius:14px;padding:18px 22px;border-top:8px solid var(--ink)}
.reflect h2{font-size:24px;margin-bottom:8px}
.reflect table{border-collapse:collapse;width:100%;font-size:15.5px}
.reflect th,.reflect td{border-bottom:1px solid var(--line);padding:8px 6px;text-align:left}
.reflect td.bx,.reflect th.bx{text-align:center;width:92px}
.box{display:inline-block;width:20px;height:20px;border:2px solid var(--ink);border-radius:4px}
footer{padding:26px 0 40px;font-size:14px;color:var(--soft)}
.printonly{display:none}
.sec-h{font-size:22px;margin:30px 0 8px;border-bottom:3px solid var(--ink);padding-bottom:4px}
.sec-h span{color:var(--rust);font-size:.7em;letter-spacing:.06em;text-transform:uppercase;margin-right:8px}
@media (max-width:640px){.lisc{grid-template-columns:1fr}.c3,.c4{grid-template-columns:repeat(2,1fr)}}
@media print{
  @page{size:A4;margin:13mm 13mm 15mm}
  body{background:#fff;font-size:10.5pt;line-height:1.4}
  .wrap{max-width:none;padding:0}
  .top{background:#fff;color:var(--ink);padding:0 0 6px;border-bottom:2.5pt solid var(--ink)}
  .eye{color:var(--rust)} .top h1 small{color:var(--soft)}
  .lisc div{background:#fff;border:1pt solid var(--line);padding:6px 10px}
  .lisc h3{color:var(--rust)} .lisc p,.lisc li{color:var(--ink);font-size:9.5pt}
  .links,.ctrl,.how:not(.instr),.no-print{display:none!important}
  .instr{border:1pt solid var(--line);padding:6px 10px;margin:8px 0}
  .sec-h{break-after:avoid;margin-top:14px}
  .printonly{display:block}
  .nameline{display:flex;gap:30px;margin:8px 0 2px;font-weight:700}
  .nameline span{flex:1;border-bottom:1pt solid var(--ink);height:18pt}
  .js .steps li.hid{display:list-item!important}.js .ans.hid{display:block!important}
  .we,.yt{border:1pt solid var(--line);padding:8px 12px;margin-bottom:8px;break-inside:auto}
  .we{break-inside:avoid}
  .part{margin-top:14px} .phead{break-after:avoid}
  .phead a{display:none}
  .qq{break-inside:avoid;padding:6px 0}
  .tip{background:#fff;border-left-width:4pt}
  .sp{display:block;height:calc(var(--l,2) * 7.5mm);background:repeating-linear-gradient(to bottom,transparent 0,transparent calc(7.5mm - .6pt),#c9c4b8 calc(7.5mm - .6pt),#c9c4b8 7.5mm)}
  .parts .sp{height:calc(var(--l,2) * 7.5mm)}
  .parts li{flex-direction:column;gap:0}
  .reflect{break-inside:avoid;border:1pt solid var(--line)}
  footer{display:none}
}
"""

JS = r"""<script>
document.documentElement.classList.add('js');
document.querySelectorAll('.we').forEach(we=>{
  const steps=[...we.querySelectorAll('.steps li')],ans=we.querySelector('.ans'),next=we.querySelector('.next'),all=we.querySelector('.all');
  let k=0;
  const render=()=>{steps.forEach((s,i)=>s.classList.toggle('hid',i>=k));ans.classList.toggle('hid',k<=steps.length);
    if(k>steps.length){next.textContent='Hide working';all.hidden=true}
    else{next.textContent=k===steps.length?'Show answer':(k?'Show next step':'Show first step')+' ('+(k+1)+' of '+steps.length+')';all.hidden=false}};
  next.onclick=()=>{k=k>steps.length?0:k+1;render()};
  all.onclick=()=>{k=steps.length+1;render()};
  render();
});
document.querySelectorAll('[data-print]').forEach(b=>b.onclick=()=>print());
</script>"""


def page(title, body, noindex=False):
    meta = '<meta name="robots" content="noindex,nofollow">' if noindex else ""
    return (f'<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">{meta}'
            f'<title>{title}</title>{FONTS}<style>{CSS}</style></head>\n<body>\n{body}\n{JS}\n</body></html>\n')


PYTH_SVG = ('<svg aria-label="A rectangular frame 1.2 metres wide and 0.9 metres high, with a diagonal brace labelled c" width="250" height="125" viewBox="0 0 300 150" style="margin:0 0 6px;display:block">'
            '<rect x="20" y="6" width="147" height="110" fill="none" stroke="#1f2326" stroke-width="4"/><line x1="20" y1="116" x2="167" y2="6" stroke="#1f7a6e" stroke-width="6"/>'
            '<text x="70" y="146" font-family="Nunito Sans, Arial, sans-serif" font-size="24" fill="#4a5157">1.2 m</text><text x="178" y="70" font-family="Nunito Sans, Arial, sans-serif" font-size="24" fill="#4a5157">0.9 m</text>'
            '<text x="74" y="56" font-family="Nunito Sans, Arial, sans-serif" font-size="26" font-weight="700" fill="#1f7a6e">c</text></svg>')


def render_q(num, q):
    out = [f'<div class="qq"><span class="qn">{num}</span><div><p>{fmt(q["text"])}</p>']
    if "parts" in q:
        cols = q.get("cols", 3)
        lines = q.get("plines", 1 if cols >= 3 else 2)
        out.append(f'<ol class="parts c{cols}">')
        for i, (p, _a) in enumerate(q["parts"]):
            out.append(f'<li><span><b>{"abcdefghij"[i]})</b> {fmt(p)}</span><div class="sp" style="--l:{lines}"></div></li>')
        out.append("</ol>")
    elif "table" in q:
        t = q["table"]
        out.append('<table class="fill"><tr>' + "".join(f"<th>{h}</th>" for h in t["head"]) + "</tr>")
        for r in t["rows"]:
            out.append("<tr>" + "".join(f"<td>{fmt(c)}</td>" for c in r) + "</tr>")
        out.append("</table>")
    else:
        out.append(f'<div class="sp" style="--l:{q.get("lines", 2)}"></div>')
    out.append("</div></div>")
    return "".join(out)


def header(eye, small, title, li, sc, links):
    scl = "".join(f"<li>{s}</li>" for s in sc)
    lk = "".join(links)
    return f"""<header class="top"><div class="wrap">
<p class="eye">{eye}</p>
<h1><small>{small}</small>{title}</h1>
<div class="lisc"><div><h3>Learning intention</h3><p>{li}</p></div><div><h3>Success criteria</h3><ul>{scl}</ul></div></div>
<nav class="links" aria-label="Page links">{lk}<button data-print>Print this sheet</button></nav>
<div class="printonly nameline"><b>Name</b><span></span><b>Date</b><span style="flex:.5"></span></div>
</div></header>"""


def build_worksheet(ws):
    n = ws["n"]
    prev_next = []
    if n > 1:
        prev_next.append(f'<a href="chapter-1-worksheet-{n-1}.html">← Worksheet 1.{n-1}</a>')
    if n < len(WORKSHEETS):
        prev_next.append(f'<a href="chapter-1-worksheet-{n+1}.html">Worksheet 1.{n+1} →</a>')
    links = [f'<a href="index.html">← All chapters</a>', f'<a class="hl" href="chapter-1.html#{ws["sec"]}">Slides for this section</a>'] + prev_next
    body = [header(f"VM Numeracy · Chapter 1 · Doing the Numbers", f"Worksheet 1.{n}", ws["title"], ws["li"], ws["sc"], links)]
    body.append('<main class="wrap">')
    body.append("""<section class="how"><b>How to use this worksheet</b><ol>
<li>Read the worked example and try it yourself first.</li>
<li>Click <b>Show first step</b> to check the working one step at a time.</li>
<li>Do the <b>Your turn</b> questions in your book (or on the printed sheet). Show your working, like the worked example.</li></ol></section>""")
    qnum = 1
    for pi, p in enumerate(ws["parts"]):
        L = LETTERS[pi]
        we = p["we"]
        steps = "".join(f"<li>{fmt(s)}</li>" for s in we["steps"])
        svg = PYTH_SVG if p.get("svg") else ""
        body.append(f"""<section class="part" id="part-{L.lower()}">
<div class="phead"><span class="pl">Part {L}</span><h2>{p["title"]}</h2><a href="chapter-1.html#{p["slide"]}">Slide {p["slide"]}</a></div>
<div class="we"><p class="tag">Worked example</p><p class="q">{fmt(we["q"])}</p>{svg}
<ol class="steps">{steps}</ol><p class="ans">{fmt(we["ans"])}</p>
<div class="ctrl"><button class="next main">Show first step</button><button class="all">Show all</button></div></div>
<p class="tip"><b>Tip:</b> {fmt(p["tip"])}</p>
<div class="yt"><p class="tag">Your turn</p>""")
        for q in p["qs"]:
            body.append(render_q(qnum, q))
            qnum += 1
        body.append("</div></section>")
    rows = "".join(f'<tr><td>{s}</td><td class="bx"><span class="box"></span></td><td class="bx"><span class="box"></span></td><td class="bx"><span class="box"></span></td></tr>' for s in ws["sc"])
    body.append(f"""<section class="reflect"><h2>Check yourself</h2><p style="margin:0 0 8px;font-size:15px">Tick one box for each success criterion. Show your teacher anything you ticked “Not yet”.</p>
<table><tr><th>Success criteria</th><th class="bx">Not yet</th><th class="bx">Getting there</th><th class="bx">Got it</th></tr>{rows}</table></section>""")
    nav = " · ".join([f'<a href="index.html">All chapters</a>', f'<a href="chapter-1.html#{ws["sec"]}">Slides for this section</a>'] + prev_next)
    body.append(f"</main><footer class=\"wrap\">{nav}</footer>")
    name = f"chapter-1-worksheet-{n}.html"
    (OUT / name).write_text(page(f"Worksheet 1.{n} · {ws['title']}", "\n".join(body)))
    return name, qnum - 1


def build_diagnostic(d):
    links = ['<a href="index.html">← All chapters</a>', '<a class="hl" href="chapter-1.html#1">Chapter 1 slides</a>', '<a href="chapter-1-worksheet-1.html">Worksheet 1.1 →</a>']
    body = [header("VM Numeracy · Chapter 1 · Doing the Numbers", "Before we start", d["title"],
                   "We are finding out what you already know about number, so we know where to start.",
                   ["I can show what I already know", "I can find the topics I need help with"], links)]
    body.append(f'<main class="wrap"><section class="how instr"><b>Instructions.</b> {d["intro"]}</section>')
    q = 1
    for s in d["sections"]:
        body.append(f'<h2 class="sec-h"><span>Section {s["n"]}</span>{s["name"]}</h2><div class="yt" style="border-top-width:0">')
        for item in s["qs"]:
            body.append(render_q(q, dict(item, lines=item.get("lines", 1))))
            q += 1
        body.append("</div>")
    rows = "".join(f'<tr><td>{i+1}. {t}</td><td class="bx"><span class="box"></span></td><td class="bx"><span class="box"></span></td><td class="bx"><span class="box"></span></td></tr>' for i, t in enumerate(d["rating_topics"]))
    body.append(f"""<section class="reflect"><h2>How confident are you?</h2><p style="margin:0 0 8px;font-size:15px">Tick one box for each topic.</p>
<table><tr><th>Topic</th><th class="bx">Never seen it</th><th class="bx">I can do some</th><th class="bx">Confident</th></tr>{rows}</table></section>""")
    body.append('</main><footer class="wrap"><a href="index.html">All chapters</a> · <a href="chapter-1.html#1">Chapter 1 slides</a></footer>')
    (OUT / "chapter-1-diagnostic.html").write_text(page("Chapter 1 diagnostic · Doing the Numbers", "\n".join(body)))
    return q - 1


KEY_CSS = """
.key h2{font-size:26px;margin:30px 0 6px;border-bottom:3px solid var(--ink);padding-bottom:4px}
.key h3{font-size:19px;margin:16px 0 4px;color:var(--teal)}
.key table{border-collapse:collapse;width:100%;font-size:15px;background:var(--card)}
.key td,.key th{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
.key td:first-child{width:44px;font-weight:800;color:var(--rust)}
.key th{background:#efebe2}
@media print{.key h2{break-after:avoid}.key h3{break-after:avoid}.key tr{break-inside:avoid}.key{font-size:9.5pt}}
"""


def build_key(diag_total):
    b = ['<header class="top"><div class="wrap"><p class="eye">VM Numeracy · Teacher only · not linked from student pages</p>'
         '<h1><small>Chapter 1 · Doing the Numbers</small>Answer key</h1>'
         '<nav class="links"><a href="chapter-1-diagnostic.html">Diagnostic</a>'
         + "".join(f'<a href="chapter-1-worksheet-{w["n"]}.html">1.{w["n"]}</a>' for w in WORKSHEETS)
         + '<button data-print>Print</button></nav></div></header><main class="wrap key">']
    b.append("<h2>Diagnostic</h2><p>Each section of the diagnostic matches a worksheet. Students who miss two or more questions in a section need that worksheet’s worked examples taught explicitly before they start.</p>")
    q = 1
    b.append("<table><tr><th>Q</th><th>Answer</th><th>Section</th></tr>")
    for s in DIAGNOSTIC["sections"]:
        for item in s["qs"]:
            b.append(f'<tr><td>{q}</td><td>{fmt(item["ans"])}</td><td>Worksheet 1.{s["n"]}</td></tr>')
            q += 1
    b.append("</table>")
    for ws in WORKSHEETS:
        b.append(f'<h2>Worksheet 1.{ws["n"]} · {ws["title"]}</h2>')
        qn = 1
        for pi, p in enumerate(ws["parts"]):
            b.append(f'<h3>Part {LETTERS[pi]} · {p["title"]}</h3><table>')
            for qq in p["qs"]:
                if "parts" in qq:
                    a = "; ".join(f'<b>{"abcdefghij"[i]})</b> {fmt(x[1])}' for i, x in enumerate(qq["parts"]))
                else:
                    a = fmt(qq["ans"])
                b.append(f"<tr><td>{qn}</td><td>{a}</td></tr>")
                qn += 1
            b.append("</table>")
    b.append("</main>")
    (OUT / KEY_FILE).write_text(page("Chapter 1 answer key (teacher)", "\n".join(b), noindex=True).replace("</style>", KEY_CSS + "</style>", 1))


if __name__ == "__main__":
    total = 0
    for ws in WORKSHEETS:
        name, n = build_worksheet(ws)
        total += n
        print(name, n, "questions")
    d = build_diagnostic(DIAGNOSTIC)
    print("diagnostic", d, "questions")
    build_key(d)
    print("key", KEY_FILE, "| worksheet questions total", total)
