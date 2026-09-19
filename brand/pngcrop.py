"""Crop a PNG's height in pure Python.

Headless Chromium's --window-size is the WINDOW, not the viewport: the viewport
comes out ~87px shorter, and --screenshot still writes a window-sized image
whose bottom strip was never painted. So we render taller by that offset and
crop back, rather than hiding the strip behind a matching background colour.
"""
import struct, zlib, sys, pathlib

CHROME_OFFSET = 87  # window height minus viewport height, headless=new

def _chunks(data):
    i = 8
    while i < len(data):
        (ln,) = struct.unpack(">I", data[i:i + 4])
        typ = data[i + 4:i + 8]
        yield typ, data[i + 8:i + 8 + ln]
        i += 8 + ln + 4

def _chunk(typ, payload):
    return struct.pack(">I", len(payload)) + typ + payload + \
           struct.pack(">I", zlib.crc32(typ + payload) & 0xFFFFFFFF)

def crop_height(path, keep):
    raw = pathlib.Path(path).read_bytes()
    idat = b""
    for typ, payload in _chunks(raw):
        if typ == b"IHDR":
            w, h, depth, ctype, comp, filt, inter = struct.unpack(">IIBBBBB", payload)
        elif typ == b"IDAT":
            idat += payload
    if depth != 8 or ctype not in (2, 6) or inter != 0:
        raise SystemExit(f"{path}: unsupported PNG (depth={depth} ctype={ctype})")
    if keep >= h:
        return
    bpp = 4 if ctype == 6 else 3
    stride = w * bpp
    data = zlib.decompress(idat)

    out, prev = bytearray(), bytearray(stride)
    for y in range(keep):
        f = data[y * (stride + 1)]
        line = bytearray(data[y * (stride + 1) + 1:(y + 1) * (stride + 1)])
        for x in range(stride):
            a = line[x - bpp] if x >= bpp else 0
            b = prev[x]
            c = prev[x - bpp] if x >= bpp else 0
            if f == 1:   line[x] = (line[x] + a) & 0xFF
            elif f == 2: line[x] = (line[x] + b) & 0xFF
            elif f == 3: line[x] = (line[x] + ((a + b) >> 1)) & 0xFF
            elif f == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 0xFF
        out += b"\x00" + line          # re-emit with filter 0
        prev = line

    hdr = struct.pack(">IIBBBBB", w, keep, depth, ctype, comp, filt, inter)
    png = (b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", hdr)
           + _chunk(b"IDAT", zlib.compress(bytes(out), 9)) + _chunk(b"IEND", b""))
    pathlib.Path(path).write_bytes(png)

if __name__ == "__main__":
    crop_height(sys.argv[1], int(sys.argv[2]))
