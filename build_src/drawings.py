"""
Geometry the templates draw, computed here so every build is identical.

tripwire_homes(): the simulated neighbourhood for the Teesri Shikayat demo.
Positions are in metres on a 900 × 520 m plot, seeded, so the page is
byte-identical from build to build. They're illustrative homes, not a real
map; the rule they test is the project's own (3 homes, every pair within
250 m, inside 72 hours).
"""

import math
import random

PLOT_W, PLOT_H = 900, 520


def tripwire_homes(n=46, seed=7, spacing=46, margin=28):
    rng = random.Random(seed)
    homes = []
    tries = 0
    while len(homes) < n and tries < 20000:
        tries += 1
        # Denser towards the middle, like a neighbourhood round a main road.
        x = margin + (PLOT_W - 2 * margin) * (rng.random() + rng.random()) / 2
        y = margin + (PLOT_H - 2 * margin) * (rng.random() + rng.random() + rng.random()) / 3
        if all(math.hypot(x - hx, y - hy) >= spacing for hx, hy in homes):
            homes.append((round(x), round(y)))
    homes.sort(key=lambda h: (h[1] // 60, h[0]))   # reading order for keyboard users
    return {
        "w": PLOT_W,
        "h": PLOT_H,
        "homes": [{"i": i + 1, "x": x, "y": y,
                   "px": round(100 * x / PLOT_W, 3), "py": round(100 * y / PLOT_H, 3)}
                  for i, (x, y) in enumerate(homes)],
    }
