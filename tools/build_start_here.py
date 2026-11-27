"""Builds vm-numeracy/start-here.html: the Units 3 and 4 introduction deck.
Order: the 3 outcomes (what you must show) -> the 6 numeracies (the real-life contexts of Outcome 1)
-> the 4 Unit 3 areas of study (the maths used in those contexts) -> how it all fits together.
Content is drawn from the VCE VM Numeracy study design (VCAA, 2023), reworded for students."""
from deck import build_deck, ROOT

CSS = """
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:32px;margin-top:8px;}
.grid2{display:grid;grid-template-columns:repeat(2,1fr);gap:28px 36px;margin-top:8px;}
.card{background:var(--card);border-radius:18px;padding:34px 38px;border-top:12px solid var(--teal);display:flex;flex-direction:column;}
.card.y{border-top-color:var(--orange);} .card.r{border-top-color:var(--rust);} .card.g{border-top-color:#9aa1a6;}
.card h3{margin:0 0 14px;color:var(--ink);}
.card p,.card li{font-size:28px;line-height:1.35;color:var(--soft);}
.card li{margin-bottom:8px;}
.card .k{font-family:'Oswald',Arial,sans-serif;font-weight:600;font-size:26px;letter-spacing:.08em;text-transform:uppercase;color:var(--rust);margin:0 0 8px;}
.pill{display:inline-block;font-weight:800;font-size:22px;letter-spacing:.06em;text-transform:uppercase;padding:6px 16px;border-radius:999px;margin:0 0 12px;align-self:flex-start;}
.pill.u3{background:var(--orange);color:var(--ink);} .pill.u4{background:#dcd7cc;color:var(--ink);}
.lede{font-size:34px;line-height:1.35;margin:0 0 34px;max-width:1500px;}
.quote{background:#2c3236;color:var(--paper);border-left:12px solid var(--orange);border-radius:14px;padding:30px 38px;margin:0 0 32px;}
.quote p{font-size:30px;margin:0;color:var(--paper);}
.quote .src{font-size:22px;color:var(--softdark);margin-top:10px;}
.words{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;}
.words div{background:var(--card);border-radius:14px;padding:24px 28px;}
.words b{font-family:'Oswald',Arial,sans-serif;font-weight:600;font-size:32px;display:block;margin-bottom:6px;color:var(--teal);}
.words span{font-size:26px;line-height:1.3;color:var(--soft);}
table.map{border-collapse:separate;border-spacing:0;width:100%;font-size:30px;background:var(--card);border-radius:18px;overflow:hidden;}
table.map th,table.map td{padding:22px 26px;text-align:center;border-bottom:2px solid var(--line);}
table.map th{font-family:'Oswald',Arial,sans-serif;font-weight:600;font-size:30px;background:var(--ink);color:var(--paper);}
table.map td:first-child,table.map th:first-child{text-align:left;}
table.map td.tick{color:var(--teal);font-weight:800;font-size:40px;}
table.map tr:last-child td{border-bottom:0;}
table.map .sub{display:block;font-size:22px;color:var(--soft);font-weight:400;}
table.map th .sub{color:var(--softdark);}
.year{display:grid;grid-template-columns:repeat(5,1fr);gap:20px;margin-top:10px;}
.year>a,.year>div{display:block;text-decoration:none;background:#2c3236;border-radius:14px;padding:22px 24px;border-top:10px solid var(--orange);}
.year .n{font-family:'Oswald',Arial,sans-serif;font-weight:600;font-size:56px;color:var(--orange);line-height:1;}
.year .t{font-size:26px;font-weight:800;color:var(--paper);margin-top:8px;}
.year .m{font-size:22px;color:var(--softdark);margin-top:4px;}
.card ul.big{columns:2;column-gap:64px;margin-top:10px;} .card ul.big li{font-size:34px;line-height:1.3;margin-bottom:26px;color:var(--ink);break-inside:avoid;}
.go{display:inline-block;background:var(--orange);color:var(--ink);font-weight:800;font-size:30px;padding:16px 34px;border-radius:14px;text-decoration:none;margin-right:20px;}
"""


