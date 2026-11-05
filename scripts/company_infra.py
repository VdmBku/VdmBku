"""Renders assets/company-infra/*.svg: every server described in code, and one baseline for every new server.

A Terraform server module creates each server with its own firewall, a primary IP and a private network
attachment. Internal services and every client project are separate stacks on Hetzner Cloud. A new server
then goes through one Jenkins pipeline with Ansible: the inventory is built at run time, secrets come from
Ansible Vault, each part is switched on or off for the run, and the server ends in the same baseline as the rest.

python scripts/company_infra.py
"""
from pathlib import Path

from pipeline import FONT, SLOW, THEMES, esc, tool_icon

HOLD, CYCLE = 11.0, 11.8

PARTS = [  # what the module creates for the new server, and when it appears
    ("server", 0.8),
    ("own firewall", 1.3),
    ("primary IP", 1.8),
    ("private network", 2.3),
]
APPLY = 0.4             # terraform apply starts
HANDOVER = 2.7          # the new server goes to the baseline pipeline
STEPS = [  # (title, subtitle, done)
    ("Jenkins run", "for the new server", 3.2),
    ("Inventory", "built at run time", 3.7),
    ("Secrets", "from Ansible Vault", 4.2),
    ("Ansible", "each part on or off per run", 7.7),
]
BASELINED = 8.2
# the switchable parts in two columns; False means switched off for this run
CHECKS = [[("Docker", False), ("log rotation", True), ("security updates", True), ("fail2ban", True)],
          [("Zabbix agent", True), ("Wazuh agent", True), ("hardening", True), ("users", True)]]
NOTES = ["hardening: SSH, audit, file integrity, AppArmor", "users: a simple form in Jenkins"]
INTERNAL = ["CI master", "CI worker", "ARM worker", "Git + runner", "registry", "monitoring", "security", "logging", "files"]
CLIENTS = ["client A", "client B"]      # client B gets the new server


def check_times():
    """Ticks run down the first column, then the second; a part that is off is skipped."""
    at, out = 4.6, {}
    for col in CHECKS:
        for label, on in col:
            if on:
                out[label] = at
                at += 0.45
    return out


def pct(t):
    return f"{t / CYCLE * 100:.2f}%"


class Anim:
    """One keyframes rule per animated element; class names start with q."""

    def __init__(self):
        self.rules, self.n = [], 0

    def _cls(self):
        self.n += 1
        return f"q{self.n}"

    def show(self, at):
        c = self._cls()
        self.rules.append(f".{c} {{ animation: {c} {CYCLE * SLOW:.2f}s linear infinite; }} @keyframes {c} {{ 0%, {pct(at - 0.05)} "
                          f"{{ opacity: 0 }} {pct(at + 0.1)}, {pct(HOLD)} {{ opacity: 1 }} {pct(HOLD + 0.4)}, 100% {{ opacity: 0 }} }}")
        return c

    def window(self, start, end):
        c = self._cls()
        self.rules.append(f".{c} {{ animation: {c} {CYCLE * SLOW:.2f}s linear infinite; }} @keyframes {c} {{ 0%, {pct(start - 0.05)} "
                          f"{{ opacity: 0 }} {pct(start + 0.1)}, {pct(end)} {{ opacity: 1 }} {pct(end + 0.25)}, 100% {{ opacity: 0 }} }}")
        return c


