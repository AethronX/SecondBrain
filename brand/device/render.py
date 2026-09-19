#!/usr/bin/env python3
"""Render the device showcase sheets at 2000x2000.

Chromium's --window-size is the window, so the viewport is ~87px shorter and
the bottom strip of a window-sized screenshot is never painted. Render taller,
then crop back to the intended canvas.
"""
import subprocess, sys, pathlib
sys.path.insert(0, "..")
from pngcrop import crop_height, CHROME_OFFSET

SIZE = 2000
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

for n in (sys.argv[1:] or ["1", "2", "3"]):
    out = f"nazzim-device-{n}.png"
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu",
                    "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--window-size={SIZE},{SIZE + CHROME_OFFSET}",
                    f"--screenshot={out}", "--virtual-time-budget=4000",
                    f"{n}.html"], capture_output=True)
    crop_height(out, SIZE)
    print(out)
