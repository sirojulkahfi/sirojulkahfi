# -*- coding: utf-8 -*-
"""
generate_industrial_svg.py
Generates: assets/industrial_mario_bros_scene.svg
─────────────────────────────────────────────────
Mario Bros Anime Industrial Factory — Fully Animated SVG
Built entirely from scratch using SVG primitives + CSS/SMIL animations.

Layers (back to front):
  1. Brick wall background
  2. Arched windows (sky)
  3. Chimneys
  4. Left pipe system + fittings + valves
  5. Gauges × 3 (animated needles via animateTransform)
  6. Gear cluster × 3 (animated via animateTransform)
  7. Factory machines (colored PLC boxes)
  8. Right control console + monitor + buttons
  9. Conveyor belt (animated pattern)
 10. Catwalk / platform + railings
 11. Worker figures
 12. Warning signs
 13. Steam clouds (10 staggered)
 14. Bouncing coins
 15. Pipe energy arrows (CSS)
 16. Indicator lamps
 17. Vignette overlay
"""
import math, os

W, H = 960, 540

# ─────────────────────────────────────────────────────────────────────────────
# UTILITIES
# ─────────────────────────────────────────────────────────────────────────────

def gear_path(cx, cy, n, r1, r2, tf=0.38, vf=0.22):
    """Return SVG path string for a spur gear.
    n=tooth count, r1=inner(root) radius, r2=outer(tip) radius.
    tf=tooth-fraction of step angle, vf=valley-fraction of step.
    """
    step = 2 * math.pi / n
    segs = []
    for i in range(n):
        base = i * step
        ts   = base - tf * step
        te   = base + tf * step
        vs   = base - vf * step
        nv   = (i + 1) * step - vf * step

        def p(r, a):
            return f"{cx + r*math.cos(a):.2f},{cy + r*math.sin(a):.2f}"

        if i == 0:
            segs.append(f"M{p(r1, vs)}")
        segs.append(f"L{p(r1, ts)} L{p(r2, ts)} L{p(r2, te)} L{p(r1, te)}")
        segs.append(f"A{r1:.2f},{r1:.2f} 0 0,1 {p(r1, nv)}")
    segs.append("Z")
    return " ".join(segs)


def worker(cx, by, color="#FF8820", hat="#EE2222"):
    """Simple 2D worker figure SVG (returns string)."""
    hy = by - 54
    segs = [
        # Hat
        f'<rect x="{cx-8}" y="{hy}" width="16" height="7" rx="2" fill="{hat}"/>',
        f'<rect x="{cx-5}" y="{hy+5}" width="10" height="4" rx="1" fill="{hat}"/>',
        # Head
        f'<circle cx="{cx}" cy="{hy+16}" r="10" fill="#FFCC88"/>',
        # Body
        f'<rect x="{cx-9}" y="{hy+26}" width="18" height="20" rx="3" fill="{color}"/>',
        # Arms
        f'<line x1="{cx-9}" y1="{hy+30}" x2="{cx-18}" y2="{hy+42}" stroke="{color}" stroke-width="5" stroke-linecap="round"/>',
        f'<line x1="{cx+9}" y1="{hy+30}" x2="{cx+16}" y2="{hy+28}" stroke="{color}" stroke-width="5" stroke-linecap="round"/>',
        # Legs
        f'<line x1="{cx-4}" y1="{hy+46}" x2="{cx-6}" y2="{by}" stroke="#224488" stroke-width="6" stroke-linecap="round"/>',
        f'<line x1="{cx+4}" y1="{hy+46}" x2="{cx+6}" y2="{by}" stroke="#224488" stroke-width="6" stroke-linecap="round"/>',
    ]
    return "\n".join(segs)


def gauge(cx, cy, r, label, ndl_from, ndl_to, ndl_mid, ndl_dur, accent):
    """Detailed industrial pressure gauge with animated needle."""
    segs = []
    # Drop shadow
    segs.append(f'<circle cx="{cx+4}" cy="{cy+5}" r="{r+7}" fill="#00000050"/>')
    # Bezel
    segs.append(f'<circle cx="{cx}" cy="{cy}" r="{r+8}" fill="url(#gbezel)"/>')
    segs.append(f'<circle cx="{cx}" cy="{cy}" r="{r+4}" fill="none" stroke="#787878" stroke-width="2"/>')
    # Glass face
    segs.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#gface)"/>')
    # Tick marks (scale: 225° → 495° = 270° arc, CCW standard)
    for ti in range(21):
        frac   = ti / 20
        adeg   = 225 + frac * 270
        arad   = math.radians(adeg)
        major  = (ti % 4 == 0)
        r_out  = r - 3
        r_in   = r_out - (10 if major else 5)
        x1     = cx + r_out * math.cos(arad)
        y1     = cy + r_out * math.sin(arad)
        x2     = cx + r_in  * math.cos(arad)
        y2     = cy + r_in  * math.sin(arad)
        segs.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                    f'stroke="{"#444" if major else "#666"}" stroke-width="{"2" if major else "1"}"/>')
        if major:
            val   = int(frac * 100)
            nr    = r_in - 10
            nx    = cx + nr * math.cos(arad)
            ny    = cy + nr * math.sin(arad)
            segs.append(f'<text x="{nx:.1f}" y="{ny:.1f}" fill="#3A3A3A" font-size="7" '
                        f'text-anchor="middle" dominant-baseline="middle" '
                        f'font-family="monospace">{val}</text>')
    # Red zone arc (80–100%)
    def arc_pt(frac):
        a = math.radians(225 + frac * 270)
        return f"{cx+(r-4)*math.cos(a):.1f},{cy+(r-4)*math.sin(a):.1f}"
    rz1 = math.radians(225 + 0.78 * 270)
    rz2 = math.radians(225 + 1.00 * 270)
    ax1 = cx + (r-4) * math.cos(rz1);  ay1 = cy + (r-4) * math.sin(rz1)
    ax2 = cx + (r-4) * math.cos(rz2);  ay2 = cy + (r-4) * math.sin(rz2)
    segs.append(f'<path d="M{ax1:.1f},{ay1:.1f} A{r-4},{r-4} 0 0,1 {ax2:.1f},{ay2:.1f}" '
                f'fill="none" stroke="#DD2222" stroke-width="6" opacity="0.65"/>')
    # Label
    segs.append(f'<text x="{cx}" y="{cy+r*0.32:.0f}" fill="{accent}" font-size="{"7" if len(label)>6 else "8"}" '
                f'font-family="monospace" font-weight="bold" text-anchor="middle">{label}</text>')
    # Needle (draw pointing at 225° = 0 value; animate rotation around center)
    nl  = r * 0.72
    cw  = r * 0.20   # counterweight
    arad0 = math.radians(225)
    nx  = cx + nl  * math.cos(arad0)
    ny  = cy + nl  * math.sin(arad0)
    cwx = cx - cw  * math.cos(arad0)
    cwy = cy - cw  * math.sin(arad0)
    # Animate: rotate from ndl_from to ndl_to around gauge center
    anim = (f'<animateTransform attributeName="transform" type="rotate" '
            f'values="{ndl_from} {cx} {cy};{ndl_to} {cx} {cy};{ndl_mid} {cx} {cy};{ndl_from} {cx} {cy}" '
            f'keyTimes="0;0.35;0.65;1" dur="{ndl_dur}s" repeatCount="indefinite" '
            f'calcMode="spline" keySplines=".42 0 .58 1;.42 0 .58 1;.42 0 .58 1"/>')
    segs.append(f'<g>{anim}'
                f'<line x1="{cwx:.1f}" y1="{cwy:.1f}" x2="{nx:.1f}" y2="{ny:.1f}" '
                f'stroke="#CC1010" stroke-width="3" stroke-linecap="round"/>'
                f'<line x1="{cwx:.1f}" y1="{cwy:.1f}" x2="{nx:.1f}" y2="{ny:.1f}" '
                f'stroke="#FF5555" stroke-width="1.5" stroke-linecap="round"/>'
                f'</g>')
    # Center hub
    segs.append(f'<circle cx="{cx}" cy="{cy}" r="6" fill="#222"/>')
    segs.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="#666"/>')
    segs.append(f'<circle cx="{cx}" cy="{cy}" r="2" fill="#CCC"/>')
    # Glass glare
    gr = r * 0.50
    segs.append(f'<ellipse cx="{cx-r*0.25:.0f}" cy="{cy-r*0.32:.0f}" '
                f'rx="{gr*0.45:.0f}" ry="{gr*0.30:.0f}" fill="#FFFFFF" opacity="0.14" '
                f'transform="rotate(-30 {cx} {cy})"/>')
    return "\n".join(segs)