def style(t, anim):
    return f"""<style>
  text {{ font-family: {FONT}; }}
  .card {{ fill: {t['fill']}; stroke: {t['stroke']}; stroke-width: 1; }}
  .hl {{ fill: none; stroke: {t['accent']}; stroke-width: 2; }}
  .name {{ font-size: 15px; font-weight: 600; fill: {t['text']}; }}
  .what {{ font-size: 12px; fill: {t['muted']}; }}
  .title {{ font-size: 13px; font-weight: 600; fill: {t['text']}; }}
  .label {{ font-size: 11.5px; fill: {t['text']}; }}
  .label-off {{ font-size: 11.5px; fill: {t['muted']}; }}
  .tiny {{ font-size: 10.5px; fill: {t['muted']}; }}
  .tiny-on {{ font-size: 10.5px; font-weight: 600; fill: {t['accent']}; }}
  .frame {{ fill: none; stroke: {t['stroke']}; stroke-width: 1.5; stroke-dasharray: 6 5; }}
  .frame-title {{ font-size: 13px; font-weight: 600; fill: {t['text']}; }}
  .stack {{ fill: none; stroke: {t['stroke']}; stroke-width: 1.2; stroke-dasharray: 3 3; }}
  .stack-title {{ font-size: 12px; font-weight: 600; fill: {t['text']}; }}
  .module {{ fill: none; stroke: {t['muted']}; stroke-width: 1.2; stroke-dasharray: 4 3; }}
  .srv {{ fill: {t['fill']}; stroke: {t['muted']}; stroke-width: 1.4; }}
  .srv-new {{ fill: {t['fill']}; stroke: {t['accent']}; stroke-width: 1.6; stroke-dasharray: 3 2; }}
  .srv-done {{ fill: {t['accent']}; fill-opacity: .2; stroke: {t['accent']}; stroke-width: 1.8; }}
  .srv-led {{ fill: {t['muted']}; }}
  .led-on {{ fill: {t['accent']}; }}
  .srv-line {{ stroke: {t['muted']}; stroke-width: 1.2; }}
  .fw {{ fill: {t['fill']}; stroke: {t['muted']}; stroke-width: 1.2; }}
  .fw-line {{ stroke: {t['muted']}; stroke-width: .9; }}
  .fw-new {{ fill: {t['fill']}; stroke: {t['accent']}; stroke-width: 1.4; }}
  .fw-line-new {{ stroke: {t['accent']}; stroke-width: .9; }}
  .ipb {{ fill: {t['fill']}; stroke: {t['muted']}; stroke-width: 1; }}
  .ipb-text {{ font-size: 7px; font-weight: 700; fill: {t['muted']}; }}
  .ipb-new {{ fill: {t['fill']}; stroke: {t['accent']}; stroke-width: 1.2; }}
  .ipb-text-new {{ font-size: 7px; font-weight: 700; fill: {t['accent']}; }}
  .rail {{ stroke: {t['muted']}; stroke-width: 1.6; stroke-linecap: round; opacity: .55; }}
  .net {{ stroke: {t['muted']}; stroke-width: 1.2; opacity: .8; }}
  .net-dot {{ fill: {t['muted']}; }}
  .net-new {{ stroke: {t['accent']}; stroke-width: 1.8; }}
  .net-dot-new {{ fill: {t['accent']}; }}
  .wire {{ stroke: {t['stroke']}; stroke-width: 3; stroke-linecap: round; }}
  .wire-on {{ stroke: {t['accent']}; stroke-width: 3; stroke-linecap: round; opacity: 0; }}
  .node {{ fill: {t['fill']}; stroke: {t['stroke']}; stroke-width: 2; }}
  .done {{ fill: {t['accent']}; opacity: 0; }}
  .tick {{ fill: none; stroke: #ffffff; stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; opacity: 0; }}
  .ok {{ fill: {t['accent']}; }}
  .okv {{ fill: none; stroke: #ffffff; stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round; }}
  .pend {{ fill: none; stroke: {t['stroke']}; stroke-width: 1.3; }}
  .pill {{ fill: none; stroke: {t['stroke']}; stroke-width: 1.2; }}
  .pill-text {{ font-size: 11px; fill: {t['muted']}; }}
  .pill-on {{ fill: {t['accent']}; fill-opacity: .14; stroke: {t['accent']}; stroke-width: 1.4; }}
  .pill-text-on {{ font-size: 11px; font-weight: 600; fill: {t['accent']}; }}
  .tg-on {{ fill: {t['accent']}; }}
  .tg-off {{ fill: none; stroke: {t['muted']}; stroke-width: 1.2; }}
  .knob {{ fill: #ffffff; }}
  .knob-off {{ fill: {t['muted']}; }}
  .badge {{ fill: none; stroke: {t['accent']}; stroke-width: 1.2; }}
  .badge-text {{ font-size: 10.5px; font-weight: 700; fill: {t['accent']}; }}
  .chip {{ fill: {t['fill']}; stroke: {t['accent']}; stroke-width: 1.5; }}
  .chip-text {{ font-size: 11px; font-weight: 600; fill: {t['text']}; }}
  .step-line {{ stroke: {t['muted']}; stroke-width: 2; }}
  .step-head {{ fill: {t['muted']}; }}
  .step-line-on {{ stroke: {t['accent']}; stroke-width: 2; }}
  .step-head-on {{ fill: {t['accent']}; }}
  {' '.join(anim.rules)}
  @media (prefers-reduced-motion: reduce) {{
    [class^="q"], [class*=" q"] {{ animation: none !important; opacity: 1 !important; transform: none !important; }} }}
</style>"""