def li(sec_no, title, eyebrow, intention, criteria, sid):
    crit = "".join(f"<li>{c}</li>" for c in criteria)
    return dict(id=sid, dark=True, li=True, sec=f"sec-{sec_no}", toc=title, html=f"""
<p class="eyebrow">{eyebrow}</p>
<h1>{title}</h1>
<div class="row" style="margin-top:56px;">
<div class="box rise"><h3>Learning intention</h3><p>{intention}</p></div>
<div class="box rise d1"><h3>Success criteria</h3><ul>{crit}</ul></div>
</div>
<p class="backlink"><a href="#1">← Contents</a></p>""")


def plain(sid, toc, html):
    return dict(id=sid, toc=toc, html=html)


slides = []

# 1 cover
slides.append(dict(id="cover", dark=True, li=True, toc="How this course works", html="""
<p class="eyebrow">VM Numeracy · Units 3 and 4 · Start here</p>
<h1>How this course works</h1>
<div class="toc">
<div class="item"><p><a href="#sec-1">1 · The three outcomes</a></p><p class="pg">What you must show to get an S</p></div>
<div class="item"><p><a href="#sec-3">3 · The four areas of study</a></p><p class="pg">The maths you will use in Unit 3</p></div>
<div class="item"><p><a href="#sec-2">2 · The six numeracies</a></p><p class="pg">The real-life places maths turns up</p></div>
<div class="item"><p><a href="#sec-4">4 · Putting it together</a></p><p class="pg">How the chapters, numeracies and outcomes fit</p></div>
</div>
<p class="backlink"><a href="chapter-1.html#1">Chapter 1: Doing the Numbers →</a> &nbsp;&nbsp; <a href="index.html">← All chapters</a></p>"""))

# Section 1: outcomes
slides.append(li(1, "The three outcomes", "Section 1 · Unit 3",
                 "We are learning what you need to show to complete Unit 3.",
                 ["I can explain what S and N mean", "I can name the three outcomes",
                  "I can say what each outcome asks me to do"], "s1-li"))

slides.append(plain("s1-pass", "How you pass Unit 3", """
<p class="eyebrow">Section 1 · The three outcomes</p>
<h2>How you pass Unit 3</h2>
<p class="lede">Each unit is marked <b>S</b> (Satisfactory) or <b>N</b> (Not Satisfactory). To get an S you must show all three outcomes. Your worksheets, assessment tasks and projects are the evidence.</p>
<div class="grid3">
<div class="card"><p class="k">Outcome 1</p><h3>Numeracy in context</h3><p>Find the maths in real-life situations, use it, and judge whether your answers make sense.</p></div>
<div class="card y"><p class="k">Outcome 2</p><h3>The problem-solving cycle</h3><p>Plan, solve, check and report on real problems using the four stages of the cycle.</p></div>
<div class="card r"><p class="k">Outcome 3</p><h3>Mathematical toolkit</h3><p>Choose and use the right tools accurately: calculators, tape measures, spreadsheets and apps.</p></div>
</div>"""))

slides.append(plain("s1-o1", "Outcome 1: Numeracy in context", """
<p class="eyebrow">Section 1 · The three outcomes</p>
<h2>Outcome 1: Numeracy in context</h2>
<div class="quote"><p>Extract, evaluate and apply the maths from Areas of Study 1–4, in routine, non-routine, unfamiliar and some specialised contexts, across the chosen numeracies.</p><p class="src">VCE VM Numeracy study design, Unit 3 Outcome 1 (shortened)</p></div>
<p class="lede" style="margin-bottom:26px;">In plain words: <b>find the maths hiding in a real situation, use it, and decide if your answer is reasonable.</b> The situations come from the numeracies (Section 2). The maths comes from the areas of study (Section 3).</p>
<div class="words">
<div><b>Routine</b><span>Tasks people do often, like working out change or a shift’s pay.</span></div>
<div><b>Unfamiliar</b><span>Situations you haven’t met before, so you must work out which maths fits.</span></div>
<div><b>Specialised</b><span>Tasks with their own words and rules, like a trade’s mixing ratios or tolerances.</span></div>
</div>"""))