# ─────────────────────────────────────────────────────────────────────────────
# BUILD SVG
# ─────────────────────────────────────────────────────────────────────────────

lines = []
_ = lines.append

_(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
  f'viewBox="0 0 {W} {H}" width="100%" '
  f'style="max-width:{W}px;display:block;margin:0 auto;background:#1E0800">')

# ═══════════════════════════════════════════════════════
# DEFS
# ═══════════════════════════════════════════════════════
_('<defs>')

# ── Clip paths for windows ──
WIN_SPECS = [(294, 162, 52, 145, 58), (440, 146, 62, 162, 68), (576, 155, 50, 140, 56)]
for i, (cx, yb, hw, ah, ar) in enumerate(WIN_SPECS):
    rect_top = yb - ah + ar
    d = (f"M{cx-hw},{yb} L{cx-hw},{rect_top} "
         f"A{hw},{ar} 0 0,1 {cx+hw},{rect_top} L{cx+hw},{yb} Z")
    _(f'<clipPath id="wc{i}"><path d="{d}"/></clipPath>')

_( '''<!-- ── FILTERS ── -->
<filter id="glow4" x="-40%" y="-40%" width="180%" height="180%">
  <feGaussianBlur stdDeviation="4" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="glow8" x="-60%" y="-60%" width="220%" height="220%">
  <feGaussianBlur stdDeviation="8" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="glow16" x="-100%" y="-100%" width="300%" height="300%">
  <feGaussianBlur stdDeviation="16" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="shadow" x="-20%" y="-20%" width="160%" height="180%">
  <feDropShadow dx="2" dy="5" stdDeviation="7" flood-color="#00000075"/>
</filter>
<filter id="fsteam" x="-80%" y="-120%" width="360%" height="440%">
  <feGaussianBlur stdDeviation="14"/>
</filter>

<!-- ── GRADIENTS ── -->
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%"   stop-color="#1070C0"/>
  <stop offset="45%"  stop-color="#38B0E8"/>
  <stop offset="100%" stop-color="#A0E0F8"/>
</linearGradient>
<linearGradient id="ph" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%"   stop-color="#0C3A0C"/>
  <stop offset="18%"  stop-color="#249824"/>
  <stop offset="50%"  stop-color="#44E644"/>
  <stop offset="82%"  stop-color="#249824"/>
  <stop offset="100%" stop-color="#0C3A0C"/>
</linearGradient>
<linearGradient id="pv" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%"   stop-color="#0C3A0C"/>
  <stop offset="18%"  stop-color="#249824"/>
  <stop offset="50%"  stop-color="#44E644"/>
  <stop offset="82%"  stop-color="#249824"/>
  <stop offset="100%" stop-color="#0C3A0C"/>
</linearGradient>
<linearGradient id="pvr" x1="1" y1="0" x2="0" y2="0">
  <stop offset="0%"   stop-color="#0C3A0C"/>
  <stop offset="18%"  stop-color="#249824"/>
  <stop offset="50%"  stop-color="#44E644"/>
  <stop offset="82%"  stop-color="#249824"/>
  <stop offset="100%" stop-color="#0C3A0C"/>
</linearGradient>
<radialGradient id="gg1" cx="33%" cy="28%" r="72%">
  <stop offset="0%"   stop-color="#FFEE7A"/>
  <stop offset="32%"  stop-color="#C08808"/>
  <stop offset="100%" stop-color="#482A00"/>
</radialGradient>
<radialGradient id="gg2" cx="38%" cy="33%" r="68%">
  <stop offset="0%"   stop-color="#FFD84A"/>
  <stop offset="38%"  stop-color="#B07608"/>
  <stop offset="100%" stop-color="#3C2000"/>
</radialGradient>
<radialGradient id="gface" cx="40%" cy="35%" r="65%">
  <stop offset="0%"   stop-color="#F0FFF0"/>
  <stop offset="62%"  stop-color="#C8DCC8"/>
  <stop offset="100%" stop-color="#86A886"/>
</radialGradient>
<radialGradient id="gbezel" cx="28%" cy="22%" r="78%">
  <stop offset="0%"   stop-color="#5A5A5A"/>
  <stop offset="52%"  stop-color="#262626"/>
  <stop offset="100%" stop-color="#060606"/>
</radialGradient>
<linearGradient id="cpanel" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%"   stop-color="#2C2C42"/>
  <stop offset="100%" stop-color="#101018"/>
</linearGradient>
<linearGradient id="cpanel2" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%"   stop-color="#363648" stop-opacity="0.8"/>
  <stop offset="100%" stop-color="#1A1A28" stop-opacity="0.8"/>
</linearGradient>
<radialGradient id="mscreen" cx="48%" cy="46%" r="60%">
  <stop offset="0%"   stop-color="#2AFFA0"/>
  <stop offset="52%"  stop-color="#00BB44"/>
  <stop offset="100%" stop-color="#001E0A"/>
</radialGradient>
<linearGradient id="mb" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%"   stop-color="#5CB8F0"/>
  <stop offset="100%" stop-color="#2644A0"/>
</linearGradient>
<linearGradient id="mp" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%"   stop-color="#B84AF0"/>
  <stop offset="100%" stop-color="#5A10A8"/>
</linearGradient>
<linearGradient id="mt" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%"   stop-color="#30CC60"/>
  <stop offset="100%" stop-color="#105828"/>
</linearGradient>
<linearGradient id="my" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%"   stop-color="#FFBB20"/>
  <stop offset="100%" stop-color="#A05000"/>
</linearGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%"   stop-color="#464646"/>
  <stop offset="100%" stop-color="#161616"/>
</linearGradient>
<linearGradient id="catw" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%"   stop-color="#B09040"/>
  <stop offset="50%"  stop-color="#D8B840"/>
  <stop offset="100%" stop-color="#786018"/>
</linearGradient>
<radialGradient id="vig" cx="50%" cy="50%" r="72%">
  <stop offset="0%"   stop-color="#000" stop-opacity="0"/>
  <stop offset="62%"  stop-color="#000" stop-opacity="0"/>
  <stop offset="100%" stop-color="#000" stop-opacity="0.62"/>
</radialGradient>
<linearGradient id="sborder" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0%"   stop-color="#448844"/>
  <stop offset="50%"  stop-color="#AACC22"/>
  <stop offset="100%" stop-color="#448844"/>
</linearGradient>

<!-- ── PATTERNS ── -->
<pattern id="brick" x="0" y="0" width="64" height="30" patternUnits="userSpaceOnUse">
  <rect width="64" height="30" fill="#7A2A0A"/>
  <rect x="1"  y="1"  width="61" height="13" rx="1" fill="#9C3A10"/>
  <rect x="33" y="16" width="30" height="13" rx="1" fill="#9C3A10"/>
  <rect x="1"  y="16" width="30" height="13" rx="1" fill="#9C3A10"/>
  <line x1="0" y1="14" x2="64" y2="14" stroke="#3E0A04" stroke-width="2.5"/>
  <line x1="0" y1="29" x2="64" y2="29" stroke="#3E0A04" stroke-width="1.5"/>
  <line x1="32" y1="0" x2="32" y2="14" stroke="#3E0A04" stroke-width="1.5"/>
  <line x1="0"  y1="14" x2="0"  y2="30" stroke="#3E0A04" stroke-width="1.5"/>
  <line x1="63" y1="14" x2="63" y2="30" stroke="#3E0A04" stroke-width="1.5"/>
</pattern>
<pattern id="grat" x="0" y="0" width="18" height="18" patternUnits="userSpaceOnUse">
  <rect width="18" height="18" fill="#282828"/>
  <line x1="0" y1="0"  x2="18" y2="18" stroke="#363636" stroke-width="1.5"/>
  <line x1="18" y1="0" x2="0"  y2="18" stroke="#363636" stroke-width="1.5"/>
  <circle cx="9" cy="9" r="2" fill="#303030"/>
</pattern>
<pattern id="conv" x="0" y="0" width="48" height="36" patternUnits="userSpaceOnUse">
  <rect width="48" height="36" fill="#252525"/>
  <rect x="0" y="0"  width="24" height="36" fill="#2E2E2E"/>
  <rect x="0" y="0"  width="48" height="5"  fill="#181818"/>
  <rect x="0" y="16" width="48" height="4"  fill="#181818"/>
  <rect x="0" y="31" width="48" height="5"  fill="#181818"/>
  <animateTransform attributeName="patternTransform" type="translate"
    from="0 0" to="48 0" dur="1.3s" repeatCount="indefinite"/>
</pattern>
''')

