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
