"""Renders assets/edtech-release/*.svg: a release goes to a cloud stage first, then to about 20 client servers.

python scripts/edtech_release.py
"""
from pathlib import Path

from app_delivery import Anim, grid, node, style
from pipeline import THEMES, esc

# (kind, title, subtitle, start, done)
STEPS = [
    ("node", "Pick versions", "components, toggles", 0.3, 0.8),
    ("node", "Dry run", "validate first", 0.9, 1.4),
    ("node", "Cloud stage", "Terraform, Ansible", 1.5, 2.4),
    ("node", "Stage OK", "checked", 2.5, 2.9),
    ("grid", "Client servers", "about 20, on-prem", 3.0, 7.0),
    ("node", "Done", "all clients updated", 7.1, 7.5),
]

import app_delivery as ad  # noqa: E402  (shared timing knobs)

ad.HOLD = 9.0
ad.CYCLE = 9.8
ad.PICKED = set(range(20))     # every client server gets the release


def wide(t):
    W, y = 1000, 40
    anim, out = Anim(), []
    xs, x = [], 70
    for kind, *_ in STEPS:
        xs.append(x)
        x += 140 if kind == "node" else 185 + 120
    label_y = y + 17 + 22
    for (k1, *_a, d1), x1, (k2, *_b), x2 in zip(STEPS, xs, STEPS[1:], xs[1:]):
        a = x1 + (12 if k1 == "node" else 185 + 8)
        b = x2 - (12 if k2 == "node" else 8)
        out.append(f'<line class="wire" x1="{a}" y1="{y}" x2="{b}" y2="{y}"/>'
                   f'<line class="wire-on {anim.show(d1 + 0.05)}" x1="{a}" y1="{y}" x2="{b}" y2="{y}"/>')
    for (kind, title, sub, start, done), x in zip(STEPS, xs):
        cx = x if kind == "node" else x + 185 / 2
        out.append(node(anim, x, y, done) if kind == "node" else grid(anim, x, y, start, done))
        out.append(f'<text class="title" x="{cx}" y="{label_y}" text-anchor="middle">{esc(title)}</text>'
                   f'<text class="sub" x="{cx}" y="{label_y + 17}" text-anchor="middle">{esc(sub)}</text>')
    return svg(W, label_y + 30, t, anim, out)


def narrow(t):
    W, row = 400, 46
    anim, out = Anim(), []
    ys = [24 + i * row for i in range(len(STEPS))]
    for (k1, *_a, d1), y1, y2 in zip(STEPS, ys, ys[1:]):
        out.append(f'<line class="wire" x1="28" y1="{y1 + 12}" x2="28" y2="{y2 - 12}"/>'
                   f'<line class="wire-on {anim.show(d1 + 0.05)}" x1="28" y1="{y1 + 12}" x2="28" y2="{y2 - 12}"/>')
    for (kind, title, sub, start, done), y in zip(STEPS, ys):
        out.append(node(anim, 28, y, done, r=9))
        out.append(f'<text class="title" x="48" y="{y - 2}">{esc(title)}</text>'
                   f'<text class="sub" x="48" y="{y + 14}">{esc(sub)}</text>')
        if kind == "grid":
            out.append(grid(anim, 200, y, start, done, size=14, gap=5))
    return svg(W, ys[-1] + 30, t, anim, out)


def svg(w, h, t, anim, body):
    title = ("A release: pick component versions, dry run, deploy to a cloud stage with Terraform and Ansible, check it, "
             "then roll the same release out to about 20 client servers on-prem.")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">\n'
            f"<title>{esc(title)}</title>\n" + "\n".join(body) + f"\n{style(t, anim)}\n</svg>\n")


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "edtech-release"
    out.mkdir(parents=True, exist_ok=True)
    for theme, t in THEMES.items():
        (out / f"{theme}.svg").write_text(wide(t), encoding="utf-8", newline="\n")
        (out / f"{theme}-narrow.svg").write_text(narrow(t), encoding="utf-8", newline="\n")
    print("written to", out)
