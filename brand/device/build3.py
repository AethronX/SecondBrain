import re, sys

def read(p): return open(p).read()

def style_of(src):
    return re.search(r'<style>(.*?)</style>', src, re.S).group(1)

def scope(css, sel_prefix, skip=('.sheet',)):
    out=[]
    for chunk in css.split('}'):
        if '{' not in chunk: continue
        sels, body = chunk.split('{',1)
        sels = sels.strip()
        if not sels: continue
        if any(sels.startswith(s) for s in skip): continue
        parts=[]
        for s in sels.split(','):
            s=s.strip()
            if not s: continue
            parts.append(s if s.startswith(sel_prefix) else sel_prefix+' '+s)
        out.append(', '.join(parts)+'{'+body.strip()+'}')
    return '\n'.join(out)

def block(src, opentag):
    i = src.index(opentag)
    depth=0; j=i
    for m in re.finditer(r'<div\b|</div>', src[i:]):
        depth += 1 if m.group(0)!='</div>' else -1
        if depth==0:
            j = i+m.end(); break
    return src[i:j]

one, two = read('1.html'), read('2.html')
lap_css   = scope(style_of(one), '.lap')
phone_css = scope(style_of(two), '.ph')
lap  = block(one, '<div class="lap">')
ph   = block(two, '<div class="ph">')

html = f'''<link rel="stylesheet" href="_d.css">
<style>
.sheet{{padding:110px 90px 120px}}
.rig{{position:relative;width:1820px;height:1150px}}
.lapwrap{{position:absolute;left:0;top:0;transform:scale(.82);transform-origin:top left}}
.phwrap{{position:absolute;right:30px;bottom:0;transform:scale(.62);transform-origin:bottom right;z-index:3}}
.phwrap .ph{{box-shadow:0 2px 0 rgba(255,255,255,.14) inset,-90px 70px 150px -40px rgba(0,0,0,.42)}}
{lap_css}
{phone_css}
</style>
<div class="sheet">
  <div class="eyebrow">Notion Life OS · Desktop &amp; Mobile</div>
  <div class="stage">
    <div class="rig">
      <div class="lapwrap">{lap}</div>
      <div class="phwrap">{ph}</div>
    </div>
  </div>
  <div class="foot">
    <div>
      <div class="wordmark">NAZZIM</div>
      <div class="tag">Turn information into execution.</div>
    </div>
    <div class="meta">Second Brain Pro<br>Same system, both screens<br>Notion template</div>
  </div>
</div>
'''
open('3.html','w').write(html)
print('3.html', len(html))