# ── CSS Animations ──────────────────────────────────────────────────────────
_( '''<style>
/* GEARS */
.gA{animation:cw  5.4s linear infinite;transform-box:fill-box;transform-origin:center}
.gB{animation:ccw 3.1s linear infinite;transform-box:fill-box;transform-origin:center}
.gC{animation:cw  4.1s linear infinite;transform-box:fill-box;transform-origin:center}
@keyframes cw {to{transform:rotate(360deg)}}
@keyframes ccw{to{transform:rotate(-360deg)}}

/* STEAM */
.sa{animation:stm 3.1s ease-out 0.0s infinite}
.sb{animation:stm 3.1s ease-out 1.0s infinite}
.sc{animation:stm 3.1s ease-out 2.1s infinite}
.sd{animation:stm 2.5s ease-out 0.4s infinite}
.se{animation:stm 2.5s ease-out 1.5s infinite}
.sf{animation:stm 2.5s ease-out 2.6s infinite}
.sg{animation:stm 3.8s ease-out 0.7s infinite}
.sh{animation:stm 3.8s ease-out 1.9s infinite}
.si{animation:stm 2.9s ease-out 0.3s infinite}
.sj{animation:stm 2.9s ease-out 1.4s infinite}
@keyframes stm{
  0%  {transform:translateY(0)    scale(0.32);opacity:.82}
  22% {transform:translateY(-26px) scale(0.80);opacity:.62}
  58% {transform:translateY(-72px) scale(1.70);opacity:.26}
  100%{transform:translateY(-120px) scale(2.70);opacity:0}
}

/* BUTTONS */
.b0{animation:btn 1.6s step-end 0.00s infinite}
.b1{animation:btn 1.6s step-end 0.18s infinite}
.b2{animation:btn 1.6s step-end 0.36s infinite}
.b3{animation:btn 1.6s step-end 0.53s infinite}
.b4{animation:btn 1.6s step-end 0.71s infinite}
.b5{animation:btn 1.6s step-end 0.89s infinite}
.b6{animation:btn 1.6s step-end 1.07s infinite}
.b7{animation:btn 1.6s step-end 1.24s infinite}
.b8{animation:btn 1.6s step-end 1.42s infinite}
@keyframes btn{0%,49%{opacity:1}50%,100%{opacity:.09}}

/* BEACON */
.bcon{animation:bcon .52s ease-in-out infinite alternate}
.bhal{animation:bhal .52s ease-in-out infinite alternate}
@keyframes bcon{from{opacity:.06}to{opacity:1}}
@keyframes bhal{from{opacity:0;r:14}to{opacity:.62;r:32}}

/* MONITOR */
.scrf{animation:scrf 7s ease-in-out infinite}
@keyframes scrf{0%,86%,100%{opacity:1}87%{opacity:.2}89%{opacity:.8}91%{opacity:.15}93%{opacity:1}}
.scrl{animation:scrl 1.6s linear infinite}
@keyframes scrl{from{transform:translateY(0)}to{transform:translateY(24px)}}

/* LAMPS */
.lr{animation:lmp .85s step-end 0.00s infinite}
.ly{animation:lmp .85s step-end 0.28s infinite}
.lg{animation:lmp .85s step-end 0.57s infinite}
@keyframes lmp{0%,49%{opacity:1}50%,100%{opacity:.10}}

/* ENERGY ARROWS */
.ea{animation:ea .85s ease-in-out infinite alternate}
@keyframes ea{from{fill:#1A9A1A;opacity:.45}to{fill:#66FF66;opacity:1}}

/* MACHINE GLOW */
.mg{animation:mg 2.4s ease-in-out infinite alternate}
@keyframes mg{from{opacity:.28}to{opacity:.82}}

/* COINS */
.ca{animation:coi 1.5s ease-in-out 0.0s infinite}
.cb{animation:coi 1.5s ease-in-out 0.5s infinite}
.cc{animation:coi 1.5s ease-in-out 1.0s infinite}
@keyframes coi{0%,100%{transform:translateY(0)}46%,54%{transform:translateY(-24px)}}

/* WARNING SIGN */
.ws{animation:ws 1.2s step-end infinite}
@keyframes ws{0%,49%{opacity:1}50%,100%{opacity:.20}}

/* PIPE PULSE */
.pp{animation:pp 2.0s ease-in-out infinite}
@keyframes pp{0%,100%{opacity:.18}50%{opacity:.65}}

/* SCREEN SCANLINES */
.scanl{animation:scanl 3s linear infinite}
@keyframes scanl{from{transform:translateY(-100%)}to{transform:translateY(100%)}}
</style>''')

