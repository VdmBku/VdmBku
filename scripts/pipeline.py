"""Renders assets/pipeline/*.svg: the delivery pipeline picture at the top of the profile.

Also the shared module for the other pictures: THEMES, FONT, esc.

python scripts/pipeline.py
"""
from pathlib import Path

THEMES = {
    "light": dict(text="#1f2328", muted="#59636e", fill="#f6f8fa", stroke="#d0d7de", accent="#0f8a82", red="#cf222e"),
    "dark": dict(text="#e6edf3", muted="#9198a1", fill="#151b23", stroke="#3d444d", accent="#2fbfb4", red="#f85149"),
}
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"

# 24x24 line icons, drawn by hand for this picture
ICONS = {
    "Commit": '<circle cx="12" cy="12" r="3.2"/><path d="M3 12h5.8M15.2 12H21"/>',
    "Build & test": '<circle cx="12" cy="12" r="9"/><path d="M8 12.4l2.8 2.8L16.2 9.6"/>',
    "Package": '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M4 7.5l8 4.5 8-4.5M12 12v9"/>',
    "Provision": '<rect x="3.5" y="4" width="17" height="7" rx="2"/><rect x="3.5" y="13" width="17" height="7" rx="2"/>'
                 '<path d="M7.5 7.5h.01M7.5 16.5h.01"/>',
    "Deploy": '<path d="M12 15V4M7.5 8.5L12 4l4.5 4.5"/><path d="M4 15v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3"/>',
    "Observe": '<path d="M3 12h4l3-7 4 14 3-7h4"/>',
    "Bell": '<path d="M6 16V11a6 6 0 0 1 12 0v5l1.5 2h-15z"/><path d="M10 20a2 2 0 0 0 4 0"/>',
}

STAGES = [  # (title, subtitle, tool lines, lit from, lit until)
    ("Commit", "push or merge", ["Git · GitLab · GitHub"], 0.0, 0.9),
    ("Build & test", "checks in parallel", ["Jenkins · GitLab CI", "GitHub Actions"], 0.9, 2.6),
    ("Package", "artifact to a registry", ["Docker · Harbor · Nexus"], 2.6, 3.6),
    ("Provision", "create or change infra", ["Terraform", "AWS · Azure · GCP · Hetzner"], 3.6, 5.0),
    ("Deploy", "to the servers from 04", ["Ansible · Helm · Argo CD"], 5.0, 6.5),
]
OBSERVE_TOOLS = "Prometheus · Grafana · Zabbix · Wazuh"
CHECKS = [("build", 1.9), ("lint", 1.5), ("unit tests", 2.5), ("secret scan", 2.1)]  # name, done
ALERT = (7.4, 9.4)
HOLD, CYCLE = 9.8, 10.6


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def pct(t):
    return f"{t / CYCLE * 100:.2f}%"


class Anim:
    def __init__(self):
        self.rules, self.n = [], 0

    def _cls(self):
        self.n += 1
        return f"k{self.n}"

    def show(self, at, base=0.0):
        c = self._cls()
        self.rules.append(f".{c} {{ animation: {c} {CYCLE}s linear infinite; }} @keyframes {c} {{ 0%, {pct(at - 0.05)} "
                          f"{{ opacity: {base} }} {pct(at + 0.1)}, {pct(HOLD)} {{ opacity: 1 }} {pct(HOLD + 0.4)}, 100% {{ opacity: {base} }} }}")
        return c

    def window(self, start, end, peak=1.0):
        c = self._cls()
        self.rules.append(f".{c} {{ animation: {c} {CYCLE}s linear infinite; }} @keyframes {c} {{ 0%, {pct(start - 0.05)} "
                          f"{{ opacity: 0 }} {pct(start + 0.1)}, {pct(end)} {{ opacity: {peak} }} {pct(end + 0.25)}, 100% {{ opacity: 0 }} }}")
        return c

    def grow(self, start, end):
        c = self._cls()
        self.rules.append(f".{c} {{ transform-box: fill-box; transform-origin: left center; animation: {c} {CYCLE}s linear infinite; }} "
                          f"@keyframes {c} {{ 0%, {pct(start)} {{ transform: scaleX(0) }} {pct(end)}, {pct(HOLD)} {{ transform: scaleX(1) }} "
                          f"{pct(HOLD + 0.4)}, 100% {{ transform: scaleX(0) }} }}")
        return c

    def move(self, start, end, dx):
        c = self._cls()
        self.rules.append(f".{c} {{ animation: {c} {CYCLE}s ease-in-out infinite; }} @keyframes {c} {{ 0%, {pct(start)} "
                          f"{{ transform: translateX(0) }} {pct(end)}, {pct(HOLD)} {{ transform: translateX({dx}px) }} "
                          f"{pct(HOLD + 0.4)}, 100% {{ transform: translateX(0) }} }}")
        return c

    def red(self, start, end):
        c = self._cls()
        self.rules.append(f".{c} {{ animation: {c} {CYCLE}s linear infinite; }} @keyframes {c} {{ 0%, {pct(start - 0.05)} "
                          f"{{ stroke: var(--accent) }} {pct(start + 0.1)}, {pct(end)} {{ stroke: var(--red) }} "
                          f"{pct(end + 0.3)}, 100% {{ stroke: var(--accent) }} }}")
        return c


