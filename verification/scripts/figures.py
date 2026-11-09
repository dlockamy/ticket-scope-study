#!/usr/bin/env python3
"""Build the three figures as hand-written SVG. stdlib only. Every plotted number is read from the raw per-run results.
usage: python3 -I figures.py <output-dir>
"""
import sys, os, json, re, glob, datetime as dt
from zoneinfo import ZoneInfo
from html import escape
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from load import ROOT, load_runs

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
DATA = os.path.dirname(ROOT)
R = load_runs(); single = [r for r in R if r['tag'] not in ('s6', 's7')]; team = [r for r in R if r['tag'] in ('s6', 's7')]
FONT = "font-family=\"Helvetica, Arial, sans-serif\""
INK = '#1a1a1a'; GREY = '#666666'; LIGHT = '#d9d9d9'
BLUE = '#0072B2'; VERM = '#D55E00'; SKY = '#56B4E9'; GREEN = '#009E73'

def defs():
    return f'''<defs>
<pattern id="hatch" patternUnits="userSpaceOnUse" width="5" height="5" patternTransform="rotate(45)"><rect width="5" height="5" fill="#ffffff"/><rect width="2" height="5" fill="{BLUE}"/></pattern>
<pattern id="dots" patternUnits="userSpaceOnUse" width="5" height="5"><rect width="5" height="5" fill="#ffffff"/><circle cx="2.5" cy="2.5" r="1.4" fill="#1f7fb8"/></pattern>
<pattern id="cross" patternUnits="userSpaceOnUse" width="6" height="6"><rect width="6" height="6" fill="#ffffff"/><path d="M0 0L6 6M6 0L0 6" stroke="{VERM}" stroke-width="1.4"/></pattern>
</defs>'''

class Svg:
    def __init__(self, w, title, desc):
        self.w = w; self.parts = []; self.title = title; self.desc = desc
    def add(self, s): self.parts.append(s)
    def text(self, x, y, s, size=11, anchor='start', weight='normal', fill=INK, style=''):
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}" {style} {FONT}>{escape(s)}</text>')
    def rect(self, x, y, w, h, fill, stroke='none', sw=1):
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def line(self, x1, y1, x2, y2, stroke=LIGHT, sw=1, dash=''):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
    def render(self, h):
        body = '\n'.join(self.parts)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{h:.0f}" viewBox="0 0 {self.w} {h:.0f}" role="img" aria-labelledby="t d">\n'
                f'<title id="t">{escape(self.title)}</title><desc id="d">{escape(self.desc)}</desc>\n{defs()}\n'
                f'<rect width="{self.w}" height="{h:.0f}" fill="#ffffff"/>\n{body}\n</svg>\n')

def legend_item(svg, x, y, fill, label, stroke=None):
    svg.rect(x, y - 9, 16, 11, fill, stroke or INK, 0.8)
    svg.text(x + 21, y, label, 11)

# ---------------------------------------------------------------- figure (a)
ARM_A = [('A1', 'A1 Open-ended, no list'), ('A2', 'A2 Sub-tasks, partial list'), ('A3', 'A3 Sub-tasks, complete list'),
         ('A4', 'A4 Sub-tasks, decoy list'), ('A5', 'A5 Open-ended + catalog'), ('A6', 'A6 Open-ended + stale catalog'),
         ('A7', 'A7 Partial list + per-repo checks')]
