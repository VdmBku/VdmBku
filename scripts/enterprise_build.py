"""Renders assets/enterprise-build/*.svg: release build, dependency audit and the antivirus service image.

python scripts/enterprise_build.py
"""
from pathlib import Path

import app_delivery as ad
from app_delivery import Anim, node, style
from media_gitops import tiles, wire
from pipeline import THEMES, esc

ad.HOLD = 11.0
ad.CYCLE = 11.8

# (kind, title, subtitle, start, done); kind is "node" or an int n for a row of n tiles
TRACKS = [
    ("Release build", "one pipeline", [
        ("node", "Checkout", "release tag", 0.3, 0.7),
        (3, "Web bundles", "3 front-ends", 0.8, 1.8),
        ("node", "Server tests", "cached per commit", 1.9, 2.6),
        ("node", "Server JAR", "bundles inside", 2.7, 3.1),
        ("node", "Image", "Docker", 3.2, 3.6),
        ("node", "Deploy", "Ansible, picked target", 3.7, 4.2),
    ]),
    ("Dependency audit", "front-end packages", [
        (4, "4 front-ends", "npm audit each", 4.6, 6.2),
        ("node", "Gate", "fails on high severity", 6.3, 6.7),
        ("node", "Reports", "archived", 6.8, 7.1),
    ]),
    ("Antivirus service", "its own image", [
        ("node", "Keep previous", "rollback tag", 7.5, 7.9),
        ("node", "Build", "ClamAV image", 8.0, 8.4),
        ("node", "Push", "registry", 8.5, 8.8),
        ("node", "Deploy", "Ansible", 8.9, 9.3),
    ]),
]
SIZE, GAP = 22, 8


def width(kind):
    return 0 if kind == "node" else kind * (SIZE + GAP) - GAP


def wide(t):
    W = 1000
    anim, out = Anim(), []
    y, dividers = 52, []
    for title, sub, items in TRACKS:
        out.append(f'<text class="track-title" x="12" y="{y - 2}">{esc(title)}</text>'
                   f'<text class="track-sub" x="12" y="{y + 15}">{esc(sub)}</text>')
        label_y = y + 33
        x, spans = 200, []
        for kind, *_ in items:
            spans.append((x, x + width(kind), kind))
            x += width(kind) + 124
        for (a1, b1, k1), (a2, b2, k2), (_k, _t, _s, _st, d1) in zip(spans, spans[1:], items):
            a = b1 + (12 if k1 == "node" else 8)
            b = a2 - (12 if k2 == "node" else 8)
            out.append(wire(anim, f"M {a} {y} L {b} {y}", d1 + 0.05))
        for (xa, xb, kind), (_k, it, isub, start, done) in zip(spans, items):
            cx = (xa + xb) / 2
            out.append(node(anim, xa, y, done) if kind == "node"
                       else tiles(anim, xa, y - SIZE / 2, kind, start, done, size=SIZE, gap=GAP))
            out.append(f'<text class="title" x="{cx}" y="{label_y}" text-anchor="middle">{esc(it)}</text>'
                       f'<text class="sub" x="{cx}" y="{label_y + 17}" text-anchor="middle">{esc(isub)}</text>')
        dividers.append(label_y + 35)
        y = label_y + 35 + 40
    for d in dividers[:-1]:
        out.append(f'<line class="divider" x1="12" y1="{d}" x2="{W - 12}" y2="{d}"/>')
    return svg(W, dividers[-1], t, anim, out)


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
        for (_k, _t, _s, _st, d1), y1, y2 in zip(items, ys, ys[1:]):
            out.append(wire(anim, f"M 28 {y1 + 12} L 28 {y2 - 12}", d1 + 0.05))
        for (kind, it, isub, start, done), yy in zip(items, ys):
            out.append(node(anim, 28, yy, done, r=9))
            out.append(f'<text class="title" x="48" y="{yy - 2}">{esc(it)}</text>'
                       f'<text class="sub" x="48" y="{yy + 14}">{esc(isub)}</text>')
            if kind != "node":
                out.append(tiles(anim, 250, yy - 8, kind, start, done, size=16, gap=6))
        y = ys[-1] + 44
    return svg(W, y - 14, t, anim, out)


def svg(w, h, t, anim, body):
    title = ("Release build: checkout, three web front-ends, server tests cached per commit, server JAR with the "
             "bundles inside, Docker image, deploy with Ansible. Dependency audit: npm audit on four front-ends, a gate "
             "that fails on high severity, archived reports. Antivirus service: keep the previous image for rollback, "
             "build the ClamAV image, push, deploy with Ansible.")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">\n'
            f"<title>{esc(title)}</title>\n" + "\n".join(body) + f"\n{style(t, anim)}\n</svg>\n")


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "enterprise-build"
    out.mkdir(parents=True, exist_ok=True)
    for theme, t in THEMES.items():
        (out / f"{theme}.svg").write_text(wide(t), encoding="utf-8", newline="\n")
        (out / f"{theme}-narrow.svg").write_text(narrow(t), encoding="utf-8", newline="\n")
    print("written to", out)