def style(t, anim):
    return f"""<style>
  svg {{ --accent: {t['accent']}; --red: {t['red']}; }}
  text {{ font-family: {FONT}; }}
  .card {{ fill: {t['fill']}; stroke: {t['stroke']}; stroke-width: 1; }}
  .hl {{ fill: none; stroke: {t['accent']}; stroke-width: 2; }}
  .num {{ font-size: 12px; font-weight: 600; fill: {t['accent']}; letter-spacing: .08em; }}
  .name {{ font-size: 15px; font-weight: 600; fill: {t['text']}; }}
  .what {{ font-size: 12px; fill: {t['muted']}; }}
  .tool {{ font-size: 11px; fill: {t['muted']}; }}
  .tiny {{ font-size: 10.5px; fill: {t['muted']}; }}
  .tiny-on {{ font-size: 10.5px; font-weight: 600; fill: {t['accent']}; }}
  .icon {{ fill: none; stroke: {t['accent']}; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }}
  .wire {{ stroke: {t['stroke']}; stroke-width: 1.5; fill: none; }}
  .head {{ fill: {t['stroke']}; }}
  .slot {{ fill: {t['stroke']}; opacity: .55; }}
  .bar {{ fill: {t['accent']}; }}
  .dot {{ fill: {t['fill']}; stroke: {t['stroke']}; stroke-width: 1.5; }}
  .dot-on {{ fill: {t['accent']}; }}
  .ok {{ fill: {t['accent']}; }}
  .okv {{ fill: none; stroke: #ffffff; stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round; }}
  .chip {{ fill: {t['fill']}; stroke: {t['accent']}; stroke-width: 1.5; }}
  .chip-text {{ font-size: 11px; font-weight: 600; fill: {t['text']}; }}
  .srv {{ fill: {t['fill']}; stroke: {t['stroke']}; stroke-width: 1.5; }}
  .srv-new {{ fill: {t['accent']}; fill-opacity: .18; stroke: {t['accent']}; stroke-width: 1.5; }}
  .srv-chg {{ fill: none; stroke: {t['accent']}; stroke-width: 1.8; stroke-dasharray: 3 2; }}
  .srv-led {{ fill: {t['muted']}; }}
  .app {{ fill: {t['accent']}; }}
  .db {{ fill: {t['fill']}; stroke: {t['accent']}; stroke-width: 1.5; }}
  .box-body {{ fill: {t['accent']}; fill-opacity: .2; }}
  .box-frame {{ fill: none; stroke: {t['accent']}; stroke-width: 1.6; }}
  .ridge {{ stroke: {t['accent']}; stroke-width: 1.2; opacity: .75; }}
  .pulse {{ fill: none; stroke: {t['accent']}; stroke-width: 2; stroke-linejoin: round; animation: beat 1.2s linear infinite; }}
  .live {{ fill: {t['accent']}; animation: blink 1.4s ease-in-out infinite; }}
  .badge {{ fill: none; stroke: {t['accent']}; stroke-width: 1.2; }}
  .badge-text {{ font-size: 11px; font-weight: 700; fill: {t['accent']}; }}
  .alert {{ fill: {t['fill']}; stroke: {t['red']}; stroke-width: 1.8; }}
  .alert-icon {{ fill: none; stroke: {t['red']}; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }}
  .alert-title {{ font-size: 13px; font-weight: 700; fill: {t['red']}; }}
  .loop {{ fill: none; stroke: {t['accent']}; stroke-width: 1.5; stroke-dasharray: 5 5; opacity: .7; animation: flow 1.6s linear infinite; }}
  @keyframes beat {{ to {{ transform: translateX(-50px) }} }}
  @keyframes blink {{ 0%, 100% {{ opacity: 1 }} 50% {{ opacity: .3 }} }}
  @keyframes flow {{ to {{ stroke-dashoffset: -20 }} }}
  {' '.join(anim.rules)}
  @media (prefers-reduced-motion: reduce) {{
    [class^="k"], [class*=" k"], .pulse, .live, .loop {{ animation: none !important; }}
    [class^="k"], [class*=" k"] {{ opacity: 1 !important; transform: none !important; }} }}
</style>"""


