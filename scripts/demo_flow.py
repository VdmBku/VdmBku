"""Renders assets/demo-flow/*.svg: from the "Request a demo" button to a running environment.

python scripts/demo_flow.py
"""
from pathlib import Path

from pipeline import FONT, THEMES, esc

BUTTON = "Request a demo"
STEPS = [
    ("Approve", "manual check"),
    ("Pipeline", "one job"),
    ("Server + DNS", "per customer"),
    ("Hardening", "security baseline"),
    ("Proxy + TLS", "auto certificates"),
    ("6 services", "built, deployed"),
    ("Ready", "access sent"),
]

CYCLE = 10.0  # seconds
PRESS = 0.7   # button click
STEP = 1.0    # per step
HOLD = 9.3    # everything stays done until here, then resets


def pct(t):
    return f"{t / CYCLE * 100:.2f}%"


def style(t):
    css = [f"""
  text {{ font-family: {FONT}; }}
  .btn {{ fill: {t['accent']}; transform-box: fill-box; transform-origin: center;
          animation: press {CYCLE}s ease-in-out infinite; }}
  .btn-text {{ font-size: 14px; font-weight: 600; fill: #ffffff; pointer-events: none; }}
  .ripple {{ fill: none; stroke: {t['accent']}; stroke-width: 2; opacity: 0; transform-box: fill-box;
             transform-origin: center; animation: ripple {CYCLE}s ease-out infinite; }}
  .track {{ stroke: {t['stroke']}; stroke-width: 3; fill: none; stroke-linecap: round; }}
  .fill {{ stroke: {t['accent']}; stroke-width: 3; fill: none; stroke-linecap: round;
           animation: fill {CYCLE}s linear infinite; }}
  .node {{ fill: {t['fill']}; stroke: {t['stroke']}; stroke-width: 2; }}
  .done {{ fill: {t['accent']}; opacity: 0; }}
  .tick {{ fill: none; stroke: #ffffff; stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; opacity: 0; }}
  .title {{ font-size: 13px; font-weight: 600; fill: {t['text']}; }}
  .sub {{ font-size: 12px; fill: {t['muted']}; }}
  .glow {{ fill: none; stroke: {t['accent']}; stroke-width: 2; opacity: 0; transform-box: fill-box;
           transform-origin: center; animation: glow {CYCLE}s ease-out infinite; }}
  @keyframes press {{ 0% {{ transform: scale(1) }} {pct(0.25)} {{ transform: scale(.93) }}
                      {pct(0.5)} {{ transform: scale(1) }} 100% {{ transform: scale(1) }} }}
  @keyframes ripple {{ 0% {{ opacity: 0; transform: scale(1) }} {pct(0.25)} {{ opacity: .8; transform: scale(1) }}
                       {pct(1.1)} {{ opacity: 0; transform: scale(1.25, 1.6) }} 100% {{ opacity: 0 }} }}
  @keyframes glow {{ 0%, {pct(PRESS + STEP * len(STEPS))} {{ opacity: 0; transform: scale(1) }}
                     {pct(PRESS + STEP * len(STEPS) + 0.1)} {{ opacity: .9; transform: scale(1) }}
                     {pct(PRESS + STEP * len(STEPS) + 1.2)} {{ opacity: 0; transform: scale(2.2) }} 100% {{ opacity: 0 }} }}
  @media (prefers-reduced-motion: reduce) {{
    .btn, .ripple, .fill, .done, .tick, .glow {{ animation: none !important; }}
    .fill {{ stroke-dashoffset: 0 !important; }} .done, .tick {{ opacity: 1 !important; }} }}
"""]
    for i in range(len(STEPS)):
        on = PRESS + STEP * (i + 1)
        css.append(f"  .s{i} {{ animation: s{i} {CYCLE}s linear infinite; }}\n"
                   f"  @keyframes s{i} {{ 0%, {pct(on - 0.05)} {{ opacity: 0 }} {pct(on + 0.15)}, {pct(HOLD)} {{ opacity: 1 }} "
                   f"{pct(HOLD + 0.4)}, 100% {{ opacity: 0 }} }}\n")
    return "<style>" + "".join(css) + "</style>"


