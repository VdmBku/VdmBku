"""Renders assets/db-matrix/*.svg: every release checked on four database engines, one after another.

python scripts/db_matrix.py
"""
from pathlib import Path

from pipeline import FONT, SLOW, THEMES, esc

ENGINES = ["PostgreSQL", "Oracle", "MariaDB", "MySQL"]
STEPS = ["DB up", "Build + tests", "Restore dump", "Migrate", "Server up"]
STEPS_SHORT = ["DB", "Build", "Dump", "Migrate", "Up"]

START = 0.6   # release chip pulses first
STEP = 0.45   # per step
LANE_GAP = 0.15
LANE = STEP * len(STEPS) + LANE_GAP
DONE = START + LANE * len(ENGINES)
HOLD = DONE + 1.4
CYCLE = HOLD + 0.8


def pct(t):
    return f"{t / CYCLE * 100:.2f}%"


def lane_t0(i):
    return START + i * LANE


def style(t):
    css = [f"""
  text {{ font-family: {FONT}; }}
  .chip {{ fill: {t['fill']}; stroke: {t['accent']}; stroke-width: 1.5; }}
  .chip-text {{ font-size: 13px; font-weight: 600; fill: {t['text']}; }}
  .chip-sub {{ font-size: 11px; fill: {t['muted']}; }}
  .release {{ transform-box: fill-box; transform-origin: center; animation: pulse {CYCLE * SLOW:.2f}s ease-out infinite; }}
  .head {{ font-size: 12px; fill: {t['muted']}; }}
  .engine {{ font-size: 14px; font-weight: 600; fill: {t['text']}; }}
  .wire {{ stroke: {t['stroke']}; stroke-width: 1.5; fill: none; }}
  .track {{ stroke: {t['stroke']}; stroke-width: 3; stroke-linecap: round; }}
  .fill {{ stroke: {t['accent']}; stroke-width: 3; stroke-linecap: round; }}
  .node {{ fill: {t['fill']}; stroke: {t['stroke']}; stroke-width: 2; }}
  .done {{ fill: {t['accent']}; opacity: 0; }}
  .tick {{ fill: none; stroke: #ffffff; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; opacity: 0; }}
  .row {{ fill: {t['accent']}; opacity: 0; }}
  .ok {{ opacity: .35; }}
  .glow {{ fill: none; stroke: {t['accent']}; stroke-width: 2; opacity: 0; transform-box: fill-box;
           transform-origin: center; animation: glow {CYCLE * SLOW:.2f}s ease-out infinite; }}
  @keyframes pulse {{ 0% {{ transform: scale(1) }} {pct(0.25)} {{ transform: scale(1.06) }} {pct(0.55)}, 100% {{ transform: scale(1) }} }}
  @keyframes glow {{ 0%, {pct(DONE)} {{ opacity: 0; transform: scale(1) }} {pct(DONE + 0.1)} {{ opacity: .9; transform: scale(1) }}
                     {pct(DONE + 1.2)} {{ opacity: 0; transform: scale(1.25) }} 100% {{ opacity: 0 }} }}
  .verdict {{ animation: verdict {CYCLE * SLOW:.2f}s linear infinite; }}
  @keyframes verdict {{ 0%, {pct(DONE - 0.05)} {{ opacity: .35 }} {pct(DONE + 0.1)}, {pct(HOLD)} {{ opacity: 1 }} {pct(HOLD + 0.4)}, 100% {{ opacity: .35 }} }}
  @media (prefers-reduced-motion: reduce) {{
    .release, .glow, .done, .tick, .fill, .row, .verdict {{ animation: none !important; }}
    .done, .tick, .verdict {{ opacity: 1 !important; }} .fill {{ stroke-dashoffset: 0 !important; }} }}
"""]
    for i in range(len(ENGINES)):
        t0 = lane_t0(i)
        t1 = t0 + STEP * len(STEPS)
        css.append(f"  .r{i} {{ animation: r{i} {CYCLE * SLOW:.2f}s linear infinite; }}\n"
                   f"  @keyframes r{i} {{ 0%, {pct(t0 - 0.05)} {{ opacity: 0 }} {pct(t0 + 0.1)}, {pct(t1)} {{ opacity: .08 }} "
                   f"{pct(t1 + 0.2)}, 100% {{ opacity: 0 }} }}\n")
        for j in range(len(STEPS)):
            on = t0 + STEP * (j + 1)
            css.append(f"  .s{i}{j} {{ animation: s{i}{j} {CYCLE * SLOW:.2f}s linear infinite; }}\n"
                       f"  @keyframes s{i}{j} {{ 0%, {pct(on - 0.05)} {{ opacity: 0 }} {pct(on + 0.1)}, {pct(HOLD)} {{ opacity: 1 }} "
                       f"{pct(HOLD + 0.4)}, 100% {{ opacity: 0 }} }}\n")
    return "<style>" + "".join(css) + "</style>"


def lane_fill(i, x1, x2, y, vertical=False):
    length = x2 - x1
    t0 = lane_t0(i)
    seg = length / (len(STEPS) - 1)
    frames = [f"0%, {pct(t0 + STEP)} {{ stroke-dashoffset: {length} }}"]
    for j in range(1, len(STEPS)):
        reach = t0 + STEP * (j + 1)
        frames.append(f"{pct(reach)} {{ stroke-dashoffset: {length - seg * j:.1f} }}")
    frames.append(f"{pct(HOLD)} {{ stroke-dashoffset: 0 }}")
    frames.append(f"{pct(HOLD + 0.4)}, 100% {{ stroke-dashoffset: {length} }}")
    line = (f'<line class="track" x1="{x1}" y1="{y}" x2="{x2}" y2="{y}"/>'
            f'<line class="fill" x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke-dasharray="{length}" '
            f'style="animation: f{i} {CYCLE * SLOW:.2f}s linear infinite"/>')
    return line, f"@keyframes f{i} {{ {' '.join(frames)} }}"