CYCLE = """<svg viewBox="0 0 760 700" width="700" height="645" role="img" aria-label="The problem-solving cycle: 1 Identify the maths, 2 Act on and use maths, 3 Evaluate and reflect, 4 Communicate and report, then back to 1.">
<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#a84b16"/></marker></defs>
<g font-family="Nunito Sans, Arial, sans-serif">
<rect x="20" y="20" width="320" height="250" rx="22" fill="#1f7a6e"/><rect x="420" y="20" width="320" height="250" rx="22" fill="#f6c21a"/>
<rect x="420" y="430" width="320" height="250" rx="22" fill="#1f2326"/><rect x="20" y="430" width="320" height="250" rx="22" fill="#a84b16"/>
<text x="180" y="96" text-anchor="middle" font-family="Oswald, Arial" font-size="56" font-weight="600" fill="#f4f2ec">1</text>
<text x="180" y="160" text-anchor="middle" font-size="34" font-weight="800" fill="#f4f2ec">Identify</text><text x="180" y="202" text-anchor="middle" font-size="34" font-weight="800" fill="#f4f2ec">the maths</text>
<text x="580" y="96" text-anchor="middle" font-family="Oswald, Arial" font-size="56" font-weight="600" fill="#1f2326">2</text>
<text x="580" y="160" text-anchor="middle" font-size="34" font-weight="800" fill="#1f2326">Act on and</text><text x="580" y="202" text-anchor="middle" font-size="34" font-weight="800" fill="#1f2326">use maths</text>
<text x="580" y="506" text-anchor="middle" font-family="Oswald, Arial" font-size="56" font-weight="600" fill="#f6c21a">3</text>
<text x="580" y="570" text-anchor="middle" font-size="34" font-weight="800" fill="#f4f2ec">Evaluate</text><text x="580" y="612" text-anchor="middle" font-size="34" font-weight="800" fill="#f4f2ec">and reflect</text>
<text x="180" y="506" text-anchor="middle" font-family="Oswald, Arial" font-size="56" font-weight="600" fill="#f4f2ec">4</text>
<text x="180" y="570" text-anchor="middle" font-size="34" font-weight="800" fill="#f4f2ec">Communicate</text><text x="180" y="612" text-anchor="middle" font-size="34" font-weight="800" fill="#f4f2ec">&amp; report</text>
<g stroke="#a84b16" stroke-width="8" fill="none" marker-end="url(#ah)">
<path d="M346 145 H408"/><path d="M580 278 V418"/><path d="M412 555 H352"/><path d="M180 422 V284"/></g>
<text x="380" y="365" text-anchor="middle" font-size="26" font-weight="700" fill="#3d4448">a real problem</text></g></svg>"""

slides.append(plain("s1-o2", "Outcome 2: The problem-solving cycle", f"""
<p class="eyebrow">Section 1 · The three outcomes</p>
<h2>Outcome 2: The problem-solving cycle</h2>
<div class="row" style="gap:56px;align-items:flex-start;">
<div style="flex:none;">{CYCLE}</div>
<div style="flex:1;">
<p class="step" style="font-size:27px;margin-bottom:18px;"><b style="color:var(--teal);">1 Identify the maths:</b> Find, identify and interpret the numerical information. Look for numbers, words, images, measures, shapes and questions.</p>
<p class="step" style="font-size:27px;margin-bottom:18px;"><b style="color:#9a7300;">2 Act on and use maths:</b> Do the estimates, calculations or actions, and use suitable technology.</p>
<p class="step" style="font-size:27px;margin-bottom:18px;"><b style="color:var(--ink);">3 Evaluate and reflect:</b> Check the right information and the right maths were used. Is the result close to your estimate? What did you do well? What do you need to improve?</p>
<p class="step" style="font-size:27px;margin-bottom:18px;"><b style="color:var(--rust);">4 Communicate &amp; report:</b> Share your results and findings in a suitable format, using words, numbers, graphs or other media.</p>
</div></div>"""))