# small pieces

def tick(anim, x, y, at, r=5.5):
    return (f'<g class="{anim.show(at)}"><circle class="ok" cx="{x}" cy="{y}" r="{r}"/>'
            f'<path class="okv" d="M {x - r * .45:.1f} {y + .3:.1f} l {r * .3:.1f} {r * .3:.1f} l {r * .6:.1f} {-r * .65:.1f}"/></g>')


def node(anim, x, y, done, r=9):
    on = anim.show(done)
    return (f'<circle class="node" cx="{x}" cy="{y}" r="{r}"/>'
            f'<circle class="done {on}" cx="{x}" cy="{y}" r="{r}"/>'
            f'<path class="tick {on}" d="M {x - 4} {y + 0.5} l 2.7 2.7 l 5.4 -5.9"/>')


def arrow(anim, x1, y1, x2, y2, at):
    """A step arrow between two blocks; it turns accent at `at`."""
    def draw(line, head):
        if y1 == y2:
            return (f'<line class="{line}" x1="{x1}" y1="{y1}" x2="{x2 - 7}" y2="{y2}"/>'
                    f'<polygon class="{head}" points="{x2},{y2} {x2 - 8},{y2 - 5} {x2 - 8},{y2 + 5}"/>')
        return (f'<line class="{line}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2 - 7}"/>'
                f'<polygon class="{head}" points="{x2},{y2} {x2 - 5},{y2 - 8} {x2 + 5},{y2 - 8}"/>')
    return draw("step-line", "step-head") + f'<g class="{anim.show(at)}">{draw("step-line-on", "step-head-on")}</g>'


def box(x, y, w=32, h=20, cls="srv", led="srv-led"):
    return (f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="4"/>'
            f'<circle class="{led}" cx="{x + 7}" cy="{y + h / 2}" r="2"/>'
            f'<line class="srv-line" x1="{x + 13}" y1="{y + h / 2}" x2="{x + w - 6}" y2="{y + h / 2}"/>')


def brick(x, y, w=11, h=20, new=False):
    """The server's own firewall: a small brick wall."""
    s = "-new" if new else ""
    return (f'<rect class="fw{s}" x="{x}" y="{y}" width="{w}" height="{h}" rx="1.5"/>'
            f'<line class="fw-line{s}" x1="{x}" y1="{y + h / 3:.1f}" x2="{x + w}" y2="{y + h / 3:.1f}"/>'
            f'<line class="fw-line{s}" x1="{x}" y1="{y + 2 * h / 3:.1f}" x2="{x + w}" y2="{y + 2 * h / 3:.1f}"/>'
            f'<line class="fw-line{s}" x1="{x + w / 2:.1f}" y1="{y}" x2="{x + w / 2:.1f}" y2="{y + h / 3:.1f}"/>'
            f'<line class="fw-line{s}" x1="{x + w * .3:.1f}" y1="{y + h / 3:.1f}" x2="{x + w * .3:.1f}" y2="{y + 2 * h / 3:.1f}"/>'
            f'<line class="fw-line{s}" x1="{x + w * .7:.1f}" y1="{y + 2 * h / 3:.1f}" x2="{x + w * .7:.1f}" y2="{y + h}"/>')