def icon(name, x, y, size=20, cls="icon"):
    return f'<g class="{cls}" transform="translate({x} {y}) scale({size / 24:.4f})">{ICONS[name]}</g>'


def tick(anim, x, y, at, r=6):
    c = anim.show(at)
    return (f'<circle class="ok {c}" cx="{x}" cy="{y}" r="{r}"/>'
            f'<path class="okv {c}" d="M {x - r * .45:.1f} {y + .3:.1f} l {r * .3:.1f} {r * .3:.1f} l {r * .6:.1f} {-r * .65:.1f}"/>')


def server(x, y, cls="srv", w=34, h=22):
    return (f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="4"/>'
            f'<circle class="srv-led" cx="{x + 7}" cy="{y + h / 2}" r="2"/><line class="wire" x1="{x + 13}" y1="{y + h / 2}" x2="{x + w - 6}" y2="{y + h / 2}"/>')


# visualisations inside a card; (rx, ry) top-left of the region, rw x rh its size

def viz_commit(anim, rx, ry, rw, rh):
    y = ry + rh / 2
    out = [f'<line class="wire" x1="{rx}" y1="{y}" x2="{rx + rw}" y2="{y}"/>']
    for i in range(3):
        out.append(f'<circle class="dot" cx="{rx + 10 + i * 32}" cy="{y}" r="6"/>')
    nx = rx + 10 + 3 * 32
    c = anim.show(0.35)
    out.append(f'<circle class="dot-on {c}" cx="{nx}" cy="{y}" r="7"/><text class="tiny-on {c}" x="{nx}" y="{y + 22}" text-anchor="middle">new</text>')
    return "".join(out)


def viz_build(anim, rx, ry, rw, rh):
    out, row = [], rh / len(CHECKS)
    for i, (name, done) in enumerate(CHECKS):
        y = ry + row * i + row / 2
        bx, bw = rx + 66, rw - 66 - 16
        out.append(f'<text class="tiny" x="{rx}" y="{y + 3.5}">{esc(name)}</text>'
                   f'<rect class="slot" x="{bx}" y="{y - 3}" width="{bw}" height="6" rx="3"/>'
                   f'<rect class="bar {anim.grow(1.0, done)}" x="{bx}" y="{y - 3}" width="{bw}" height="6" rx="3"/>')
        out.append(tick(anim, rx + rw - 5, y, done + 0.05, r=5))
    return "".join(out)


def container(x, y, w=44, h=20):
    """A shipping container: the image that goes to the registry."""
    ridges = "".join(f'<line class="ridge" x1="{x + k}" y1="{y + 3}" x2="{x + k}" y2="{y + h - 3}"/>' for k in range(7, w - 3, 6))
    return (f'<rect class="box-body" x="{x}" y="{y}" width="{w}" height="{h}" rx="2"/>{ridges}'
            f'<rect class="box-frame" x="{x}" y="{y}" width="{w}" height="{h}" rx="2"/>')


