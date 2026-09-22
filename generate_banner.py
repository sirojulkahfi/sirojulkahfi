"""
Advanced Anime Industrial Robotic Arm Banner Generator
Features:
- Segmented Kinematic Articulation of the Robotic Arm (shoulder, elbow, forearm, wrist, nozzle)
- Rigid Surface Anchoring: motherboard and background stay 100% crisp and unwarped
- Realistic Multi-Phase Welding Cycle: welding pass, lift/retract, traversal, touchdown, return seam
- Animated Cyberpunk Holographic HUDs: scrolling telemetry wave, sweeping scanlines, blinking status LEDs
- Animated Conveyor Belt: perspective translation into the background tunnel and roller motion
- Dynamic Welding Physics: intense arc flash, metallic reflections, flying spark particle trails with gravity
- Atmospheric Anime Lighting: mecha visor glints, glowing Japanese neon signage
- Optimized export to GIF (850px width, ~4MB, smooth 28-frame loop) for GitHub profile README
"""

import os
import math
import random
import cv2
import numpy as np
from PIL import Image

def generate_anime_industrial_banner(
    base_image_path="assets/anime_banner_base.jpg",
    output_gif_path="assets/banner.gif",
    num_frames=28,
    duration=80,
    target_width=850
):
    if not os.path.exists(base_image_path):
        raise FileNotFoundError(f"Base image not found at {base_image_path}")

    print(f"Loading anime base image: {base_image_path}...")
    base_bgr = cv2.imread(base_image_path)
    h_orig, w_orig, _ = base_bgr.shape

    # Region of Interest around the Robotic Arm
    rx1, ry1, rx2, ry2 = 180, 200, 840, 680
    rh, rw = ry2 - ry1, rx2 - rx1

    # Static anchor points around the perimeter of ROI (displacement = 0)
    anchors = []
    for x in np.linspace(0, rw - 1, 14):
        anchors.append([x, 0])
        anchors.append([x, rh - 1])
    for y in np.linspace(0, rh - 1, 10):
        anchors.append([0, y])
        anchors.append([rw - 1, y])

    # PCB Chip Surface Anchors - strictly anchors the motherboard beneath the tip
    for cx in range(620, 790, 12):
        anchors.append([cx - rx1, 569 - ry1])
        anchors.append([cx - rx1, 582 - ry1])
        anchors.append([cx - rx1, 600 - ry1])

    # Additional stable anchors in factory interior
    anchors.extend([
        [500 - rx1, 480 - ry1],
        [240 - rx1, 620 - ry1],
        [370 - rx1, 620 - ry1],
        [210 - rx1, 380 - ry1],
        [430 - rx1, 240 - ry1]
    ])
    anchor_pts = np.array(anchors, dtype=np.float32)

    # Arm Kinematic Bone Positions relative to ROI
    bone_base = [310 - rx1, 580 - ry1]
    bone_lower = [290 - rx1, 450 - ry1]
    bone_knuckle = [340 - rx1, 320 - ry1]
    bone_forearm = [470 - rx1, 390 - ry1]
    bone_wrist = [590 - rx1, 460 - ry1]
    bone_nozzle = [670 - rx1, 510 - ry1]
    bone_tip = [722 - rx1, 555 - ry1] # Center of nozzle tip
    bones_rel = [bone_base, bone_lower, bone_knuckle, bone_forearm, bone_wrist, bone_nozzle, bone_tip]

    yy, xx = np.mgrid[0:rh, 0:rw].astype(np.float32)
    grid_pts = np.stack([xx, yy], axis=-1)

    # Pre-generate physics sparks for clean looping
    random.seed(2026)
    num_sparks_pool = 80
    spark_pool = []
    for _ in range(num_sparks_pool):
        ang = random.uniform(math.radians(-165), math.radians(-15))
        spd = random.uniform(5.0, 16.0)
        life = random.randint(4, 9)
        spark_pool.append({
            'angle': ang,
            'speed': spd,
            'life': life,
            'color': random.choice([
                (255, 255, 255),
                (180, 245, 255),
                (120, 230, 255),
                (80, 200, 255),
                (255, 220, 130)
            ])
        })

    frames_bgr = []
    print(f"Synthesizing {num_frames} dynamic anime frames...")

    for f_idx in range(num_frames):
        t = f_idx / num_frames
        frame = base_bgr.copy()

        # -------------------------------------------------------------
        # 1. Robotic Arm Kinematic Motion Trajectory
        # -------------------------------------------------------------
        # 0..10: Welding seam 1 (moving right across chip pins: -28 -> +16)
        # 11..15: Quick vertical lift & retraction (+16 -> +8, lifting up 18px)
        # 16..20: Horizontal traverse across header (+8 -> -20, maintaining elevation)
        # 21..24: Smooth touchdown to second track (-20 -> -28, descending back)
        # 25..27: Arc strike & return weld seam
        if f_idx <= 10:
            p = f_idx / 10.0
            tdx = -28.0 + p * 44.0
            tdy = -4.0 + math.sin(p * math.pi) * 3.0
            arc_active = True
            arc_intensity = 0.9 + 0.3 * math.sin(f_idx * 2.0)
        elif 11 <= f_idx <= 15:
            p = (f_idx - 11) / 4.0
            tdx = 16.0 - p * 8.0
            tdy = -4.0 - math.sin(p * math.pi * 0.5) * 16.0
            arc_active = False
            arc_intensity = max(0.0, 0.6 - p * 0.8)
        elif 16 <= f_idx <= 20:
            p = (f_idx - 16) / 4.0
            tdx = 8.0 - p * 26.0
            tdy = -20.0 + p * 3.0
            arc_active = False
            arc_intensity = 0.0
        elif 21 <= f_idx <= 24:
            p = (f_idx - 21) / 3.0
            tdx = -18.0 - p * 10.0
            tdy = -17.0 + p * 13.0
            arc_active = (f_idx >= 23)
            arc_intensity = 0.6 if f_idx == 23 else 1.3 # arc strike flash
        else: # 25..27
            p = (f_idx - 25) / 2.0
            tdx = -28.0 + p * 2.0
            tdy = -4.0
            arc_active = True
            arc_intensity = 0.95 + 0.25 * math.sin(f_idx * 2.5)

        # Bone displacements with realistic kinematic articulation
        bone_disps = [
            [0.0, 0.0],
            [tdx * 0.05, tdy * 0.02],
            [tdx * 0.20, tdy * 0.15],
            [tdx * 0.45, tdy * 0.40],
            [tdx * 0.70, tdy * 0.65],
            [tdx * 0.88, tdy * 0.85],
            [tdx * 1.00, tdy * 1.00],
        ]

        all_pts = np.vstack([bones_rel, anchor_pts])
        all_disps = np.vstack([bone_disps, np.zeros((len(anchor_pts), 2), dtype=np.float32)])

        # IDW Kinematic Warp
        dx = grid_pts[:, :, 0:1] - all_pts[:, 0]
        dy = grid_pts[:, :, 1:2] - all_pts[:, 1]
        dist_sq = dx**2 + dy**2
        weights = 1.0 / (dist_sq**1.3 + 16.0)
        weights /= weights.sum(axis=-1, keepdims=True)

        df_x = (weights * all_disps[:, 0]).sum(axis=-1)
        df_y = (weights * all_disps[:, 1]).sum(axis=-1)

        map_x = (xx - df_x).astype(np.float32)
        map_y = (yy - df_y).astype(np.float32)

        roi_img = frame[ry1:ry2, rx1:rx2]
        warped_arm = cv2.remap(roi_img, map_x, map_y, interpolation=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
        frame[ry1:ry2, rx1:rx2] = warped_arm

        tip_world_x = int(722 + tdx)
        tip_world_y = int(558 + tdy)

        # -------------------------------------------------------------
        # 2. Conveyor Belt Motion
        # -------------------------------------------------------------
        # Right conveyor line markers sliding into the background tunnel
        drift = int((f_idx * 2.4) % 36)
        for c_step in range(0, 360, 42):
            cy = 505 + int((c_step + drift) * 0.42)
            if cy < 645:
                cx_l = int(795 + (cy - 505) * 0.82)
                cx_r = int(885 + (cy - 505) * 1.38)
                cv2.line(frame, (cx_l, cy), (cx_r, cy), (65, 120, 140), 1)

        # Rollers rotating under the main board
        roller_shift = int((f_idx * 1.8) % 8)
        for rx in range(540, 750, 24):
            lx = rx + roller_shift
            if lx < 750:
                cv2.line(frame, (lx, 655), (lx - 28, 715), (75, 100, 115), 1)

        # -------------------------------------------------------------
        # 3. Holographic HUD Displays & Telemetry
        # -------------------------------------------------------------
        # A. Cyan HUD Screen (x: 250..500, y: 20..250)
        # Sweeping horizontal scanline
        scan_y = int(35 + ((f_idx * 8) % 195))
        cv2.line(frame, (255, scan_y), (495, scan_y), (255, 245, 120), 1)

        # Blinking Status Dots
        dot_blink = (f_idx % 6 < 3)
        # [SYSTEM: ONLINE] green dot
        cv2.circle(frame, (260, 72), 3, (100, 255, 120) if dot_blink else (30, 120, 50), -1)
        # [WELDER-73: ACTIVE] cyan dot
        welder_dot = (0, 240, 255) if arc_active else (180, 110, 30)
        cv2.circle(frame, (260, 93), 3, welder_dot, -1)

        # Dynamic Scrolling Telemetry Waveform in graph box
        graph_x1, graph_y1, graph_x2, graph_y2 = 378, 185, 442, 230
        cv2.rectangle(frame, (graph_x1, graph_y1), (graph_x2, graph_y2), (18, 48, 55), -1)
        wave_pts = []
        for gx in range(graph_x1, graph_x2):
            g_phase = (gx - graph_x1) * 0.35 + f_idx * 0.6
            gy = int((graph_y1 + graph_y2) / 2 + math.sin(g_phase) * 12 + math.cos(g_phase * 2.1) * 5)
            wave_pts.append((gx, gy))
        for p_i in range(len(wave_pts) - 1):
            cv2.line(frame, wave_pts[p_i], wave_pts[p_i+1], (255, 235, 80), 1)

        # Temperature fluctuation
        temp_val = 450 + int(math.sin(f_idx * 0.5) * 9)
        cv2.putText(frame, f"{temp_val}C", (370, 160), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 230, 255), 1)

        # B. Orange HUD Screen (x: 560..745, y: 410..615)
        # Rotating reticle crosshair in circular scope
        ret_cx, ret_cy = 582, 472
        ret_r = 15
        ret_ang = t * 4 * math.pi
        cv2.circle(frame, (ret_cx, ret_cy), ret_r, (40, 180, 255), 1)
        rx_end = int(ret_cx + ret_r * math.cos(ret_ang))
        ry_end = int(ret_cy + ret_r * math.sin(ret_ang))
        cv2.line(frame, (ret_cx, ret_cy), (rx_end, ry_end), (40, 200, 255), 1)

        # C. Oscilloscope on far left screen (x: 50..195, y: 410..550)
        osc_x1, osc_y1, osc_w = 75, 485, 95
        osc_pts = []
        for ox in range(osc_w):
            phase_o = ox * 0.28 - f_idx * 0.5
            pulse = math.sin(phase_o) * math.exp(-((ox % 28 - 14) / 5.5)**2) * 13
            osc_pts.append((osc_x1 + ox, int(osc_y1 + pulse)))
        for p_i in range(len(osc_pts) - 1):
            cv2.line(frame, osc_pts[p_i], osc_pts[p_i+1], (230, 255, 120), 1)

        # D. Background Gundam / Mecha Eye Visor Glint (head at x: 724, y: 275)
        mecha_glint = (math.sin(t * 2 * math.pi) * 0.5 + 0.5) ** 3
        if mecha_glint > 0.15:
            g_rad = int(2 + 4 * mecha_glint)
            cv2.circle(frame, (724, 275), g_rad, (50, 110, 255), -1)
            cv2.circle(frame, (724, 275), 1, (220, 240, 255), -1)

        # -------------------------------------------------------------
        # 4. Dynamic Welding Arc Flare & Physics Sparks
        # -------------------------------------------------------------
        if arc_intensity > 0.05:
            glow_layer = np.zeros_like(frame, dtype=np.uint8)
            g_radius = int(50 * arc_intensity)
            cv2.circle(glow_layer, (tip_world_x, tip_world_y), g_radius, (255, 190, 80), -1)
            cv2.circle(glow_layer, (tip_world_x, tip_world_y), int(g_radius * 0.55), (255, 230, 180), -1)
            cv2.circle(glow_layer, (tip_world_x, tip_world_y), int(g_radius * 0.25), (255, 255, 255), -1)
            glow_blurred = cv2.GaussianBlur(glow_layer, (41, 41), 0)
            frame = cv2.addWeighted(frame, 1.0, glow_blurred, 0.70 * arc_intensity, 0)

            # Core intense arc flash
            core_r = max(2, int(6 * arc_intensity))
            cv2.circle(frame, (tip_world_x, tip_world_y), core_r, (255, 255, 255), -1)
            spk_len = int(14 * arc_intensity)
            cv2.line(frame, (tip_world_x - spk_len, tip_world_y), (tip_world_x + spk_len, tip_world_y), (255, 255, 240), 1)
            cv2.line(frame, (tip_world_x, tip_world_y - spk_len), (tip_world_x, tip_world_y + spk_len), (255, 255, 240), 1)

            # Flying sparks spray
            num_sparks = int(24 * arc_intensity)
            for s_idx in range(num_sparks):
                p_data = spark_pool[(s_idx * 3 + f_idx) % num_sparks_pool]
                spark_age = (f_idx * 1.3 + s_idx * 1.5) % p_data['life']
                spark_frac = spark_age / p_data['life']

                s_dist = p_data['speed'] * spark_age * 2.8
                ang = p_data['angle'] + math.sin(f_idx + s_idx) * 0.15
                spx = int(tip_world_x + s_dist * math.cos(ang))
                spy = int(tip_world_y + s_dist * math.sin(ang) + 0.5 * 1.4 * (spark_age**2)) # gravity

                if 0 <= spx < w_orig and 0 <= spy < h_orig:
                    trail_dist = max(0, s_dist - p_data['speed'] * 1.3)
                    tpx = int(tip_world_x + trail_dist * math.cos(ang))
                    tpy = int(tip_world_y + trail_dist * math.sin(ang) + 0.5 * 1.4 * (max(0, spark_age - 1)**2))
                    
                    alpha = max(0.2, 1.0 - spark_frac)
                    color = tuple(int(c * alpha) for c in p_data['color'])
                    thickness = 2 if spark_frac < 0.25 else 1
                    cv2.line(frame, (tpx, tpy), (spx, spy), color, thickness)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames_bgr.append(frame_rgb)

    # -------------------------------------------------------------
    # 5. Export to Optimized GIF with Global Adaptive Palette
    # -------------------------------------------------------------
    print(f"Resizing and quantizing {len(frames_bgr)} frames to target width {target_width}px...")
    aspect = h_orig / w_orig
    target_height = int(target_width * aspect)

    pil_rgb = [Image.fromarray(f).resize((target_width, target_height), Image.Resampling.LANCZOS) for f in frames_bgr]

    # Global palette from first frame with dither for rich anime colors
    base_palette_img = pil_rgb[0].convert("P", palette=Image.Palette.ADAPTIVE, colors=160)
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
    
    file_size_mb = os.path.getsize(output_gif_path) / (1024 * 1024)
    print(f"Success! Banner GIF created: {output_gif_path} ({file_size_mb:.2f} MB, {target_width}x{target_height}, {num_frames} frames)")

if __name__ == "__main__":
    generate_anime_industrial_banner()
