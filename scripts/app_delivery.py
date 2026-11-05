"""Renders assets/app-delivery/*.svg: three flows of the cross-platform product.

Every branch is built and tested with suites in parallel, a release deploys only the services picked for it,
and a dependency scan looks for known vulnerabilities.

python scripts/app_delivery.py
"""
from pathlib import Path

from pipeline import FONT, THEMES, esc

# (kind, title, subtitle, start, done); kinds: node, bars, grid, scan
TRACKS = [
    ("Every branch", "build and test", [
        ("node", "Checkout", "branch", 0.3, 0.8),
        ("node", "Build", "app and images", 0.9, 1.4),
        ("bars", "Tests", "9 suites in parallel", 1.5, 3.8),
        ("node", "Image", "to registry", 3.9, 4.2),
        ("node", "Reports", "test results", 4.3, 4.6),
    ]),
    ("Release", "on demand", [
        ("node", "Pick release", "tag and services", 5.0, 5.5),
        ("node", "Preflight", "params, secrets", 5.6, 6.0),
        ("node", "Lint", "deploy code", 6.1, 6.5),
        ("grid", "Deploy", "picked services only", 6.6, 8.6),
        ("node", "Rollouts", "all healthy", 8.7, 9.1),
        ("node", "Version page", "updated", 9.2, 9.6),
    ]),
    ("Dependency scan", "known vulnerabilities", [
        ("node", "Resolve", "dependencies", 10.0, 10.5),
        ("scan", "Scan", "against CVE data", 10.6, 12.0),
        ("node", "Report", "published", 12.1, 12.4),
    ]),
]

HOLD = 14.0
CYCLE = 14.8
BAR_ENDS = [2.6, 3.1, 2.9, 3.8, 2.4, 3.4, 3.0, 3.6, 2.8]   # parallel suites finish at different times
GRID = (2, 10)                                             # rows x cols of services
PICKED = {0, 2, 3, 5, 8, 9, 11, 12, 14, 17, 18, 19}         # services ticked in the release form


def pct(t):
    return f"{t / CYCLE * 100:.2f}%"


class Anim:
    """Collects one keyframes rule per animated element."""

    def __init__(self):
        self.rules, self.n = [], 0

    def show(self, at, base=0.0):
        """opacity base -> 1 at `at`, back to base after HOLD"""
        self.n += 1
        c = f"a{self.n}"
        self.rules.append(f".{c} {{ animation: {c} {CYCLE}s linear infinite; }} "
                          f"@keyframes {c} {{ 0%, {pct(at - 0.05)} {{ opacity: {base} }} {pct(at + 0.1)}, {pct(HOLD)} {{ opacity: 1 }} "
                          f"{pct(HOLD + 0.4)}, 100% {{ opacity: {base} }} }}")
        return c

    def grow(self, start, end):
        """scaleX 0 -> 1 between start and end"""
        self.n += 1
        c = f"a{self.n}"
        self.rules.append(f".{c} {{ transform-box: fill-box; transform-origin: left center; animation: {c} {CYCLE}s linear infinite; }} "
                          f"@keyframes {c} {{ 0%, {pct(start)} {{ transform: scaleX(0) }} {pct(end)}, {pct(HOLD)} {{ transform: scaleX(1) }} "
                          f"{pct(HOLD + 0.4)}, 100% {{ transform: scaleX(0) }} }}")
        return c


