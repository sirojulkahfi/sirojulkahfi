"""
Script to generate or enhance anime industrial robotic arm banner GIFs.
Features:
- Animated cyberpunk HUD scanline & grid effects
- Pulsing neon glow on robotic arm & circuitry
- Animated spark particles & laser welding light
- Smooth looping GIF export with palette optimization
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

def create_animated_banner(
    base_image_path="assets/banner_base.jpg",
    output_gif_path="assets/banner_custom.gif",
    num_frames=24,
    duration=80,
    target_width=960
):
    if not os.path.exists(base_image_path):
        print(f"Error: Base image '{base_image_path}' not found.")
        return

    print(f"Loading base image: {base_image_path}...")
    base_img = Image.open(base_image_path).convert("RGB")
    
    # Resize keeping aspect ratio
    aspect = base_img.height / base_img.width
    target_height = int(target_width * aspect)
    base_img = base_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    width, height = base_img.size
    print(f"Base image resized to {width}x{height}, generating {num_frames} frames...")

    # Spark source coordinates (welding tip on chip)
    # Scaled according to image size (approx 47% from left, 75% from top)
    spark_cx = int(width * 0.472)
    spark_cy = int(height * 0.748)

    frames = []
    random.seed(42)

    for i in range(num_frames):
        t = i / num_frames
        angle = t * 2 * math.pi
        
        # Start with a copy of the base
        frame = base_img.copy()
        
        # Overlay drawing layer
        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # 1. Animated Horizontal HUD Laser / Scanline
        scan_y = int((math.sin(angle) * 0.5 + 0.5) * height)
        scan_color = (0, 240, 255, int(40 + 20 * math.sin(angle * 2)))
        draw.line([(0, scan_y), (width, scan_y)], fill=scan_color, width=2)
        # Scanline glow
        draw.line([(0, scan_y - 1), (width, scan_y - 1)], fill=(0, 240, 255, 20), width=1)
        draw.line([(0, scan_y + 1), (width, scan_y + 1)], fill=(0, 240, 255, 20), width=1)

        # 2. Glowing pulse on welding contact point
        pulse = 0.7 + 0.3 * math.sin(angle * 3)
        glow_radius = int(25 * pulse)
        for r in range(glow_radius, 5, -4):
            alpha = int(40 * (1 - r / glow_radius) * pulse)
            draw.ellipse(
                [spark_cx - r, spark_cy - r, spark_cx + r, spark_cy + r],
                fill=(255, 220, 100, alpha)
            )
        # Core intense white/cyan spark center
        core_r = int(6 + 3 * math.sin(angle * 5))
        draw.ellipse(
            [spark_cx - core_r, spark_cy - core_r, spark_cx + core_r, spark_cy + core_r],
            fill=(255, 255, 240, 220)
        )

        # 3. Dynamic Flying Sparks
        num_sparks = 18
        for s in range(num_sparks):
            spark_phase = (t + s / num_sparks) % 1.0
            spark_ang = math.radians(-160 + (s * 25) % 140 + math.sin(angle + s) * 15)
            spark_dist = 20 + spark_phase * 120
            sx = spark_cx + spark_dist * math.cos(spark_ang)
            sy = spark_cy + spark_dist * math.sin(spark_ang) + (spark_phase ** 2) * 40  # gravity fall
            spark_size = max(1, int(3 * (1.0 - spark_phase)))
            spark_alpha = int(255 * (1.0 - spark_phase))
            
            # Spark streak
            prev_dist = max(0, spark_dist - 8)
            psx = spark_cx + prev_dist * math.cos(spark_ang)
            psy = spark_cy + prev_dist * math.sin(spark_ang) + (spark_phase ** 2) * 35
            
            draw.line([(psx, psy), (sx, sy)], fill=(255, 200, 80, spark_alpha), width=spark_size)

        # Composite overlay
        frame.paste(overlay, (0, 0), overlay)
        
        # Subtle contrast / cybernetic pop
        enhancer = ImageEnhance.Color(frame)
        frame = enhancer.enhance(1.05)
        
        frames.append(frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=256))

    print(f"Saving optimized GIF to {output_gif_path}...")
    frames[0].save(
        output_gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
        optimize=True
    )
    print("Done! GIF banner successfully generated.")

if __name__ == "__main__":
    create_animated_banner()
