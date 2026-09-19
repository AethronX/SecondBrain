#!/usr/bin/env python3
"""A fanned stack of tablets, each showing a different NAZZIM page.

The reference this answers sells a BUNDLE - six tablets, six products. NAZZIM is
one product, so the fan shows six pages of it instead. Same persuasive mechanic
(this is large), honest claim (this is one system), and NAZZIM's own palette
rather than the reference's black-and-neon, which its dark screens would vanish
against.
"""
import subprocess, pathlib, sys
sys.path.insert(0, "..")
from pngcrop import crop_height, CHROME_OFFSET

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
W, H = 780, 1120          # tablet outer
SW, SH = 720, 1060        # tablet screen

def shoot(name, w, h, html):
    pathlib.Path(f"_{name}.html").write_text(html)
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", f"--window-size={w},{h + CHROME_OFFSET}",
                    f"--screenshot={name}.png", "--virtual-time-budget=4000", f"_{name}.html"],
                   capture_output=True)
    crop_height(f"{name}.png", h)
    pathlib.Path(f"_{name}.html").unlink()
    return f"{name}.png"

CSS = f"""
@font-face{{font-family:IS;src:url('file:///mnt/skills/examples/canvas-design/canvas-fonts/InstrumentSans-Regular.ttf');font-weight:400}}
@font-face{{font-family:IS;src:url('file:///mnt/skills/examples/canvas-design/canvas-fonts/InstrumentSans-Bold.ttf');font-weight:700}}
@font-face{{font-family:GM;src:url('file:///mnt/skills/examples/canvas-design/canvas-fonts/GeistMono-Regular.ttf')}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#F5F1E8}}
body{{font-family:IS,sans-serif;-webkit-font-smoothing:antialiased}}
.t{{width:{W}px;height:{H}px;background:linear-gradient(158deg,#55555a,#2a2a2d);
  border-radius:34px;padding:{(W-SW)//2}px;display:flex;align-items:center;justify-content:center}}
.ts{{width:{SW}px;height:{SH}px;background:#191919;border-radius:22px;overflow:hidden;
  color:#d4d4d4;font-size:20px;line-height:1.5;display:flex;flex-direction:column}}
.cv{{height:150px;flex:none;overflow:hidden}}
.cv img{{width:100%;height:150px;object-fit:cover;object-position:center;display:block}}
.doc{{flex:1;min-height:0;padding:0 56px}}
.ic{{font-size:44px;line-height:1;margin:-30px 0 10px;position:relative}}
.dot{{width:54px;height:54px;border-radius:50%;border:7px solid var(--c,#9b9b9b);margin:-30px 0 10px;position:relative;background:#191919}}
.dot:after{{content:'';position:absolute;inset:10px;border-radius:50%;background:var(--c,#9b9b9b)}}
h1{{font-size:42px;font-weight:700;color:#fff;letter-spacing:-.025em;margin-bottom:14px}}
.q{{border-left:4px solid #d4d4d4;padding-left:17px;margin-bottom:15px}}
.q b{{display:block;font-size:24px;color:#fff}}
.q i{{display:block;font-size:22px;color:#9b9b9b;font-style:normal}}
.co{{border-radius:7px;padding:14px 17px;display:flex;gap:13px;margin-bottom:17px;font-size:19px;line-height:1.45}}
.co .i{{flex:none;font-size:20px}}
.g-bg{{background:#1c3829;color:#8fbfae}} .g-bg b{{color:#d6f0e5}} .g-bg .i{{color:#4dab9a}}
.p-bg{{background:#2b2233;color:#a78bc4}} .p-bg b{{color:#e6d6f7}} .p-bg .i{{color:#b58ae0}}
.b-bg{{background:#1d2a38;color:#8aa9c6}} .b-bg b{{color:#d3e6f7}} .b-bg .i{{color:#7ab3e8}}
.o-bg{{background:#3a2c1a;color:#c9a97a}} .o-bg b{{color:#f5e2c6}} .o-bg .i{{color:#ffa344}}
.vh{{display:flex;gap:8px;font-size:18px;color:#9b9b9b;margin-bottom:10px}}
.tiles{{display:flex;gap:15px;margin-bottom:17px}}
.tile{{flex:1;border:1px solid #2f2f2f;border-radius:7px;padding:11px 15px 13px;text-align:center}}
.tile .s{{font-size:16px;color:#9b9b9b;text-align:left;margin-bottom:6px}}
.tile .n{{font-size:44px;line-height:1.05}}
.tile .c{{font-size:15px;color:#9b9b9b}}
.gr{{color:#4dab9a}}.pu{{color:#9a6dd7}}.or{{color:#ffa344}}.bl{{color:#5e9ed6}}
.tabs{{display:flex;gap:18px;font-size:18px;color:#6f6f6f;border-bottom:1px solid #232323;
  padding-bottom:9px;margin-bottom:8px}}
.tabs .on{{color:#e8e8e8;font-weight:700;box-shadow:0 9px 0 -7px #e8e8e8}}
.grp{{font-size:17px;color:#8a8a8a;font-weight:700;padding:13px 0 3px;display:flex;gap:8px}}
.grp span{{color:#5f5f5f;font-weight:400}}
.row{{display:flex;align-items:center;gap:11px;padding:10px 0;border-bottom:1px solid #232323}}
.row .tk{{flex:1;font-size:20px;color:#e4e4e4}}
.ch{{font-size:15px;padding:3px 9px;border-radius:5px;white-space:nowrap}}
.c-red{{background:#5c2320;color:#ff7369}}.c-org{{background:#5c3b23;color:#ffa344}}
.c-blu{{background:#1f3a5c;color:#5e9ed6}}.c-gry{{background:#373737;color:#9b9b9b}}
.c-pur{{background:#3f2d5c;color:#9a6dd7}}.c-grn{{background:#1c3829;color:#4dab9a}}
.dt{{font-size:16px;color:#9b9b9b;white-space:nowrap}}
.chart{{display:flex;align-items:flex-end;gap:8px;border-bottom:1px solid #2f2f2f;height:130px}}
.chart i{{flex:1;background:#4dab9a;border-radius:2px 2px 0 0}}
.cap{{font-size:16px;color:#9b9b9b;padding-top:8px}}
.card{{border:1px solid #2f2f2f;border-radius:8px;padding:15px 17px;margin-bottom:13px}}
.card .h{{font-size:22px;color:#fff;font-weight:700;margin-bottom:9px}}
.card .m{{display:flex;gap:10px;align-items:center;margin-bottom:8px}}
.card .w{{font-size:17px;color:#8a8a8a;line-height:1.4}}
.pct{{font-size:22px;font-weight:700}}
.mini{{display:grid;grid-template-columns:1fr 1fr;gap:13px}}
.mc{{border:1px solid #2f2f2f;border-radius:7px;padding:12px 14px;height:158px;overflow:hidden}}
.mc .s{{font-size:15px;color:#9b9b9b;margin-bottom:9px}}
.mc .bars{{display:flex;align-items:flex-end;gap:5px;height:78px}}
.mc .bars i{{flex:1;border-radius:2px 2px 0 0}}
.donut{{width:78px;height:78px;border-radius:50%;margin:0 auto;
  background:conic-gradient(#5e9ed6 0 42%,#9a6dd7 42% 70%,#4dab9a 70% 88%,#373737 88% 100%)}}
.donut:after{{content:'';display:block;width:42px;height:42px;margin:18px;border-radius:50%;background:#191919}}
.hb{{display:flex;flex-direction:column;gap:9px;padding-top:4px}}
.hb .r{{display:flex;align-items:center;gap:9px;font-size:15px;color:#9b9b9b}}
.hb .b{{height:11px;border-radius:3px;background:#5e9ed6}}
.big{{font-size:52px;text-align:center;line-height:1.1;padding-top:8px}}
"""