slides.append(plain("s1-o3", "Outcome 3: Mathematics toolkit", """
<p class="eyebrow">Section 1 · The three outcomes</p>
<h2>Outcome 3: Your mathematics toolkit</h2>
<p class="lede">Analogue, digital and technological tools. All year you build skills in using them for your personal, work, health, recreation, money and community life.</p>
<div class="grid3">
<div class="card"><p class="k">Measure, time and count</p><ul><li>Measuring devices</li><li>Timing devices</li><li>Counters and sensors</li><li>Monitoring and alarms</li></ul></div>
<div class="card y"><p class="k">Calculate and analyse</p><ul><li>Calculators and computing</li><li>Spreadsheets and software</li><li>Apps and processors</li><li>Data, statistics and information</li></ul></div>
<div class="card r"><p class="k">Plan, show and record</p><ul><li>Tables, planners, rosters and organisers</li><li>Graphing, mapping and drawing</li><li>Designing and making</li><li>Collecting and recording, inputs and outputs</li></ul></div>
</div>
<p class="muted" style="font-size:26px;margin-top:24px;">Coursebook: Mathematics Toolkit, Unit 3 introduction. You will use these tools with the cycle: pick the right tool, use it accurately, check the result.</p>"""))

# Section 2: numeracies
slides.append(li(2, "The six numeracies", "Section 2 · Units 3 and 4",
                 "We are learning the six parts of life where we use maths, and which ones we cover in each unit.",
                 ["I can name all six numeracies", "I can say which three are in Unit 3 and which three are in Unit 4",
                  "I can give a real example of each one"], "s2-li"))

slides.append(plain("s2-all", "Six numeracies, two units", """
<p class="eyebrow">Section 2 · The six numeracies</p>
<h2>Six numeracies: maths in six parts of life</h2>
<p class="lede" style="margin-bottom:26px;">Each unit covers three numeracies. Across Units 3 and 4 you cover all six.</p>
<div class="grid3" style="gap:26px;">
<div class="card y"><span class="pill u3">Unit 3</span><h3>Personal</h3><p>Organising your own life: numbers, money, time and travel.</p></div>
<div class="card y"><span class="pill u3">Unit 3</span><h3>Vocational</h3><p>Doing the job: workplace measurements, plans, tools and instructions.</p></div>
<div class="card y"><span class="pill u3">Unit 3</span><h3>Health</h3><p>Looking after health, safety and well-being, yours and your community’s.</p></div>
<div class="card g"><span class="pill u4">Unit 4</span><h3>Civic</h3><p>Staying informed: government, news and social data.</p></div>
<div class="card g"><span class="pill u4">Unit 4</span><h3>Financial</h3><p>Managing money: budgets, bills, tax, credit and good decisions.</p></div>
<div class="card g"><span class="pill u4">Unit 4</span><h3>Recreational</h3><p>Sport, arts, games, social media, travel and time off.</p></div>
</div>"""))

slides.append(plain("s2-u3", "Unit 3 numeracies: examples", """
<p class="eyebrow">Section 2 · The six numeracies · Unit 3</p>
<h2>Unit 3: Personal, Vocational, Health</h2>
<div class="grid3">
<div class="card y"><span class="pill u3">Personal</span><ul><li>Planning a BBQ, party or family event</li><li>Comparing prices, discounts and payment deals</li><li>Cooking, gardening and travel</li><li>Comparing fuel costs for cars</li></ul></div>
<div class="card y"><span class="pill u3">Vocational</span><ul><li>Reading workplace plans, diagrams and formulas</li><li>Ratios for mixing chemicals</li><li>Measuring tools and tolerances</li><li>Safety data sheets</li></ul></div>
<div class="card y"><span class="pill u3">Health</span><ul><li>Medication doses and timing</li><li>Nutrition and fitness goals</li><li>Heart rate, blood pressure and temperature</li><li>Health care costs and insurance</li></ul></div>
</div>"""))

