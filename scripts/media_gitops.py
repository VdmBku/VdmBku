"""Renders assets/media-gitops/*.svg: build-only CI, a promoted release tag pinned in Git, Argo CD syncing the cluster.

python scripts/media_gitops.py
"""
from pathlib import Path

import app_delivery as ad
from app_delivery import Anim, node, style
from pipeline import THEMES, esc

ad.HOLD = 11.5
ad.CYCLE = 12.4

SERVICES = 10
GROUPS = [("Platform", 5, 4.6, 5.6), ("Stateful", 3, 5.7, 6.4), ("Services", SERVICES, 6.5, 8.5)]
BUILD = (0.3, 2.3)
STEPS = [  # (title, subtitle, done)
    ("Dev registry", "every build", 2.5),
    ("Promote", "to prod registry", 3.0),
    ("Git", "tag pinned", 3.6),
    ("Argo CD", "app of apps", 4.2),
]
SYNCED = 8.7


def tiles(anim, x, y, n, start, end, size, gap, cols=None):
    cols = cols or n
    step = (end - start) / n
    out = []
    for i in range(n):
        r, c = divmod(i, cols)
        xx, yy = x + c * (size + gap), y + r * (size + gap)
        out.append(f'<rect class="svc" x="{xx}" y="{yy}" width="{size}" height="{size}" rx="4"/>'
                   f'<rect class="svc-on {anim.show(start + step * (i + 1))}" x="{xx}" y="{yy}" width="{size}" height="{size}" rx="4"/>')
    return "".join(out)


def wire(anim, d, lit):
    return f'<path class="wire" d="{d}" fill="none"/><path class="wire-on {anim.show(lit)}" d="{d}" fill="none"/>'


def extra_style(t):
    return f"""<style>
  .frame {{ fill: none; stroke: {t['stroke']}; stroke-width: 1.5; stroke-dasharray: 6 5; }}
  .frame-title {{ font-size: 13px; font-weight: 600; fill: {t['text']}; }}
  .group {{ font-size: 12px; font-weight: 600; fill: {t['text']}; }}
  .count {{ font-size: 12px; fill: {t['muted']}; }}
  .chip {{ fill: {t['fill']}; stroke: {t['accent']}; stroke-width: 1.5; }}
  .chip-text {{ font-size: 13px; font-weight: 600; fill: {t['text']}; }}
</style>"""


def wide(t):
    W, y = 1000, 112
    anim, out = Anim(), []
    # build: one tile per service, built on every branch
    out.append(f'<text class="title" x="20" y="44">Every branch</text><text class="sub" x="20" y="61">build only, no deploy</text>')
    out.append(tiles(anim, 20, 84, SERVICES, *BUILD, size=22, gap=8, cols=5))
    out.append(f'<text class="title" x="91" y="{y + 52}" text-anchor="middle">{SERVICES} services</text>'
               f'<text class="sub" x="91" y="{y + 69}" text-anchor="middle">images per branch</text>')
    xs = [232, 334, 436, 538]
    out.append(wire(anim, f"M 170 {y} L {xs[0] - 12} {y}", BUILD[1] + 0.05))
    for (title, sub, done), x, nxt in zip(STEPS, xs, xs[1:] + [None]):
        out.append(node(anim, x, y, done))
        out.append(f'<text class="title" x="{x}" y="{y + 32}" text-anchor="middle">{esc(title)}</text>'
                   f'<text class="sub" x="{x}" y="{y + 49}" text-anchor="middle">{esc(sub)}</text>')
        if nxt:
            out.append(wire(anim, f"M {x + 12} {y} L {nxt - 12} {y}", done + 0.05))
    # cluster frame with the three ApplicationSets
    fx, fy, fw, fh = 600, 26, 388, 176
    out.append(f'<rect class="frame" x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="12"/>'
               f'<text class="frame-title" x="{fx + 14}" y="{fy + 22}">GKE Autopilot</text>'
               f'<text class="count" x="{fx + fw - 14}" y="{fy + 22}" text-anchor="end">staging, production</text>')
    gys = [76, 116, 156]
    for (name, n, start, end), gy in zip(GROUPS, gys):
        out.append(wire(anim, f"M {xs[-1] + 12} {y} C {xs[-1] + 40} {y}, {fx - 10} {gy}, {fx + 12} {gy}", STEPS[-1][2] + 0.05))
        out.append(f'<text class="group" x="{fx + 20}" y="{gy + 4}">{name}</text>'
                   f'<text class="count" x="{fx + 92}" y="{gy + 4}">{n}</text>')
        out.append(tiles(anim, fx + 118, gy - 9, n, start, end, size=18, gap=7))
    on = anim.show(SYNCED)
    out.append(f'<g class="{on}"><rect class="chip" x="{fx + fw - 128}" y="{fy + fh + 12}" width="128" height="30" rx="15"/>'
               f'<text class="chip-text" x="{fx + fw - 64}" y="{fy + fh + 32}" text-anchor="middle">In sync</text></g>')
    return svg(W, fy + fh + 50, t, anim, out)


def narrow(t):
    W, row = 400, 48
    anim, out = Anim(), []
    items = [("Every branch", f"{SERVICES} services, build only", BUILD[1], "build")] + \
            [(a, b, d, "node") for a, b, d in STEPS] + \
            [(name, f"{n} in Argo CD", end, ("group", n, start, end)) for name, n, start, end in GROUPS] + \
            [("In sync", "GKE Autopilot, staging", SYNCED, "node")]
    ys = [24 + i * row for i in range(len(items))]
    for (_a, _b, d1, _k), y1, y2 in zip(items, ys, ys[1:]):
        out.append(wire(anim, f"M 28 {y1 + 12} L 28 {y2 - 12}", d1 + 0.05))
    for (title, sub, done, kind), y in zip(items, ys):
        out.append(node(anim, 28, y, done, r=9))
        out.append(f'<text class="title" x="48" y="{y - 2}">{esc(title)}</text>'
                   f'<text class="sub" x="48" y="{y + 14}">{esc(sub)}</text>')
        if kind == "build":
            out.append(tiles(anim, 230, y - 15, SERVICES, *BUILD, size=13, gap=4, cols=5))
        elif isinstance(kind, tuple):
            _, n, start, end = kind
            cols = 5
            out.append(tiles(anim, 230, y - (7 if n <= cols else 15), n, start, end, size=13, gap=4, cols=cols))
    return svg(W, ys[-1] + 30, t, anim, out)


def svg(w, h, t, anim, body):
    title = ("Every branch of ten services is built into images, with no deploy from CI. A release tag is promoted to the "
             "production registry and pinned in Git. Argo CD, as an app of apps, syncs platform components, stateful "
             "services and the ten services into GKE Autopilot.")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">\n'
            f"<title>{esc(title)}</title>\n" + "\n".join(body) + f"\n{style(t, anim)}\n{extra_style(t)}\n</svg>\n")


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "media-gitops"
    out.mkdir(parents=True, exist_ok=True)
    for theme, t in THEMES.items():
        (out / f"{theme}.svg").write_text(wide(t), encoding="utf-8", newline="\n")
        (out / f"{theme}-narrow.svg").write_text(narrow(t), encoding="utf-8", newline="\n")
    print("written to", out)
