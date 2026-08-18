from pathlib import Path
import math
import random

from PIL import Image, ImageDraw, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "loki_source.jpg"
FALLBACK = ROOT / "portrait_fallback.png"
GIF = ROOT / "portrait_morph.gif"

SIZE = 320
PALETTE = {
    "void_black": "#0A0A12",
    "dark_circuit": "#12121F",
    "night_panel": "#1A1A2E",
    "ghost_white": "#E8E8F0",
    "soft_circuit": "#A0A0B8",
    "cyan_flash": "#00F0FF",
    "pure_ghost": "#F8F8FF",
    "soft_cyan": "#00C4D4",
    "circuit_edge": "#2A2A3D",
}


def rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


VOID = rgb(PALETTE["void_black"])
DARK = rgb(PALETTE["dark_circuit"])
PANEL = rgb(PALETTE["night_panel"])
SOFT = rgb(PALETTE["soft_circuit"])
CYAN = rgb(PALETTE["cyan_flash"])
PURE = rgb(PALETTE["pure_ghost"])
SOFT_CYAN = rgb(PALETTE["soft_cyan"])
EDGE = rgb(PALETTE["circuit_edge"])


def source_field():
    """Build a Loki-only source field and explicitly exclude the right-side creature/background."""
    source = Image.open(SOURCE).convert("RGB")
    source = ImageOps.fit(
        source,
        (SIZE, SIZE),
        method=Image.Resampling.LANCZOS,
        centering=(0.47, 0.46),
    )
    source = ImageEnhance.Contrast(source).enhance(1.16)
    luminance = source.convert("L")
    # A conservative silhouette polygon keeps Loki’s face, hair, and armor while
    # excluding the original green background and the right-side creature.
    mask = Image.new("L", (SIZE, SIZE), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.polygon(
        [
            (112, 0), (248, 0), (278, 34), (286, 82),
            (284, 140), (276, 180), (270, 216), (276, 252),
            (258, 286), (218, 320), (68, 320), (0, 300),
            (0, 132), (48, 66),
        ],
        fill=255,
    )
    # Remove the outer-right region where the original creature and hand sit.
    mask_draw.rectangle((270, 126, SIZE, SIZE), fill=0)
    # Keep only luminance-bearing source pixels inside the silhouette.
    points = []
    pixels = luminance.load()
    rgb_pixels = source.load()
    mask_pixels = mask.load()
    rng = random.Random(314159)
    for y in range(0, SIZE, 2):
        for x in range(0, SIZE, 2):
            if mask_pixels[x, y] == 0:
                continue
            red, green, blue = rgb_pixels[x, y]
            lum = pixels[x, y]
            # Suppress the bright green photographic background while retaining
            # dark green armor and high-contrast face/hair features.
            if green > red + 28 and green > blue + 18 and lum > 92:
                continue
            if lum < 16:
                continue
            probability = 0.22 + (lum / 255.0) * 0.52
            if rng.random() > probability:
                continue
            if lum >= 204:
                color = PURE
                radius = 1.22
            elif lum >= 134:
                color = CYAN
                radius = 0.96
            else:
                color = SOFT_CYAN
                radius = 0.74
            points.append((float(x), float(y), color, radius, lum))
    # Add a deterministic sparse set of edge/detail points to preserve the face
    # outline and hair silhouette in the particle reconstruction.
    for y in range(2, SIZE - 2, 2):
        for x in range(2, SIZE - 2, 2):
            if mask_pixels[x, y] == 0:
                continue
            center = pixels[x, y]
            edge_strength = abs(center - pixels[x - 1, y]) + abs(center - pixels[x + 1, y])
            edge_strength += abs(center - pixels[x, y - 1]) + abs(center - pixels[x, y + 1])
            if edge_strength > 120 and (x * 7 + y * 13) % 5 == 0:
                points.append((float(x), float(y), PURE, 0.92, center))
    return points


def draw_particle(draw, x, y, color, radius, brightness):
    if x < 0 or y < 0 or x >= SIZE or y >= SIZE:
        return
    # A low-intensity secondary pixel gives the field a breathing, non-solid feel.
    r = max(0.55, radius * (0.78 + brightness * 0.34))
    x0 = int(round(x))
    y0 = int(round(y))
    if r < 0.9:
        draw.point((x0, y0), fill=color)
    else:
        draw.ellipse((x0 - r, y0 - r, x0 + r, y0 + r), fill=color)


def frame_canvas():
    canvas = Image.new("RGB", (SIZE, SIZE), VOID)
    draw = ImageDraw.Draw(canvas)
    # The frame is intentionally quiet so particles remain the primary language.
    draw.rectangle((8, 8, SIZE - 9, SIZE - 9), outline=EDGE, width=1)
    draw.text((16, 14), "IDENTITY.FIELD // LOKI", fill=SOFT, font=None)
    draw.text((16, SIZE - 22), "PARTICLE RECONSTRUCTION // ACTIVE", fill=SOFT_CYAN, font=None)
    return canvas, draw


def particle_frame(points, frame_index, total_frames=24, fallback=False):
    canvas, draw = frame_canvas()
    rng = random.Random(9000 + frame_index * 71)
    phase = frame_index / float(total_frames)
    center_x, center_y = 145.0, 165.0
    # Stable living motion: every point jitters and drifts while the silhouette
    # remains anchored to the same underlying portrait coordinates.
    base_breathe = 1.0 + 0.014 * math.sin(frame_index * 0.56)
    wave_radius = (frame_index - 5.0) * 42.0
    dispersal = 0.0
    if 9 <= frame_index <= 13:
        dispersal = (frame_index - 9) / 4.0
    elif 14 <= frame_index <= 18:
        dispersal = 1.0 - (frame_index - 14) / 4.0
    wave_strength = 0.0
    if 5 <= frame_index <= 9:
        wave_strength = math.sin((frame_index - 5) / 4.0 * math.pi) * 8.0
    for index, (bx, by, color, radius, lum) in enumerate(points):
        dx = bx - center_x
        dy = by - center_y
        distance = math.hypot(dx, dy)
        angle = math.atan2(dy, dx)
        local_phase = frame_index * 0.36 + index * 0.071
        jitter_x = math.sin(local_phase) * (0.55 + (lum / 255.0) * 0.55)
        jitter_y = math.cos(local_phase * 1.13) * (0.45 + (lum / 255.0) * 0.5)
        drift = math.sin(frame_index * 0.23 + by * 0.035) * 0.65
        x = center_x + dx * base_breathe + jitter_x + drift
        y = center_y + dy * base_breathe + jitter_y
        # Periodic wave reaction: a soft ring travels through the field.
        if wave_strength:
            ring = math.exp(-((distance - wave_radius) ** 2) / (2 * 18.0 ** 2))
            x += math.cos(angle) * ring * wave_strength
            y += math.sin(angle) * ring * wave_strength
        # Controlled dispersal/reformation keeps particles related to the portrait.
        if dispersal:
            outward = 1.0 + dispersal * (0.42 + 0.10 * math.sin(index * 0.17))
            x = center_x + (x - center_x) * outward
            y = center_y + (y - center_y) * outward
            x += math.sin(index * 0.19 + frame_index) * dispersal * 3.0
            y += math.cos(index * 0.23 + frame_index) * dispersal * 2.2
        # Density breathes subtly; high-value face points remain persistent.
        keep_bias = 0.90 + 0.10 * math.sin(frame_index * 0.45 + index * 0.013)
        if not fallback and lum < 110 and rng.random() > keep_bias:
            continue
        if dispersal > 0.55 and rng.random() < dispersal * 0.10:
            continue
        draw_particle(draw, x, y, color, radius, lum / 255.0)
    # A very restrained cyan boundary line makes the module read as a field, not a photo.
    draw.line((18, 31, 76, 31), fill=CYAN, width=1)
    draw.line((SIZE - 76, SIZE - 31, SIZE - 18, SIZE - 31), fill=CYAN, width=1)
    return canvas


def main():
    points = source_field()
    total_frames = 24
    frames = [particle_frame(points, index, total_frames=total_frames) for index in range(total_frames)]
    fallback = particle_frame(points, 2, total_frames=total_frames, fallback=True)
    fallback.save(FALLBACK, "PNG", optimize=True)
    indexed = [frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=96) for frame in frames]
    durations = [180] * total_frames
    indexed[0].save(
        GIF,
        save_all=True,
        append_images=indexed[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=2,
    )
    print(f"SOURCE_POINTS={len(points)}")
    print(f"GIF={GIF}")
    print(f"PNG={FALLBACK}")
    print(f"FRAMES_REQUESTED={len(frames)}")
    print(f"GIF_BYTES={GIF.stat().st_size}")
    print(f"PNG_BYTES={FALLBACK.stat().st_size}")


if __name__ == "__main__":
    main()