_('</defs>')

# ═══════════════════════════════════════════════════════════════════════════════
# LAYER 1 — BACKGROUND
# ═══════════════════════════════════════════════════════════════════════════════
_(f'<rect width="{W}" height="{H}" fill="url(#brick)"/>')
# Ceiling shadow
_(f'<rect x="0" y="0" width="{W}" height="88" fill="#000" opacity="0.35"/>')
# Floor shadow
_(f'<rect x="0" y="400" width="{W}" height="140" fill="#000" opacity="0.25"/>')
# Warm factory ambient light (center)
_(f'<ellipse cx="478" cy="275" rx="320" ry="190" fill="#FF6600" opacity="0.055"/>')

# ═══════════════════════════════════════════════════════════════════════════════
# LAYER 2 — ARCHED WINDOWS
# ═══════════════════════════════════════════════════════════════════════════════

def draw_window(i, cx, yb, hw, ah, ar):
    rect_top = yb - ah + ar
    d = (f"M{cx-hw},{yb} L{cx-hw},{rect_top} "
         f"A{hw},{ar} 0 0,1 {cx+hw},{rect_top} L{cx+hw},{yb} Z")
    _( f'<g filter="url(#shadow)">')
    # Sky fill
    _( f'  <path d="{d}" fill="url(#sky)" clip-path="url(#wc{i})"/>')
    # Clouds in sky
    _( f'  <ellipse cx="{cx-10}" cy="{rect_top+30}" rx="22" ry="11" fill="#FFFFFFCC" clip-path="url(#wc{i})"/>')
    _( f'  <ellipse cx="{cx+15}" cy="{rect_top+22}" rx="18" ry="9"  fill="#FFFFFFBB" clip-path="url(#wc{i})"/>')
    _( f'  <ellipse cx="{cx}"    cy="{rect_top+42}" rx="28" ry="13" fill="#FFFFFF88" clip-path="url(#wc{i})"/>')
    # Frame
    _( f'  <path d="{d}" fill="none" stroke="#382008" stroke-width="9"/>')
    # Crossbars
    bar_y = int(rect_top + (yb - rect_top) * 0.52)
    _( f'  <line x1="{cx-hw}" y1="{bar_y}" x2="{cx+hw}" y2="{bar_y}" stroke="#382008" stroke-width="7"/>')
    _( f'  <line x1="{cx}" y1="{rect_top}" x2="{cx}" y2="{yb}" stroke="#382008" stroke-width="7"/>')
    # Glare
    _( f'  <ellipse cx="{cx-hw*0.38:.0f}" cy="{rect_top+ah*0.18:.0f}" rx="{hw*0.32:.0f}" ry="{ah*0.14:.0f}" '
       f'fill="#FFF" opacity="0.16" clip-path="url(#wc{i})"/>')
    # Sill ledge
    _( f'  <rect x="{cx-hw-6}" y="{yb}" width="{(hw+6)*2}" height="9" rx="2" fill="#52300A"/>')
    _( f'</g>')

for i, (cx, yb, hw, ah, ar) in enumerate(WIN_SPECS):
    draw_window(i, cx, yb, hw, ah, ar)

# ═══════════════════════════════════════════════════════════════════════════════
# LAYER 3 — CHIMNEYS (exterior, top)
# ═══════════════════════════════════════════════════════════════════════════════
# Left chimney
_(f'<rect x="272" y="-4" width="46" height="78" fill="#8A3010" stroke="#3E0A06" stroke-width="2"/>')
_(f'<rect x="264" y="65" width="62" height="17" rx="3" fill="#6A2008" stroke="#3E0A06" stroke-width="2"/>')
for gy in range(0, 75, 15):
    _(f'<line x1="272" y1="{gy}" x2="318" y2="{gy}" stroke="#3E0A06" stroke-width="1.5" opacity="0.65"/>')
# Right chimney
_(f'<rect x="546" y="-4" width="38" height="65" fill="#8A3010" stroke="#3E0A06" stroke-width="2"/>')
_(f'<rect x="539" y="54" width="52" height="14" rx="3" fill="#6A2008" stroke="#3E0A06" stroke-width="2"/>')
for gy in range(0, 58, 15):
    _(f'<line x1="546" y1="{gy}" x2="584" y2="{gy}" stroke="#3E0A06" stroke-width="1.5" opacity="0.65"/>')

# ═══════════════════════════════════════════════════════════════════════════════
# LAYER 4 — LEFT PIPE SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════
PVX, PVW = 14, 36          # main vertical pipe x, width
BPH = 22                   # branch pipe height
H1Y, H2Y = 288, 408        # horizontal branches y
BRANCH_END = 256           # pipes extend to x=256

# Main left vertical pipe
_(f'<rect x="{PVX}" y="0" width="{PVW}" height="{H}" fill="url(#pv)" rx="3"/>')
# Highlight stripe on pipe
_(f'<rect x="{PVX+8}" y="0" width="8" height="{H}" fill="#66FF66" opacity="0.16"/>')
# Ring joints every ~80px
for jy in [78, 158, 238, 318, 398, 478]:
    _(f'<rect x="{PVX-5}" y="{jy-5}" width="{PVW+10}" height="10" rx="4" '
      f'fill="#1C5A1C" stroke="#0A2E0A" stroke-width="1.5"/>')

# Secondary thinner pipe (x=84)
SPX, SPW = 82, 18
_(f'<rect x="{SPX}" y="86" width="{SPW}" height="205" fill="url(#pv)" rx="2"/>')

# Branch 1 horizontal (y=H1Y)
_(f'<rect x="{PVX+PVW}" y="{H1Y}" width="{BRANCH_END-PVX-PVW}" height="{BPH}" fill="url(#ph)" rx="2"/>')
_(f'<rect x="{PVX+PVW+12}" y="{H1Y+5}" width="170" height="5" fill="#66FF66" opacity="0.15"/>')
# Energy arrows B1
for ax in range(62, 244, 42):
    _(f'<polygon points="{ax},{H1Y+4} {ax+16},{H1Y+BPH//2} {ax},{H1Y+BPH-4}" '
      f'fill="#2EEE2E" class="ea"/>')

# Branch 2 horizontal (y=H2Y)
_(f'<rect x="{PVX+PVW}" y="{H2Y}" width="{BRANCH_END-PVX-PVW}" height="{BPH}" fill="url(#ph)" rx="2"/>')
_(f'<rect x="{PVX+PVW+12}" y="{H2Y+5}" width="170" height="5" fill="#66FF66" opacity="0.15"/>')
for ax in range(62, 244, 42):
    _(f'<polygon points="{ax},{H2Y+4} {ax+16},{H2Y+BPH//2} {ax},{H2Y+BPH-4}" '
      f'fill="#2EEE2E" class="ea"/>')

# Pipe end caps
for y_cap in [H1Y, H2Y]:
    _(f'<rect x="{BRANCH_END-3}" y="{y_cap-4}" width="8" height="{BPH+8}" rx="4" '
      f'fill="#1C5A1C" stroke="#0A2E0A" stroke-width="1.5"/>')

