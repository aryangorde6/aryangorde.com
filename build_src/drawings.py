"""
Geometry for the SVG drawings on the page, computed at build time so the
browser receives finished SVG and no layout maths runs client-side.

  stack_diagram()   connector paths + boundary for the system drawing
  ring_figure()     the Teesri Shikayat ring: a schematic of the demo incident

Everything here is deterministic: same content in, byte-identical SVG out,
which keeps `build.py --check` honest.
"""

from __future__ import annotations

# The system drawing's coordinate space. Node x/y/w in content.py live in it.
VIEW_W, VIEW_H = 1200, 660
# Connectors attach this far below a node's top edge — the middle of its title
# bar — so a node can grow taller without its lines drifting off it.
ATTACH_Y = 24


def _fmt(n: float) -> str:
    """Compact, stable number formatting for SVG path data."""
    s = f"{n:.1f}"
    return s[:-2] if s.endswith(".0") else s


def elbow(x1: float, y1: float, x2: float, y2: float, r: float = 12) -> str:
    """Orthogonal connector: across, up/down, across — with rounded corners."""
    if abs(y2 - y1) < 1:
        return f"M{_fmt(x1)} {_fmt(y1)}H{_fmt(x2)}"
    mx = (x1 + x2) / 2
    r = min(r, abs(y2 - y1) / 2, abs(mx - x1))
    d = 1 if y2 > y1 else -1
    return (
        f"M{_fmt(x1)} {_fmt(y1)}"
        f"H{_fmt(mx - r)}"
        f"Q{_fmt(mx)} {_fmt(y1)} {_fmt(mx)} {_fmt(y1 + d * r)}"
        f"V{_fmt(y2 - d * r)}"
        f"Q{_fmt(mx)} {_fmt(y2)} {_fmt(mx + r)} {_fmt(y2)}"
        f"H{_fmt(x2)}"
    )


def stack_diagram(nodes: list[dict], ci: dict) -> dict:
    """Edges, boundary and CI lane for the system drawing.

    Each edge also gets a slot in the animation cycle (`t0`..`t1`, as fractions
    of one loop) so a request visibly travels client → edge → app and then fans
    out to data / async / AI, rather than every packet moving at once.
    """
    by_id = {n["id"]: n for n in nodes}

    # Depth of each node from the client, for sequencing the packets.
    depth = {nodes[0]["id"]: 0}
    queue = [nodes[0]["id"]]
    while queue:
        cur = queue.pop(0)
        for nxt in by_id[cur]["edges"]:
            if nxt not in depth:
                depth[nxt] = depth[cur] + 1
                queue.append(nxt)

    max_depth = max(depth.values()) or 1
    hop = 0.62 / max_depth          # the request spends ~62% of a loop in flight

    edges = []
    for n in nodes:
        for target in n["edges"]:
            t = by_id[target]
            x1, y1 = n["x"] + n["w"], n["y"] + ATTACH_Y
            x2, y2 = t["x"], t["y"] + ATTACH_Y
            start = depth[n["id"]] * hop
            edges.append({
                "from": n["id"], "to": target,
                "d": elbow(x1, y1, x2, y2),
                "t0": round(start, 3), "t1": round(start + hop * 0.9, 3),
            })

    # Dashed runtime boundary around every node except the client.
    server = [n for n in nodes if n is not nodes[0]]
    pad = 26
    bx = min(n["x"] for n in server) - pad
    by = min(n["y"] for n in server) - pad - 18     # headroom for the label
    bw = max(n["x"] + n["w"] for n in server) + pad - bx
    bh = VIEW_H - 16 - by

    # CI lane sits under the client and ships into the boundary.
    ci_box = {"x": nodes[0]["x"], "y": 478, "w": nodes[0]["w"]}
    cy = ci_box["y"] + ATTACH_Y
    edges.append({
        "from": "ci", "to": "runtime",
        "d": f"M{_fmt(ci_box['x'] + ci_box['w'])} {_fmt(cy)}H{_fmt(bx)}",
        "t0": 0.70, "t1": 0.92,
    })

    return {
        "view_w": VIEW_W, "view_h": VIEW_H,
        "edges": edges,
        "boundary": {"x": bx, "y": by, "w": bw, "h": bh,
                     "label_x": bx + 14, "label_y": by + 10},
        "ci": ci_box,
    }


# ---------------------------------------------------------------------------
# Teesri Shikayat: the ring
# ---------------------------------------------------------------------------
# A schematic of the recorded demo incident: 3 homes report, every enrolled
# home inside 250 m is warned — 23 in all, 20 of which never complained — and
# homes outside the ring are not. Positions are illustrative (seeded, so the
# build stays deterministic); the counts are the demo's real ones.

RING_REPORTED, RING_WARNED, RING_OUTSIDE = 3, 20, 11


def ring_figure(seed: int = 11) -> dict:
    import math
    import random

    W, H = 600, 380
    cx, cy, R = 300, 196, 150
    rng = random.Random(seed)
    placed: list[tuple[float, float]] = []
    # keep labels clear: legend top-left, scale label top-right
    keep_out = [(0, 0, 210, 74), (420, 0, 600, 60)]

    def free(x, y, gap):
        if any(x0 - 8 <= x <= x1 + 8 and y0 - 8 <= y <= y1 + 8 for x0, y0, x1, y1 in keep_out):
            return False
        return all((x - px) ** 2 + (y - py) ** 2 >= gap * gap for px, py in placed)

    def sample(n, rmin, rmax, gap, box=None):
        out, tries = [], 0
        while len(out) < n:
            tries += 1
            if tries > 20000:
                raise RuntimeError("ring_figure: could not place homes; loosen the layout")
            a = rng.uniform(0, 2 * math.pi)
            r = math.sqrt(rng.uniform(rmin ** 2, rmax ** 2))
            x, y = cx + r * math.cos(a), cy + r * math.sin(a)
            if box and not (box[0] <= x <= box[2] and box[1] <= y <= box[3]):
                continue
            if free(x, y, gap):
                placed.append((x, y))
                out.append((x, y))
        return out

    reported = sample(RING_REPORTED, 8, 42, 24)
    warned = sample(RING_WARNED, 30, R - 12, 30)
    outside = sample(RING_OUTSIDE, R + 18, 290, 34, box=(16, 16, W - 16, H - 16))

    def home(p, kind):
        d = math.hypot(p[0] - cx, p[1] - cy) / R
        return {"x": _fmt(p[0] - 5), "y": _fmt(p[1] - 5), "kind": kind,
                "delay": f"{0.55 + d * 0.9:.2f}s"}

    homes = ([home(p, "reported") for p in reported]
             + sorted((home(p, "warned") for p in warned), key=lambda h: h["delay"])
             + [home(p, "outside") for p in outside])

    ang = math.radians(-32)
    return {
        "w": W, "h": H, "cx": cx, "cy": cy, "r": R,
        "homes": homes,
        "scale": {"x2": _fmt(cx + R * math.cos(ang)), "y2": _fmt(cy + R * math.sin(ang)),
                  "lx": _fmt(cx + R * 0.55 * math.cos(ang) + 6),
                  "ly": _fmt(cy + R * 0.55 * math.sin(ang) - 8)},
        "counts": {"reported": RING_REPORTED, "warned": RING_REPORTED + RING_WARNED,
                   "never": RING_WARNED},
    }