def viz_package(anim, rx, ry, rw, rh):
    y = ry + rh / 2
    dbx = rx + rw - 40
    out = [f'<line class="wire" x1="{rx + 60}" y1="{y}" x2="{dbx - 4}" y2="{y}"/>',
           f'<ellipse class="db" cx="{dbx + 18}" cy="{y + 14}" rx="18" ry="5"/>'
           f'<rect class="db" x="{dbx}" y="{y - 12}" width="36" height="26" style="stroke-width:0"/>'
           f'<line class="db" x1="{dbx}" y1="{y - 12}" x2="{dbx}" y2="{y + 14}"/><line class="db" x1="{dbx + 36}" y1="{y - 12}" x2="{dbx + 36}" y2="{y + 14}"/>'
           f'<ellipse class="db" cx="{dbx + 18}" cy="{y - 12}" rx="18" ry="5"/>',
           f'<text class="tiny" x="{dbx + 18}" y="{y + 32}" text-anchor="middle">registry</text>']
    m = anim.move(2.75, 3.45, dbx - rx - 58)
    out.append(f'<g class="{m}">{container(rx, y - 10)}'
               f'<text class="chip-text" x="{rx + 22}" y="{y - 15}" text-anchor="middle">app:1.4</text></g>')
    out.append(tick(anim, dbx + 34, y - 16, 3.5, r=6))
    return "".join(out)


SRV_X = (0, 46, 92)


def viz_provision(anim, rx, ry, rw, rh):
    c = anim.show(3.8)
    out = [f'<text class="tiny-on {c}" x="{rx}" y="{ry + 10}">plan: +2 ~1</text>',
           f'<text class="tiny {anim.show(4.25)}" x="{rx + 76}" y="{ry + 10}">apply</text>']
    sy = ry + 24
    out.append(server(rx + SRV_X[0], sy))
    out.append(f'<rect class="srv-chg {anim.show(4.4)}" x="{rx + SRV_X[0] - 3}" y="{sy - 3}" width="40" height="28" rx="6"/>')
    out.append(f'<text class="tiny-on {anim.show(4.4)}" x="{rx + SRV_X[0] + 17}" y="{sy + 40}" text-anchor="middle">~ changed</text>')
    for i, at in ((1, 4.6), (2, 4.8)):
        out.append(f'<g class="{anim.show(at)}">{server(rx + SRV_X[i], sy, "srv-new")}</g>')
    out.append(f'<text class="tiny-on {anim.show(4.8)}" x="{rx + SRV_X[1] + 40}" y="{sy + 40}" text-anchor="middle">+ new</text>')
    return "".join(out)


def viz_deploy(anim, rx, ry, rw, rh):
    out = [f'<text class="tiny {anim.show(5.15)}" x="{rx}" y="{ry + 10}">rolling update</text>']
    sy = ry + 24
    for i, at in enumerate((5.5, 5.9, 6.3)):
        x = rx + SRV_X[i]
        out.append(server(x, sy))
        out.append(f'<rect class="app {anim.show(at)}" x="{x + 22}" y="{sy + 5}" width="8" height="12" rx="2"/>')
        out.append(tick(anim, x + 17, sy + 38, at + 0.05, r=6))
    return "".join(out)


VIZ = [viz_commit, viz_build, viz_package, viz_provision, viz_deploy]


def pulse(anim, x, y, w, h, clip):
    """A heartbeat line that never stops; it turns red while an alert is open."""
    pattern = [(0, 0), (14, 0), (18, -4), (22, 0), (26, 0), (29, 7), (32, -20), (35, 9), (38, 0), (50, 0)]
    pts = []
    for k in range(int(w / 50) + 2):
        pts += [(x + k * 50 + px, y + h / 2 + py) for px, py in pattern]
    d = "M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in pts)
    return (f'<clipPath id="{clip}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>'
            f'<g clip-path="url(#{clip})"><path class="pulse {anim.red(*ALERT)}" d="{d}"/></g>')


def alert(anim, x, y, w):
    c = anim.window(*ALERT)
    return (f'<g class="{c}"><rect class="alert" x="{x}" y="{y}" width="{w}" height="46" rx="10"/>'
            f'{icon("Bell", x + 12, y + 12, 22, "alert-icon")}'
            f'<text class="alert-title" x="{x + 44}" y="{y + 20}">Alert</text>'
            f'<text class="what" x="{x + 44}" y="{y + 36}">to on-call SRE / DevOps</text></g>')