# Valve wheel on main pipe at y=196
VCX, VCY, VR = PVX + PVW//2, 196, 24
_(f'<circle cx="{VCX}" cy="{VCY}" r="{VR}" fill="none" stroke="#907820" stroke-width="7"/>')
_(f'<circle cx="{VCX}" cy="{VCY}" r="7" fill="#907820"/>')
for sp in range(0, 360, 60):
    a = math.radians(sp)
    _(f'<line x1="{VCX+7*math.cos(a):.1f}" y1="{VCY+7*math.sin(a):.1f}" '
      f'x2="{VCX+VR*math.cos(a):.1f}" y2="{VCY+VR*math.sin(a):.1f}" '
      f'stroke="#907820" stroke-width="5"/>')

# Pipe indicator lamps (3 colors)
LAMP_Y = 460
for li, (lx, lc_fill, cls) in enumerate([
    (130, "#EE2222", "lr"),
    (154, "#FFCC00", "ly"),
    (178, "#22EE22", "lg"),
]):
    _(f'<circle cx="{lx}" cy="{LAMP_Y}" r="7" fill="{lc_fill}" class="{cls}" filter="url(#glow4)"/>')
    _(f'<circle cx="{lx}" cy="{LAMP_Y}" r="9" fill="none" stroke="#444" stroke-width="2"/>')

# Pulse glow on main vertical pipe
_(f'<rect x="{PVX}" y="0" width="{PVW}" height="{H}" '
  f'fill="#44FF44" opacity="0.0" class="pp"/>')

# ═══════════════════════════════════════════════════════════════════════════════
# LAYER 5 — GAUGES × 3
# ═══════════════════════════════════════════════════════════════════════════════
# Each gauge: (cx, cy, r, label, ndl_from, ndl_to, ndl_mid, dur, accent_color)
GAUGE_DEFS = [
    (150, 238, 52, "PRESSURE", -28, 19,  9,  2.9, "#2299EE"),
    (222, 318, 44, "STEAM",    -32, 26, -8,  2.0, "#22CC44"),
    (150, 408, 48, "POWER",    -22, 20, 12,  3.5, "#EE8822"),
]
for (cx, cy, r, lbl, nf, nt, nm, dur, acc) in GAUGE_DEFS:
    _(gauge(cx, cy, r, lbl, nf, nt, nm, dur, acc))

# ═══════════════════════════════════════════════════════════════════════════════
# LAYER 6 — GEAR CLUSTER × 3
# ═══════════════════════════════════════════════════════════════════════════════
# Big gear  : cx=420, cy=362
# Medium    : cx=536, cy=286
# Top-left  : cx=346, cy=262
GCX_A, GCY_A, GN_A, GR1_A, GR2_A = 420, 362, 14, 74, 92
GCX_B, GCY_B, GN_B, GR1_B, GR2_B = 536, 286, 10, 43, 55
GCX_C, GCY_C, GN_C, GR1_C, GR2_C = 348, 260,  9, 35, 47

def draw_gear(cx, cy, n, r1, r2, grad, css_class, spoke_r=None, bolt_n=6):
    """Draw a full decorated gear with shadow, teeth, hub, spokes, bolts."""
    if spoke_r is None:
        spoke_r = r1 - 10
    # Gear group (rotated)
    _(f'<g class="{css_class}">')
    # Shadow (doesn't rotate — drawn separately below)
    # Teeth + body
    gp = gear_path(cx, cy, n, r1, r2)
    _(f'  <path d="{gp}" fill="{grad}"/>')
    _(f'  <path d="{gp}" fill="none" stroke="#3A2000" stroke-width="1.5"/>')
    # Hub ring
    _(f'  <circle cx="{cx}" cy="{cy}" r="{r1-10}" fill="{grad}" opacity="0.8"/>')
    _(f'  <circle cx="{cx}" cy="{cy}" r="{r1-10}" fill="none" stroke="#3A2000" stroke-width="1.5"/>')
    # Spokes (6)
    for si in range(6):
        sa = math.radians(si * 60)
        sx1 = cx + 14 * math.cos(sa);  sy1 = cy + 14 * math.sin(sa)
        sx2 = cx + spoke_r * math.cos(sa); sy2 = cy + spoke_r * math.sin(sa)
        _(f'  <line x1="{sx1:.1f}" y1="{sy1:.1f}" x2="{sx2:.1f}" y2="{sy2:.1f}" '
          f'stroke="#3A2000" stroke-width="6"/>')
        _(f'  <line x1="{sx1:.1f}" y1="{sy1:.1f}" x2="{sx2:.1f}" y2="{sy2:.1f}" '
          f'stroke="#FFDD80" stroke-width="2" opacity="0.45"/>')
    # Center hub
    _(f'  <circle cx="{cx}" cy="{cy}" r="14" fill="#2A1800"/>')
    _(f'  <circle cx="{cx}" cy="{cy}" r="10" fill="#8A6820"/>')
    _(f'  <circle cx="{cx}" cy="{cy}" r="6"  fill="#CCAA40"/>')
    _(f'  <circle cx="{cx}" cy="{cy}" r="3"  fill="#FFE880"/>')
    # Bolt holes on bolt circle
    bc_r = r1 - 20
    for bi in range(bolt_n):
        ba = math.radians(bi * 360 / bolt_n + 15)
        bx = cx + bc_r * math.cos(ba); by = cy + bc_r * math.sin(ba)
        _(f'  <circle cx="{bx:.1f}" cy="{by:.1f}" r="3.5" fill="#1A1000" stroke="#4A3400" stroke-width="1"/>')
    # Gear sheen
    _(f'  <path d="{gp}" fill="none" stroke="#FFE880" stroke-width="0.8" opacity="0.35"/>')
    _(f'</g>')

# Draw gear drop-shadows FIRST (static, not animated)
_(f'<circle cx="{GCX_A+5}" cy="{GCY_A+6}" r="{GR2_A+4}" fill="#00000040"/>')
_(f'<circle cx="{GCX_B+4}" cy="{GCY_B+5}" r="{GR2_B+3}" fill="#00000040"/>')
_(f'<circle cx="{GCX_C+3}" cy="{GCY_C+4}" r="{GR2_C+3}" fill="#00000040"/>')

draw_gear(GCX_A, GCY_A, GN_A, GR1_A, GR2_A, "url(#gg1)", "gA", spoke_r=GR1_A-8, bolt_n=7)
draw_gear(GCX_B, GCY_B, GN_B, GR1_B, GR2_B, "url(#gg2)", "gB", spoke_r=GR1_B-6, bolt_n=5)
draw_gear(GCX_C, GCY_C, GN_C, GR1_C, GR2_C, "url(#gg1)", "gC", spoke_r=GR1_C-6, bolt_n=5)