def ip_badge(x, y, new=False):
    s = "-new" if new else ""
    return (f'<rect class="ipb{s}" x="{x}" y="{y}" width="15" height="10" rx="5"/>'
            f'<text class="ipb-text{s}" x="{x + 7.5}" y="{y + 7.6}" text-anchor="middle">IP</text>')


UNIT_W = 45     # firewall 11, gap 2, server 32


def unit(anim, x, y, rail_y, new=False):
    """One server as the module makes it: own firewall on the left, primary IP on the corner,
    a link down to the private network. new=True builds it part by part during the cycle."""
    bx, sx = x + 13, x + 13 + 16
    stub = (f'<line class="net{"-new" if new else ""}" x1="{sx}" y1="{y + 20}" x2="{sx}" y2="{rail_y}"/>'
            f'<circle class="net-dot{"-new" if new else ""}" cx="{sx}" cy="{rail_y}" r="2.2"/>')
    if not new:
        return stub + brick(x, y) + box(bx, y, led="led-on") + ip_badge(bx + 21, y - 6)
    at = dict(PARTS)
    done = anim.show(BASELINED)
    return (f'<g class="{anim.show(at["private network"])}">{stub}</g>'
            f'<g class="{anim.show(at["own firewall"])}">{brick(x, y, new=True)}</g>'
            f'<g class="{anim.show(at["server"])}">{box(bx, y, cls="srv-new")}</g>'
            f'<g class="{done}">{box(bx, y, cls="srv-done", led="led-on")}</g>'
            f'<g class="{anim.show(at["primary IP"])}">{ip_badge(bx + 21, y - 6, new=True)}</g>')


def rail(x1, x2, y):
    return f'<line class="rail" x1="{x1}" y1="{y}" x2="{x2}" y2="{y}"/>'


# the three blocks

def legend_glyph(name, x, cy):
    if name == "server":
        return box(x, cy - 9, w=30, h=18)
    if name == "own firewall":
        return brick(x + 9, cy - 9, h=18)
    if name == "primary IP":
        return ip_badge(x + 7, cy - 5)
    return (rail(x + 2, x + 28, cy + 6) + f'<line class="net" x1="{x + 15}" y1="{cy - 7}" x2="{x + 15}" y2="{cy + 6}"/>'
            f'<circle class="net-dot" cx="{x + 15}" cy="{cy + 6}" r="2.2"/>')


