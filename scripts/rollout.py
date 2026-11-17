"""Draws the typical ALDI rollout as an SVG flow chart and writes it into work.html,
between the <!-- rollout:start --> and <!-- rollout:end --> markers.

Run: python3 -I scripts/rollout.py
Edit the columns and links below, then run it again.
"""
import html
import pathlib
import re

COLUMNS = [
    ("Brief", 128, [
        dict(id="brief", label="Campaign brief", sub="Media schedule", tall=True),
    ]),
    ("Masters", 150, [
        dict(id="brand", label="Brand masters", sub="Key visual, line, logo", tall=True),
        dict(id="product", label="Product masters", sub="Cut-outs, price, legal", tall=True),
    ]),
    ("Channels", 136, [
        dict(id="ooh", label="OOH", app="adobe"),
        dict(id="dooh", label="Digital OOH", app="figma"),
        dict(id="print", label="Print", app="adobe"),
        dict(id="pos", label="In-store POS", app="adobe"),
        dict(id="social", label="Social", app="figma"),
        dict(id="linkedin", label="LinkedIn", app="figma"),
        dict(id="web", label="Website (CMS)", app="figma"),
        dict(id="display", label="Display banners", app="adobe"),
        dict(id="dco", label="DCO", app="adobe"),
    ]),
    ("Delivered as", 150, [
        dict(id="pdf", label="PDF print-ready", mono=True),
        dict(id="jpg", label="JPG · PNG", mono=True),
        dict(id="mp4", label="MP4", mono=True),
        dict(id="html5", label="PSD", mono=True),
    ]),
]

LINKS = [
    ("brief", "brand"), ("brief", "product"),
    ("brand", "ooh"), ("brand", "dooh"), ("brand", "social"), ("brand", "linkedin"), ("brand", "web"), ("brand", "display"),
    ("product", "dooh"), ("product", "print"), ("product", "pos"), ("product", "social"), ("product", "web"),
    ("product", "display"), ("product", "dco"),
    ("ooh", "pdf"), ("print", "pdf"), ("pos", "pdf"),
    ("dooh", "jpg"), ("dooh", "mp4"), ("social", "jpg"), ("social", "mp4"), ("linkedin", "jpg"),
    ("web", "jpg"), ("display", "html5"), ("dco", "html5"),
]

# Drawn in the house blue: the Special Buys digital OOH on this page.
CHOSEN = ["brief", "product", "dooh", "jpg"]

# The mark on each channel: Adobe for print (CMYK) work, Figma for screen (RGB) work. Paths from Simple Icons (CC0).
APP_MARKS = {
    "adobe": "M13.966 22.624l-1.69-4.281H8.122l3.892-9.144 5.662 13.425zM8.884 1.376H0v21.248zm15.116 0h-8.884L24 22.624Z",
    "figma": open(pathlib.Path(__file__).resolve().parent.parent / "assets/icons/figma.svg").read().split(' d="')[1].split('"')[0],
}
APP_TITLES = {"adobe": "Print, made in Adobe apps", "figma": "Screen (RGB), made in Figma"}

GAP = 36        # between columns
ROW = 32        # node height
TALL = 44       # node height with a second line
ROW_GAP = 10
TOP = 30        # room for the column titles


def build():
    height_of = lambda n: TALL if n.get("tall") else ROW
    col_h = lambda nodes: sum(height_of(n) for n in nodes) + ROW_GAP * (len(nodes) - 1)
    body = max(col_h(nodes) for _, _, nodes in COLUMNS)

    nodes, titles, x = {}, [], 0
    for title, w, col in COLUMNS:
        titles.append((x, title))
        y = TOP + (body - col_h(col)) / 2
        for n in col:
            h = height_of(n)
            nodes[n["id"]] = dict(n, x=x, y=y, w=w, h=h)
            y += h + ROW_GAP
        x += w + GAP
    width, height = x - GAP, TOP + body

    def edge(a, b):
        s, t = nodes[a], nodes[b]
        x1, y1 = s["x"] + s["w"], s["y"] + s["h"] / 2
        x2, y2 = t["x"], t["y"] + t["h"] / 2
        dx = (x2 - x1) / 2
        return f"M{x1:.1f} {y1:.1f}C{x1 + dx:.1f} {y1:.1f} {x2 - dx:.1f} {y2:.1f} {x2:.1f} {y2:.1f}"

    chosen_pairs = set(zip(CHOSEN, CHOSEN[1:]))
    out = [f'<svg class="flow-graph" viewBox="-1 0 {width + 2} {height + 1}" role="img" '
           f'aria-label="A typical ALDI rollout: the brief, the brand and product masters, nine channels and what each one is delivered as.">']
    out.append("<defs>" + "".join(
        f'<symbol id="mk-{k}" viewBox="0 0 24 24"><path d="{d}"/></symbol>' for k, d in APP_MARKS.items()) + "</defs>")
    for tx, t in titles:
        out.append(f'<text class="fl-title" x="{tx}" y="12">{html.escape(t.upper())}</text>')
    # Plain edges first, the chosen path on top.
    for a, b in sorted(LINKS, key=lambda l: l in chosen_pairs):
        cls = "fe fe-chosen" if (a, b) in chosen_pairs else "fe"
        out.append(f'<path class="{cls}" d="{edge(a, b)}"/>')
    for n in nodes.values():
        chosen = n["id"] in CHOSEN
        out.append(f'<g class="fn{" fn-chosen" if chosen else ""}" transform="translate({n["x"]} {n["y"]:.1f})">')
        out.append(f'<rect class="fn-box" x="0.5" y="0.5" width="{n["w"] - 1}" height="{n["h"] - 1}" rx="6"/>')
        label = html.escape(n["label"])
        if n.get("tall"):
            out.append(f'<text class="fn-label" x="11" y="19">{label}</text>')
            out.append(f'<text class="fn-sub" x="11" y="33">{html.escape(n["sub"])}</text>')
        else:
            cls = "fn-label fn-mono" if n.get("mono") else "fn-label"
            out.append(f'<text class="{cls}" x="11" y="{n["h"] / 2 + 4:.1f}">{label}</text>')
        if n.get("app"):
            s = 12
            out.append(f'<use class="fn-app" href="#mk-{n["app"]}" x="{n["w"] - s - 10}" y="{(n["h"] - s) / 2:.1f}" '
                       f'width="{s}" height="{s}"><title>{APP_TITLES[n["app"]]}</title></use>')
        out.append("</g>")
    out.append("</svg>")
    return "\n".join(out)


page = pathlib.Path(__file__).resolve().parent.parent / "work.html"
text = page.read_text()
new, count = re.subn(r"(<!-- rollout:start -->).*?(<!-- rollout:end -->)",
                     lambda m: m.group(1) + "\n" + build() + "\n" + m.group(2), text, flags=re.S)
if count != 1:
    raise SystemExit("work.html needs one <!-- rollout:start --> ... <!-- rollout:end --> pair")
page.write_text(new)
print("rollout written into", page)