def tablet(slug, cover, body):
    return shoot(slug, W, H, f"<style>{CSS}</style>"
        f'<div class="t"><div class="ts">'
        f'<div class="cv"><img src="../covers/cover-{cover}.png"></div>'
        f'<div class="doc">{body}</div></div></div>')

BARS = [1,2,2,3,1,3,1,1,2,4,3,5,5,3]
bars = "".join(f'<i style="height:{b/5*100}%"></i>' for b in BARS)

tablet("t1-home", "nazzim-pro", f"""
<div class="dot"></div><h1>NAZZIM Pro</h1>
<div class="q"><b>You are further along than you think.</b><i>Turn information into execution.</i></div>
<div class="co g-bg"><div class="i">◎</div><div><b>This week, you finished this.</b> Most systems open with what you owe. NAZZIM opens with what you did.</div></div>
<div class="tiles">
 <div class="tile"><div class="s">↗ Tasks</div><div class="n gr">24</div><div class="c">Finished this week</div></div>
 <div class="tile"><div class="s">↗ Goals</div><div class="n pu">68%</div><div class="c">Average progress</div></div>
 <div class="tile"><div class="s">↗ Reviews</div><div class="n or">9</div><div class="c">Weeks you showed up</div></div></div>
<div class="vh">↗ Tasks</div><div class="chart">{bars}</div>
<div class="cap">Every bar is a day you moved something forward</div>
<div class="vh" style="margin-top:16px">↗ Goals</div>
<div class="row"><div class="tk">Run a half marathon under 1:55</div><span class="pct gr">74%</span><span class="ch c-grn">On Track</span></div>
<div class="row"><div class="tk">Ship the second edition of the course</div><span class="pct gr">62%</span><span class="ch c-grn">On Track</span></div>""")

