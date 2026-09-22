"""
Mario Bros Anime Industrial Factory Banner Generator (GIF & PNG) v3.0
======================================================================
Fixes & Improvements:
  ✅ GEARS: All 3 gears rotate with CORRECT calibrated coordinates:
     - Big Lower Gear: center (495, 550), r=112, 18 teeth, clockwise
     - Medium Gear: center (543, 400), r=52, 14 teeth, counter-clockwise
     - Top Gear: center (455, 315), r=72, 16 teeth, clockwise
  ✅ STEAM/ASAP: 4-source animated rising steam clouds (puff, grow, fade)
  ✅ GAUGE NEEDLES: PRESSURE, STEAM, POWER oscillate naturally with jitter
  ✅ BUTTONS & BEACON: Arcade panel flashing, amber strobe
  ✅ ENERGY PULSE: Green pipe glow flow
  ✅ Color: Vibrant Mario palette maintained (NO cold blue grading)
"""

import os
import math
import random
import cv2
import numpy as np
from PIL import Image, ImageEnhance

def generate_mario_industrial_banner(
    base_image_path="assets/banner_base.jpg",
    output_gif_path="assets/banner.gif",
    output_png_path="assets/banner.png",
    num_frames=30,
    duration=80,
    target_width=850
):
    if not os.path.exists(base_image_path):
        raise FileNotFoundError(f"Base image not found at {base_image_path}")

    print(f"Loading Mario anime industrial base image: {base_image_path}...")
    base_bgr = cv2.imread(base_image_path)
    h_orig, w_orig, _ = base_bgr.shape
    print(f"  Image size: {w_orig}x{h_orig}")

    # Enhance color vibrancy slightly for rich Mario anime aesthetic
    base_pil = Image.fromarray(cv2.cvtColor(base_bgr, cv2.COLOR_BGR2RGB))
    base_pil_vibrant = ImageEnhance.Color(base_pil).enhance(1.15)
    base_pil_vibrant = ImageEnhance.Contrast(base_pil_vibrant).enhance(1.06)

    # Save clean pristine PNG banner at target width
    aspect = h_orig / w_orig
    target_height = int(target_width * aspect)
    clean_png = base_pil_vibrant.resize((target_width, target_height), Image.Resampling.LANCZOS)
    clean_png.save(output_png_path, format="PNG", optimize=True)
    print(f"PNG saved: {output_png_path} ({target_width}x{target_height})")

    base_vibrant_bgr = cv2.cvtColor(np.array(base_pil_vibrant), cv2.COLOR_RGB2BGR)

    # -----------------------------------------------------------------
    # GEAR TRAIN (calibrated from debug grid analysis)
    # -----------------------------------------------------------------
    GEARS = [
        {"cx": 495, "cy": 550, "r": 112, "pitch_deg": 20.0,  "dir": 1,  "name": "big_lower"},
        {"cx": 543, "cy": 400, "r": 52,  "pitch_deg": 25.7,  "dir": -1, "name": "medium"},
        {"cx": 455, "cy": 315, "r": 72,  "pitch_deg": 22.5,  "dir": 1,  "name": "top"},
    ]

    # -----------------------------------------------------------------
    # Foreground mask (elements that stay IN FRONT of gears)
    # -----------------------------------------------------------------
    fg_mask = np.zeros((h_orig, w_orig), dtype=np.uint8)
    fg_mask[:, :430] = 255                          # Left pipe & gauges
    fg_mask[590:650, 420:560] = 255                 # Horizontal green pipe

    pts_worker = np.array([
        [474, 498], [540, 498], [552, 540],
        [552, 660], [462, 660], [462, 545]
    ], np.int32)
    cv2.fillPoly(fg_mask, [pts_worker], 255)

    pts_catwalk = np.array([
        [420, 615], [600, 615], [600, 768], [420, 768]
    ], np.int32)
    cv2.fillPoly(fg_mask, [pts_catwalk], 255)
    fg_mask[:, 560:] = 255                          # Right console

    # Build soft-edged blend masks for each gear
    gear_masks = []
    for g in GEARS:
        raw = np.zeros((h_orig, w_orig), dtype=np.uint8)
        cv2.circle(raw, (g["cx"], g["cy"]), g["r"], 255, -1)
        raw[fg_mask > 0] = 0
        blur = cv2.GaussianBlur(raw, (5, 5), 0)[:, :, None] / 255.0
        gear_masks.append(blur)

    # -----------------------------------------------------------------
    # GAUGE NEEDLE CONFIGURATION (calibrated positions)
    # -----------------------------------------------------------------
    GAUGES = [
        {
            "name": "PRESSURE",
            "cx": 128, "cy": 468,
            "needle_len": 36,
            "base_deg": -80, "swing": 20, "speed": 0.8,
            "color": (0, 0, 160), "tip_color": (40, 40, 255),
            "min_deg": -130, "max_deg": -50,
        },
        {
            "name": "STEAM",
            "cx": 215, "cy": 497,
            "needle_len": 26,
            "base_deg": -95, "swing": 25, "speed": 1.2,
            "color": (0, 80, 0), "tip_color": (0, 200, 80),
            "min_deg": -130, "max_deg": -50,
        },
        {
            "name": "POWER",
            "cx": 138, "cy": 575,
            "needle_len": 28,
            "base_deg": -75, "swing": 28, "speed": 0.65,
            "color": (0, 0, 140), "tip_color": (0, 30, 255),
            "min_deg": -130, "max_deg": -50,
        },
    ]

    # -----------------------------------------------------------------
    # STEAM Cloud Seeds (4 sources throughout the scene)
    # -----------------------------------------------------------------
    random.seed(1985)
    steam_seeds = []

    # Source 1: Top center chimney area (~530, 160)
    for _ in range(30):
        steam_seeds.append({
            'ox': random.uniform(515, 565),
            'oy': random.uniform(80, 200),
            'r': random.uniform(14, 32),
            'spd': random.uniform(1.5, 3.0),
            'drift': random.uniform(-2.5, 2.5),
            'alpha': random.uniform(0.18, 0.38),
            'phase': random.uniform(0, 2 * math.pi),
        })

    # Source 2: Red brick chimney (top right, ~620, 120)
    for _ in range(25):
        steam_seeds.append({
            'ox': random.uniform(600, 660),
            'oy': random.uniform(10, 130),
            'r': random.uniform(12, 28),
            'spd': random.uniform(1.8, 3.5),
            'drift': random.uniform(-3.0, 3.0),
            'alpha': random.uniform(0.14, 0.30),
            'phase': random.uniform(0, 2 * math.pi),
        })

    # Source 3: Lower catwalk pipe vent (~710, 680)
    for _ in range(20):
        steam_seeds.append({
            'ox': random.uniform(695, 745),
            'oy': random.uniform(620, 690),
            'r': random.uniform(8, 18),
            'spd': random.uniform(1.0, 2.2),
            'drift': random.uniform(-2.0, 2.0),
            'alpha': random.uniform(0.15, 0.35),
            'phase': random.uniform(0, 2 * math.pi),
        })

    # Source 4: Top-left pipe vent (~80, 150)
    for _ in range(15):
        steam_seeds.append({
            'ox': random.uniform(55, 110),
            'oy': random.uniform(50, 200),
            'r': random.uniform(10, 22),
            'spd': random.uniform(1.2, 2.5),
            'drift': random.uniform(-1.5, 1.5),
            'alpha': random.uniform(0.12, 0.28),
            'phase': random.uniform(0, 2 * math.pi),
        })

    # -----------------------------------------------------------------
    # Arcade Console Buttons & Flashing Signals Setup
    # -----------------------------------------------------------------
    buttons = [
        (980, 420, 11, (0, 0, 255)),
        (1030, 420, 11, (0, 220, 255)),
        (1085, 420, 11, (50, 255, 50)),
        (1090, 450, 11, (255, 180, 0)),
        (980, 480, 11, (50, 255, 50)),
        (1030, 480, 11, (0, 220, 255)),
        (1085, 480, 11, (0, 0, 255)),
    ]
    beacon_pos = (1048, 345)

    pipe_indicators = [
        (130, 715, (0, 0, 255)),
        (152, 712, (0, 220, 255)),
        (175, 710, (50, 255, 80)),
    ]

    frames_bgr = []
    print(f"Synthesizing {num_frames} frames: gears + needles + steam + lights...")

    for f_idx in range(num_frames):
        t = f_idx / num_frames
        ang = t * 2 * math.pi
        frame = base_vibrant_bgr.copy().astype(np.float32)

        # -------------------------------------------------------------
        # 1. ROTATING MECHANICAL GEARS (all 3 gears)
        # -------------------------------------------------------------
        for gear, g_mask in zip(GEARS, gear_masks):
            rot_deg = t * gear["pitch_deg"] * gear["dir"]
            M = cv2.getRotationMatrix2D((gear["cx"], gear["cy"]), rot_deg, 1.0)
            rot_img = cv2.warpAffine(
                base_vibrant_bgr, M, (w_orig, h_orig),
                flags=cv2.INTER_CUBIC
            ).astype(np.float32)
            frame = (1.0 - g_mask) * frame + g_mask * rot_img

        frame = np.clip(frame, 0, 255).astype(np.uint8)

        # -------------------------------------------------------------
        # 2. ANIMATED GAUGE NEEDLES (PRESSURE, STEAM, POWER)
        # -------------------------------------------------------------
        for g_idx, gauge in enumerate(GAUGES):
            osc = math.sin(ang * gauge["speed"] + g_idx * 1.2)
            jitter = 0.12 * math.sin(ang * gauge["speed"] * 3.3 + g_idx + 1.1)
            needle_deg = gauge["base_deg"] + osc * gauge["swing"] + jitter * gauge["swing"] * 0.3
            needle_deg = max(gauge["min_deg"], min(gauge["max_deg"], needle_deg))

            rad = math.radians(needle_deg)
            cx, cy = gauge["cx"], gauge["cy"]
            nl = gauge["needle_len"]
            tip_x = int(cx + nl * math.cos(rad))
            tip_y = int(cy + nl * math.sin(rad))
            hub_x = int(cx - 5 * math.cos(rad))
            hub_y = int(cy - 5 * math.sin(rad))

            cv2.line(frame, (hub_x, hub_y), (tip_x, tip_y), gauge["color"], 3, cv2.LINE_AA)
            cv2.line(frame, (hub_x, hub_y), (tip_x, tip_y), gauge["tip_color"], 1, cv2.LINE_AA)
            cv2.circle(frame, (cx, cy), 4, (50, 50, 50), -1)
            cv2.circle(frame, (cx, cy), 2, (220, 220, 220), -1)

        # -------------------------------------------------------------
        # 3. RISING ANIME STEAM / ASAP CLOUDS (4 sources, animated)
        # -------------------------------------------------------------
        steam_layer = np.zeros((h_orig, w_orig), dtype=np.float32)

        for s in steam_seeds:
            rise = (f_idx * s['spd']) % 120
            cur_y = s['oy'] - rise
            cur_x = s['ox'] + s['drift'] * math.sin(ang + s['phase'])
            puff_r = int(s['r'] + rise * 0.25)
            alpha_fade = s['alpha'] * max(0.0, 1.0 - rise / 110.0)

            ix, iy = int(cur_x), int(cur_y)
            if 0 < ix < w_orig and 0 < iy < h_orig and puff_r > 0:
                cv2.circle(steam_layer, (ix, iy), puff_r, alpha_fade, -1)
                off = int(puff_r * 0.45)
                ox2, oy2 = ix + off, iy - off // 2
                if 0 < ox2 < w_orig and 0 < oy2 < h_orig:
                    cv2.circle(steam_layer, (ox2, oy2), int(puff_r * 0.7), alpha_fade * 0.6, -1)

        steam_blur = cv2.GaussianBlur(steam_layer, (31, 31), 0)
        frame_float = frame.astype(np.float32)
        for c in range(3):
            frame_float[:, :, c] = np.clip(frame_float[:, :, c] + steam_blur * 220.0, 0, 255)
        frame = frame_float.astype(np.uint8)

        # -------------------------------------------------------------
        # 4. Flashing Arcade Pushbuttons on Control Console
        # -------------------------------------------------------------
        for b_idx, (bx, by, br, bcol) in enumerate(buttons):
            b_active = ((f_idx + b_idx * 3) % 6 < 3)
            if b_active:
                btn_glow = np.zeros_like(frame, dtype=np.uint8)
                cv2.circle(btn_glow, (bx, by), br + 4, bcol, -1)
                cv2.circle(btn_glow, (bx, by), br - 2, (255, 255, 255), -1)
                btn_glow = cv2.GaussianBlur(btn_glow, (9, 9), 0)
                frame = cv2.addWeighted(frame, 1.0, btn_glow, 0.65, 0)

        # -------------------------------------------------------------
        # 5. Pipe Indicator Lamps Blinking (Red, Yellow, Green)
        # -------------------------------------------------------------
        for i_idx, (ix, iy, icol) in enumerate(pipe_indicators):
            lamp_on = ((f_idx + i_idx * 2) % 4 < 2)
            if lamp_on:
                lamp_glow = np.zeros_like(frame, dtype=np.uint8)
                cv2.circle(lamp_glow, (ix, iy), 8, icol, -1)
                lamp_glow = cv2.GaussianBlur(lamp_glow, (11, 11), 0)
                frame = cv2.addWeighted(frame, 1.0, lamp_glow, 0.55, 0)

        # -------------------------------------------------------------
        # 6. Industrial Amber Warning Strobe on Console
        # -------------------------------------------------------------
        beacon_flash = (math.sin(ang * 3) * 0.5 + 0.5) ** 4
        if beacon_flash > 0.15:
            bc_x, bc_y = beacon_pos
            b_rad = int(12 + 18 * beacon_flash)
            b_glow = np.zeros_like(frame, dtype=np.uint8)
            cv2.circle(b_glow, (bc_x, bc_y), b_rad, (0, 200, 255), -1)
            cv2.circle(b_glow, (bc_x, bc_y), int(b_rad * 0.4), (180, 245, 255), -1)
            b_glow_blur = cv2.GaussianBlur(b_glow, (21, 21), 0)
            frame = cv2.addWeighted(frame, 1.0, b_glow_blur, 0.85 * beacon_flash, 0)

        # -------------------------------------------------------------
        # 7. Flowing Energy Pulse on Green Pipe Arrows
        # -------------------------------------------------------------
        arrow_pulse = 0.5 + 0.5 * math.sin(ang * 2)
        arrow_layer = np.zeros_like(frame, dtype=np.uint8)
        cv2.ellipse(arrow_layer, (205, 715), (40, 20), 0, 0, 360, (100, 255, 120), -1)
        arrow_layer = cv2.GaussianBlur(arrow_layer, (15, 15), 0)
        frame = cv2.addWeighted(frame, 1.0, arrow_layer, 0.40 * arrow_pulse, 0)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames_bgr.append(frame_rgb)

    # -------------------------------------------------------------
    # 8. Export High-Quality Animated Looping GIF
    # -------------------------------------------------------------
    print(f"Resizing and quantizing {len(frames_bgr)} frames to {target_width}px...")
    pil_rgb = [Image.fromarray(f).resize((target_width, target_height), Image.Resampling.LANCZOS) for f in frames_bgr]

    base_palette_img = pil_rgb[0].convert("P", palette=Image.Palette.ADAPTIVE, colors=240)
    pil_p = [pim.quantize(palette=base_palette_img, dither=Image.Dither.FLOYDSTEINBERG) for pim in pil_rgb]

    print(f"Saving looping GIF to {output_gif_path}...")
    pil_p[0].save(
        output_gif_path,
        save_all=True,
        append_images=pil_p[1:],
        duration=duration,
        loop=0,
        optimize=True
    )

    gif_mb = os.path.getsize(output_gif_path) / (1024 * 1024)
    png_mb = os.path.getsize(output_png_path) / (1024 * 1024)
    print("\n✅ SUCCESS!")
    print(f"  PNG: {output_png_path} ({png_mb:.2f} MB, {target_width}x{target_height})")
    print(f"  GIF: {output_gif_path} ({gif_mb:.2f} MB, {target_width}x{target_height}, {num_frames} frames)")

if __name__ == "__main__":
    generate_mario_industrial_banner()
