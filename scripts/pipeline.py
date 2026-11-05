"""Renders assets/pipeline/*.svg: the delivery pipeline picture at the top of the profile.

python scripts/pipeline.py
"""
from pathlib import Path

STAGES = [
    ("Commit", ["Git", "GitLab", "GitHub"]),
    ("Build & test", ["Jenkins", "GitLab CI", "GitHub Actions"]),
    ("Package", ["Docker", "Harbor", "Nexus"]),
    ("Provision", ["Terraform", "AWS, Azure", "GCP, Hetzner"]),
    ("Deploy", ["Ansible", "Helm", "Argo CD"]),
    ("Observe", ["Prometheus", "Grafana", "Zabbix", "Wazuh"]),
]

# 24x24 line icons, drawn by hand for this picture
ICONS = {
    "Commit": '<circle cx="12" cy="12" r="3.2"/><path d="M3 12h5.8M15.2 12H21"/>',
    "Build & test": '<circle cx="12" cy="12" r="9"/><path d="M8 12.4l2.8 2.8L16.2 9.6"/>',
    "Package": '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M4 7.5l8 4.5 8-4.5M12 12v9"/>',
    "Provision": '<rect x="3.5" y="4" width="17" height="7" rx="2"/><rect x="3.5" y="13" width="17" height="7" rx="2"/>'
                 '<path d="M7.5 7.5h.01M7.5 16.5h.01"/>',
    "Deploy": '<path d="M12 15V4M7.5 8.5L12 4l4.5 4.5"/><path d="M4 15v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3"/>',
    "Observe": '<path d="M3 12h4l3-7 4 14 3-7h4"/>',
}

THEMES = {
    "light": dict(text="#1f2328", muted="#59636e", fill="#f6f8fa", stroke="#d0d7de", accent="#0f8a82"),
    "dark": dict(text="#e6edf3", muted="#9198a1", fill="#151b23", stroke="#3d444d", accent="#2fbfb4"),
}

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
STEP = 1.2  # seconds each stage stays lit
CYCLE = STEP * len(STAGES)


def style(t):
    lit = 100 / len(STAGES)
    return f"""<style>
  text {{ font-family: {FONT}; }}
  .num {{ font-size: 12px; font-weight: 600; fill: {t['accent']}; letter-spacing: .08em; }}
  .name {{ font-size: 15px; font-weight: 600; fill: {t['text']}; }}
  .tool {{ font-size: 13px; fill: {t['muted']}; }}
  .note {{ font-size: 12px; fill: {t['muted']}; }}
  .icon {{ fill: none; stroke: {t['accent']}; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }}
  .box {{ fill: {t['fill']}; stroke: {t['stroke']}; stroke-width: 1; }}
  .hl {{ fill: none; stroke: {t['accent']}; stroke-width: 2; opacity: 0;
         animation: lit {CYCLE}s linear infinite; }}
  .wire {{ stroke: {t['stroke']}; stroke-width: 1.5; fill: none; }}
  .head {{ fill: {t['stroke']}; }}
  .loop {{ stroke: {t['accent']}; stroke-width: 1.5; fill: none; stroke-dasharray: 5 5;
           opacity: .7; animation: flow 1.6s linear infinite; }}
  @keyframes lit {{ 0% {{ opacity: 0 }} 3% {{ opacity: 1 }} {lit:.1f}% {{ opacity: 1 }}
                   {lit + 3:.1f}% {{ opacity: 0 }} 100% {{ opacity: 0 }} }}
  @keyframes flow {{ to {{ stroke-dashoffset: -20 }} }}
  @media (prefers-reduced-motion: reduce) {{ .hl, .loop {{ animation: none; }} }}
</style>"""


def arrow(x1, y1, x2, y2):
    # straight wire with a small triangular head at (x2, y2)
    if y1 == y2:
        head = f"{x2},{y2} {x2 - 7},{y2 - 4} {x2 - 7},{y2 + 4}"
        end = x2 - 6
        return f'<line class="wire" x1="{x1}" y1="{y1}" x2="{end}" y2="{y2}"/><polygon class="head" points="{head}"/>'
    head = f"{x2},{y2} {x2 - 4},{y2 - 7} {x2 + 4},{y2 - 7}"
    end = y2 - 6
    return f'<line class="wire" x1="{x1}" y1="{y1}" x2="{x2}" y2="{end}"/><polygon class="head" points="{head}"/>'


