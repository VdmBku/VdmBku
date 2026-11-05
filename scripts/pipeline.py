"""Renders assets/pipeline/*.svg: the delivery pipeline picture at the top of the profile.

Also the shared module for the other pictures: THEMES, FONT, esc.

python scripts/pipeline.py
"""
from pathlib import Path

THEMES = {
    "light": dict(text="#1f2328", muted="#59636e", fill="#f6f8fa", stroke="#d0d7de", accent="#0f8a82", red="#cf222e"),
    "dark": dict(text="#e6edf3", muted="#9198a1", fill="#151b23", stroke="#3d444d", accent="#2fbfb4", red="#f85149"),
}
SLOW = 2.2  # every animation runs this many times slower than the timings written in the code
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
    "Shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6z"/><path d="M8.5 12.2l2.4 2.4 4.6-4.8"/>',
    "Mail": '<rect x="3" y="5.5" width="18" height="13" rx="2"/><path d="M3.5 7l8.5 6 8.5-6"/>',
    "Phone": '<path d="M6.5 3.5h3l1.5 4-2 1.3a11 11 0 0 0 6.2 6.2l1.3-2 4 1.5v3a2 2 0 0 1-2.2 2A17 17 0 0 1 4.5 5.7a2 2 0 0 1 2-2.2z"/>',
    "Bell": '<path d="M6 16V11a6 6 0 0 1 12 0v5l1.5 2h-15z"/><path d="M10 20a2 2 0 0 0 4 0"/>',
}

