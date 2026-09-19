#!/usr/bin/env python3
"""Render the Gumroad listing assets: four 1280x720 covers and a 600x600 thumbnail.

Gumroad shows product covers at 16:9 and the Discover/library thumbnail as a
square, so these are separate layouts rather than crops of the 2000x2000 sheets.
The device screens themselves are lifted from brand/device so the UI on a
Gumroad cover is the same UI the product actually renders.
"""
import subprocess, pathlib, sys
sys.path.insert(0, "..")
from blocks import style_of, scope, block
from pngcrop import crop_height, CHROME_OFFSET

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
DEV = pathlib.Path("../device")
one, two = (DEV / "1.html").read_text(), (DEV / "2.html").read_text()
LAP_CSS, PH_CSS = scope(style_of(one), '.lap'), scope(style_of(two), '.ph')
LAP, PH = block(one, '<div class="lap">'), block(two, '<div class="ph">')
COV = "../covers"

def device_png(name, w, h, css, body):
    """Render a device on its own, at natural size, so later layouts can place it
    as an <img>. A CSS transform leaves the un-scaled box outside the viewport,
    and Chromium does not paint what never landed in it."""
    html = ('<link rel="stylesheet" href="../device/_d.css">\n<style>\n'
            f'html,body{{width:{w}px;height:{h}px;overflow:hidden;background:#F7F6FD}}\n'
            f'.wrap{{width:{w}px;height:{h}px;display:flex;align-items:center;justify-content:center}}\n'
            f'{css}\n</style>\n<div class="wrap">{body}</div>')
    pathlib.Path(f"_{name}.html").write_text(html)
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", f"--window-size={w},{h + CHROME_OFFSET}",
                    f"--screenshot={name}.png", "--virtual-time-budget=4000", f"_{name}.html"],
                   capture_output=True)
    crop_height(f"{name}.png", h)
    pathlib.Path(f"_{name}.html").unlink()
    return f"{name}.png"

device_png("_lap", 1900, 1240, LAP_CSS, LAP)
device_png("_ph", 900, 1520, PH_CSS, PH)

BASE = """<link rel="stylesheet" href="../device/_d.css">
<style>
html,body{width:%(W)spx;height:%(H)spx;overflow:hidden;background:#F7F6FD}
.g{width:%(W)spx;height:%(H)spx;position:relative;overflow:hidden;background:#F7F6FD;
   display:flex;align-items:center;padding:0 0 0 76px}
.gl{width:%(LW)spx;flex:none;z-index:4}
.ge{font-family:GM;font-size:16px;letter-spacing:.34em;text-transform:uppercase;color:#9A9AAE}
.gh{font-size:%(HS)spx;font-weight:700;letter-spacing:-.036em;line-height:1.06;color:#A8A8BC;margin-top:16px}
.gh b{font-weight:700;background:linear-gradient(96deg,#4F52E8 0%%,#9B51E0 100%%);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:transparent}
.ga{height:5px;width:86px;background:linear-gradient(96deg,#4F52E8 0%%,#9B51E0 100%%);border-radius:3px;margin-top:20px}
.gs{font-size:19px;color:#6B6B80;margin-top:20px;line-height:1.55}
.gw{position:absolute;left:76px;bottom:44px;z-index:4}
.gw .m{font-weight:700;font-size:28px;letter-spacing:-.03em;color:#0B0B14;line-height:1}
.gw .t{font-family:GM;font-size:13px;letter-spacing:.2em;text-transform:uppercase;color:#A8A8BC;margin-top:7px}
%(EXTRA)s
</style>
%(BODY)s"""

def page(name, w, h, lw, hs, extra, body):
    html = BASE % dict(W=w, H=h, LW=lw, HS=hs, EXTRA=extra, BODY=body)
    pathlib.Path(f"_{name}.html").write_text(html)
    out = f"{name}.png"
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", f"--window-size={w},{h + CHROME_OFFSET}",
                    f"--screenshot={out}", "--virtual-time-budget=4000", f"_{name}.html"],
                   capture_output=True)
    crop_height(out, h)
    pathlib.Path(f"_{name}.html").unlink()
    print(out)

WM = '<div class="gw"><div class="m">Nazzim <span style="color:#9A9AAE">نظّم</span></div><div class="t">Second Brain Pro</div></div>'

# 1 — hero, laptop
page("g1-hero", 1280, 720, 560, 54,
 ".dev{position:absolute;right:-96px;top:50%;transform:translateY(-50%);width:790px;z-index:2}\n .dev img{display:block;width:100%}",
 f'''<div class="g"><div class="gl">
 <div class="ge">Notion Life OS</div>
 <div class="gh">Most systems show<br>what you owe.<br><b>This one shows<br>what you did.</b></div>
 <div class="ga"></div></div>
 <div class="dev"><img src="_lap.png"></div>{WM}</div>''')