def icon(name, x, y, size=20):
    return f'<g class="icon" transform="translate({x} {y}) scale({size / 24:.4f})">{ICONS[name]}</g>'


def stage_box(i, x, y, w, h):
    delay = f"animation-delay: {i * STEP:.1f}s"
    return (f'<rect class="box" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>'
            f'<rect class="hl" x="{x}" y="{y}" width="{w}" height="{h}" rx="10" style="{delay}"/>')


def wide(t):
    W, H = 960, 290
    bw, gap, x0, y0, bh = 136, 24, 12, 16, 172
    out = []
    for i, (name, tools) in enumerate(STAGES):
        x = x0 + i * (bw + gap)
        out.append(stage_box(i, x, y0, bw, bh))
        out.append(f'<text class="num" x="{x + 16}" y="{y0 + 28}">{i + 1:02d}</text>')
        out.append(icon(name, x + bw - 36, y0 + 13))
        out.append(f'<text class="name" x="{x + 16}" y="{y0 + 50}">{esc(name)}</text>')
        for j, tool in enumerate(tools):
            out.append(f'<text class="tool" x="{x + 16}" y="{y0 + 82 + j * 21}">{esc(tool)}</text>')
        if i:
            out.append(arrow(x - gap + 3, y0 + 45, x - 1, y0 + 45))
    first = x0 + bw / 2
    last = x0 + 5 * (bw + gap) + bw / 2
    bottom = y0 + bh
    out.append(f'<path class="loop" d="M {last} {bottom + 2} C {last} {bottom + 70}, {first} {bottom + 70}, {first} {bottom + 8}"/>')
    out.append(f'<polygon fill="{t["accent"]}" opacity=".7" points="{first},{bottom + 2} {first - 4},{bottom + 10} {first + 4},{bottom + 10}"/>')
    out.append(f'<text class="note" x="{W / 2}" y="{bottom + 76}" text-anchor="middle">metrics and alerts feed the next change</text>')
    return svg(W, H, t, out)


def narrow(t):
    W, bh, gap, x0, y0, bw = 400, 64, 22, 12, 12, 330
    H = y0 + len(STAGES) * bh + (len(STAGES) - 1) * gap + 16
    out = []
    for i, (name, tools) in enumerate(STAGES):
        y = y0 + i * (bh + gap)
        out.append(stage_box(i, x0, y, bw, bh))
        out.append(f'<text class="num" x="{x0 + 16}" y="{y + 26}">{i + 1:02d}</text>')
        out.append(icon(name, x0 + bw - 38, y + (bh - 22) / 2, 22))
        out.append(f'<text class="name" x="{x0 + 46}" y="{y + 26}">{esc(name)}</text>')
        out.append(f'<text class="tool" x="{x0 + 46}" y="{y + 47}">{esc(", ".join(tools))}</text>')
        if i:
            out.append(arrow(x0 + 26, y - gap + 3, x0 + 26, y - 1))
    right = x0 + bw
    top = y0 + bh / 2
    bottom = y0 + 5 * (bh + gap) + bh / 2
    out.append(f'<path class="loop" d="M {right + 2} {bottom} C {right + 50} {bottom}, {right + 50} {top}, {right + 8} {top}"/>')
    out.append(f'<polygon fill="{t["accent"]}" opacity=".7" points="{right + 2},{top} {right + 10},{top - 4} {right + 10},{top + 4}"/>')
    return svg(W, H, t, out)


def svg(w, h, t, body):
    title = "Delivery pipeline: " + ", ".join(name.lower() for name, _ in STAGES)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">\n'
            f"<title>{esc(title)}</title>\n{style(t)}\n" + "\n".join(body) + "\n</svg>\n")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "pipeline"
    out.mkdir(parents=True, exist_ok=True)
    for theme, t in THEMES.items():
        (out / f"{theme}.svg").write_text(wide(t), encoding="utf-8")
        (out / f"{theme}-narrow.svg").write_text(narrow(t), encoding="utf-8")
    print("written to", out)
