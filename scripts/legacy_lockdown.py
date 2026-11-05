"""Renders assets/legacy-lockdown/*.svg: closing direct access to the origin, step by step, with no downtime.

python scripts/legacy_lockdown.py
"""
from pathlib import Path

import app_delivery as ad
from app_delivery import Anim, node, style
from pipeline import FONT, SLOW, THEMES, esc

ad.HOLD = 12.6
ad.CYCLE = 13.4

STEPS = [  # (title, subtitle, time it is done)
    ("Report only", "log, refuse nothing", 1.6),
    ("Secret header", "CDN to origin", 3.1),
    ("Client IP", "set by the edge", 4.6),
    ("DNS", "apex, wildcard to CDN", 6.1),
    ("Refuse the rest", "403 without the secret", 7.6),
    ("Firewall", "CDN and uptime checks", 9.1),
]
RED = {"light": "#cf222e", "dark": "#f85149"}


def pct(t):
    return f"{t / ad.CYCLE * 100:.2f}%"


def extra(t, theme):
    red = RED[theme]
    blocked = STEPS[-1][2]
    refused = STEPS[-2][2]
    return f"""<style>
  text {{ font-family: {FONT}; }}
  .box {{ fill: {t['fill']}; stroke: {t['stroke']}; stroke-width: 1.5; }}
  .box-title {{ font-size: 14px; font-weight: 600; fill: {t['text']}; }}
  .box-sub {{ font-size: 12px; fill: {t['muted']}; }}
  .good {{ fill: none; stroke: {t['accent']}; stroke-width: 2.5; stroke-dasharray: 7 6; animation: flow {1.1 * SLOW:.2f}s linear infinite; }}
  .bad {{ fill: none; stroke: {red}; stroke-width: 2.5; stroke-dasharray: 7 6;
          animation: flow {1.1 * SLOW:.2f}s linear infinite, cut {ad.CYCLE * SLOW:.2f}s linear infinite; }}
  .bad-text {{ font-size: 12px; font-weight: 600; fill: {red}; }}
  .tag {{ font-size: 11px; fill: {t['accent']}; font-weight: 600; }}
  .refused {{ animation: refused {ad.CYCLE * SLOW:.2f}s linear infinite; }}
  .cross {{ stroke: {red}; stroke-width: 3; stroke-linecap: round; animation: cross {ad.CYCLE * SLOW:.2f}s linear infinite; }}
  .uptime {{ fill: {t['fill']}; stroke: {t['accent']}; stroke-width: 1.5; }}
  .uptime-text {{ font-size: 12px; font-weight: 600; fill: {t['text']}; }}
  .dot {{ fill: {t['accent']}; animation: beat {1.4 * SLOW:.2f}s ease-in-out infinite; }}
  @keyframes flow {{ to {{ stroke-dashoffset: -26 }} }}
  @keyframes beat {{ 0%, 100% {{ opacity: 1 }} 50% {{ opacity: .35 }} }}
  @keyframes cut {{ 0%, {pct(blocked - 0.05)} {{ opacity: 1 }} {pct(blocked + 0.3)}, {pct(ad.HOLD)} {{ opacity: .12 }}
                   {pct(ad.HOLD + 0.4)}, 100% {{ opacity: 1 }} }}
  @keyframes refused {{ 0%, {pct(refused - 0.05)} {{ opacity: 0 }} {pct(refused + 0.1)}, {pct(blocked)} {{ opacity: 1 }}
                       {pct(blocked + 0.3)}, 100% {{ opacity: 0 }} }}
  @keyframes cross {{ 0%, {pct(blocked - 0.05)} {{ opacity: 0 }} {pct(blocked + 0.1)}, {pct(ad.HOLD)} {{ opacity: 1 }}
                     {pct(ad.HOLD + 0.4)}, 100% {{ opacity: 0 }} }}
  @media (prefers-reduced-motion: reduce) {{
    .good, .bad, .dot {{ animation: none !important; }} .bad {{ opacity: .12 !important; }}
    .refused {{ animation: none !important; opacity: 0 !important; }} .cross {{ animation: none !important; opacity: 1 !important; }} }}
</style>"""


def box(x, y, w, h, title, sub):
    return (f'<rect class="box" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>'
            f'<text class="box-title" x="{x + 14}" y="{y + 24}">{esc(title)}</text>'
            f'<text class="box-sub" x="{x + 14}" y="{y + 42}">{esc(sub)}</text>')


def tag(anim, x, y, text, at, anchor="middle"):
    return f'<text class="tag {anim.show(at)}" x="{x}" y="{y}" text-anchor="{anchor}">{esc(text)}</text>'


def uptime(x, y):
    return (f'<rect class="uptime" x="{x}" y="{y}" width="138" height="30" rx="15"/>'
            f'<circle class="dot" cx="{x + 18}" cy="{y + 15}" r="5"/>'
            f'<text class="uptime-text" x="{x + 32}" y="{y + 19}">Uptime 100%</text>')