def module_card(anim, x, y, w, h=None, cols=1):
    """Terraform: the one server module, what it creates for every server, and the stacks that use it.
    Without h the card is just tall enough for its content."""
    rows = (len(PARTS) + cols - 1) // cols
    bx, by, bw, bh = x + 12, y + 62, w - 24, 34 + rows * 30
    sy = by + bh + 24                       # "used by every stack" and one pill per stack under it
    pills_h = 3 * 26 if cols == 1 else 26
    h = h or sy + 8 + pills_h + 6 - y
    out = [f'<rect class="card" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>',
           f'<rect class="hl {anim.window(APPLY - 0.2, HANDOVER)}" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>',
           tool_icon("terraform", x + w - 34, y + 12, 22),
           f'<text class="name" x="{x + 14}" y="{y + 30}">Terraform</text>',
           f'<text class="what" x="{x + 14}" y="{y + 48}">one module for every server</text>']
    out.append(f'<rect class="module" x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="8"/>'
               f'<text class="tiny" x="{bx + 12}" y="{by + 18}">each server gets</text>')
    cw = bw / cols
    for i, (name, at) in enumerate(PARTS):
        r, c = i % rows, i // rows
        gx, cy = bx + 12 + c * cw, by + 40 + r * 30
        out.append(legend_glyph(name, gx, cy))
        out.append(f'<text class="label" x="{gx + 38}" y="{cy + 4}">{esc(name)}</text>')
        out.append(tick(anim, bx + (c + 1) * cw - 16, cy, at))
    out.append(f'<text class="tiny" x="{x + 14}" y="{sy}">used by every stack</text>')
    px, py = x + 14, sy + 8
    names = ["internal services"] + CLIENTS
    for name in names:
        pw = 22 + (max(map(len, names)) if cols == 1 else len(name)) * 6.1
        lit = name == CLIENTS[1]
        out.append(pill(px, py, pw, name))
        if lit:
            out.append(f'<g class="{anim.show(APPLY)}">{pill(px, py, pw, name, on=True)}</g>')
        if cols == 1:
            py += 26
        else:
            px += pw + 8
    if cols == 1:
        out.append(f'<text class="tiny-on {anim.show(APPLY)}" x="{x + 14}" y="{py + 12}">apply: +1 server</text>')
    return "".join(out), h


def pill(x, y, w, text, on=False):
    s = "-on" if on else ""
    return (f'<rect class="pill{s}" x="{x}" y="{y}" width="{w:.1f}" height="19" rx="9.5"/>'
            f'<text class="pill-text{s}" x="{x + w / 2:.1f}" y="{y + 13}" text-anchor="middle">{esc(text)}</text>')


def stack_frame(x, y, w, h, title):
    return (f'<rect class="stack" x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>'
            f'<text class="stack-title" x="{x + 12}" y="{y + 19}">{esc(title)}</text>')