# 2 — mobile
page("g2-mobile", 1280, 720, 560, 54,
 ".dev{position:absolute;right:104px;top:50%;transform:translateY(-50%);width:400px;z-index:2}\n .dev img{display:block;width:100%}",
 f'''<div class="g"><div class="gl">
 <div class="ge">Built for the phone first</div>
 <div class="gh">The first thing<br>you see is<br><b>what you did.</b></div>
 <div class="ga"></div>
 <div class="gs">Every view reads on a phone screen.<br>No app to install.</div></div>
 <div class="dev"><img src="_ph.png"></div>{WM}</div>''')

# 3 — the cover system
CELLS = ["nazzim-pro", "today", "tasks", "reviews"]   # one per zone, sized to stay legible
page("g3-pages", 1280, 720, 470, 48,
 """.grid{position:absolute;right:62px;top:50%;transform:translateY(-50%);width:606px;
   display:grid;grid-template-columns:1fr;gap:15px;z-index:2}
 .grid div{border-radius:7px;overflow:hidden;box-shadow:0 12px 26px -16px rgba(28,22,70,.45)}
 .grid img{display:block;width:100%;height:auto}""",
 f'''<div class="g"><div class="gl">
 <div class="ge">Every page</div>
 <div class="gh">Fifteen pages.<br><b>One design system.</b></div>
 <div class="ga"></div>
 <div class="gs">Colour-coded by zone. The bars on<br>every cover are the product's own data.</div></div>
 <div class="grid">{"".join(f'<div><img src="{COV}/cover-{c}.png"></div>' for c in CELLS)}</div>{WM}</div>''')

# 4 — what is in the box
ITEMS = [("14", "pages, every one designed"), ("9", "linked databases"),
         ("20", "charts and rollups, all computed"), ("0", "manual upkeep beyond Sunday")]
page("g4-inside", 1280, 720, 520, 48,
 """.box{position:absolute;right:76px;top:50%;transform:translateY(-50%);width:560px;z-index:2}
 .it{display:flex;align-items:baseline;gap:22px;padding:19px 0;border-bottom:1px solid #DFD8CA}
 .it:last-child{border-bottom:none}
 .it .n{font-size:46px;font-weight:700;color:#5B4FE8;line-height:1;width:76px;flex:none;text-align:right;
   letter-spacing:-.03em}
 .it .l{font-size:23px;color:#3A342B}""",
 f'''<div class="g"><div class="gl">
 <div class="ge">What is in the box</div>
 <div class="gh">A whole system,<br><b>not a to-do list.</b></div>
 <div class="ga"></div>
 <div class="gs">Goals, Areas, Projects, Tasks, Knowledge,<br>Reviews and Analytics — wired together.</div></div>
 <div class="box">{"".join(f'<div class="it"><div class="n">{n}</div><div class="l">{l}</div></div>' for n,l in ITEMS)}</div>{WM}</div>''')

# 5 — square thumbnail for Discover and the library grid
page("thumb", 600, 600, 600, 44,
 """.g{padding:0;display:block;background:#191510}
 .tw{position:absolute;inset:0;padding:54px;display:flex;flex-direction:column;justify-content:center;z-index:4}
 .tw .e{font-family:GM;font-size:14px;letter-spacing:.4em;text-transform:uppercase;color:#7C7468}
 .tw .m{font-size:78px;font-weight:700;letter-spacing:-.035em;color:#F7F6FD;line-height:.98;margin-top:14px}
 .tw .s{font-size:24px;color:#A8A8BC;margin-top:12px;line-height:1.35}
 .tw .r{height:5px;width:74px;background:#4dab9a;border-radius:3px;margin-top:22px}
 .tb{position:absolute;left:54px;right:54px;bottom:54px;display:flex;align-items:flex-end;
   gap:9px;height:118px;z-index:3}
 .tb i{flex:1;background:#4dab9a;border-radius:3px 3px 0 0;opacity:.34}
 .tg{position:absolute;left:-120px;top:-160px;width:620px;height:620px;border-radius:50%;
   background:radial-gradient(circle,#4dab9a2E 0%,#4dab9a12 40%,transparent 70%);z-index:1}""",
 '<div class="g"><div class="tg"></div><div class="tb">'
 + "".join(f'<i style="height:{b*22}px"></i>' for b in [1,2,2,3,1,3,1,1,2,4,3,5,5,3])
 + '</div><div class="tw"><div class="e">Notion Life OS</div>'
   '<div class="m">Nazzim <span style="color:#9A9AAE">نظّم</span></div><div class="s">Second Brain Pro</div>'
   '<div class="r"></div></div></div>')