slides.append(plain("s2-u4", "Unit 4 numeracies: examples", """
<p class="eyebrow">Section 2 · The six numeracies · Unit 4</p>
<h2>Unit 4: Civic, Financial, Recreational</h2>
<div class="grid3">
<div class="card g"><span class="pill u4">Civic</span><ul><li>Government and news statistics</li><li>Elections and voting</li><li>Unemployment, inflation and interest rates</li><li>Environmental issues, including First Nations perspectives</li></ul></div>
<div class="card g"><span class="pill u4">Financial</span><ul><li>Budgets in a spreadsheet or app</li><li>Comparing bills and providers over time</li><li>Tax, GST and superannuation</li><li>Odds and the risks of gambling</li></ul></div>
<div class="card g"><span class="pill u4">Recreational</span><ul><li>Sport and performance statistics</li><li>Social media use and overuse</li><li>Navigating: bushwalks, bike rides, orienteering</li><li>Planning a trip with maps and GPS</li></ul></div>
</div>"""))

# Section 3: areas of study
slides.append(li(3, "The four areas of study", "Section 3 · Unit 3",
                 "We are learning the four areas of maths in Unit 3 and which chapters cover them.",
                 ["I can name the four areas of study in Unit 3", "I can match each area of study to its chapters",
                  "I can describe some skills in each area"], "s3-li"))

slides.append(plain("s3-all", "Four areas of study, five chapters", """
<p class="eyebrow">Section 3 · The four areas of study</p>
<h2>Unit 3: four areas of study, five chapters</h2>
<div class="grid2">
<div class="card"><p class="k">Area of Study 1</p><h3>Number</h3><p>Chapter 1 · Doing the Numbers</p></div>
<div class="card"><p class="k">Area of Study 2</p><h3>Shape</h3><p>Chapter 2 · Shape Up</p></div>
<div class="card"><p class="k">Area of Study 3</p><h3>Quantity and measures</h3><p>Chapter 3 · Measuring Up &nbsp;·&nbsp; Chapter 4 · Got the Time?</p></div>
<div class="card"><p class="k">Area of Study 4</p><h3>Relationships</h3><p>Chapter 5 · Relationships</p></div>
</div>
<p class="muted" style="font-size:26px;margin-top:30px;">Unit 4 has four different areas of study: 5 Dimension and direction, 6 Data, 7 Uncertainty and 8 Systematics.</p>"""))


def aos(n, name, chapters, skills, sid):
    items = "".join(f"<li>{s}</li>" for s in skills)
    return plain(sid, f"AOS {n}: {name}", f"""
<p class="eyebrow">Section 3 · Area of Study {n} · {chapters}</p>
<h2>Area of Study {n}: {name}</h2>
<div class="card"><p class="k">By the end you will be able to</p><ul class="big">{items}</ul></div>""")


slides.append(aos(1, "Number", "Chapter 1", [
    "Read very large and very small numbers", "Calculate with positive and negative numbers",
    "Round whole numbers, and decimals to 3 places", "Use the order of operations",
    "Move between fractions, decimals and percentages", "Calculate percentage increase and decrease",
    "Use powers (up to cubed) and square roots", "Solve problems with ratios and proportions"], "s3-a1"))
slides.append(aos(2, "Shape", "Chapter 2", [
    "Name and sort 2D shapes and 3D objects, like cones and pyramids", "Find lines of symmetry and rotational symmetry",
    "Use angle facts: 180° in a triangle, 360° in a quadrilateral", "Tell when shapes are congruent or similar",
    "Build compound shapes and objects, including with technology", "Enlarge and reduce shapes using a scale",
    "Spot shape patterns in bridges, buildings and design"], "s3-a2"))
