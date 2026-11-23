"""Renders printable A4 PDFs of the Chapter 1 diagnostic, worksheets and answer key.
Student PDFs go to vm-numeracy/print/ (linked from each page); the answer key and a
combined student pack go to the folder given as argv[1] (not published).
Fonts: pass a folder of fontsource packages as argv[2] so Oswald / Nunito Sans embed
(the sandbox can't reach Google Fonts). Run: python3 make_pdfs.py /tmp/out /home/claude/fonts"""
import asyncio, sys, pathlib, glob
from playwright.async_api import async_playwright
from pypdf import PdfWriter, PdfReader

ROOT = pathlib.Path(__file__).resolve().parent.parent / "vm-numeracy"
PRINT = ROOT / "print"
EXTRA = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/pdf-out")
FONTS = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else None

TITLES = {"chapter-1-diagnostic": "Chapter 1 diagnostic"}
TITLES.update({f"chapter-1-worksheet-{n}": f"Worksheet 1.{n} · {t}" for n, t in enumerate(
    ["Solving problems", "Addition and subtraction", "Multiplying and dividing",
     "Fractions, decimals and ratios", "Percentages", "Rounding, powers and roots"], 1)})


def font_css():
    if not FONTS:
        return ""
    css = []
    for fam, pkg, weights in [("Oswald", "oswald", (500, 600)), ("Nunito Sans", "nunito-sans", (400, 700, 800))]:
        d = glob.glob(str(FONTS / f"fontsource-{pkg}-*" / "files"))[0]
        for w in weights:
            css.append(f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:normal;src:url('file://{d}/{pkg}-latin-{w}-normal.woff2') format('woff2')}}")
    return "\n".join(css)


def footer(label):
    return (f'<div style="font:8px Arial,sans-serif;color:#777;width:100%;padding:0 13mm;display:flex;justify-content:space-between">'
            f'<span>VM Numeracy Units 3 and 4 · {label}</span><span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>')


async def render(page, src, out, label):
    await page.goto(f"file://{src}")
    css = font_css()
    if css:
        await page.add_style_tag(content=css)
    await page.evaluate("document.fonts.ready")
    await page.wait_for_timeout(300)
    await page.pdf(path=str(out), format="A4", print_background=True, prefer_css_page_size=True,
                   display_header_footer=True, header_template="<span></span>", footer_template=footer(label))


async def main():
    PRINT.mkdir(exist_ok=True)
    EXTRA.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page()
        for stem, label in TITLES.items():
            await render(pg, ROOT / f"{stem}.html", PRINT / f"{stem}.pdf", label)
        key = next(ROOT.glob("teacher-key-ch1-*.html"))
        await render(pg, key, EXTRA / "Chapter 1 answer key (teacher).pdf", "Chapter 1 answer key · teacher only")
        await b.close()
    w = PdfWriter()
    for stem in TITLES:
        r = PdfReader(str(PRINT / f"{stem}.pdf"))
        if len(r.pages) % 2:            # pad to even pages so each sheet starts on a new page when printed double-sided
            for pgx in r.pages: w.add_page(pgx)
            w.add_blank_page()
        else:
            for pgx in r.pages: w.add_page(pgx)
    w.write(str(EXTRA / "Chapter 1 student pack (diagnostic + worksheets 1.1-1.6).pdf"))
    for f in sorted(list(PRINT.glob("*.pdf")) + list(EXTRA.glob("*.pdf"))):
        print(f.name, len(PdfReader(str(f)).pages), "pages")

asyncio.run(main())