# ═══════════════════════════════════════════════════════════════════════════════
# LAYER 7 — FACTORY MACHINES (center-right)
# ═══════════════════════════════════════════════════════════════════════════════
# Blue machine
_(f'<rect x="476" y="256" width="62" height="82" rx="5" fill="url(#mb)" stroke="#1A2A6A" stroke-width="2"/>')
_(f'<rect x="482" y="262" width="50" height="16" rx="2" fill="#FFFFFF" opacity="0.10"/>')
_(f'<rect x="485" y="286" width="44" height="28" rx="3" fill="#001A5A" stroke="#2244CC" stroke-width="1.5"/>')
_(f'<circle cx="497" cy="313" r="6" fill="#00AAFF" class="mg" filter="url(#glow4)"/>')
_(f'<circle cx="514" cy="313" r="6" fill="#00FF88" class="b4" filter="url(#glow4)"/>')
# Blue machine vent pipe
_(f'<rect x="508" y="238" width="14" height="22" rx="2" fill="url(#pv)"/>')
_(f'<rect x="504" y="232" width="22" height="8" rx="3" fill="#1C5A1C" stroke="#0A2E0A" stroke-width="1"/>')

# Purple machine
_(f'<rect x="548" y="268" width="58" height="70" rx="5" fill="url(#mp)" stroke="#2A0A5A" stroke-width="2"/>')
_(f'<rect x="554" y="274" width="46" height="14" rx="2" fill="#FFFFFF" opacity="0.10"/>')
_(f'<rect x="556" y="294" width="40" height="24" rx="3" fill="#1A0040" stroke="#8844EE" stroke-width="1.5"/>')
_(f'<circle cx="567" cy="318" r="5" fill="#FF44FF" class="mg" filter="url(#glow4)"/>')
_(f'<circle cx="582" cy="318" r="5" fill="#FFAA22" class="b6" filter="url(#glow4)"/>')

# Green/teal machine (above)
_(f'<rect x="480" y="202" width="56" height="52" rx="5" fill="url(#mt)" stroke="#0A3A18" stroke-width="2"/>')
_(f'<rect x="486" y="208" width="44" height="12" rx="2" fill="#FFF" opacity="0.10"/>')
_(f'<rect x="488" y="226" width="38" height="18" rx="3" fill="#001A08" stroke="#22CC55" stroke-width="1.5"/>')
_(f'<circle cx="500" cy="235" r="5" fill="#44FF88" class="b2" filter="url(#glow4)"/>')

# Yellow machine (further right)
_(f'<rect x="614" y="272" width="46" height="60" rx="5" fill="url(#my)" stroke="#4A2000" stroke-width="2"/>')
_(f'<rect x="620" y="278" width="34" height="10" rx="2" fill="#FFF" opacity="0.10"/>')
_(f'<rect x="622" y="295" width="30" height="20" rx="3" fill="#2A1000" stroke="#FFAA22" stroke-width="1.5"/>')
_(f'<circle cx="633" cy="307" r="5" fill="#FFDD22" class="b7" filter="url(#glow4)"/>')

# Connecting small pipe from left branch to machines
_(f'<rect x="{BRANCH_END}" y="{H1Y}" width="235" height="{BPH}" fill="url(#ph)" rx="2"/>')
_(f'<rect x="{BRANCH_END+12}" y="{H1Y+5}" width="200" height="5" fill="#66FF66" opacity="0.15"/>')
for ax in range(BRANCH_END+20, BRANCH_END+230, 42):
    _(f'<polygon points="{ax},{H1Y+4} {ax+16},{H1Y+BPH//2} {ax},{H1Y+BPH-4}" '
      f'fill="#2EEE2E" class="ea"/>')

# ═══════════════════════════════════════════════════════════════════════════════
# LAYER 8 — RIGHT CONTROL CONSOLE
# ═══════════════════════════════════════════════════════════════════════════════
CON_X, CON_Y, CON_W, CON_H = 646, 244, 308, 290

# Console shadow
_(f'<rect x="{CON_X+6}" y="{CON_Y+7}" width="{CON_W}" height="{CON_H}" rx="6" fill="#000" opacity="0.5"/>')
# Console body
_(f'<rect x="{CON_X}" y="{CON_Y}" width="{CON_W}" height="{CON_H}" rx="6" fill="url(#cpanel)" '
  f'stroke="#383848" stroke-width="2"/>')
# Top accent strip
_(f'<rect x="{CON_X}" y="{CON_Y}" width="{CON_W}" height="10" rx="6" fill="#CCBB44" opacity="0.7"/>')
_(f'<rect x="{CON_X}" y="{CON_Y+10}" width="{CON_W}" height="4" fill="#888822" opacity="0.4"/>')
# Side rivet detail
for ry in range(CON_Y+30, CON_Y+CON_H-20, 40):
    _(f'<circle cx="{CON_X+8}" cy="{ry}" r="4" fill="#242434" stroke="#484858" stroke-width="1"/>')
    _(f'<circle cx="{CON_X+CON_W-8}" cy="{ry}" r="4" fill="#242434" stroke="#484858" stroke-width="1"/>')

# Monitor screen (above console)
MON_X, MON_Y, MON_W, MON_H = 660, 155, 222, 145
# Monitor outer casing
_(f'<rect x="{MON_X-8}" y="{MON_Y-8}" width="{MON_W+16}" height="{MON_H+16}" rx="6" fill="#1E1E2E" stroke="#383848" stroke-width="2"/>')
# Screen glass
_(f'<rect x="{MON_X}" y="{MON_Y}" width="{MON_W}" height="{MON_H}" rx="3" fill="url(#mscreen)"/>')
# Screen content (flickers)
_(f'<g class="scrf">')
_(f'  <rect x="{MON_X}" y="{MON_Y}" width="{MON_W}" height="{MON_H}" rx="3" fill="#000A04" opacity="0.4"/>')
# PLC status text
MON_TX = MON_X + 10
for row, (txt, col) in enumerate([
    ("PLC RUN ▶  ONLINE",   "#22FF88"),
    ("CPU: MITSUBISHI Q",   "#AAFFCC"),
    ("SCAN: 0.24ms  OK",    "#AAFFCC"),
    ("PROG: SIROJUL.LD",    "#44CCFF"),
    ("MOTOR:  ▮▮▮▮▮▮▮░",  "#22FF88"),
    ("PRESS:  ▮▮▮▮▮░░░",  "#FFCC22"),
]):
    ty = MON_Y + 18 + row * 20
    _(f'  <text x="{MON_TX}" y="{ty}" fill="{col}" font-size="11" font-family="monospace">{txt}</text>')
# Scanline effect (scrolling)
_(f'  <rect x="{MON_X}" y="{MON_Y}" width="{MON_W}" height="{MON_H}" rx="3" '
  f'fill="none" stroke="#000" stroke-width="0"/>')
_(f'</g>')
# Screen glare
_(f'<ellipse cx="{MON_X+MON_W*0.28:.0f}" cy="{MON_Y+MON_H*0.22:.0f}" '
  f'rx="{MON_W*0.22:.0f}" ry="{MON_H*0.15:.0f}" fill="#FFF" opacity="0.12" '
  f'transform="rotate(-18 {MON_X+MON_W//2} {MON_Y+MON_H//2})"/>')
# Monitor stand
_(f'<rect x="{MON_X+MON_W//2-18}" y="{MON_Y+MON_H+16}" width="36" height="12" rx="4" fill="#1A1A2A"/>')
_(f'<rect x="{CON_X+20}" y="{CON_Y}" width="{CON_W-40}" height="8" rx="3" fill="#252535"/>')

