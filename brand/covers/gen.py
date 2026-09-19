import subprocess, pathlib, json, sys
sys.path.insert(0, "..")
from pngcrop import crop_height

BARS = [1,2,2,3,1,3,1,1,2,4,3,5,5,3]          # the product's real 14-day completion shape
ZONE = {
    "ROOT":   "#4dab9a", "DAILY":  "#9a6dd7", "BUILD":  "#5e9ed6",
    "THINK":  "#4dab9a", "RHYTHM": "#ffa344", "SYSTEM": "#8f8madd".replace("add",""),
}
ZONE["SYSTEM"] = "#8f8a82"
SPECTRUM = ["#9a6dd7","#5e9ed6","#4dab9a","#ffa344","#8f8a82"]

PAGES = [                       # slug, page name (small), zone, masthead word (large)
    ("nazzim-pro",      "SECOND BRAIN PRO",   "ROOT",   "NAZZIM"),
    ("today",           "TODAY",              "DAILY",  "DAILY"),
    ("inbox",           "INBOX",              "DAILY",  "DAILY"),
    ("command-center",  "COMMAND CENTER",     "DAILY",  "DAILY"),
    ("tasks",           "TASKS",              "BUILD",  "BUILD"),
    ("projects",        "PROJECTS",           "BUILD",  "BUILD"),
    ("goals",           "GOALS",              "BUILD",  "BUILD"),
    ("areas",           "AREAS",              "BUILD",  "BUILD"),
    ("knowledge",       "KNOWLEDGE",          "THINK",  "THINK"),
    ("reviews",         "REVIEWS",            "RHYTHM", "RHYTHM"),
    ("analytics",       "ANALYTICS",          "RHYTHM", "RHYTHM"),
    ("archive",         "ARCHIVE",            "RHYTHM", "RHYTHM"),
    ("start-here",      "START HERE",         "SYSTEM", "SYSTEM"),
    ("settings",        "SETTINGS & HELP",    "SYSTEM", "SYSTEM"),
    ("databases",       "SYSTEM — DATABASES", "SYSTEM", "SYSTEM"),
]

TPL = """<!doctype html><meta charset="utf-8">
<style>
@font-face{{font-family:IS;src:url('file:///mnt/skills/examples/canvas-design/canvas-fonts/InstrumentSans-Bold.ttf');font-weight:700}}
@font-face{{font-family:GM;src:url('file:///mnt/skills/examples/canvas-design/canvas-fonts/GeistMono-Regular.ttf')}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1600px;height:400px;overflow:hidden}}
body{{background:#16130E;-webkit-font-smoothing:antialiased}}
.cv{{width:1600px;height:400px;position:relative;overflow:hidden;display:flex;align-items:center;justify-content:flex-end;padding:0 92px;
  background:#191510}}
.grain{{position:absolute;inset:0;z-index:5;opacity:.05;pointer-events:none;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)'/%3E%3C/svg%3E")}}
.glow{{position:absolute;left:-180px;top:-280px;width:940px;height:940px;border-radius:50%;
  background:radial-gradient(circle,{accent}2E 0%,{accent}12 40%,transparent 70%)}}
.bars{{position:absolute;left:92px;top:0;bottom:0;display:flex;align-items:flex-end;gap:13px;padding-bottom:100px;z-index:1}}
.bars i{{width:23px;border-radius:3px 3px 0 0}}
.txt{{position:relative;z-index:3;text-align:right}}
.eb{{font-family:GM;font-size:21px;letter-spacing:.44em;text-transform:uppercase;color:#7C7468}}
.rule{{height:5px;width:62px;background:{accent};border-radius:3px;margin:17px 0 21px auto}}
.nm{{font-family:IS;font-size:70px;font-weight:700;letter-spacing:.012em;text-transform:uppercase;
  color:#F5F1E8;line-height:1;white-space:nowrap}}
</style>
<div class="cv">
  <div class="glow"></div>
  <div class="grain"></div>
  <div class="bars">{bars}</div>
  <div class="txt">
    <div class="eb">NAZZIM · {eyebrow}</div>
    <div class="rule"></div>
    <div class="nm">{name}</div>
  </div>
</div>"""

def build(slug, eyebrow, zone, name):
    accent = ZONE[zone]
    bars = ""
    for i, b in enumerate(BARS):
        col = SPECTRUM[i % len(SPECTRUM)] if zone == "ROOT" else accent
        bars += f'<i style="height:{b*36}px;background:{col};opacity:.36"></i>'
    html = TPL.format(accent=accent, bars=bars, eyebrow=eyebrow, name=name)
    pathlib.Path(f"{slug}.html").write_text(html)
    subprocess.run(["/opt/pw-browsers/chromium-1194/chrome-linux/chrome","--headless=new","--no-sandbox",
        "--disable-gpu","--hide-scrollbars","--force-device-scale-factor=1","--window-size=1600,487",
        f"--screenshot=cover-{slug}.png","--virtual-time-budget=3000",f"{slug}.html"],
        capture_output=True)
    pathlib.Path(f"{slug}.html").unlink()
    crop_height(f"cover-{slug}.png", 400)
    return f"cover-{slug}.png"

if __name__ == "__main__":
    import sys
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for slug, eyebrow, zone, name in PAGES:
        if only and slug != only: continue
        print(build(slug, eyebrow, zone, name))
