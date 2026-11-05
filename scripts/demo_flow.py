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
    ("6 service releases", "each from its branch"),
    ("Ready", "access sent"),
]

PRESS = 0.7   # button click
SVC = 5       # index of the step where the services are released one by one
SERVICES = 6
DUR = [1.0, 1.0, 1.0, 1.0, 1.0, 2.6, 1.0]   # seconds per step; the service releases take longer
ON = [PRESS + sum(DUR[:i + 1]) for i in range(len(DUR))]
HOLD = ON[-1] + 1.6   # everything stays done until here, then resets
CYCLE = HOLD + 0.7


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
  @keyframes glow {{ 0%, {pct(ON[-1])} {{ opacity: 0; transform: scale(1) }}
                     {pct(ON[-1] + 0.1)} {{ opacity: .9; transform: scale(1) }}
                     {pct(ON[-1] + 1.2)} {{ opacity: 0; transform: scale(2.2) }} 100% {{ opacity: 0 }} }}
  @media (prefers-reduced-motion: reduce) {{
    .btn, .ripple, .fill, .done, .tick, .glow {{ animation: none !important; }}
    .fill {{ stroke-dashoffset: 0 !important; }} .done, .tick {{ opacity: 1 !important; }} }}
"""]
    t0, t1 = ON[SVC - 1] + 0.1, ON[SVC] - 0.1
    for j in range(SERVICES):
        on = t0 + (t1 - t0) * (j + 1) / SERVICES
        css.append(f"  .v{j} {{ animation: v{j} {CYCLE}s linear infinite; }}\n"
                   f"  @keyframes v{j} {{ 0%, {pct(on - 0.05)} {{ opacity: 0 }} {pct(on + 0.1)}, {pct(HOLD)} {{ opacity: 1 }} "
                   f"{pct(HOLD + 0.4)}, 100% {{ opacity: 0 }} }}\n")
    css.append(f"  .svc {{ fill: {t['fill']}; stroke: {t['stroke']}; stroke-width: 1.5; }} .svc-on {{ fill: {t['accent']}; opacity: 0; }}\n"
               f"  .panel {{ fill: {t['fill']}; stroke: {t['stroke']}; stroke-width: 1.5; }}\n"
               f"  @media (prefers-reduced-motion: reduce) {{ .svc-on {{ animation: none !important; opacity: 1 !important; }} }}\n")
    for i in range(len(STEPS)):
        on = ON[i]
        css.append(f"  .s{i} {{ animation: s{i} {CYCLE}s linear infinite; }}\n"
                   f"  @keyframes s{i} {{ 0%, {pct(on - 0.05)} {{ opacity: 0 }} {pct(on + 0.15)}, {pct(HOLD)} {{ opacity: 1 }} "
                   f"{pct(HOLD + 0.4)}, 100% {{ opacity: 0 }} }}\n")
    return "<style>" + "".join(css) + "</style>"


def fill_keyframes(length):
    # progress line grows step by step, waits at each node
    frames = [f"0%, {pct(PRESS)} {{ stroke-dashoffset: {length} }}"]
    seg = length / len(STEPS)
    for i in range(len(STEPS)):
        reach = ON[i]
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


def releases(cx, cy, size=12, gap=4, cols=3, panel=True):
    """One tile per service release, lit one after another."""
    rows = -(-SERVICES // cols)
    w, h = cols * size + (cols - 1) * gap, rows * size + (rows - 1) * gap
    x0, y0 = cx - w / 2, cy - h / 2
    out = [f'<rect class="panel" x="{x0 - 7}" y="{y0 - 7}" width="{w + 14}" height="{h + 14}" rx="8"/>'] if panel else []
    for j in range(SERVICES):
        r, c = divmod(j, cols)
        x, y = x0 + c * (size + gap), y0 + r * (size + gap)
        out.append(f'<rect class="svc" x="{x}" y="{y}" width="{size}" height="{size}" rx="3"/>'
                   f'<rect class="svc-on v{j}" x="{x}" y="{y}" width="{size}" height="{size}" rx="3"/>')
    return "".join(out)


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
        out.append(releases(x, cy) if i == SVC else node(i, x, cy))
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
        if i == SVC:
            out.append(releases(330, y, size=11, gap=4, cols=6, panel=False))
        out.append(f'<text class="title" x="{x + 24}" y="{y - 2}">{esc(title)}</text>')
        out.append(f'<text class="sub" x="{x + 24}" y="{y + 15}">{esc(sub)}</text>')
    return svg(W, H, t, out, fill_keyframes(length))


def svg(w, h, t, body, extra):
    title = (f"{BUTTON}, then: approve, pipeline, server and DNS, hardening, proxy and TLS, "
             f"{SERVICES} service releases one by one, ready with access sent")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">\n'
            f"<title>{esc(title)}</title>\n{style(t)}\n{extra}\n" + "\n".join(body) + "\n</svg>\n")


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "demo-flow"
    out.mkdir(parents=True, exist_ok=True)
    for theme, t in THEMES.items():
        (out / f"{theme}.svg").write_text(wide(t), encoding="utf-8")
        (out / f"{theme}-narrow.svg").write_text(narrow(t), encoding="utf-8")
    print("written to", out)