def clients_row(anim, x, y, w, gap=12):
    out, cw = [], (w - gap) / 2
    step = min(56, (cw - 14 - 49 - 8) // 2)     # three servers; the IP badge reaches 4 px past the server
    for k, name in enumerate(CLIENTS):
        fx = x + k * (cw + gap)
        out.append(stack_frame(fx, y, cw, 76, name))
        uy, ry = y + 34, y + 64
        out.append(rail(fx + 10, fx + cw - 10, ry))
        for j in range(3):
            new = k == 1 and j == 2
            out.append(unit(anim, fx + 14 + j * step, uy, ry, new=new))
        if k == 1:
            out.append(f'<g class="{anim.show(BASELINED)}"><rect class="chip" x="{fx + cw - 82}" y="{y + 7}" width="72" height="18" rx="9"/>'
                       f'<text class="chip-text" x="{fx + cw - 46}" y="{y + 20}" text-anchor="middle">baselined</text></g>')
    new_mid = (x + cw + gap + 14 + 2 * step + UNIT_W / 2, y + 44)
    return "".join(out), 76, new_mid


def internal_stack(x, y, w, above=False, extra=0):
    rows, cols = 3, 3
    step, first = (58, 50) if above else (50, 34)
    h = first + (rows - 1) * step + 32 + 14 + extra  # the last rail plus a margin, plus any stretch
    add = extra // rows                               # stretch: a bit more between rows, the rest above and below
    step += add
    first += (extra - (rows - 1) * add) // 2
    out = [stack_frame(x, y, w, h, "internal services")]
    cw = (w - 24) / cols
    spine = x + 10
    rails = []
    for r in range(rows):
        uy = y + first + r * step
        ry = uy + 32
        rails.append(ry)
        out.append(rail(spine, x + w - 10, ry))
        for c in range(cols):
            ux = x + 20 + c * cw
            name = esc(INTERNAL[r * cols + c])
            out.append(unit(None, ux, uy, ry))
            if above:
                out.append(f'<text class="label" x="{ux}" y="{uy - 10}">{name}</text>')
            else:
                out.append(f'<text class="label" x="{ux + UNIT_W + 7}" y="{uy + 14}">{name}</text>')
    out.append(f'<line class="rail" x1="{spine}" y1="{rails[0]}" x2="{spine}" y2="{rails[-1]}"/>')
    return "".join(out), h


def cloud(anim, x, y, w, clients_first=True, min_h=0, pad=12):
    """Hetzner Cloud: internal services and each client project as separate stacks."""
    out = [tool_icon("hetzner", x + 12, y + 11, 18),
           f'<text class="frame-title" x="{x + 38}" y="{y + 25}">Hetzner Cloud</text>',
           f'<text class="tiny" x="{x + w - 12}" y="{y + 25}" text-anchor="end">separate stacks</text>']
    iw = w - 2 * pad
    if clients_first:
        cl, ch, new_mid = clients_row(anim, x + pad, y + 40, iw, pad)
        _, ih = internal_stack(x + pad, 0, iw)          # unstretched height, to see how much is left to fill
        it, ih = internal_stack(x + pad, y + 40 + ch + 12, iw, extra=max(0, min_h - (40 + ch + 12 + ih + 12)))
    else:
        it, ih = internal_stack(x + pad, y + 40, iw, above=True)
        cl, ch, new_mid = clients_row(anim, x + pad, y + 40 + ih + 12, iw, pad)
    h = 40 + ch + 12 + ih + 12
    out += [cl, it, f'<rect class="frame" x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/>']
    return "".join(out), h, new_mid


def toggle(x, cy, on):
    if on:
        return (f'<rect class="tg-on" x="{x}" y="{cy - 5.5}" width="20" height="11" rx="5.5"/>'
                f'<circle class="knob" cx="{x + 14.5}" cy="{cy}" r="3.6"/>')
    return (f'<rect class="tg-off" x="{x}" y="{cy - 5.5}" width="20" height="11" rx="5.5"/>'
            f'<circle class="knob-off" cx="{x + 5.5}" cy="{cy}" r="3.2"/>')


def baseline_card(anim, x, y, w, first_node_y, col1=142):
    """One Jenkins pipeline with Ansible brings the new server to the baseline."""
    times = check_times()
    nx = x + 24
    ys = [first_node_y + i * 42 for i in range(len(STEPS))]
    cy0 = ys[-1] + 26                     # first checklist row
    note_y = cy0 + 3 * 20 + 22
    end_y = note_y + 14 * (len(NOTES) - 1) + 30
    h = end_y + 28 - y
    out = [f'<rect class="card" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>',
           f'<rect class="hl {anim.window(HANDOVER, BASELINED + 0.6)}" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>',
           tool_icon("jenkins", x + w - 60, y + 12, 22), tool_icon("ansible", x + w - 34, y + 12, 22),
           f'<text class="name" x="{x + 14}" y="{y + 30}">Baseline</text>',
           f'<rect class="badge" x="{x + 88}" y="{y + 16}" width="124" height="18" rx="9"/>'
           f'<text class="badge-text" x="{x + 150}" y="{y + 29}" text-anchor="middle">released in versions</text>',
           f'<text class="what" x="{x + 14}" y="{y + 48}">one Jenkins pipeline with Ansible</text>']
    all_ys = ys + [end_y]
    lit = [d for *_x, d in STEPS]
    for y1, y2, d in zip(all_ys, all_ys[1:], lit):
        out.append(f'<line class="wire" x1="{nx}" y1="{y1 + 12}" x2="{nx}" y2="{y2 - 12}"/>'
                   f'<line class="wire-on {anim.show(d + 0.05)}" x1="{nx}" y1="{y1 + 12}" x2="{nx}" y2="{y2 - 12}"/>')
    for (title, sub, done), yy in zip(STEPS + [("Baselined", "same state as the rest", BASELINED)], all_ys):
        out.append(node(anim, nx, yy, done))
        out.append(f'<text class="title" x="{nx + 20}" y="{yy - 2}">{esc(title)}</text>'
                   f'<text class="what" x="{nx + 20}" y="{yy + 14}">{esc(sub)}</text>')
    # the checklist: every part has its own switch; ticks run in order, the part that is off stays off
    cxs = [nx + 20, nx + 20 + col1]
    for c, col in enumerate(CHECKS):
        for r, (label, on) in enumerate(col):
            cy, cx = cy0 + r * 20, cxs[c]
            if on:
                out.append(f'<circle class="pend" cx="{cx + 5}" cy="{cy}" r="5"/>' + tick(anim, cx + 5, cy, times[label], r=5.5))
            out.append(toggle(cx + 16, cy, on))
            out.append(f'<text class="{"label" if on else "label-off"}" x="{cx + 42}" y="{cy + 4}">{esc(label)}</text>')
            if not on:
                out.append(f'<text class="tiny" x="{cx + 42 + len(label) * 7 + 6}" y="{cy + 4}">off</text>')
    for k, note in enumerate(NOTES):
        out.append(f'<text class="tiny" x="{nx + 20}" y="{note_y + 14 * k}">{esc(note)}</text>')
    return "".join(out), h


# layouts

def wide(t):
    W, top = 1000, 16
    anim, out = Anim(), []
    mx, mw = 12, 180
    cx, cw = 220, 420
    bx, bw = 668, 320
    _, _, (_, ny) = cloud(Anim(), cx, top, cw)                # where the new server sits
    bl, bh = baseline_card(anim, bx, top, bw, ny)
    cl, ch, _ = cloud(anim, cx, top, cw, min_h=bh)
    H = max(ch, bh)
    ml, _ = module_card(anim, mx, top, mw, H)
    out += [ml, cl, bl]
    out.append(arrow(anim, mx + mw + 2, ny, cx - 2, ny, APPLY))
    out.append(arrow(anim, cx + cw + 2, ny, bx - 2, ny, HANDOVER))
    return svg(W, top + H + 16, t, anim, out)


def narrow(t):
    W, x, w = 400, 12, 376
    anim, out = Anim(), []
    ml, mh = module_card(anim, x, 12, w, cols=2)
    out.append(ml)
    cy = 12 + mh + 30
    cl, ch, (nx, ny) = cloud(anim, x, cy, w, clients_first=False, pad=8)
    out.append(arrow(anim, 200, 12 + mh + 2, 200, cy - 2, APPLY))
    out.append(f'<text class="tiny-on {anim.show(APPLY)}" x="210" y="{12 + mh + 19}">apply: +1 server</text>')
    out.append(cl)
    by = cy + ch + 30
    bl, bh = baseline_card(anim, x, by, w, by + 84, col1=170)
    out.append(arrow(anim, nx, cy + ch + 2, nx, by - 2, HANDOVER))
    out.append(bl)
    return svg(W, by + bh + 12, t, anim, out)


def svg(w, h, t, anim, body):
    w, h = round(w), round(h)
    title = ("A Terraform server module creates every server on Hetzner Cloud with its own firewall, a primary IP and a "
             "private network attachment. Internal services and each client project are separate stacks. A new server "
             "then goes through one Jenkins pipeline with Ansible: the inventory is built at run time, secrets come from "
             "Ansible Vault, each part is switched on or off for the run, and the server reaches the same baseline as the rest.")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">\n'
            f"<title>{esc(title)}</title>\n" + "\n".join(body) + f"\n{style(t, anim)}\n</svg>\n")


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "company-infra"
    out.mkdir(parents=True, exist_ok=True)
    for theme, t in THEMES.items():
        (out / f"{theme}.svg").write_text(wide(t), encoding="utf-8", newline="\n")
        (out / f"{theme}-narrow.svg").write_text(narrow(t), encoding="utf-8", newline="\n")
    print("written to", out)
