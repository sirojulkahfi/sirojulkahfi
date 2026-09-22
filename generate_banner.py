# Mario Bros Anime Industrial Factory Banner Generator v5.0
# PROFESSIONAL OVERHAUL - Maximum quality cinematic animation
# Steps:
#   A. Rotating Gears (ultra-smooth, 48 frames)
#   B. Gauge Needles (physics-based oscillation + micro-tremor)
#   C. Steam Clouds (3-layer organic puffs, 4 sources)
#   D. Monitor Screen Glow + Scanlines
#   E. Arcade Buttons (staggered 7-step sequencer)
#   F. Amber Warning Strobe
#   G. Pipe Indicator Lamps
#   H. Energy Pulse (directional sweep on green pipe)
#   I. Electric Sparks near gears
#   J. Cinematic Vignette

import os
import math
import random
import cv2
import numpy as np
from PIL import Image, ImageEnhance

NUM_FRAMES  = 48
DURATION_MS = 65
TARGET_W    = 860
SEED        = 1985


def generate_mario_industrial_banner(
    base_image_path="assets/banner_base.jpg",
    output_gif_path="assets/banner.gif",
    output_png_path="assets/banner.png",
    num_frames=NUM_FRAMES,
    duration=DURATION_MS,
    target_width=TARGET_W,
):
    if not os.path.exists(base_image_path):
        raise FileNotFoundError(f"Base image not found: {base_image_path}")

    print(f"[1/7] Loading base image: {base_image_path}")
    base_bgr = cv2.imread(base_image_path)
    h_orig, w_orig = base_bgr.shape[:2]
    print(f"      Source: {w_orig}x{h_orig}")

    # Color grading - warm vibrant Mario aesthetic
    base_pil = Image.fromarray(cv2.cvtColor(base_bgr, cv2.COLOR_BGR2RGB))
    base_pil = ImageEnhance.Color(base_pil).enhance(1.18)
    base_pil = ImageEnhance.Contrast(base_pil).enhance(1.07)
    base_pil = ImageEnhance.Brightness(base_pil).enhance(1.03)

    # Save pristine PNG
    aspect = h_orig / w_orig
    target_height = int(target_width * aspect)
    clean = base_pil.resize((target_width, target_height), Image.Resampling.LANCZOS)
    clean.save(output_png_path, format="PNG", optimize=True)
    print(f"      PNG saved: {output_png_path} ({target_width}x{target_height})")

    base_vib = cv2.cvtColor(np.array(base_pil), cv2.COLOR_RGB2BGR)

    # -----------------------------------------------------------------
    # [2/7] GEAR TRAIN
    # -----------------------------------------------------------------
    print("[2/7] Configuring gear train...")
    GEARS = [
        {"cx": 495, "cy": 550, "r": 112, "pitch": 18.0, "dir":  1},
        {"cx": 543, "cy": 400, "r":  52, "pitch": 24.0, "dir": -1},
        {"cx": 455, "cy": 315, "r":  72, "pitch": 21.0, "dir":  1},
    ]

    fg_mask = np.zeros((h_orig, w_orig), dtype=np.uint8)
    fg_mask[:, :430] = 255
    fg_mask[590:650, 420:560] = 255
    cv2.fillPoly(fg_mask, [np.array([[474,498],[540,498],[552,540],[552,660],[462,660],[462,545]], np.int32)], 255)
    cv2.fillPoly(fg_mask, [np.array([[420,615],[600,615],[600,768],[420,768]], np.int32)], 255)
    fg_mask[:, 560:] = 255

    gear_alphas = []
    for g in GEARS:
        raw = np.zeros((h_orig, w_orig), dtype=np.uint8)
        cv2.circle(raw, (g["cx"], g["cy"]), g["r"], 255, -1)
        raw[fg_mask > 0] = 0
        blurred = cv2.GaussianBlur(raw.astype(np.float32), (7, 7), 0) / 255.0
        gear_alphas.append(blurred[:, :, np.newaxis])

    # -----------------------------------------------------------------
    # [3/7] GAUGE NEEDLES
    # -----------------------------------------------------------------
    print("[3/7] Configuring gauge needles...")
    GAUGES = [
        {"cx": 128, "cy": 468, "nl": 36, "base": -80, "swing": 22, "spd": 0.75,
         "col": (0,0,150), "tip": (30,30,255), "lo": -130, "hi": -50},
        {"cx": 215, "cy": 497, "nl": 26, "base": -90, "swing": 28, "spd": 1.15,
         "col": (0,70,0), "tip": (0,190,70), "lo": -130, "hi": -50},
        {"cx": 138, "cy": 575, "nl": 28, "base": -72, "swing": 30, "spd": 0.60,
         "col": (0,0,130), "tip": (0,20,245), "lo": -130, "hi": -50},
    ]

    # -----------------------------------------------------------------
    # [4/7] STEAM CLOUD SEEDS
    # -----------------------------------------------------------------
    print("[4/7] Seeding steam system...")
    rng = random.Random(SEED)

    def seeds(n, oxlo, oxhi, oylo, oyhi, rlo, rhi, slo, shi, dlo, dhi, alo, ahi):
        return [{"ox": rng.uniform(oxlo, oxhi), "oy": rng.uniform(oylo, oyhi),
                 "r": rng.uniform(rlo, rhi), "spd": rng.uniform(slo, shi),
                 "drift": rng.uniform(dlo, dhi), "alpha": rng.uniform(alo, ahi),
                 "phase": rng.uniform(0, 2*math.pi),
                 "off_r": rng.uniform(0.30, 0.55), "off_a": rng.uniform(0.50, 0.75)}
                for _ in range(n)]

    steam_seeds = (
        seeds(32, 515, 565,  70, 210, 13, 30, 1.4, 2.8, -2.5, 2.5, 0.16, 0.36) +
        seeds(26, 598, 660,   5, 135, 11, 26, 1.7, 3.3, -3.0, 3.0, 0.12, 0.28) +
        seeds(22, 694, 746, 615, 695,  8, 18, 0.9, 2.1, -2.0, 2.0, 0.13, 0.33) +
        seeds(16,  52, 112,  40, 205,  9, 20, 1.1, 2.4, -1.5, 1.5, 0.10, 0.26)
    )

    # -----------------------------------------------------------------
    # [5/7] CONSOLE SIGNALS
    # -----------------------------------------------------------------
    print("[5/7] Configuring console signals...")
    BUTTONS = [
        (980,420,11,(0,0,235)), (1030,420,11,(0,215,250)), (1085,420,11,(45,255,45)),
        (1090,450,11,(255,175,0)), (980,480,11,(45,255,45)),
        (1030,480,11,(0,215,250)), (1085,480,11,(0,0,235)),
    ]
    BEACON = (1048, 345)
    LAMPS  = [(130,715,(0,0,240)), (152,712,(0,215,250)), (175,710,(45,255,75))]
    SCREEN = (565, 330, 755, 475)

    # Precompute vignette (slow pure-python, done once)
    print("      Building vignette kernel...")
    vig = np.zeros((h_orig, w_orig), dtype=np.float32)
    cx_v, cy_v = w_orig / 2.0, h_orig / 2.0
    yy, xx = np.mgrid[0:h_orig, 0:w_orig]
    dx = (xx - cx_v) / cx_v
    dy = (yy - cy_v) / cy_v
    vig = np.clip(1.0 - 0.40 * (dx*dx + dy*dy), 0.52, 1.0).astype(np.float32)
    vig = vig[:, :, np.newaxis]   # (H, W, 1)

    # -----------------------------------------------------------------
    # [6/7] FRAME SYNTHESIS
    # -----------------------------------------------------------------
    print(f"[6/7] Synthesizing {num_frames} frames...")
    frames_rgb = []
    rng2 = random.Random(SEED + 1)

    for f_idx in range(num_frames):
        t   = f_idx / num_frames
        ang = t * 2 * math.pi
        frame = base_vib.copy().astype(np.float32)

        # A. Gears
        for gear, alpha in zip(GEARS, gear_alphas):
            rot_deg = t * gear["pitch"] * gear["dir"]
            M = cv2.getRotationMatrix2D((gear["cx"], gear["cy"]), rot_deg, 1.0)
            rot = cv2.warpAffine(base_vib, M, (w_orig, h_orig),
                                 flags=cv2.INTER_CUBIC,
                                 borderMode=cv2.BORDER_REFLECT101).astype(np.float32)
            frame = (1.0 - alpha) * frame + alpha * rot

        frame = np.clip(frame, 0, 255).astype(np.uint8)

        # B. Gauge needles
        for gi, g in enumerate(GAUGES):
            ph = gi * 1.37
            osc = math.sin(ang * g["spd"] + ph)
            jit = 0.10 * math.sin(ang * g["spd"] * 3.7 + ph + 1.2)
            deg = g["base"] + osc * g["swing"] + jit * g["swing"] * 0.25
            deg = max(g["lo"], min(g["hi"], deg))
            rad = math.radians(deg)
            cx, cy, nl = g["cx"], g["cy"], g["nl"]
            tx = int(cx + nl * math.cos(rad))
            ty = int(cy + nl * math.sin(rad))
            hx = int(cx - 6 * math.cos(rad))
            hy = int(cy - 6 * math.sin(rad))
            cv2.line(frame, (hx, hy), (tx, ty), g["col"], 3, cv2.LINE_AA)
            cv2.line(frame, (hx, hy), (tx, ty), g["tip"], 1, cv2.LINE_AA)
            cv2.circle(frame, (cx, cy), 5, (45,45,45), -1)
            cv2.circle(frame, (cx, cy), 3, (215,215,215), -1)

        # C. Steam clouds (3-layer)
        slayer = np.zeros((h_orig, w_orig), dtype=np.float32)
        for s in steam_seeds:
            rise   = (f_idx * s["spd"]) % 130
            cx_s   = s["ox"] + s["drift"] * math.sin(ang + s["phase"])
            cy_s   = s["oy"] - rise
            pr     = int(s["r"] + rise * 0.22)
            fade   = s["alpha"] * max(0.0, 1.0 - rise / 120.0)
            ix, iy = int(cx_s), int(cy_s)
            if 0 < ix < w_orig and 0 < iy < h_orig and pr > 0:
                cv2.circle(slayer, (ix, iy), pr, fade, -1)
                off = int(pr * s["off_r"])
                ox2, oy2 = ix + off, iy - off // 2
                if 0 < ox2 < w_orig and 0 < oy2 < h_orig:
                    cv2.circle(slayer, (ox2, oy2), int(pr * s["off_a"]), fade*0.55, -1)
                oy3 = iy - int(pr * 0.70)
                if 0 < ix < w_orig and 0 < oy3 < h_orig:
                    cv2.circle(slayer, (ix, oy3), int(pr * 0.40), fade*0.35, -1)

        sblur = cv2.GaussianBlur(slayer, (35, 35), 0)
        ff = frame.astype(np.float32)
        for c in range(3):
            ff[:, :, c] = np.clip(ff[:, :, c] + sblur * 215.0, 0, 255)
        frame = ff.astype(np.uint8)

        # D. Monitor screen glow + scanlines
        x1s, y1s, x2s, y2s = SCREEN
        sp = 0.60 + 0.40 * math.sin(ang * 1.7 + 0.5)
        sg = np.zeros_like(frame, dtype=np.uint8)
        cv2.rectangle(sg, (x1s, y1s), (x2s, y2s), (30, 220, 100), -1)
        sg = cv2.GaussianBlur(sg, (25, 25), 0)
        frame = cv2.addWeighted(frame, 1.0, sg, 0.22 * sp, 0)
        for sy in range(y1s, y2s, 4):
            if sy < h_orig:
                frame[sy, x1s:x2s] = (frame[sy, x1s:x2s].astype(np.float32) * 0.72).astype(np.uint8)

        # E. Arcade buttons (7-step sequencer)
        for bi, (bx, by, br, bcol) in enumerate(BUTTONS):
            if ((f_idx + bi * 4) % 7) < 3:
                bg = np.zeros_like(frame, dtype=np.uint8)
                cv2.circle(bg, (bx, by), br+5, bcol, -1)
                cv2.circle(bg, (bx, by), br-2, (255,255,255), -1)
                bg = cv2.GaussianBlur(bg, (11, 11), 0)
                frame = cv2.addWeighted(frame, 1.0, bg, 0.60, 0)

        # F. Amber strobe beacon
        bf = (math.sin(ang * 3.2) * 0.5 + 0.5) ** 3
        if bf > 0.12:
            bx, by = BEACON
            brad = int(11 + 20 * bf)
            bg2 = np.zeros_like(frame, dtype=np.uint8)
            cv2.circle(bg2, (bx, by), brad, (0,195,255), -1)
            cv2.circle(bg2, (bx, by), int(brad*0.38), (170,245,255), -1)
            bg2 = cv2.GaussianBlur(bg2, (23, 23), 0)
            frame = cv2.addWeighted(frame, 1.0, bg2, 0.82 * bf, 0)

        # G. Pipe indicator lamps
        for li, (lx, ly, lc) in enumerate(LAMPS):
            if ((f_idx + li * 3) % 5) < 2:
                lg = np.zeros_like(frame, dtype=np.uint8)
                cv2.circle(lg, (lx, ly), 9, lc, -1)
                lg = cv2.GaussianBlur(lg, (13, 13), 0)
                frame = cv2.addWeighted(frame, 1.0, lg, 0.52, 0)

        # H. Energy pulse sweep on green pipe (left->right)
        ap = 0.45 + 0.55 * math.sin(ang * 2.3)
        sweep_x = int(160 + 90 * ((t * 2) % 1.0))
        al = np.zeros_like(frame, dtype=np.uint8)
        cv2.ellipse(al, (sweep_x, 715), (45, 18), 0, 0, 360, (80, 255, 110), -1)
        al = cv2.GaussianBlur(al, (17, 17), 0)
        frame = cv2.addWeighted(frame, 1.0, al, 0.38 * ap, 0)

        # I. Random electric sparks near gear edges
        if (f_idx % 7 == 0) and rng2.random() < 0.55:
            gidx = rng2.randint(0, len(GEARS)-1)
            g = GEARS[gidx]
            sa = rng2.uniform(0, 2*math.pi)
            sr = g["r"] * rng2.uniform(0.85, 1.05)
            sx = int(g["cx"] + sr * math.cos(sa))
            sy = int(g["cy"] + sr * math.sin(sa))
            if 0 < sx < w_orig and 0 < sy < h_orig:
                spk = np.zeros_like(frame, dtype=np.uint8)
                cv2.circle(spk, (sx, sy), 6, (150, 255, 255), -1)
                spk = cv2.GaussianBlur(spk, (9, 9), 0)
                frame = cv2.addWeighted(frame, 1.0, spk, 0.75, 0)

        # J. Cinematic vignette
        frame = np.clip(frame.astype(np.float32) * vig, 0, 255).astype(np.uint8)

        frames_rgb.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if (f_idx + 1) % 12 == 0:
            print(f"      Frame {f_idx+1}/{num_frames} done")

    # -----------------------------------------------------------------
    # [7/7] EXPORT GIF
    # -----------------------------------------------------------------
    print(f"[7/7] Resizing {len(frames_rgb)} frames to {target_width}px...")
    pil_frames = [
        Image.fromarray(f).resize((target_width, target_height), Image.Resampling.LANCZOS)
        for f in frames_rgb
    ]

    print("      Per-frame adaptive 256-color quantization...")
    pil_p = [
        frm.quantize(colors=256, method=Image.Quantize.MEDIANCUT,
                     dither=Image.Dither.FLOYDSTEINBERG)
        for frm in pil_frames
    ]

    print(f"      Writing: {output_gif_path}")
    pil_p[0].save(
        output_gif_path,
        save_all=True,
        append_images=pil_p[1:],
        duration=duration,
        loop=0,
        optimize=True,
    )

    gif_mb = os.path.getsize(output_gif_path) / (1024*1024)
    png_mb = os.path.getsize(output_png_path) / (1024*1024)

    print()
    print("=" * 60)
    print("  SUCCESS - Banner v5.0 Generated!")
    print(f"  PNG : {output_png_path} ({png_mb:.2f} MB)")
    print(f"  GIF : {output_gif_path} ({gif_mb:.2f} MB)")
    print(f"  Size: {target_width}x{target_height}  |  {num_frames} frames  |  {duration}ms/frame")
    print("=" * 60)


if __name__ == "__main__":
    generate_mario_industrial_banner()