# Amber Warning Beacon (top right of console)
BCX, BCY = 858, 162
_(f'<circle cx="{BCX}" cy="{BCY}" r="32" class="bhal" fill="#FF9900" opacity="0"/>')
_(f'<circle cx="{BCX}" cy="{BCY}" r="18" fill="#220800"/>')
_(f'<circle cx="{BCX}" cy="{BCY}" r="14" fill="#FF9900" class="bcon" filter="url(#glow8)"/>')
_(f'<circle cx="{BCX}" cy="{BCY}" r="8"  fill="#FFEEAA" class="bcon"/>')
# Beacon casing ring
_(f'<circle cx="{BCX}" cy="{BCY}" r="20" fill="none" stroke="#6A4A00" stroke-width="4"/>')

# Button grid (3×3 layout)
BTN_COLORS = [
    "#EE2222", "#22AAEE", "#22EE44",
    "#FFCC00", "#22EE44", "#22AAEE",
    "#22AAEE", "#EE2222", "#22EE44",
]
BTN_CLASSES = ["b0","b1","b2","b3","b4","b5","b6","b7","b8"]
BTN_START_X, BTN_START_Y = CON_X + 22, CON_Y + 38
for bi, (bc, bcls) in enumerate(zip(BTN_COLORS, BTN_CLASSES)):
    col = bi % 3
    row = bi // 3
    bx = BTN_START_X + col * 50
    by = BTN_START_Y + row * 46
    # Button body
    _(f'<rect x="{bx}" y="{by}" width="38" height="30" rx="5" fill="#1A1A28" stroke="#303040" stroke-width="1.5"/>')
    # Button cap
    _(f'<rect x="{bx+4}" y="{by+4}" width="30" height="22" rx="4" fill="{bc}" class="{bcls}" filter="url(#glow4)"/>')
    # Shine
    _(f'<rect x="{bx+6}" y="{by+6}" width="12" height="6" rx="2" fill="#FFF" opacity="0.28" class="{bcls}"/>')

# Separator divider on console (vertical)
DIV_X = CON_X + 180
_(f'<line x1="{DIV_X}" y1="{CON_Y+20}" x2="{DIV_X}" y2="{CON_Y+CON_H-12}" stroke="#404050" stroke-width="2"/>')

# Slider / large lever (right side of console)
SL_X, SL_Y = CON_X + 198, CON_Y + 35
_(f'<rect x="{SL_X}" y="{SL_Y}" width="22" height="120" rx="4" fill="#181828" stroke="#303048" stroke-width="1.5"/>')
for sk in range(3):
    sly2 = SL_Y + 18 + sk * 40
    _(f'<rect x="{SL_X+3}" y="{sly2}" width="16" height="8" rx="3" fill="#4A4A6A" stroke="#606080" stroke-width="1"/>')
# Lever handle (middle)
_(f'<rect x="{SL_X-4}" y="{SL_Y+52}" width="30" height="16" rx="5" fill="#AA4422" stroke="#882200" stroke-width="1.5"/>')
_(f'<rect x="{SL_X-1}" y="{SL_Y+55}" width="24" height="10" rx="3" fill="#FF6633" opacity="0.7"/>')

# Digital readout display
DIS_X, DIS_Y = CON_X + 232, CON_Y + 35
_(f'<rect x="{DIS_X}" y="{DIS_Y}" width="110" height="50" rx="4" fill="#060C06" stroke="#224422" stroke-width="1.5"/>')
for dr, dtxt in enumerate(["082.4 kPa", "1412 RPM"]):
    _(f'<text x="{DIS_X+8}" y="{DIS_Y+18+dr*22}" fill="#00FF44" font-size="12" font-family="monospace" font-weight="bold">{dtxt}</text>')

# Bottom console labels
for li2, (lbl2, lx2) in enumerate([("CTRL-A", CON_X+39), ("CTRL-B", CON_X+89), ("CTRL-C", CON_X+139)]):
    _(f'<text x="{lx2}" y="{CON_Y+CON_H-8}" fill="#8888AA" font-size="8" font-family="monospace" text-anchor="middle">{lbl2}</text>')

# Warning sign on console
WS_X, WS_Y = CON_X + 240, CON_Y + 100
_(f'<rect x="{WS_X}" y="{WS_Y}" width="90" height="30" rx="4" fill="#1A0A00" stroke="#AA6600" stroke-width="1.5"/>')
_(f'<text x="{WS_X+45}" y="{WS_Y+12}" fill="#FFAA00" font-size="10" font-family="monospace" font-weight="bold" '
  f'text-anchor="middle" class="ws">⚠ WARNING</text>')
_(f'<text x="{WS_X+45}" y="{WS_Y+24}" fill="#FF6600" font-size="8" font-family="monospace" '
  f'text-anchor="middle" class="ws">PRESSURE HIGH</text>')

# Right wall pipe (vertical, far right)
_(f'<rect x="{W-38}" y="0" width="24" height="{H}" fill="url(#pvr)" rx="3"/>')
_(f'<rect x="{W-32}" y="0" width="8" height="{H}" fill="#66FF66" opacity="0.12"/>')
for jy2 in [80, 180, 280, 380, 480]:
    _(f'<rect x="{W-43}" y="{jy2-5}" width="34" height="10" rx="4" '
      f'fill="#1C5A1C" stroke="#0A2E0A" stroke-width="1.5"/>')

# Warning signs on walls (top area)
for wsx, wst in [(75, "工場稼働中"), (255, "安全第一"), (400, "第4区域")]:
    _(f'<rect x="{wsx}" y="94" width="92" height="26" rx="3" fill="#FFEE44" stroke="#AA8800" stroke-width="1.5"/>')
    _(f'<text x="{wsx+46}" y="{94+18}" fill="#222200" font-size="12" font-family="serif" '
      f'font-weight="bold" text-anchor="middle">{wst}</text>')

# ═══════════════════════════════════════════════════════════════════════════════
# LAYER 9 — CONVEYOR BELT
# ═══════════════════════════════════════════════════════════════════════════════
CB_X, CB_Y, CB_W, CB_H = 190, 452, 428, 36

# Belt rollers (end drums)
for rx_c in [CB_X + 4, CB_X + CB_W - 4]:
    _(f'<ellipse cx="{rx_c}" cy="{CB_Y + CB_H//2}" rx="10" ry="{CB_H//2-2}" fill="#3A3A3A" stroke="#555" stroke-width="2"/>')
# Belt surface
_(f'<rect x="{CB_X}" y="{CB_Y}" width="{CB_W}" height="{CB_H}" rx="4" fill="url(#conv)"/>')
# Belt edge highlights
_(f'<rect x="{CB_X}" y="{CB_Y}" width="{CB_W}" height="4" rx="2" fill="#444" opacity="0.8"/>')
_(f'<rect x="{CB_X}" y="{CB_Y+CB_H-4}" width="{CB_W}" height="4" rx="2" fill="#444" opacity="0.8"/>')
# Items on belt (3 crates, different positions)
for crate_x, crate_cls, crate_col in [
    (230, "ca", "#CC4400"),
    (350, "cb", "#2244CC"),
    (490, "cc", "#228822"),
]:
    _(f'<g class="{crate_cls}">')
    _(f'  <rect x="{crate_x-12}" y="{CB_Y-18}" width="24" height="20" rx="2" fill="{crate_col}" stroke="#1A1A1A" stroke-width="1.5"/>')
    _(f'  <line x1="{crate_x-12}" y1="{CB_Y-8}" x2="{crate_x+12}" y2="{CB_Y-8}" stroke="#1A1A1A" stroke-width="1"/>')
    _(f'  <line x1="{crate_x}" y1="{CB_Y-18}" x2="{crate_x}" y2="{CB_Y+2}" stroke="#1A1A1A" stroke-width="1"/>')
    _(f'</g>')