def card(anim, i, x, y, w, h, narrow=False):
    title, sub, tools, t0, t1 = STAGES[i]
    out = [f'<rect class="card" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>',
           f'<rect class="hl {anim.window(t0, t1)}" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>',
           f'<text class="num" x="{x + 14}" y="{y + 24}">{i + 1:02d}</text>']
    if not narrow:
        out.append(icon(title, x + w - 34, y + 9))
    if not narrow:
        out += [f'<text class="name" x="{x + 14}" y="{y + 46}">{esc(title)}</text>',
                f'<text class="what" x="{x + 14}" y="{y + 63}">{esc(sub)}</text>']
        for k, line in enumerate(tools):
            out.append(f'<text class="tool" x="{x + 14}" y="{y + h - 26 + k * 14 - (len(tools) - 1) * 0}">{esc(line)}</text>')
        out.append(VIZ[i](anim, x + 14, y + 76, w - 28, 70))
    else:
        out += [f'<text class="name" x="{x + 44}" y="{y + 24}">{esc(title)}</text>',
                f'<text class="what" x="{x + 44}" y="{y + 41}">{esc(sub)}</text>',
                f'<text class="tool" x="{x + 44}" y="{y + h - 14}">{esc(tools[0])}</text>']
        out.append(VIZ[i](anim, x + 210, y + 12, w - 224, h - 24))
    return "".join(out)


def arrow(x1, y1, x2, y2):
    if y1 == y2:
        return (f'<line class="wire" x1="{x1}" y1="{y1}" x2="{x2 - 5}" y2="{y2}"/>'
                f'<polygon class="head" points="{x2},{y2} {x2 - 6},{y2 - 4} {x2 - 6},{y2 + 4}"/>')
    return (f'<line class="wire" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2 - 5}"/>'
            f'<polygon class="head" points="{x2},{y2} {x2 - 4},{y2 - 6} {x2 + 4},{y2 - 6}"/>')


def observe(anim, x, y, w, h, narrow=False):
    out = [f'<rect class="card" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>',
           f'<text class="num" x="{x + 14}" y="{y + 24}">06</text>',
           f'<text class="name" x="{x + 44}" y="{y + 24}">Observe</text>',
           f'<rect class="badge" x="{x + 112}" y="{y + 10}" width="50" height="19" rx="9.5"/>'
           f'<circle class="live" cx="{x + 123}" cy="{y + 19.5}" r="3.5"/>'
           f'<text class="badge-text" x="{x + 131}" y="{y + 24}">24/7</text>',
           f'<text class="what" x="{x + 14}" y="{y + 46}">metrics, logs, security events</text>',
           f'<text class="tool" x="{x + 14}" y="{y + 64}">{esc(OBSERVE_TOOLS)}</text>']
    if not narrow:
        out.append(pulse(anim, x + 300, y + 18, 360, 52, "beat-w"))
        out.append(alert(anim, x + w - 228, y + 22, 214))
    else:
        out.append(pulse(anim, x + 14, y + 78, w - 28, 44, "beat-n"))
        out.append(alert(anim, x + 14, y + 128, w - 28))
    return "".join(out)


def wide(t):
    W, H = 960, 330
    anim, out = Anim(), []
    cw, gap, cy, ch = 172, 15, 16, 186
    xs = [20 + i * (cw + gap) for i in range(len(STAGES))]
    for i, x in enumerate(xs):
        out.append(card(anim, i, x, cy, cw, ch))
        if i:
            out.append(arrow(x - gap + 2, cy + 46, x - 1, cy + 46))
    by = cy + ch + 30
    out.append(observe(anim, 20, by, W - 40, 96))
    # deployed servers are watched; incidents come back as commits
    out.append(arrow(xs[-1] + cw / 2, cy + ch + 2, xs[-1] + cw / 2, by - 1))
    out.append(f'<path class="loop" d="M 60 {by} L 60 {cy + ch + 4}"/>'
               f'<polygon fill="{t["accent"]}" opacity=".7" points="60,{cy + ch + 2} 56,{cy + ch + 9} 64,{cy + ch + 9}"/>'
               f'<text class="tiny" x="70" y="{cy + ch + 19}">fixes come back as commits</text>')
    return svg(W, H, t, anim, out)


def narrow(t):
    W = 400
    anim, out = Anim(), []
    ch, gap = 96, 16
    ys = [12 + i * (ch + gap) for i in range(len(STAGES))]
    for i, y in enumerate(ys):
        out.append(card(anim, i, 12, y, W - 24, ch, narrow=True))
        if i:
            out.append(arrow(40, y - gap + 2, 40, y - 1))
    by = ys[-1] + ch + gap
    out.append(arrow(40, by - gap + 2, 40, by - 1))
    out.append(observe(anim, 12, by, W - 24, 186, narrow=True))
    return svg(W, by + 198, t, anim, out)


