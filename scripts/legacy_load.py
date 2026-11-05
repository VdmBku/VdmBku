"""Renders assets/legacy-load/*.svg: server load before and after the cache for the image resize endpoint.

The curve is illustrative; the before and after values (~85, 2 to 7) are the ones from the incident.

python scripts/legacy_load.py
"""
import math
import random
from pathlib import Path

from pipeline import FONT, SLOW, THEMES, esc

RED = {"light": "#cf222e", "dark": "#f85149"}
CYCLE, DRAW, HOLD = 11.0, 6.0, 9.6
N, DROP = 64, 36            # points, index where the cache goes live


def series():
    rnd = random.Random(7)
    out = []
    for i in range(N):
        if i < DROP:
            base = 62 + 18 * math.sin(i / 4.0) + rnd.uniform(-8, 8)
            out.append(min(85.0, max(48.0, base)) if i != 27 else 85.0)
        else:
            out.append(rnd.uniform(2.0, 7.0))
    return out


def pct(t):
    return f"{t / CYCLE * 100:.2f}%"


def poly(points):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def length(points):
    return sum(math.dist(a, b) for a, b in zip(points, points[1:]))


def chart(t, theme, W, H, x0, x1, y0, y1, big=True):
    red = RED[theme]
    vals = series()
    sx = lambda i: x0 + (x1 - x0) * i / (N - 1)
    sy = lambda v: y1 - (y1 - y0) * v / 90
    before = [(sx(i), sy(v)) for i, v in enumerate(vals[:DROP + 1])]
    after = [(sx(i), sy(v)) for i, v in enumerate(vals) if i >= DROP]
    lb, la = length(before), length(after)
    t_split = DRAW * lb / (lb + la)
    cx = sx(DROP)
    out = []
    for v in (0, 25, 50, 75):
        out.append(f'<line class="grid" x1="{x0}" y1="{sy(v):.1f}" x2="{x1}" y2="{sy(v):.1f}"/>'
                   f'<text class="axis" x="{x0 - 8}" y="{sy(v) + 4:.1f}" text-anchor="end">{v}</text>')
    out.append(f'<text class="axis" x="{x0}" y="{y0 - 12}">server load</text>')
    out.append(f'<polyline class="before" points="{poly(before)}" stroke-dasharray="{lb:.0f}"/>'
               f'<polyline class="after" points="{poly(after)}" stroke-dasharray="{la:.0f}"/>')
    out.append(f'<g class="mark"><line class="marker" x1="{cx:.1f}" y1="{y0 - 4}" x2="{cx:.1f}" y2="{y1}"/>'
               f'<text class="note" x="{cx + 10:.1f}" y="{y0 + 12}">{"cache for the resize endpoint" if big else "cache on"}</text>'
               f'<text class="note-sub" x="{cx + 10:.1f}" y="{y0 + 29}">{"repeat request " if big else ""}0.57 s to 0.0005 s</text></g>')
    peak = max(range(DROP), key=lambda i: vals[i])
    out.append(f'<text class="value-bad before-label" x="{sx(peak):.1f}" y="{sy(vals[peak]) - 10:.1f}" text-anchor="middle">~85</text>')
    out.append(f'<text class="value-good after-label" x="{x1:.1f}" y="{sy(7) - 12:.1f}" text-anchor="end">2 to 7</text>')
    out.append(f'<text class="foot" x="{x1}" y="{H - 6}" text-anchor="end">Illustrative curve. The before and after values are from the incident.</text>')
    css = f"""<style>
  text {{ font-family: {FONT}; }}
  .grid {{ stroke: {t['stroke']}; stroke-width: 1; opacity: .6; }}
  .axis {{ font-size: {12 if big else 11}px; fill: {t['muted']}; }}
  .before {{ fill: none; stroke: {red}; stroke-width: 2.5; stroke-linejoin: round;
             animation: db {CYCLE * SLOW:.2f}s linear infinite; }}
  .after {{ fill: none; stroke: {t['accent']}; stroke-width: 2.5; stroke-linejoin: round;
            animation: da {CYCLE * SLOW:.2f}s linear infinite; }}
  .marker {{ stroke: {t['accent']}; stroke-width: 1.5; stroke-dasharray: 4 4; }}
  .note {{ font-size: {13 if big else 12}px; font-weight: 600; fill: {t['text']}; }}
  .note-sub {{ font-size: {12 if big else 11}px; fill: {t['muted']}; }}
  .value-bad {{ font-size: 13px; font-weight: 600; fill: {red}; }}
  .value-good {{ font-size: 13px; font-weight: 600; fill: {t['accent']}; }}
  .foot {{ font-size: {11 if big else 10}px; fill: {t['muted']}; }}
  .mark {{ animation: show {CYCLE * SLOW:.2f}s linear infinite; }}
  .before-label {{ animation: peak {CYCLE * SLOW:.2f}s linear infinite; }}
  .after-label {{ animation: low {CYCLE * SLOW:.2f}s linear infinite; }}
  @keyframes db {{ 0% {{ stroke-dashoffset: {lb:.0f} }} {pct(t_split)}, {pct(HOLD)} {{ stroke-dashoffset: 0 }}
                  {pct(HOLD + 0.4)}, 100% {{ stroke-dashoffset: {lb:.0f} }} }}
  @keyframes da {{ 0%, {pct(t_split)} {{ stroke-dashoffset: {la:.0f} }} {pct(DRAW)}, {pct(HOLD)} {{ stroke-dashoffset: 0 }}
                  {pct(HOLD + 0.4)}, 100% {{ stroke-dashoffset: {la:.0f} }} }}
  @keyframes show {{ 0%, {pct(t_split - 0.05)} {{ opacity: 0 }} {pct(t_split + 0.2)}, {pct(HOLD)} {{ opacity: 1 }} {pct(HOLD + 0.4)}, 100% {{ opacity: 0 }} }}
  @keyframes peak {{ 0%, {pct(t_split * 0.75)} {{ opacity: 0 }} {pct(t_split * 0.75 + 0.2)}, {pct(HOLD)} {{ opacity: 1 }} {pct(HOLD + 0.4)}, 100% {{ opacity: 0 }} }}
  @keyframes low {{ 0%, {pct(DRAW - 0.1)} {{ opacity: 0 }} {pct(DRAW + 0.2)}, {pct(HOLD)} {{ opacity: 1 }} {pct(HOLD + 0.4)}, 100% {{ opacity: 0 }} }}
  @media (prefers-reduced-motion: reduce) {{
    .before, .after, .mark, .before-label, .after-label {{ animation: none !important; stroke-dashoffset: 0 !important; opacity: 1 !important; }} }}
</style>"""
    title = ("Server load during the bot incident: around 85 before the cache for the image resize endpoint, "
             "2 to 7 after it. A repeat request went from 0.57 s to 0.0005 s.")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">\n'
            f"<title>{esc(title)}</title>\n{css}\n" + "\n".join(out) + "\n</svg>\n")


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "legacy-load"
    out.mkdir(parents=True, exist_ok=True)
    for theme, t in THEMES.items():
        (out / f"{theme}.svg").write_text(chart(t, theme, 1000, 230, 60, 980, 40, 190), encoding="utf-8", newline="\n")
        (out / f"{theme}-narrow.svg").write_text(chart(t, theme, 400, 250, 34, 390, 70, 210, big=False),
                                                encoding="utf-8", newline="\n")
    print("written to", out)