STAGES = [  # (title, subtitle, tool lines, lit from, lit until)
    ("Commit", "merge to main, tag", ["Git · GitLab · GitHub"], 0.0, 0.9),
    ("Build & test", "checks in parallel", ["Jenkins · GitLab CI", "GitHub Actions"], 0.9, 2.6),
    ("Package", "artifact to a registry", ["Docker · Harbor · Nexus"], 2.6, 3.6),
    ("Provision", "create or change infra", ["Terraform", "AWS · Azure · GCP · Hetzner"], 3.6, 5.0),
    ("Deploy", "registry to the cluster", ["Ansible · Helm · Argo CD"], 5.0, 6.7),
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
        self.rules.append(f".{c} {{ animation: {c} {CYCLE * SLOW:.2f}s linear infinite; }} @keyframes {c} {{ 0%, {pct(at - 0.05)} "
                          f"{{ opacity: {base} }} {pct(at + 0.1)}, {pct(HOLD)} {{ opacity: 1 }} {pct(HOLD + 0.4)}, 100% {{ opacity: {base} }} }}")
        return c

    def window(self, start, end, peak=1.0):
        c = self._cls()
        self.rules.append(f".{c} {{ animation: {c} {CYCLE * SLOW:.2f}s linear infinite; }} @keyframes {c} {{ 0%, {pct(start - 0.05)} "
                          f"{{ opacity: 0 }} {pct(start + 0.1)}, {pct(end)} {{ opacity: {peak} }} {pct(end + 0.25)}, 100% {{ opacity: 0 }} }}")
        return c

    def until(self, at):
        c = self._cls()
        self.rules.append(f".{c} {{ animation: {c} {CYCLE * SLOW:.2f}s linear infinite; }} @keyframes {c} {{ 0%, {pct(at - 0.05)} "
                          f"{{ opacity: 1 }} {pct(at + 0.1)}, {pct(HOLD)} {{ opacity: 0 }} {pct(HOLD + 0.4)}, 100% {{ opacity: 1 }} }}")
        return c

    def pop(self, start, end):
        c = self._cls()
        self.rules.append(f".{c} {{ transform-box: fill-box; transform-origin: left center; animation: {c} {CYCLE * SLOW:.2f}s ease-out infinite; }} "
                          f"@keyframes {c} {{ 0%, {pct(start)} {{ transform: scale(0) }} {pct(end)}, {pct(HOLD)} {{ transform: scale(1) }} "
                          f"{pct(HOLD + 0.4)}, 100% {{ transform: scale(0) }} }}")
        return c

    def grow(self, start, end):
        c = self._cls()
        self.rules.append(f".{c} {{ transform-box: fill-box; transform-origin: left center; animation: {c} {CYCLE * SLOW:.2f}s linear infinite; }} "
                          f"@keyframes {c} {{ 0%, {pct(start)} {{ transform: scaleX(0) }} {pct(end)}, {pct(HOLD)} {{ transform: scaleX(1) }} "
                          f"{pct(HOLD + 0.4)}, 100% {{ transform: scaleX(0) }} }}")
        return c

    def move(self, start, end, dx):
        c = self._cls()
        self.rules.append(f".{c} {{ animation: {c} {CYCLE * SLOW:.2f}s ease-in-out infinite; }} @keyframes {c} {{ 0%, {pct(start)} "
                          f"{{ transform: translateX(0) }} {pct(end)}, {pct(HOLD)} {{ transform: translateX({dx}px) }} "
                          f"{pct(HOLD + 0.4)}, 100% {{ transform: translateX(0) }} }}")
        return c

    def red(self, start, end):
        c = self._cls()
        self.rules.append(f".{c} {{ animation: {c} {CYCLE * SLOW:.2f}s linear infinite; }} @keyframes {c} {{ 0%, {pct(start - 0.05)} "
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
  .divider-v {{ stroke: {t['stroke']}; stroke-width: 1; stroke-dasharray: 2 4; }}
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
  .cloud-frame {{ fill: none; stroke: {t['stroke']}; stroke-width: 1.2; stroke-dasharray: 4 4; }}
  .fw {{ fill: {t['fill']}; stroke: {t['muted']}; stroke-width: 1.4; }}
  .fw-line {{ stroke: {t['muted']}; stroke-width: 1; }}
  .mark {{ font-size: 13px; font-weight: 700; fill: {t['accent']}; }}
  .ci {{ fill: {t['fill']}; stroke: {t['muted']}; stroke-width: 1.4; }}
  .ci-text {{ font-size: 10px; font-weight: 700; fill: {t['muted']}; }}
  .scan-card {{ fill: {t['fill']}; stroke: {t['muted']}; stroke-width: 1.3; stroke-dasharray: 5 4; }}
  .scan-title {{ font-size: 13px; font-weight: 600; fill: {t['text']}; }}
  .side {{ stroke: {t['muted']}; stroke-width: 1.2; stroke-dasharray: 3 3; fill: none; }}
  .glyph-tile {{ fill: #242938; }}
  .glyph {{ fill: none; stroke: #ffffff; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }}
  .ring {{ fill: none; stroke: {t['red']}; stroke-width: 2; }}
  .old-box-body {{ fill: {t['muted']}; fill-opacity: .18; }}
  .old-box-frame {{ fill: none; stroke: {t['muted']}; stroke-width: 1.4; }}
  .old-ridge {{ stroke: {t['muted']}; stroke-width: 1; opacity: .7; }}
  .box-body {{ fill: {t['accent']}; fill-opacity: .2; }}
  .box-frame {{ fill: none; stroke: {t['accent']}; stroke-width: 1.6; }}
  .ridge {{ stroke: {t['accent']}; stroke-width: 1.2; opacity: .75; }}
  .pulse {{ fill: none; stroke: {t['accent']}; stroke-width: 2; stroke-linejoin: round; animation: beat {1.2 * SLOW:.2f}s linear infinite; }}
  .live {{ fill: {t['accent']}; animation: blink {1.4 * SLOW:.2f}s ease-in-out infinite; }}
  .badge {{ fill: none; stroke: {t['accent']}; stroke-width: 1.2; }}
  .badge-text {{ font-size: 11px; font-weight: 700; fill: {t['accent']}; }}
  .alert {{ fill: {t['fill']}; stroke: {t['red']}; stroke-width: 1.8; }}
  .alert-icon {{ fill: none; stroke: {t['red']}; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }}
  .alert-title {{ font-size: 13px; font-weight: 700; fill: {t['red']}; }}
  .loop {{ fill: none; stroke: {t['accent']}; stroke-width: 1.5; stroke-dasharray: 5 5; opacity: .7; animation: flow {1.6 * SLOW:.2f}s linear infinite; }}
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
    """Two branches get commits, merge into main, and main gets a release tag."""
    tag_w = 40 if rw < 200 else 84
    span = rw - tag_w - 6
    X = lambda f: rx + span * f
    ya, ym, yb = ry + 10, ry + rh * 0.5, ry + rh - 10
    wide = rw >= 200
    out = [f'<line class="wire" x1="{rx}" y1="{ym}" x2="{rx + span}" y2="{ym}"/>',
           f'<path class="wire" d="M {X(.08)} {ym} C {X(.15)} {ym}, {X(.12)} {ya}, {X(.22)} {ya} L {X(.42)} {ya} '
           f'C {X(.50)} {ya}, {X(.46)} {ym}, {X(.55)} {ym}"/>',
           f'<path class="wire" d="M {X(.18)} {ym} C {X(.25)} {ym}, {X(.22)} {yb}, {X(.32)} {yb} L {X(.62)} {yb} '
           f'C {X(.70)} {yb}, {X(.66)} {ym}, {X(.75)} {ym}"/>',
           f'<circle class="dot" cx="{X(.03)}" cy="{ym}" r="4.5"/>',
           f'<text class="tiny" x="{X(.03)}" y="{ym + 16}" text-anchor="middle">v1.3</text>']
    if wide:
        out += [f'<text class="tiny" x="{X(.45)}" y="{ya + 3.5}">feature</text>',
                f'<text class="tiny" x="{X(.66)}" y="{yb + 3.5}">fix</text>',
                f'<text class="tiny" x="{X(.03)}" y="{ym - 9}" text-anchor="middle">main</text>']
    for f, y, at in ((.27, ya, .15), (.37, ya, .3), (.38, yb, .35), (.52, yb, .45)):
        out.append(f'<circle class="dot-on {anim.show(at)}" cx="{X(f)}" cy="{y}" r="4.5"/>')
    for f, at in ((.55, .5), (.75, .62)):
        c = anim.show(at)
        out.append(f'<circle class="dot {c}" cx="{X(f)}" cy="{ym}" r="6"/><circle class="dot-on {c}" cx="{X(f)}" cy="{ym}" r="3.5"/>')
    c = anim.show(.78)
    tx = rx + span + 6
    out.append(f'<g class="{c}"><line class="wire" x1="{X(.75) + 6}" y1="{ym}" x2="{tx}" y2="{ym}"/>'
               f'<rect class="chip" x="{tx}" y="{ym - 9}" width="{tag_w}" height="18" rx="9"/>'
               f'<text class="chip-text" x="{tx + tag_w / 2}" y="{ym + 4}" text-anchor="middle">{"release v1.4" if wide else "v1.4"}</text></g>')
    if not wide:
        out.append(f'<text class="tiny-on {c}" x="{tx + tag_w / 2}" y="{ym + 22}" text-anchor="middle">release</text>')
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


def container(x, y, w=44, h=20, old=False):
    """A shipping container: the image that goes to the registry. old=True draws the previous version, muted."""
    p = "old-" if old else ""
    ridges = "".join(f'<line class="{p}ridge" x1="{x + k}" y1="{y + 3}" x2="{x + k}" y2="{y + h - 3}"/>' for k in range(7, w - 3, 6))
    return (f'<rect class="{p}box-body" x="{x}" y="{y}" width="{w}" height="{h}" rx="2"/>{ridges}'
            f'<rect class="{p}box-frame" x="{x}" y="{y}" width="{w}" height="{h}" rx="2"/>')


VERSION_AT = {1: 0.9, 2: 2.6, 4: 5.0}   # stage index: when the v1.4 chip lights up on that card
DEPLOYED = 6.5                          # every node runs 1.4 from here


def ver_chip(anim, x, y, at):
    return (f'<g class="{anim.show(at)}"><rect class="chip" x="{x}" y="{y}" width="38" height="18" rx="9"/>'
            f'<text class="chip-text" x="{x + 19}" y="{y + 13}" text-anchor="middle">v1.4</text></g>')


def viz_package(anim, rx, ry, rw, rh):
    y = ry + rh / 2
    dbx = rx + rw - 40
    out = [f'<line class="wire" x1="{rx + 26}" y1="{y}" x2="{dbx - 4}" y2="{y}"/>',
           f'<ellipse class="db" cx="{dbx + 18}" cy="{y + 14}" rx="18" ry="5"/>'
           f'<rect class="db" x="{dbx}" y="{y - 12}" width="36" height="26" style="stroke-width:0"/>'
           f'<line class="db" x1="{dbx}" y1="{y - 12}" x2="{dbx}" y2="{y + 14}"/><line class="db" x1="{dbx + 36}" y1="{y - 12}" x2="{dbx + 36}" y2="{y + 14}"/>'
           f'<ellipse class="db" cx="{dbx + 18}" cy="{y - 12}" rx="18" ry="5"/>']
    if rw < 200:
        out.append(f'<text class="tiny" x="{dbx + 18}" y="{y + 30}" text-anchor="middle">container</text>'
                   f'<text class="tiny" x="{dbx + 18}" y="{y + 42}" text-anchor="middle">registry</text>')
    else:
        out.append(f'<text class="tiny" x="{dbx + 18}" y="{y + 32}" text-anchor="middle">container registry</text>')
    # built in CI: the container grows out of the CI box, then it is pushed along the line
    push = anim.move(3.05, 3.6, dbx - rx - 78)
    grow = anim.pop(2.6, 2.95)
    out.append(f'<g class="{push}"><g class="{grow}">{container(rx + 28, y - 10)}'
               f'<text class="chip-text" x="{rx + 50}" y="{y - 15}" text-anchor="middle">app:1.4</text></g></g>')
    out.append(f'<rect class="ci" x="{rx}" y="{y - 12}" width="26" height="24" rx="5"/>'
               f'<text class="ci-text" x="{rx + 13}" y="{y + 3.5}" text-anchor="middle">CI</text>'
               f'<text class="tiny" x="{rx + 13}" y="{y + 26}" text-anchor="middle">build</text>')
    out.append(f'<text class="tiny-on {anim.show(3.05)}" x="{(rx + 44 + dbx) / 2}" y="{y + 25}" text-anchor="middle">push</text>')
    out.append(tick(anim, dbx + 34, y - 16, 3.65, r=6))
    return "".join(out)


SRV_X = (0, 46, 92)


def viz_provision(anim, rx, ry, rw, rh):
    out = [f'<text class="tiny-on {anim.show(3.8)}" x="{rx}" y="{ry + 8}">plan: +2 servers, ~1 rule</text>',
           f'<text class="tiny-on {anim.show(4.25)}" x="{rx + rw - 6}" y="{ry + 26}" text-anchor="end">apply</text>',
           f'<rect class="cloud-frame" x="{rx}" y="{ry + 14}" width="{rw}" height="{rh - 14}" rx="8"/>',
           f'<text class="tiny" x="{rx + 6}" y="{ry + 26}">cloud</text>']
    iy = ry + 14 + (rh - 14) / 2 - 6
    # firewall: a small brick wall
    fx = rx + 8
    out.append(f'<rect class="fw" x="{fx}" y="{iy}" width="18" height="20" rx="2"/>'
               f'<line class="fw-line" x1="{fx}" y1="{iy + 7}" x2="{fx + 18}" y2="{iy + 7}"/>'
               f'<line class="fw-line" x1="{fx}" y1="{iy + 13}" x2="{fx + 18}" y2="{iy + 13}"/>'
               f'<line class="fw-line" x1="{fx + 9}" y1="{iy}" x2="{fx + 9}" y2="{iy + 7}"/>'
               f'<line class="fw-line" x1="{fx + 5}" y1="{iy + 7}" x2="{fx + 5}" y2="{iy + 13}"/>'
               f'<line class="fw-line" x1="{fx + 13}" y1="{iy + 13}" x2="{fx + 13}" y2="{iy + 20}"/>')
    c = anim.show(4.4)
    out.append(f'<rect class="srv-chg {c}" x="{fx - 3}" y="{iy - 3}" width="24" height="26" rx="4"/>'
               f'<text class="mark {c}" x="{fx + 22}" y="{iy - 2}">~</text>')
    step = min(46, (rw - 36 - 30) / 2)
    xs = [rx + 36 + k * step for k in range(3)]
    out.append(server(xs[0], iy - 1, w=30, h=22))
    for k, at in ((1, 4.6), (2, 4.8)):
        c = anim.show(at)
        out.append(f'<g class="{c}">{server(xs[k], iy - 1, "srv-new", w=30, h=22)}</g>'
                   f'<text class="mark {c}" x="{xs[k] + 26}" y="{iy - 3}">+</text>')
    return "".join(out)


def mini_registry(x, y):
    return (f'<ellipse class="db" cx="{x + 11}" cy="{y + 9}" rx="11" ry="3.5"/>'
            f'<rect class="db" x="{x}" y="{y - 8}" width="22" height="17" style="stroke-width:0"/>'
            f'<line class="db" x1="{x}" y1="{y - 8}" x2="{x}" y2="{y + 9}"/><line class="db" x1="{x + 22}" y1="{y - 8}" x2="{x + 22}" y2="{y + 9}"/>'
            f'<ellipse class="db" cx="{x + 11}" cy="{y - 8}" rx="11" ry="3.5"/>')


def viz_deploy(anim, rx, ry, rw, rh):
    fx = rx + 30
    out = [f'<text class="tiny {anim.show(5.15)}" x="{rx + rw}" y="{ry + 8}" text-anchor="end">rolling update</text>',
           f'<rect class="cloud-frame" x="{fx}" y="{ry + 14}" width="{rx + rw - fx}" height="{rh - 14}" rx="8"/>',
           f'<text class="tiny" x="{fx + 6}" y="{ry + 26}">cluster</text>']
    iy = ry + 14 + (rh - 14) / 2 - 8
    out.append(mini_registry(rx, iy + 11))
    out.append(f'<text class="tiny" x="{rx + 11}" y="{iy + 34}" text-anchor="middle">CR</text>')
    nw = 26
    step = min(46, (rx + rw - fx - 12 - nw) / 2)
    nodes = [fx + 8 + k * step for k in range(3)]
    for k, (nx, at) in enumerate(zip(nodes, (5.6, 6.0, 6.4))):
        out.append(server(nx, iy, w=nw, h=20))
        out.append(f'<g class="{anim.until(at)}">{container(nx + 9, iy + 5.5, w=14, h=9, old=True)}</g>')
        m = anim.move(at - 0.4, at, nx + 9 - (rx + 4))
        c = anim.window(at - 0.45, at)
        out.append(f'<g class="{c}"><g class="{m}">{container(rx + 4, iy + 5.5, w=14, h=9)}</g></g>')
        out.append(f'<g class="{anim.show(at)}">{container(nx + 9, iy + 5.5, w=14, h=9)}</g>')
        out.append(f'<text class="tiny {anim.until(at)}" x="{nx + nw / 2}" y="{iy + 32}" text-anchor="middle">1.3</text>'
                   f'<text class="tiny-on {anim.show(at)}" x="{nx + nw / 2}" y="{iy + 32}" text-anchor="middle">1.4</text>')
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
            f'<g clip-path="url(#{clip})"><path class="pulse" d="{d}" style="animation: beat {1.2 * SLOW:.2f}s linear infinite, '
            f'{anim.red(*ALERT)} {CYCLE * SLOW:.2f}s linear infinite"/></g>')


def alert(anim, x, y, w):
    c = anim.window(*ALERT)
    return (f'<g class="{c}"><rect class="alert" x="{x}" y="{y}" width="{w}" height="46" rx="10"/>'
            f'{icon("Bell", x + 12, y + 12, 22, "alert-icon")}'
            f'<text class="alert-title" x="{x + 44}" y="{y + 20}">Alert</text>'
            f'<text class="what" x="{x + 44}" y="{y + 36}">on-call SRE / DevOps notified</text></g>')


def scan_card(anim, x, y, w, h, two_lines=False):
    out = [f'<rect class="scan-card" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>',
           icon("Shield", x + 12, y + h / 2 - 11, 22),
           f'<text class="scan-title" x="{x + 44}" y="{y + 21}">Container scan</text>']
    if two_lines:
        out.append(f'<text class="what" x="{x + 44}" y="{y + 37}">image vulnerabilities</text>'
                   f'<text class="tiny" x="{x + 44}" y="{y + 51}">outside the main pipeline</text>')
    else:
        out.append(f'<text class="what" x="{x + 44}" y="{y + 38}">image vulnerabilities, outside the main pipeline</text>')
    bx, bw = x + w - 96, 58
    out.append(f'<rect class="slot" x="{bx}" y="{y + h / 2 - 3}" width="{bw}" height="6" rx="3"/>'
               f'<rect class="bar {anim.grow(3.7, 4.9)}" x="{bx}" y="{y + h / 2 - 3}" width="{bw}" height="6" rx="3"/>')
    out.append(tick(anim, x + w - 22, y + h / 2, 4.95, r=6))
    return "".join(out)


def card(anim, i, x, y, w, h, narrow=False):
    title, sub, tools, t0, t1 = STAGES[i]
    out = [f'<rect class="card" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>',
           f'<rect class="hl {anim.window(t0, t1)}" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>',
           f'<text class="num" x="{x + 14}" y="{y + 24}">{i + 1:02d}</text>']
    if i in VERSION_AT:
        out.append(ver_chip(anim, x + w - 52, y + 33, VERSION_AT[i]) if not narrow else ver_chip(anim, x + 150, y + 10, VERSION_AT[i]))
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


def watchers(anim, x, y):
    """What Observe keeps an eye on: always on. The app badge shows the version that runs."""
    out = [f'<rect class="badge" x="{x}" y="{y}" width="86" height="18" rx="9"/>'
           f'<circle class="live" cx="{x + 11}" cy="{y + 9}" r="3.5"/>'
           f'<text class="badge-text {anim.until(DEPLOYED)}" x="{x + 20}" y="{y + 13}">app v1.3</text>'
           f'<text class="badge-text {anim.show(DEPLOYED)}" x="{x + 20}" y="{y + 13}">app v1.4</text>']
    for k, label in enumerate(("metrics", "cluster")):
        bx = x + 96 + k * 82
        out.append(f'<rect class="badge" x="{bx}" y="{y}" width="72" height="18" rx="9"/>'
                   f'<circle class="live" cx="{bx + 11}" cy="{y + 9}" r="3.5"/>'
                   f'<text class="badge-text" x="{bx + 20}" y="{y + 13}">{label}</text>')
    return "".join(out)


CHANNELS = [("slack", "Slack"), ("teams", "Teams"), ("Mail", "email"), ("Phone", "on-call")]


def channel_icon(name, x, y, size):
    if name[0].isupper():            # a line icon on a dark tile
        return (f'<rect class="glyph-tile" x="{x}" y="{y}" width="{size}" height="{size}" rx="{size * .23:.1f}"/>'
                f'{icon(name, x + size * .2, y + size * .2, size * .6, "glyph")}')
    return tool_icon(name, x, y, size)


def channels(anim, x, y, size=24, gap=12):
    out = [f'<text class="tiny" x="{x}" y="{y - 6}">team channels</text>']
    for k, (name, label) in enumerate(CHANNELS):
        cx = x + k * (size + gap)
        out.append(channel_icon(name, cx, y, size))
        out.append(f'<rect class="ring {anim.window(ALERT[0] + 0.25 * k, ALERT[1])}" x="{cx - 3}" y="{y - 3}" '
                   f'width="{size + 6}" height="{size + 6}" rx="{size * .3:.1f}"/>')
        out.append(f'<text class="tiny" x="{cx + size / 2}" y="{y + size + 12}" text-anchor="middle">{label}</text>')
    return "".join(out)


def observe(anim, x, y, w, h, narrow=False):
    out = [f'<rect class="card" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>',
           f'<text class="num" x="{x + 14}" y="{y + 24}">06</text>',
           f'<text class="name" x="{x + 44}" y="{y + 24}">Observe</text>',
           f'<rect class="badge" x="{x + 112}" y="{y + 10}" width="50" height="19" rx="9.5"/>'
           f'<circle class="live" cx="{x + 123}" cy="{y + 19.5}" r="3.5"/>'
           f'<text class="badge-text" x="{x + 131}" y="{y + 24}">24/7</text>',
           f'<text class="what" x="{x + 14}" y="{y + 46}">watches apps, metrics and the cluster</text>',
           f'<text class="tool" x="{x + 14}" y="{y + 64}">{esc(OBSERVE_TOOLS)}</text>']
    if not narrow:
        out.append(watchers(anim, x + 300, y + 12))
        out.append(pulse(anim, x + 300, y + 34, 330, 50, "beat-w"))
        out.append(channels(anim, x + w - 226, y + 26))
        out.append(alert(anim, x + w - 226, y + 72, 212))
    else:
        out.append(watchers(anim, x + 14, y + 76))
        out.append(pulse(anim, x + 14, y + 96, w - 28, 40, "beat-n"))
        out.append(channels(anim, x + 14, y + 160))
        out.append(alert(anim, x + 14, y + 206, w - 28))
    return "".join(out)


def wide(t):
    W = 960
    anim, out = Anim(), []
    cw, gap, cy, ch = 172, 15, 16, 200
    xs = [20 + i * (cw + gap) for i in range(len(STAGES))]
    for i, x in enumerate(xs):
        out.append(card(anim, i, x, cy, cw, ch))
        if i:
            out.append(arrow(x - gap + 2, cy + 46, x - 1, cy + 46))
    sy, sh = cy + ch + 18, 60
    out.append(f'<path class="side" d="M {xs[2] + cw / 2} {cy + ch} L {xs[2] + cw / 2} {sy}"/>')
    out.append(scan_card(anim, xs[2], sy, 2 * cw + gap, sh, two_lines=True))
    by = sy + sh + 22
    out.append(observe(anim, 20, by, W - 40, 128))
    # deployed apps and the cluster are watched; incidents come back as commits
    out.append(arrow(xs[-1] + cw / 2, cy + ch + 2, xs[-1] + cw / 2, by - 1))
    out.append(f'<path class="loop" d="M 60 {by} L 60 {cy + ch + 4}"/>'
               f'<polygon fill="{t["accent"]}" opacity=".7" points="60,{cy + ch + 2} 56,{cy + ch + 9} 64,{cy + ch + 9}"/>'
               f'<text class="tiny" x="70" y="{cy + ch + 19}">fixes come back as commits</text>')
    return svg(W, by + 128 + 14, t, anim, out)


def narrow(t):
    W = 400
    anim, out = Anim(), []
    ch, gap, sh = 96, 16, 62
    ys, y = [], 12
    for i in range(len(STAGES)):
        ys.append(y)
        y += ch + gap + (sh + gap if i == 2 else 0)
    for i, y in enumerate(ys):
        out.append(card(anim, i, 12, y, W - 24, ch, narrow=True))
        if i:
            out.append(arrow(40, ys[i - 1] + ch + 2, 40, y - 1))
    sy = ys[2] + ch + gap
    out.append(f'<path class="side" d="M 230 {ys[2] + ch} L 230 {sy}"/>')
    out.append(scan_card(anim, 60, sy, W - 72, sh, two_lines=True))
    by = ys[-1] + ch + gap
    out.append(arrow(40, by - gap + 2, 40, by - 1))
    out.append(observe(anim, 12, by, W - 24, 264, narrow=True))
    return svg(W, by + 276, t, anim, out)


TOOLS = {  # icon file in assets/icons, label
    "Commit": [("git", "Git"), ("gitlab", "GitLab"), ("github", "GitHub")],
    "Build & test": [("jenkins", "Jenkins"), ("gitlab", "GitLab CI"), ("github-actions", "GitHub Actions")],
    "Package": [("docker", "Docker"), ("harbor", "Harbor"), ("nexus", "Nexus")],
    "Provision": [("terraform", "Terraform"), ("aws", "AWS"), ("azure", "Azure"), ("gcp", "GCP"), ("hetzner", "Hetzner")],
    "Deploy": [("ansible", "Ansible"), ("helm", "Helm"), ("argo-cd", "Argo CD"), ("kubernetes", "Kubernetes")],
    "Observe": [("prometheus", "Prometheus"), ("grafana", "Grafana"), ("zabbix", "Zabbix"), ("wazuh", "Wazuh")],
}
ICON_DIR = Path(__file__).resolve().parent.parent / "assets" / "icons"


def tool_icon(name, x, y, size):
    """Inline one icon tile as a nested svg; ids get a prefix so icons cannot clash."""
    import re
    raw = (ICON_DIR / f"{name}.svg").read_text(encoding="utf-8")
    inner = re.search(r"<svg[^>]*>(.*)</svg>", raw, re.S).group(1)
    ids = set(re.findall(r'id="([^"]+)"', inner))
    for i in ids:
        inner = inner.replace(f'id="{i}"', f'id="{name}-{i}"').replace(f"url(#{i})", f"url(#{name}-{i})").replace(f'href="#{i}"', f'href="#{name}-{i}"')
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 256 256">{inner}</svg>'


def tools_column(stage, x, y, h):
    items = TOOLS[stage]
    size, gap = 30, 8
    iy = y + h / 2 - size / 2 - 8
    out = [tool_icon(name, x + k * (size + gap), iy, size) for k, (name, _) in enumerate(items)]
    out.append(f'<text class="tool" x="{x}" y="{iy + size + 17}">{esc(" · ".join(label for _, label in items))}</text>')
    return "".join(out)


def vertical(t):
    W, x0 = 920, 44
    anim, out = Anim(), []
    ch, gap, cw, sh = 104, 20, 600, 60
    tx = x0 + cw + 28
    ys, yy = [], 12
    for i in range(len(STAGES)):
        ys.append(yy)
        yy += ch + gap + (sh + gap if i == 2 else 0)
    for i, y in enumerate(ys):
        title, sub, tools, t0, t1 = STAGES[i]
        out += [f'<rect class="card" x="{x0}" y="{y}" width="{cw}" height="{ch}" rx="10"/>',
                f'<rect class="hl {anim.window(t0, t1)}" x="{x0}" y="{y}" width="{cw}" height="{ch}" rx="10"/>',
                f'<text class="num" x="{x0 + 14}" y="{y + 26}">{i + 1:02d}</text>',
                icon(title, x0 + 40, y + 10),
                ver_chip(anim, x0 + 200, y + 12, VERSION_AT[i]) if i in VERSION_AT else "",
                f'<text class="name" x="{x0 + 70}" y="{y + 26}">{esc(title)}</text>',
                f'<text class="what" x="{x0 + 14}" y="{y + 48}">{esc(sub)}</text>']
        out.append(VIZ[i](anim, x0 + 250, y + 14, cw - 270, ch - 28))
        out.append(f'<line class="divider-v" x1="{x0 + cw + 1}" y1="{y + ch / 2}" x2="{tx - 8}" y2="{y + ch / 2}"/>')
        out.append(tools_column(title, tx, y, ch))
        if i:
            out.append(arrow(x0 + 26, ys[i - 1] + ch + 2, x0 + 26, y - 1))
    sy = ys[2] + ch + gap
    out.append(f'<path class="side" d="M {x0 + 360} {ys[2] + ch} L {x0 + 360} {sy}"/>')
    out.append(scan_card(anim, x0 + 48, sy, cw - 48, sh, two_lines=True))
    by = ys[-1] + ch + gap
    out.append(arrow(x0 + 26, by - gap + 2, x0 + 26, by - 1))
    oh = 184
    out += [f'<rect class="card" x="{x0}" y="{by}" width="{cw}" height="{oh}" rx="10"/>',
            f'<text class="num" x="{x0 + 14}" y="{by + 26}">06</text>',
            icon("Observe", x0 + 40, by + 10),
            f'<text class="name" x="{x0 + 70}" y="{by + 26}">Observe</text>',
            f'<rect class="badge" x="{x0 + 138}" y="{by + 12}" width="50" height="19" rx="9.5"/>'
            f'<circle class="live" cx="{x0 + 149}" cy="{by + 21.5}" r="3.5"/>'
            f'<text class="badge-text" x="{x0 + 157}" y="{by + 26}">24/7</text>',
            f'<text class="what" x="{x0 + 14}" y="{by + 48}">watches apps, metrics</text>',
            f'<text class="what" x="{x0 + 14}" y="{by + 64}">and the cluster</text>',
            watchers(anim, x0 + 250, by + 10),
            pulse(anim, x0 + 250, by + 32, cw - 270, 36, "beat-v"),
            channels(anim, x0 + 250, by + 84, size=22, gap=22),
            alert(anim, x0 + 250, by + 128, cw - 270),
            f'<line class="divider-v" x1="{x0 + cw + 1}" y1="{by + oh / 2}" x2="{tx - 8}" y2="{by + oh / 2}"/>',
            tools_column("Observe", tx, by, oh)]
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