slides.append(aos(3, "Quantity and measures", "Chapters 3 and 4", [
    "Estimate and measure with the right accuracy and tolerance", "Find perimeter, area, volume and capacity, including compound shapes",
    "Use π for circles", "Convert metric units, and metric to non-metric (cm/inch, °C/°F, g/lb)",
    "Read 24-hour time and work across time zones", "Calculate durations using calendars and clocks",
    "Read and calculate with temperatures"], "s3-a3"))
slides.append(aos(4, "Relationships", "Chapter 5", [
    "Use rates such as km/h, L/h, $/m³ and wages per hour", "Use ratios and scales on maps and plans",
    "Use formulas by substituting values", "Show a relationship in a table, graph or formula",
    "Describe how one quantity changes with another", "Use proportions when mixing chemicals or ingredients"], "s3-a4"))

# Section 4: together
slides.append(li(4, "Putting it together", "Section 4 · Unit 3",
                 "We are learning how the numeracies, areas of study and chapters link up across the year.",
                 ["I can say which numeracy goes with each chapter", "I can describe the order of the chapters",
                  "I know what to do first in Chapter 1"], "s4-li"))

slides.append(plain("s4-map", "Unit 3 map: numeracies and areas of study", """
<p class="eyebrow">Section 4 · Putting it together</p>
<h2>Unit 3 map: numeracies and areas of study</h2>
<table class="map">
<tr><th>Numeracy</th><th>AOS 1 Number<span class="sub">Ch 1</span></th><th>AOS 2 Shape<span class="sub">Ch 2</span></th><th>AOS 3 Quantity and measures<span class="sub">Ch 3, 4</span></th><th>AOS 4 Relationships<span class="sub">Ch 5</span></th></tr>
<tr><td><b>Personal</b><span class="sub">money, events, shopping, travel</span></td><td class="tick">✓</td><td class="tick">✓</td><td></td><td></td></tr>
<tr><td><b>Vocational</b><span class="sub">measuring, time and plans at work</span></td><td></td><td></td><td class="tick">✓</td><td></td></tr>
<tr><td><b>Health</b><span class="sub">rates, doses, fitness and well-being</span></td><td></td><td></td><td></td><td class="tick">✓</td></tr>
</table>
<p class="muted" style="font-size:26px;margin-top:26px;">Every chapter also builds Outcome 2 (the problem-solving cycle) and Outcome 3 (your toolkit).</p>"""))

slides.append(dict(id="s4-year", dark=True, toc="Your year and where to start", html="""
<p class="eyebrow">Section 4 · Putting it together</p>
<h2>Unit 3 chapters and where to start</h2>
<div class="year">
<a href="chapter-1.html#1"><div class="n">1</div><div class="t">Doing the Numbers</div><div class="m">Number</div></a>
<div><div class="n">2</div><div class="t">Shape Up</div><div class="m">Shape</div></div>
<div><div class="n">3</div><div class="t">Measuring Up</div><div class="m">Quantity and measures</div></div>
<div><div class="n">4</div><div class="t">Got the Time?</div><div class="m">Quantity and measures</div></div>
<div><div class="n">5</div><div class="t">Relationships</div><div class="m">Relationships</div></div>
</div>
<p style="font-size:30px;margin:44px 0 30px;color:var(--softdark);">Each chapter has slides, a worksheet for every section, and an assessment task. Unit 4 (Terms 3 and 4) covers Chapters 6 to 10.</p>
<p><a class="go" href="chapter-1-diagnostic.html">Start: Chapter 1 diagnostic →</a><a class="go" style="background:#2c3236;color:var(--paper);" href="chapter-1.html#1">Chapter 1 slides →</a></p>"""))

n = build_deck(ROOT / "vm-numeracy" / "start-here.html", "Start here · VM Numeracy Units 3 and 4",
               "Start here · How this course works", slides, CSS)
print(n, "slides")