tablet("t2-today", "today", """
<div class="ic" style="color:#9a6dd7">☀</div><h1>Today</h1>
<div class="co p-bg"><div class="i">☀</div><div>NAZZIM · <b>Today</b> · Inbox · Command · Tasks · Projects · Goals · Areas</div></div>
<div class="vh">↗ Today's plan</div>
<div class="card"><div class="h">Saturday 19 September</div><div class="w">Focus — Launch email out before noon.</div></div>
<div class="vh">↗ Tasks</div>
<div class="tabs"><span class="on">Today's work</span><span>Board</span><span>Calendar</span></div>
<div class="grp">Overdue <span>1</span></div>
<div class="row"><div class="tk">Renew the nazzim.com domain</div><span class="ch c-red">P1</span><span class="dt">2 days late</span></div>
<div class="grp">Must Do <span>2</span></div>
<div class="row"><div class="tk">Write the launch email</div><span class="ch c-red">P1</span><span class="dt">Today</span></div>
<div class="row"><div class="tk">Sign the studio lease</div><span class="ch c-red">P1</span><span class="dt">Today</span></div>
<div class="grp">Should Do <span>3</span></div>
<div class="row"><div class="tk">Outline chapter three</div><span class="ch c-org">P2</span><span class="dt">Today</span></div>
<div class="row"><div class="tk">Reply to Salim about the October schedule</div><span class="ch c-org">P2</span><span class="dt">Today</span></div>
<div class="row"><div class="tk">Book the flights before prices move</div><span class="ch c-org">P2</span><span class="dt">Tomorrow</span></div>
<div class="grp">If Time <span>1</span></div>
<div class="row"><div class="tk">Clear the reading list into Knowledge</div><span class="ch c-blu">P3</span><span class="dt">This week</span></div>""")

tablet("t3-tasks", "tasks", """
<div class="ic" style="color:#5e9ed6;font-size:38px">☰</div><h1>Tasks</h1>
<div class="co b-bg"><div class="i">◉</div><div>NAZZIM · Today · Inbox · Command · <b>Tasks</b> · Projects · Goals · Areas</div></div>
<div class="vh">↗ Tasks · Next actions</div>
<div class="row"><div class="tk">Record lesson five of the second edition</div><span class="ch c-red">@Deep Work</span><span class="ch c-org">High</span></div>
<div class="row"><div class="tk">Write the sales page first draft</div><span class="ch c-red">@Deep Work</span><span class="ch c-org">High</span></div>
<div class="row"><div class="tk">Reply to Salim about October</div><span class="ch c-pur">@Phone</span><span class="ch c-grn">Low</span></div>
<div class="row"><div class="tk">Book the flights before prices move</div><span class="ch c-blu">@Computer</span><span class="ch c-grn">Low</span></div>
<div class="row"><div class="tk">Order the new microphone</div><span class="ch c-org">@Errand</span><span class="ch c-grn">Low</span></div>
<div class="row"><div class="tk">File the receipts for the quarter</div><span class="ch c-gry">@Quick</span><span class="ch c-grn">Low</span></div>
<div class="row"><div class="tk">Interval session at the track</div><span class="ch c-grn">@Home</span><span class="ch c-org">High</span></div>
<div class="row"><div class="tk">Tidy the reading list into Knowledge</div><span class="ch c-gry">@Quick</span><span class="ch c-grn">Low</span></div>
<div class="row"><div class="tk">Review the quarter numbers</div><span class="ch c-blu">@Computer</span><span class="ch c-org">Medium</span></div>
<div class="tabs" style="margin-top:18px;border-bottom:none;border-top:1px solid #232323;padding:14px 0 0"><span class="on">Board</span><span>Calendar</span></div>
<div class="grp">Next <span>4</span></div>
<div class="row"><div class="tk">Draft the launch email</div><span class="ch c-pur">Next</span></div>""")

tablet("t4-goals", "goals", """
<div class="ic" style="color:#5e9ed6;font-size:40px">★</div><h1>Goals</h1>
<div class="co b-bg"><div class="i">◎</div><div>Every task you tick rolls up into one of these. The bar is <b>your own metric</b>, against your own deadline.</div></div>
<div class="tabs"><span class="on">Active</span><span>Timeline</span><span>Board</span></div>
<div class="card"><div class="h">Run a half marathon under 1:55</div>
 <div class="m"><span class="pct gr">74%</span><span class="ch c-grn">On Track</span><span class="dt">61 days left</span><span class="ch c-grn">Health</span></div>
 <div class="w">Metric — Training sessions completed out of the 50-session plan.<br>Why — Because the training is the point. The time is just how I will know it happened.</div></div>
<div class="card"><div class="h">Ship the second edition of the course</div>
 <div class="m"><span class="pct gr">62%</span><span class="ch c-grn">On Track</span><span class="dt">88 days left</span><span class="ch c-pur">Career</span></div>
 <div class="w">Metric — Lessons re-recorded out of 50.<br>Why — The first edition sold well and is now wrong in three places.</div></div>
<div class="co b-bg" style="margin-top:4px"><div class="i">◷</div><div><b>Health</b> compares progress against elapsed time, so a goal that is quietly slipping says so long before the deadline arrives.</div></div>""")