def style(t, anim):
    return f"""<style>
  text {{ font-family: {FONT}; }}
  .track-title {{ font-size: 14px; font-weight: 600; fill: {t['text']}; }}
  .track-sub {{ font-size: 12px; fill: {t['muted']}; }}
  .title {{ font-size: 13px; font-weight: 600; fill: {t['text']}; }}
  .sub {{ font-size: 12px; fill: {t['muted']}; }}
  .wire {{ stroke: {t['stroke']}; stroke-width: 3; stroke-linecap: round; }}
  .wire-on {{ stroke: {t['accent']}; stroke-width: 3; stroke-linecap: round; opacity: 0; }}
  .node {{ fill: {t['fill']}; stroke: {t['stroke']}; stroke-width: 2; }}
  .done {{ fill: {t['accent']}; opacity: 0; }}
  .tick {{ fill: none; stroke: #ffffff; stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; opacity: 0; }}
  .slot {{ fill: {t['stroke']}; opacity: .55; }}
  .bar {{ fill: {t['accent']}; }}
  .svc {{ fill: {t['fill']}; stroke: {t['stroke']}; stroke-width: 1.5; }}
  .svc-on {{ fill: {t['accent']}; opacity: 0; }}
  .divider {{ stroke: {t['stroke']}; stroke-width: 1; stroke-dasharray: 3 5; opacity: .7; }}
  {' '.join(anim.rules)}
  @media (prefers-reduced-motion: reduce) {{
    [class^="a"], [class*=" a"] {{ animation: none !important; opacity: 1 !important; transform: none !important; }} }}
</style>"""


def node(anim, x, y, done, r=10):
    on = anim.show(done)
    return (f'<circle class="node" cx="{x}" cy="{y}" r="{r}"/>'
            f'<circle class="done {on}" cx="{x}" cy="{y}" r="{r}"/>'
            f'<path class="tick {on}" d="M {x - 4.5} {y + 0.5} l 3 3 l 6 -6.5"/>')


def bars(anim, x, y, w, start, vertical=False):
    out = []
    n = len(BAR_ENDS)
    if not vertical:                       # horizontal bars stacked: wide layout
        h, gap = 4, 3
        top = y - (n * h + (n - 1) * gap) / 2
        for i, end in enumerate(BAR_ENDS):
            yy = top + i * (h + gap)
            out.append(f'<rect class="slot" x="{x}" y="{yy}" width="{w}" height="{h}" rx="2"/>'
                       f'<rect class="bar {anim.grow(start, end)}" x="{x}" y="{yy}" width="{w}" height="{h}" rx="2"/>')
    else:                                  # short horizontal bars side by side: narrow layout
        bw, gap = (w - (n - 1) * 4) / n, 4
        for i, end in enumerate(BAR_ENDS):
            xx = x + i * (bw + gap)
            out.append(f'<rect class="slot" x="{xx:.1f}" y="{y - 3}" width="{bw:.1f}" height="6" rx="3"/>'
                       f'<rect class="bar {anim.grow(start, end)}" x="{xx:.1f}" y="{y - 3}" width="{bw:.1f}" height="6" rx="3"/>')
    return "".join(out)


def grid(anim, x, y, start, end, size=14, gap=5):
    rows, cols = GRID
    picked = sorted(PICKED)
    step = (end - start) / len(picked)
    top = y - (rows * size + (rows - 1) * gap) / 2
    out = []
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c
            xx, yy = x + c * (size + gap), top + r * (size + gap)
            out.append(f'<rect class="svc" x="{xx}" y="{yy}" width="{size}" height="{size}" rx="3"/>')
            if i in PICKED:
                at = start + step * (picked.index(i) + 1)
                out.append(f'<rect class="svc-on {anim.show(at)}" x="{xx}" y="{yy}" width="{size}" height="{size}" rx="3"/>')
    return "".join(out)


def scan(anim, x, y, w, start, end):
    return (f'<rect class="slot" x="{x}" y="{y - 4}" width="{w}" height="8" rx="4"/>'
            f'<rect class="bar {anim.grow(start, end)}" x="{x}" y="{y - 4}" width="{w}" height="8" rx="4"/>')


WIDTH = {"node": 0, "bars": 170, "grid": 185, "scan": 150}
HALF = {"node": 10, "bars": 31, "grid": 17, "scan": 10}


