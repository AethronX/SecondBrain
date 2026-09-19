"""Pull the device markup and its scoped styles out of the 2000x2000 sheets,
so every derived layout renders the same UI instead of a second copy of it."""
import re

def style_of(src):
    return re.search(r'<style>(.*?)</style>', src, re.S).group(1)

def scope(css, sel_prefix, skip=('.sheet',)):
    out = []
    for chunk in css.split('}'):
        if '{' not in chunk:
            continue
        sels, body = chunk.split('{', 1)
        sels = sels.strip()
        if not sels or any(sels.startswith(s) for s in skip):
            continue
        parts = [s.strip() if s.strip().startswith(sel_prefix) else sel_prefix + ' ' + s.strip()
                 for s in sels.split(',') if s.strip()]
        out.append(', '.join(parts) + '{' + body.strip() + '}')
    return '\n'.join(out)

def block(src, opentag):
    i = src.index(opentag)
    depth = 0
    for m in re.finditer(r'<div\b|</div>', src[i:]):
        depth += 1 if m.group(0) != '</div>' else -1
        if depth == 0:
            return src[i:i + m.end()]
    raise ValueError(f"unclosed {opentag}")