tablet("t5-analytics", "analytics", """
<div class="dot" style="--c:#ffa344"></div><h1>Analytics</h1>
<div class="co o-bg"><div class="i">↻</div><div>Every figure here is computed from your live data. <b>There is no metrics database to maintain.</b></div></div>
<div class="tiles">
 <div class="tile"><div class="s">↗ Tasks</div><div class="n or">7</div><div class="c">Open right now</div></div>
 <div class="tile"><div class="s">↗ Projects</div><div class="n bl">4</div><div class="c">In flight</div></div>
 <div class="tile"><div class="s">↗ Notes</div><div class="n gr">31</div><div class="c">Saved</div></div></div>
<div class="tabs"><span class="on">Where the work sits</span><span>Are the weeks better</span><span>What you read</span></div>
<div class="mini">
 <div class="mc"><div class="s">Open work by area</div><div class="donut"></div></div>
 <div class="mc"><div class="s">Tasks by project</div><div class="hb">
   <div class="r"><div class="b" style="width:74%"></div>9</div>
   <div class="r"><div class="b" style="width:52%;background:#9a6dd7"></div>6</div>
   <div class="r"><div class="b" style="width:33%;background:#4dab9a"></div>4</div>
   <div class="r"><div class="b" style="width:18%;background:#ffa344"></div>2</div></div></div>
 <div class="mc"><div class="s">Completed per day</div><div class="bars">
   """ + "".join(f'<i style="height:{b/5*100}%;background:#4dab9a"></i>' for b in BARS[:10]) + """</div></div>
 <div class="mc"><div class="s">Weekly score</div><div class="big or">8.0</div><div class="s" style="text-align:center">Average, last 9 weeks</div></div></div>""")

# ---- the fanned cover ----
TABS = ["t1-home", "t2-today", "t3-tasks", "t4-goals", "t5-analytics"]
POS = [(40, 336, -10), (245, 309, -5), (450, 296, 0), (655, 309, 5), (860, 336, 10)]

cards = "".join(
    f'<img class="tab" src="{t}.png" style="left:{x}px;top:{y}px;'
    f'transform:rotate({r}deg);z-index:{i + 2}">'
    for i, (t, (x, y, r)) in enumerate(zip(TABS, POS)))

shoot("g5-fan", 1280, 720, f"""<style>
@font-face{{font-family:IS;src:url('file:///mnt/skills/examples/canvas-design/canvas-fonts/InstrumentSans-Regular.ttf');font-weight:400}}
@font-face{{font-family:IS;src:url('file:///mnt/skills/examples/canvas-design/canvas-fonts/InstrumentSans-Bold.ttf');font-weight:700}}
@font-face{{font-family:GM;src:url('file:///mnt/skills/examples/canvas-design/canvas-fonts/GeistMono-Regular.ttf')}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1280px;height:720px;overflow:hidden;background:#F5F1E8}}
body{{font-family:IS,sans-serif;-webkit-font-smoothing:antialiased}}
.s{{width:1280px;height:720px;position:relative;overflow:hidden;background:#F5F1E8}}
.wm{{position:absolute;left:52px;top:42px;z-index:20}}
.wm .m{{font-weight:700;font-size:26px;letter-spacing:-.03em;color:#16130E;line-height:1}}
.wm .t{{font-family:GM;font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:#A79F91;margin-top:6px}}
.hd{{position:absolute;left:0;right:0;top:96px;text-align:center;z-index:20}}
.hd h2{{font-size:62px;font-weight:700;letter-spacing:-.038em;line-height:1.04;color:#A79F91}}
.hd h2 b{{color:#16130E}}
.hd p{{font-size:21px;color:#6B6156;margin-top:16px}}
.hd .a{{height:5px;width:86px;background:#1E7A5A;border-radius:3px;margin:20px auto 0}}
.tab{{position:absolute;width:300px;display:block;border-radius:22px;
  box-shadow:0 30px 60px -26px rgba(48,34,18,.55)}}
</style>
<div class="s">
  <div class="wm"><div class="m">NAZZIM</div><div class="t">Second Brain Pro</div></div>
  <div class="hd">
    <h2>Not a dashboard.<br><b>A whole system.</b></h2>
    <p>Fourteen pages · Nine linked databases · Twenty computed charts</p>
    <div class="a"></div>
  </div>
  {cards}
</div>""")
print("fan done")