def wide(t, theme):
    W = 1000
    anim, out = Anim(), []
    out.append(box(20, 26, 190, 54, "Visitors", "through the CDN"))
    out.append(box(20, 120, 190, 54, "Direct hits", "bots, scanners, old DNS"))
    out.append(box(400, 26, 170, 54, "CDN", "edge, shielding"))
    out.append(box(770, 70, 190, 60, "Origin", "web servers"))
    out.append(uptime(822, 156))
    out.append('<path class="good" d="M 210 53 L 400 53"/>')
    out.append('<path class="good" d="M 570 53 C 660 53, 680 92, 770 92"/>')
    out.append('<path class="bad" d="M 210 147 C 470 147, 560 112, 770 112"/>')
    out.append(f'<text class="bad-text refused" x="700" y="146" text-anchor="middle">403</text>')
    out.append(f'<g class="cross"><line x1="470" y1="129" x2="490" y2="149"/><line x1="490" y1="129" x2="470" y2="149"/></g>')
    out.append(tag(anim, 655, 30, "secret header", STEPS[1][2]))
    out.append(tag(anim, 655, 44, "real client IP", STEPS[2][2]))
    out.append(tag(anim, 305, 44, "DNS points here", STEPS[3][2]))
    out.append(tag(anim, 865, 60, "logging who would be refused", STEPS[0][2]))
    # the checklist
    y, xs = 240, [70 + i * 172 for i in range(len(STEPS))]
    for i, ((title, sub, done), x) in enumerate(zip(STEPS, xs)):
        if i:
            out.append(f'<line class="wire" x1="{xs[i - 1] + 12}" y1="{y}" x2="{x - 12}" y2="{y}"/>'
                       f'<line class="wire-on {anim.show(STEPS[i - 1][2] + 0.05)}" x1="{xs[i - 1] + 12}" y1="{y}" x2="{x - 12}" y2="{y}"/>')
        out.append(node(anim, x, y, done))
        out.append(f'<text class="title" x="{x}" y="{y + 32}" text-anchor="middle">{i + 1}. {esc(title)}</text>'
                   f'<text class="sub" x="{x}" y="{y + 49}" text-anchor="middle">{esc(sub)}</text>')
    return svg(W, 304, t, theme, anim, out)


def narrow(t, theme):
    W = 400
    anim, out = Anim(), []
    out.append(box(12, 12, 176, 54, "Visitors", "through the CDN"))
    out.append(box(212, 12, 176, 54, "Direct hits", "bots, scanners"))
    out.append(box(12, 118, 176, 54, "CDN", "edge, shielding"))
    out.append(box(112, 226, 176, 58, "Origin", "web servers"))
    out.append('<path class="good" d="M 100 66 L 100 118"/>')
    out.append('<path class="good" d="M 100 172 C 100 200, 170 200, 170 226"/>')
    out.append('<path class="bad" d="M 300 66 C 300 150, 240 180, 240 226"/>')
    out.append(f'<text class="bad-text refused" x="300" y="200" text-anchor="middle">403</text>')
    out.append(f'<g class="cross"><line x1="282" y1="126" x2="302" y2="146"/><line x1="302" y1="126" x2="282" y2="146"/></g>')
    out.append(tag(anim, 196, 205, "secret header", STEPS[1][2], anchor="end"))
    out.append(uptime(12, 296))
    y0 = 360
    ys = [y0 + i * 44 for i in range(len(STEPS))]
    for i, ((title, sub, done), y) in enumerate(zip(STEPS, ys)):
        if i:
            out.append(f'<line class="wire" x1="28" y1="{ys[i - 1] + 12}" x2="28" y2="{y - 12}"/>'
                       f'<line class="wire-on {anim.show(STEPS[i - 1][2] + 0.05)}" x1="28" y1="{ys[i - 1] + 12}" x2="28" y2="{y - 12}"/>')
        out.append(node(anim, 28, y, done, r=9))
        out.append(f'<text class="title" x="48" y="{y - 2}">{i + 1}. {esc(title)}</text>'
                   f'<text class="sub" x="48" y="{y + 14}">{esc(sub)}</text>')
    return svg(W, ys[-1] + 30, t, theme, anim, out)


def svg(w, h, t, theme, anim, body):
    title = ("Visitors reach the origin through the CDN, while bots and scanners hit it directly. Six steps close the "
             "direct path: report-only logging, a secret header from the CDN, the client IP set by the edge, DNS moved to "
             "the CDN, 403 for anything without the secret, and a cloud firewall that lets in only the CDN and uptime "
             "checks. Uptime stays at 100% the whole time.")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">\n'
            f"<title>{esc(title)}</title>\n" + "\n".join(body) + f"\n{style(t, anim)}\n{extra(t, theme)}\n</svg>\n")


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "legacy-lockdown"
    out.mkdir(parents=True, exist_ok=True)
    for theme, t in THEMES.items():
        (out / f"{theme}.svg").write_text(wide(t, theme), encoding="utf-8", newline="\n")
        (out / f"{theme}-narrow.svg").write_text(narrow(t, theme), encoding="utf-8", newline="\n")
    print("written to", out)