def wide(t):
    W, H = 1000, 356
    rows = [58, 190, 300]
    anim, out = Anim(), []
    for (title, sub, items), y in zip(TRACKS, rows):
        out.append(f'<text class="track-title" x="12" y="{y - 2}">{esc(title)}</text>'
                   f'<text class="track-sub" x="12" y="{y + 15}">{esc(sub)}</text>')
        label_y = y + max(HALF[k] for k, *_ in items) + 22
        x = 200
        spans = []
        for kind, it, isub, start, done in items:
            w = WIDTH[kind]
            spans.append((x, x + w, kind, start, done))
            x += w + 112
        # wires between consecutive items, lit when the item on the right starts
        for (x1a, x1b, k1, s1, d1), (x2a, x2b, k2, s2, d2) in zip(spans, spans[1:]):
            a = x1b + (12 if k1 == "node" else 8)
            b = x2a - (12 if k2 == "node" else 8)
            out.append(f'<line class="wire" x1="{a}" y1="{y}" x2="{b}" y2="{y}"/>'
                       f'<line class="wire-on {anim.show(d1 + 0.05)}" x1="{a}" y1="{y}" x2="{b}" y2="{y}"/>')
        for (xa, xb, kind, start, done), (_, it, isub, *_r) in zip(spans, items):
            cx = (xa + xb) / 2
            if kind == "node":
                out.append(node(anim, xa, y, done))
            elif kind == "bars":
                out.append(bars(anim, xa, y, xb - xa, start))
            elif kind == "grid":
                out.append(grid(anim, xa, y, start, done))
            else:
                out.append(scan(anim, xa, y, xb - xa, start, done))
            out.append(f'<text class="title" x="{cx}" y="{label_y}" text-anchor="middle">{esc(it)}</text>'
                       f'<text class="sub" x="{cx}" y="{label_y + 17}" text-anchor="middle">{esc(isub)}</text>')
    for y in ((rows[0] + rows[1]) / 2 + 8, (rows[1] + rows[2]) / 2 + 6):
        out.append(f'<line class="divider" x1="12" y1="{y}" x2="{W - 12}" y2="{y}"/>')
    return svg(W, H, t, anim, out)


def narrow(t):
    W, row = 400, 46
    anim, out = Anim(), []
    y = 24
    for ti, (title, sub, items) in enumerate(TRACKS):
        if ti:
            out.append(f'<line class="divider" x1="12" y1="{y - 14}" x2="{W - 12}" y2="{y - 14}"/>')
        out.append(f'<text class="track-title" x="12" y="{y}">{esc(title)}</text>'
                   f'<text class="track-sub" x="{W - 12}" y="{y}" text-anchor="end">{esc(sub)}</text>')
        y += 30
        ys = [y + i * row for i in range(len(items))]
        for (k1, *_a, d1), y1, y2 in zip(items, ys, ys[1:]):
            out.append(f'<line class="wire" x1="28" y1="{y1 + 12}" x2="28" y2="{y2 - 12}"/>'
                       f'<line class="wire-on {anim.show(d1 + 0.05)}" x1="28" y1="{y1 + 12}" x2="28" y2="{y2 - 12}"/>')
        for (kind, it, isub, start, done), yy in zip(items, ys):
            out.append(node(anim, 28, yy, done, r=9))
            out.append(f'<text class="title" x="48" y="{yy - 2}">{esc(it)}</text>'
                       f'<text class="sub" x="48" y="{yy + 14}">{esc(isub)}</text>')
            if kind == "bars":
                out.append(bars(anim, 200, yy, 186, start, vertical=True))
            elif kind == "grid":
                out.append(grid(anim, 200, yy, start, done, size=14, gap=5))
            elif kind == "scan":
                out.append(scan(anim, 200, yy, 186, start, done))
        y = ys[-1] + 44
    return svg(W, y - 14, t, anim, out)


def svg(w, h, t, anim, body):
    title = ("Three flows: every branch is built and tested with nine suites in parallel; a release deploys only the "
             "services picked for it and waits for healthy rollouts; a dependency scan checks for known vulnerabilities.")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">\n'
            f"<title>{esc(title)}</title>\n" + "\n".join(body) + f"\n{style(t, anim)}\n</svg>\n")


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "app-delivery"
    out.mkdir(parents=True, exist_ok=True)
    for theme, t in THEMES.items():
        (out / f"{theme}.svg").write_text(wide(t), encoding="utf-8", newline="\n")
        (out / f"{theme}-narrow.svg").write_text(narrow(t), encoding="utf-8", newline="\n")
    print("written to", out)