def fig_a():
    s2 = [r for r in single if r['tag'] == 's2']
    W = 600; svg = Svg(W, 'Runs left unfinished, by ticket and repository layout',
                       'Grouped bar chart. For two changes, a rename (C2) and a policy change (C3), the number of runs out of 5 in which at least one app was not updated and live, for each of seven tickets, in a monorepo and in a multi-repo layout. Monorepo is 0 of 5 in every cell. Multi-repo is nonzero for three C3 tickets (partial list 4, decoy list 5, partial list with per-repo checks 5) and one C2 ticket (per-repo checks 2).')
    svg.text(10, 20, 'Runs left unfinished, by ticket and repository layout', 14, weight='bold')
    svg.text(10, 37, 'Main model, 5 runs per bar. Unfinished = at least one app not updated and live.', 11, fill=GREY)
    legend_item(svg, 10, 58, 'url(#hatch)', 'Monorepo', BLUE); legend_item(svg, 110, 58, VERM, 'Multi-repo', VERM)
    x0, x1 = 215, 545; per = (x1 - x0) / 5; y = 78; pitch = 33; bh = 11
    for ch, title in (('C2', 'Rename a configuration field (all three apps affected)'), ('C3', 'Policy change: every app must pass an owner (all three apps affected)')):
        svg.text(10, y + 12, f'{ch}: {title}', 12, weight='bold'); y += 22
        top = y
        for arm, label in ARM_A:
            a = [r for r in s2 if r['change'] == ch and r['arm'] == arm and r['topology'] == 'mono']
            b = [r for r in s2 if r['change'] == ch and r['arm'] == arm and r['topology'] == 'multi']
            assert len(a) == len(b) == 5, (ch, arm, len(a), len(b))
            ma = sum(not r['acceptance_pass'] for r in a); mb = sum(not r['acceptance_pass'] for r in b)
            svg.text(x0 - 8, y + 17, label, 11, 'end')
            for k, (m, n, fill, stroke) in enumerate(((ma, len(a), 'url(#hatch)', BLUE), (mb, len(b), VERM, VERM))):
                yy = y + 3 + k * (bh + 2)
                if m: svg.rect(x0, yy, m * per, bh, fill, stroke, 0.8)
                else: svg.rect(x0, yy, 1.5, bh, stroke, stroke)
                svg.text(x0 + m * per + 6, yy + 9.5, f'{m} of {n}', 11, weight='bold' if m else 'normal', fill=INK if m else GREY)
            y += pitch
        svg.line(x0, top - 2, x0, y - 2, GREY, 1)
        for t in range(6):
            svg.line(x0 + t * per, y - 2, x0 + t * per, y + 2, GREY, 1); svg.text(x0 + t * per, y + 14, str(t), 10, 'middle', fill=GREY)
        svg.text((x0 + x1) / 2, y + 28, 'runs left unfinished (of 5)', 10, 'middle', fill=GREY)
        y += 44
    svg.text(10, y - 4, 'Not shown: C1 (additive change, one app affected) had 0 misses in 20 runs.', 10, fill=GREY)
    return svg.render(y + 8)

# ---------------------------------------------------------------- figure (b)
ARM_B = [('A1', 'A1 Open-ended'), ('A5', 'A5 Open-ended + catalog'), ('A6', 'A6 Open-ended + stale catalog'), ('A3', 'A3 Sub-tasks, complete list'),
         ('B1', 'B1 Partial list + "find every app"'), ('B2', 'B2 Partial list + org-wide audit'), ('B4', 'B4 Partial list + "others may be affected"'),
         ('A2', 'A2 Sub-tasks, partial list'), ('A4', 'A4 Sub-tasks, decoy list'), ('A7', 'A7 Partial list + per-repo checks'),
         ('B3', 'B3 Partial list + may ask questions'), ('A2s', 'A2s Partial list, core shell is the missing app')]