def vertical(t):
    W, x0 = 680, 44
    anim, out = Anim(), []
    ch, gap, cw = 104, 20, W - x0 - 12
    ys = [12 + i * (ch + gap) for i in range(len(STAGES))]
    for i, y in enumerate(ys):
        title, sub, tools, t0, t1 = STAGES[i]
        out += [f'<rect class="card" x="{x0}" y="{y}" width="{cw}" height="{ch}" rx="10"/>',
                f'<rect class="hl {anim.window(t0, t1)}" x="{x0}" y="{y}" width="{cw}" height="{ch}" rx="10"/>',
                f'<text class="num" x="{x0 + 14}" y="{y + 26}">{i + 1:02d}</text>',
                icon(title, x0 + 40, y + 10),
                f'<text class="name" x="{x0 + 70}" y="{y + 26}">{esc(title)}</text>',
                f'<text class="what" x="{x0 + 14}" y="{y + 48}">{esc(sub)}</text>']
        for k, line in enumerate(tools):
            out.append(f'<text class="tool" x="{x0 + 14}" y="{y + 72 + k * 15}">{esc(line)}</text>')
        out.append(VIZ[i](anim, x0 + 300, y + 14, cw - 320, ch - 28))
        if i:
            out.append(arrow(x0 + 26, y - gap + 2, x0 + 26, y - 1))
    by = ys[-1] + ch + gap
    out.append(arrow(x0 + 26, by - gap + 2, x0 + 26, by - 1))
    oh = 124
    out += [f'<rect class="card" x="{x0}" y="{by}" width="{cw}" height="{oh}" rx="10"/>',
            f'<text class="num" x="{x0 + 14}" y="{by + 26}">06</text>',
            icon("Observe", x0 + 40, by + 10),
            f'<text class="name" x="{x0 + 70}" y="{by + 26}">Observe</text>',
            f'<rect class="badge" x="{x0 + 138}" y="{by + 12}" width="50" height="19" rx="9.5"/>'
            f'<circle class="live" cx="{x0 + 149}" cy="{by + 21.5}" r="3.5"/>'
            f'<text class="badge-text" x="{x0 + 157}" y="{by + 26}">24/7</text>',
            f'<text class="what" x="{x0 + 14}" y="{by + 48}">metrics, logs, security events</text>',
            f'<text class="tool" x="{x0 + 14}" y="{by + 72}">Prometheus · Grafana</text>',
            f'<text class="tool" x="{x0 + 14}" y="{by + 87}">Zabbix · Wazuh</text>',
            pulse(anim, x0 + 300, by + 12, cw - 320, 44, "beat-v"),
            alert(anim, x0 + 300, by + 66, cw - 320)]
    # incidents come back as commits: a dashed loop up the left side
    top, bottom = ys[0] + ch / 2, by + oh / 2
    out.append(f'<path class="loop" d="M {x0} {bottom} L 16 {bottom} L 16 {top} L {x0 - 2} {top}"/>'
               f'<polygon fill="{t["accent"]}" opacity=".7" points="{x0},{top} {x0 - 8},{top - 4} {x0 - 8},{top + 4}"/>'
               f'<text class="tiny" transform="translate(11 {(top + bottom) / 2}) rotate(-90)" text-anchor="middle">'
               f'fixes come back as commits</text>')
    return svg(W, by + oh + 12, t, anim, out)


def svg(w, h, t, anim, body):
    title = ("Delivery pipeline. Commit. Build and test with build, lint, unit tests and a secret scan in parallel. "
             "Package: the artifact goes to a registry. Provision: plan and apply create or change the servers. "
             "Deploy: a rolling update onto those servers. Observe runs 24/7 and alerts the on-call SRE or DevOps "
             "engineer; fixes come back as commits.")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">\n'
            f"<title>{esc(title)}</title>\n" + "\n".join(body) + f"\n{style(t, anim)}\n</svg>\n")


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "pipeline"
    out.mkdir(parents=True, exist_ok=True)
    for theme, t in THEMES.items():
        (out / f"{theme}.svg").write_text(wide(t), encoding="utf-8", newline="\n")
        (out / f"{theme}-narrow.svg").write_text(narrow(t), encoding="utf-8", newline="\n")
        (out / f"{theme}-vertical.svg").write_text(vertical(t), encoding="utf-8", newline="\n")
    print("written to", out)