def fill_keyframes(length):
    # progress line grows step by step, waits at each node
    frames = [f"0%, {pct(PRESS)} {{ stroke-dashoffset: {length} }}"]
    seg = length / len(STEPS)
    for i in range(len(STEPS)):
        reach = PRESS + STEP * (i + 1)
        frames.append(f"{pct(reach - 0.35)} {{ stroke-dashoffset: {length - seg * i:.1f} }}")
        frames.append(f"{pct(reach)} {{ stroke-dashoffset: {length - seg * (i + 1):.1f} }}")
    frames.append(f"{pct(HOLD)} {{ stroke-dashoffset: 0 }}")
    frames.append(f"{pct(HOLD + 0.4)}, 100% {{ stroke-dashoffset: {length} }}")
    return f"<style>@keyframes fill {{ {' '.join(frames)} }}</style>"


def node(i, x, y):
    tick = f"M {x - 4.5} {y + 0.5} l 3 3 l 6 -6.5"
    return (f'<circle class="node" cx="{x}" cy="{y}" r="10"/>'
            f'<circle class="done s{i}" cx="{x}" cy="{y}" r="10"/>'
            f'<path class="tick s{i}" d="{tick}"/>')


def button(x, y, w, h):
    return (f'<rect class="ripple" x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}"/>'
            f'<rect class="btn" x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}"/>'
            f'<text class="btn-text" x="{x + w / 2}" y="{y + h / 2 + 5}" text-anchor="middle">{esc(BUTTON)}</text>')


def wide(t):
    W, H, cy = 1000, 150, 50
    bx, bw, bh = 12, 150, 40
    first, gap = 222, 124
    xs = [first + i * gap for i in range(len(STEPS))]
    start, end = bx + bw + 14, xs[-1]
    length = end - start
    out = [button(bx, cy - bh / 2, bw, bh),
           f'<line class="track" x1="{start}" y1="{cy}" x2="{end}" y2="{cy}"/>',
           f'<line class="fill" x1="{start}" y1="{cy}" x2="{end}" y2="{cy}" stroke-dasharray="{length}"/>',
           f'<circle class="glow" cx="{xs[-1]}" cy="{cy}" r="10"/>']
    for i, (title, sub) in enumerate(STEPS):
        x = xs[i]
        out.append(node(i, x, cy))
        out.append(f'<text class="title" x="{x}" y="{cy + 36}" text-anchor="middle">{esc(title)}</text>')
        out.append(f'<text class="sub" x="{x}" y="{cy + 55}" text-anchor="middle">{esc(sub)}</text>')
    return svg(W, H, t, out, fill_keyframes(length))


def narrow(t):
    W = 400
    bx, by, bw, bh = 12, 12, 170, 42
    x, first, gap = 36, by + bh + 46, 54
    ys = [first + i * gap for i in range(len(STEPS))]
    H = ys[-1] + 30
    start, end = by + bh + 8, ys[-1]
    length = end - start
    out = [button(bx, by, bw, bh),
           f'<line class="track" x1="{x}" y1="{start}" x2="{x}" y2="{end}"/>',
           f'<line class="fill" x1="{x}" y1="{start}" x2="{x}" y2="{end}" stroke-dasharray="{length}"/>',
           f'<circle class="glow" cx="{x}" cy="{ys[-1]}" r="10"/>']
    for i, (title, sub) in enumerate(STEPS):
        y = ys[i]
        out.append(node(i, x, y))
        out.append(f'<text class="title" x="{x + 24}" y="{y - 2}">{esc(title)}</text>')
        out.append(f'<text class="sub" x="{x + 24}" y="{y + 15}">{esc(sub)}</text>')
    return svg(W, H, t, out, fill_keyframes(length))


def svg(w, h, t, body, extra):
    title = f"{BUTTON}, then: " + ", ".join(s.lower() for s, _ in STEPS)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">\n'
            f"<title>{esc(title)}</title>\n{style(t)}\n{extra}\n" + "\n".join(body) + "\n</svg>\n")


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "demo-flow"
    out.mkdir(parents=True, exist_ok=True)
    for theme, t in THEMES.items():
        (out / f"{theme}.svg").write_text(wide(t), encoding="utf-8")
        (out / f"{theme}-narrow.svg").write_text(narrow(t), encoding="utf-8")
    print("written to", out)