def fig_b():
    panels = [('Main model, 5 repositories', ('s2', 's3'), [a for a, _ in ARM_B]),
              ('Main model, 17 repositories', ('s4',), ['A1', 'A5', 'A6', 'A3', 'B4', 'A2']),
              ('Smaller model, 5 repositories', ('s5',), ['A1', 'B1', 'B2', 'B4', 'A2'])]
    labels = dict(ARM_B)
    W = 600
    svg = Svg(W, "Cloned the missing app's repository versus finished the change",
              "Grouped bar chart, one panel per condition. For each ticket, the number of multi-repo runs of the policy change that cloned the missing app's repository and the number that finished with every app updated. Open-ended tickets and the three fixes clone it and finish in every run. Partial-list tickets often finish less than they clone: in the 17-repository estate, 4 of 5 partial-list runs cloned it and none finished.")
    svg.text(10, 20, "Cloned the missing app's repository vs finished the change", 14, weight='bold')
    svg.text(10, 37, 'Multi-repo layout, policy change (C3). Bars count runs.', 11, fill=GREY)
    legend_item(svg, 10, 58, 'url(#dots)', "Cloned the missing app's repository", '#1f7fb8'); legend_item(svg, 270, 58, GREEN, 'Finished: every app updated and live', GREEN)
    x0, x1 = 265, 525; y = 78; pitch = 33; bh = 11
    for title, tags, arms in panels:
        svg.text(10, y + 12, title, 12, weight='bold'); y += 22; top = y
        for arm in arms:
            L = [r for r in single if r['tag'] in tags and r['arm'] == arm and r['change'] == 'C3' and r['topology'] == 'multi']
            n = len(L); assert n in (4, 5), (title, arm, n)
            hid = 'shell' if arm == 'A2s' else 'reports'
            cl = sum(hid in r['repos_cloned'] for r in L); fin = sum(bool(r['acceptance_pass']) for r in L)
            per = (x1 - x0) / 5
            svg.text(x0 - 8, y + 17, labels[arm], 11, 'end')
            for k, (m, fill, stroke) in enumerate(((cl, 'url(#dots)', '#1f7fb8'), (fin, GREEN, GREEN))):
                yy = y + 3 + k * (bh + 2)
                if m: svg.rect(x0, yy, m * per, bh, fill, stroke, 0.8)
                else: svg.rect(x0, yy, 1.5, bh, stroke, stroke)
                svg.text(x0 + m * per + 6, yy + 9.5, f'{m} of {n}', 11, weight='bold' if m != n else 'normal', fill=INK)
            y += pitch
        per = (x1 - x0) / 5
        svg.line(x0, top - 2, x0, y - 2, GREY, 1)
        for t in range(6):
            svg.line(x0 + t * per, y - 2, x0 + t * per, y + 2, GREY, 1); svg.text(x0 + t * per, y + 14, str(t), 10, 'middle', fill=GREY)
        y += 30
    # the 33 incomplete changes
    P4 = ('s2', 's2h', 's3', 's4', 's5')
    inc = [r for r in single if r['tag'] in P4 and r['topology'] == 'multi' and not r['acceptance_pass']]
    opened = sum(r['missed'][0] in r['repos_cloned'] for r in inc); never = len(inc) - opened
    svg.text(10, y + 12, f'All {len(inc)} incomplete changes in phases 1 to 4 (both models)', 12, weight='bold'); y += 22
    wtot = x1 - 10 - 10; xs = 10
    svg.rect(xs, y, wtot * opened / len(inc), 20, 'url(#dots)', '#1f7fb8', 0.8)
    svg.rect(xs + wtot * opened / len(inc), y, wtot * never / len(inc), 20, '#ffffff', INK, 0.8)
    svg.rect(xs + wtot * opened / len(inc) / 2 - 11, y + 3, 22, 15, '#ffffff'); svg.text(xs + wtot * opened / len(inc) / 2, y + 14, f'{opened}', 12, 'middle', weight='bold')
    svg.text(xs + wtot * opened / len(inc) + wtot * never / len(inc) / 2, y + 14, f'{never}', 12, 'middle', weight='bold')
    y += 36
    svg.text(10, y, f"{opened} cloned the missing app's repository and left it unchanged;", 11)
    svg.text(10, y + 15, f'{never} never cloned it.', 11)
    return svg.render(y + 30), (opened, never, len(inc))