# ═══════════════════════════════════════════════════════════════════════════════
# LAYER 10 — FLOOR + CATWALK
# ═══════════════════════════════════════════════════════════════════════════════
# Main floor
_(f'<rect x="0" y="492" width="{W}" height="{H-492}" fill="url(#floor)"/>')
_(f'<rect x="0" y="492" width="{W}" height="{H-492}" fill="url(#grat)" opacity="0.6"/>')
_(f'<rect x="0" y="492" width="{W}" height="4" fill="#555"/>')

# Catwalk / platform (center platform area, y=490)
CATW_Y = 488
_(f'<rect x="0" y="{CATW_Y}" width="{W}" height="8" rx="0" fill="url(#catw)"/>')
# Platform grating
_(f'<rect x="0" y="{CATW_Y}" width="{W}" height="8" fill="url(#grat)" opacity="0.5"/>')
# Railing posts
for px_r in range(40, W-20, 55):
    _(f'<line x1="{px_r}" y1="{CATW_Y-38}" x2="{px_r}" y2="{CATW_Y}" stroke="#C8A830" stroke-width="4"/>')
# Top rail
_(f'<line x1="0" y1="{CATW_Y-38}" x2="{W}" y2="{CATW_Y-38}" stroke="#D4B838" stroke-width="5"/>')
# Bottom rail (mid-height)
_(f'<line x1="0" y1="{CATW_Y-18}" x2="{W}" y2="{CATW_Y-18}" stroke="#C4A828" stroke-width="3"/>')

# Lower platform / catwalk (lower)
LCP_Y = 540
_(f'<rect x="0" y="530" width="{W}" height="10" fill="#3A3020" opacity="0.8"/>')

# ═══════════════════════════════════════════════════════════════════════════════
# LAYER 11 — WORKERS
# ═══════════════════════════════════════════════════════════════════════════════
_(worker(308, CATW_Y,  color="#3366CC", hat="#FFCC00"))
_(worker(622, CATW_Y,  color="#CC3322", hat="#22AA22"))
_(worker(760, CATW_Y,  color="#2288CC", hat="#FF4422"))

# ═══════════════════════════════════════════════════════════════════════════════
# LAYER 12 — STEAM CLOUDS (10 sources, staggered offsets)
# ═══════════════════════════════════════════════════════════════════════════════
# (x, y, rx, ry, css_class)
STEAM_SRCS = [
    # Chimney left
    (291, 62, 18, 20, "sa"), (295, 70, 14, 17, "sb"), (298, 58, 20, 22, "sc"),
    # Chimney right
    (563, 50, 15, 18, "sd"), (567, 58, 12, 15, "se"), (560, 44, 18, 20, "sf"),
    # Secondary vents / machines
    (514, 224, 12, 14, "sg"), (518, 230, 10, 12, "sh"),
    # Pipe vent left side
    ( 32, 76, 11, 12, "si"), ( 38, 82, 9, 11, "sj"),
]
for sx, sy, srx, sry, scls in STEAM_SRCS:
    _(f'<ellipse cx="{sx}" cy="{sy}" rx="{srx}" ry="{sry}" '
      f'fill="#DDDDDD" opacity="0.85" class="{scls}" filter="url(#fsteam)"/>')

# ═══════════════════════════════════════════════════════════════════════════════
# LAYER 13 — COINS (bouncing, above belt)
# ═══════════════════════════════════════════════════════════════════════════════
for coin_x, coin_cls in [(270, "ca"), (390, "cb"), (520, "cc")]:
    _(f'<g class="{coin_cls}">')
    _(f'  <circle cx="{coin_x}" cy="{CB_Y-32}" r="12" fill="#FFCC00" stroke="#AA8800" stroke-width="2"/>')
    _(f'  <circle cx="{coin_x}" cy="{CB_Y-32}" r="8" fill="none" stroke="#FFE880" stroke-width="2"/>')
    _(f'  <text x="{coin_x}" y="{CB_Y-28}" fill="#AA6600" font-size="10" font-weight="bold" '
      f'text-anchor="middle" font-family="serif">$</text>')
    _(f'</g>')

# ═══════════════════════════════════════════════════════════════════════════════
# LAYER 14 — ADDITIONAL PIPE / STRUCTURE DETAILS
# ═══════════════════════════════════════════════════════════════════════════════

# Cross-beam structural supports (dark metal)
for bx_str, bw_str in [(0, 8), (W-8, 8)]:
    _(f'<rect x="{bx_str}" y="0" width="{bw_str}" height="{H}" fill="#1A1000" opacity="0.5"/>')

# Top pipe run (horizontal, near ceiling)
_(f'<rect x="{PVX+PVW}" y="48" width="{W-PVX-PVW-10}" height="18" fill="url(#ph)" rx="2" opacity="0.85"/>')
for jt in range(100, W-30, 90):
    _(f'<rect x="{jt-4}" y="44" width="8" height="26" rx="3" fill="#1C5A1C" stroke="#0A2E0A" stroke-width="1"/>')
for axt in range(PVX+PVW+18, W-30, 40):
    _(f'<polygon points="{axt},{52} {axt+14},{57} {axt},{62}" fill="#2EEE2E" class="ea"/>')

# ═══════════════════════════════════════════════════════════════════════════════
# LAYER 15 — VIGNETTE + BORDER FRAME
# ═══════════════════════════════════════════════════════════════════════════════
_(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')

# Decorative border
_(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="4" fill="none" '
  f'stroke="url(#sborder)" stroke-width="3" opacity="0.55"/>')
_(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="3" fill="none" '
  f'stroke="#AACC22" stroke-width="1" opacity="0.25"/>')

# Corner ornaments
for fx, fy, rot in [(20,20,0),(W-20,20,90),(W-20,H-20,180),(20,H-20,270)]:
    _(f'<g transform="rotate({rot} {fx} {fy})">'
      f'<line x1="{fx}" y1="{fy}" x2="{fx+22}" y2="{fy}" stroke="#AACC22" stroke-width="2" opacity="0.5"/>'
      f'<line x1="{fx}" y1="{fy}" x2="{fx}" y2="{fy+22}" stroke="#AACC22" stroke-width="2" opacity="0.5"/>'
      f'</g>')

_('</svg>')

# ─────────────────────────────────────────────────────────────────────────────
# WRITE FILE
# ─────────────────────────────────────────────────────────────────────────────
os.makedirs("assets", exist_ok=True)
out_path = "assets/industrial_mario_bros_scene.svg"
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

size_kb = os.path.getsize(out_path) / 1024
print()
print("=" * 60)
print("  [OK] industrial_mario_bros_scene.svg - DONE!")
print(f"  Path : {out_path}")
print(f"  Size : {size_kb:.1f} KB")
print(f"  Lines: {len(lines)}")
print("=" * 60)