def node(i, j, x, y, r=9):
    tick = f"M {x - 4} {y + 0.5} l 2.8 2.8 l 5.4 -6"
    return (f'<circle class="node" cx="{x}" cy="{y}" r="{r}"/>'
            f'<circle class="done s{i}{j}" cx="{x}" cy="{y}" r="{r}"/>'
            f'<path class="tick s{i}{j}" d="{tick}"/>')


def wide(t):
    W, H = 1000, 218
    xs = [300 + j * 118 for j in range(len(STEPS))]
    ys = [70 + i * 40 for i in range(len(ENGINES))]
    mid = (ys[0] + ys[-1]) / 2
    out, kf = [], []
    out.append(f'<g class="release"><rect class="chip" x="12" y="{mid - 22}" width="118" height="44" rx="22"/>'
               f'<text class="chip-text" x="71" y="{mid + 5}" text-anchor="middle">New release</text></g>')
    for j, s in enumerate(STEPS):
        out.append(f'<text class="head" x="{xs[j]}" y="34" text-anchor="middle">{esc(s)}</text>')
    vx, vw = 852, 136
    for i, (eng, y) in enumerate(zip(ENGINES, ys)):
        out.append(f'<rect class="row r{i}" x="146" y="{y - 17}" width="{xs[-1] + 26 - 146}" height="34" rx="8"/>')
        out.append(f'<path class="wire" d="M 130 {mid} C 142 {mid}, 140 {y}, 152 {y}"/>')
        out.append(f'<text class="engine" x="160" y="{y + 5}">{esc(eng)}</text>')
        line, k = lane_fill(i, xs[0], xs[-1], y)
        out.append(line); kf.append(k)
        for j, x in enumerate(xs):
            out.append(node(i, j, x, y))
        out.append(f'<path class="wire" d="M {xs[-1] + 12} {y} C {xs[-1] + 40} {y}, {vx - 30} {mid}, {vx} {mid}"/>')
    out.append(f'<g class="verdict"><rect class="chip" x="{vx}" y="{mid - 26}" width="{vw}" height="52" rx="12"/>'
               f'<text class="chip-text" x="{vx + vw / 2}" y="{mid - 3}" text-anchor="middle">Release OK</text>'
               f'<text class="chip-sub" x="{vx + vw / 2}" y="{mid + 15}" text-anchor="middle">4 of 4 engines</text></g>')
    out.append(f'<rect class="glow" x="{vx}" y="{mid - 26}" width="{vw}" height="52" rx="12"/>')
    return svg(W, H, t, out, kf)


def narrow(t):
    W = 400
    xs = [150 + j * 56 for j in range(len(STEPS))]
    top = 78
    ys = [top + 26 + i * 44 for i in range(len(ENGINES))]
    H = ys[-1] + 92
    out, kf = [], []
    out.append(f'<g class="release"><rect class="chip" x="12" y="12" width="128" height="40" rx="20"/>'
               f'<text class="chip-text" x="76" y="37" text-anchor="middle">New release</text></g>')
    for j, s in enumerate(STEPS_SHORT):
        out.append(f'<text class="head" x="{xs[j]}" y="{top}" text-anchor="middle">{esc(s)}</text>')
    for i, (eng, y) in enumerate(zip(ENGINES, ys)):
        out.append(f'<rect class="row r{i}" x="6" y="{y - 17}" width="{W - 12}" height="34" rx="8"/>')
        out.append(f'<text class="engine" x="14" y="{y + 5}">{esc(eng)}</text>')
        line, k = lane_fill(i, xs[0], xs[-1], y)
        out.append(line); kf.append(k)
        for j, x in enumerate(xs):
            out.append(node(i, j, x, y, r=8))
    vy = ys[-1] + 34
    out.append(f'<g class="verdict"><rect class="chip" x="12" y="{vy}" width="{W - 24}" height="44" rx="12"/>'
               f'<text class="chip-text" x="{W / 2}" y="{vy + 27}" text-anchor="middle">Release OK  ·  4 of 4 engines</text></g>')
    out.append(f'<rect class="glow" x="12" y="{vy}" width="{W - 24}" height="44" rx="12"/>')
    return svg(W, H, t, out, kf)


def svg(w, h, t, body, keyframes):
    title = (f"Every release is checked on {', '.join(ENGINES[:-1])} and {ENGINES[-1]}: "
             + ", ".join(s.lower() for s in STEPS))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">\n'
            f"<title>{esc(title)}</title>\n{style(t)}\n<style>{' '.join(keyframes)}</style>\n" + "\n".join(body) + "\n</svg>\n")


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "db-matrix"
    out.mkdir(parents=True, exist_ok=True)
    for theme, t in THEMES.items():
        (out / f"{theme}.svg").write_text(wide(t), encoding="utf-8", newline="\n")
        (out / f"{theme}-narrow.svg").write_text(narrow(t), encoding="utf-8", newline="\n")
    print("written to", out)