# ---------------------------------------------------------------- figure (c)
PHASES = [('1', 'Screening', ('s2', 's2h')), ('2', 'Fixes', ('s3',)), ('3', 'Larger estate (17 repos)', ('s4',)), ('4', 'Second model', ('s5',)),
          ('5', 'Reviewers (300 reviews)', None), ('6', 'Two developers: predictable release', ('s6',)), ('7', 'Two developers: judgement call', ('s7',)),
          ('8', 'Epic with child tickets', ('s8',)), ('9', 'Noisy tickets', ('s9',)), ('9b', 'Chat thread, name stated', ('s9b',))]
def fig_c():
    tz = ZoneInfo('America/New_York')
    def span(tags):
        lo, hi, n, cost = 1e20, 0, 0, 0.0
        for r in R:
            if r['tag'] not in tags: continue
            ts = [json.loads(l)['ts'] for l in open(r['_dir'] + '/events.jsonl') if l.strip()]
            m = json.load(open(r['_dir'] + '/meta.json')); st = m.get('start_ms') or min(ts)
            lo = min(lo, st); hi = max(hi, max(ts)); n += 1; cost += r.get('agent_cost_usd') or 0
        return lo / 1000, hi / 1000, n, cost
    rows = []
    for code, name, tags in PHASES:
        if tags:
            lo, hi, n, cost = span(tags); unit = 'runs'
        else:  # phase 5: reviews; times from the driver log, count and cost from the saved reviews
            log = open(ROOT + '/reviews-driver.log').read().split('\n')
            times = [l.split()[0] for l in log if re.match(r'\d\d:\d\d:\d\d', l)]
            d0 = dt.datetime.fromtimestamp(span(('s6',))[0], tz).date()
            f = lambda t: dt.datetime.combine(d0, dt.time.fromisoformat(t), tz).timestamp()
            lo, hi = f(times[0]), f(times[-1])
            fs = glob.glob(DATA + '/review/out/*.json'); n = len(fs); cost = sum(json.load(open(x)).get('total_cost_usd') or 0 for x in fs); unit = 'reviews'
        rows.append((code, name, lo, hi, n, cost, unit))
    base1 = dt.datetime.fromtimestamp(rows[0][2], tz).replace(hour=7, minute=0, second=0, microsecond=0)
    seg1_end = base1.replace(hour=0, minute=0) + dt.timedelta(days=1)
    seg2_start = base1.replace(hour=7, minute=0) + dt.timedelta(days=1)
    pxh = 17.0; X0 = 175; GAP = 14
    def xpos(ts):
        t = dt.datetime.fromtimestamp(ts, tz)
        if t < seg1_end: return X0 + (t - base1).total_seconds() / 3600 * pxh
        return X0 + (seg1_end - base1).total_seconds() / 3600 * pxh + GAP + (t - seg2_start).total_seconds() / 3600 * pxh
    W = 600
    svg = Svg(W, 'Timeline of the nine phases (and phase 9b)',
              'Horizontal bars, one per phase, on a clock-time axis from 07:00 on 30 October to 10:00 on 31 October 2026 with the overnight gap removed. Phases 1 to 4 ran 07:51 to 18:11 on 30 October with 176, 50, 60 and 40 runs. Phase 5, 300 reviews, took about 6 minutes at 20:58. Phases 6 and 7 are two-developer runs, 30 each, 21:41 to 23:31. Phases 8, 9 and 9b ran 07:54 to 09:34 on 31 October with 30, 30 and 10 runs.')
    svg.text(10, 20, 'Timeline of the study: nine phases, 456 developer runs and 300 reviews', 14, weight='bold')
    svg.text(10, 37, 'Clock time, US Eastern. The overnight gap is removed (zigzag).', 11, fill=GREY)
    legend_item(svg, 10, 58, BLUE, 'One developer', BLUE); legend_item(svg, 120, 58, 'url(#cross)', 'Two developers', VERM); legend_item(svg, 240, 58, 'url(#dots)', 'Reviewers (no field)', '#1f7fb8')
    y0 = 82; pitch = 36; bh = 15
    nrow = len(rows); ybot = y0 + pitch * nrow
    xg0 = X0 + (seg1_end - base1).total_seconds() / 3600 * pxh
    for i, (code, name, lo, hi, n, cost, unit) in enumerate(rows):
        y = y0 + i * pitch
        if i % 2 == 0: svg.rect(0, y - 6, W, pitch, '#f4f4f4')
        svg.text(10, y + 8, f'{code}  {name}', 11, weight='bold')
        svg.text(10, y + 21, f'{n} {unit}', 10, fill=GREY)
        xa, xb = xpos(lo), xpos(hi); w = max(xb - xa, 3)
        fill, stroke = (BLUE, BLUE) if code in ('1', '2', '3', '4', '8', '9', '9b') else (('url(#cross)', VERM) if code in ('6', '7') else ('url(#dots)', '#1f7fb8'))
        svg.rect(xa, y, w, bh, fill, stroke, 0.8)
        mins = round((hi - lo) / 60); dur = f'{mins // 60} h {mins % 60:02d} min' if mins >= 60 else f'{mins} min'
        t0 = dt.datetime.fromtimestamp(lo, tz).strftime('%H:%M'); t1 = dt.datetime.fromtimestamp(hi, tz).strftime('%H:%M')
        lab = f'{t0}-{t1}, {dur}'
        # place the label to the right of the bar, or to the left when it would run off the page
        if code in ('1','2','3','4','5') and xb + 8 + len(lab) * 5.6 < W - 4: svg.text(xb + 6, y + 11.5, lab, 10)
        else: svg.text(xa - 6, y + 11.5, lab, 10, 'end')
    # axes
    ya = ybot + 2
    svg.line(X0, ya, xg0, ya, GREY, 1); svg.line(xg0 + GAP, ya, xg0 + GAP + 3 * pxh, ya, GREY, 1)
    for h in (7, 10, 13, 16, 19, 22):
        x = X0 + (h - 7) * pxh; svg.line(x, ya, x, ya + 4, GREY); svg.text(x, ya + 16, f'{h:02d}:00', 10, 'middle', fill=GREY)
    for h in (7, 9):
        x = xg0 + GAP + (h - 7) * pxh; svg.line(x, ya, x, ya + 4, GREY); svg.text(x, ya + 16, f'{h:02d}:00', 10, 'middle', fill=GREY)
    svg.text(X0 + 3.5 * pxh, ya + 32, 'Fri 30 Oct', 10, 'middle', fill=GREY); svg.text(xg0 + GAP + 1.5 * pxh, ya + 32, 'Sat 31 Oct', 10, 'middle', fill=GREY)
    zx = xg0 + GAP / 2
    svg.add(f'<path d="M{zx-4:.1f} {ya-4} l8 4 l-8 4 l8 4" fill="none" stroke="{GREY}" stroke-width="1.2"/>')
    return svg.render(ya + 44), rows

if __name__ == '__main__':
    a = fig_a(); open(os.path.join(OUT, 'fig-a-misses-by-ticket-and-layout.svg'), 'w').write(a)
    b, bstat = fig_b(); open(os.path.join(OUT, 'fig-b-mechanism-cloned-vs-finished.svg'), 'w').write(b)
    c, rows = fig_c(); open(os.path.join(OUT, 'fig-c-timeline-of-phases.svg'), 'w').write(c)
    print('33-split', bstat)
    for r in rows: print(r[0], r[4], r[6], round(r[5], 2), dt.datetime.fromtimestamp(r[2], ZoneInfo('America/New_York')).strftime('%d %H:%M:%S'), dt.datetime.fromtimestamp(r[3], ZoneInfo('America/New_York')).strftime('%d %H:%M:%S'))
