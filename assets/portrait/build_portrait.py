from pathlib import Path
import math
import random

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

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
    "glitch_red": "#FF003C",
    "signal_blue": "#0088FF",
    "neon_fluorescent": "#39FF14",
    "circuit_edge": "#2A2A3D",
    "pure_ghost": "#F8F8FF",
    "soft_cyan": "#00C4D4",
    "deep_navy": "#0B0F1A",
}


def hex_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i+2], 16) for i in (0, 2, 4))


VOID = hex_rgb(PALETTE["void_black"])
DARK = hex_rgb(PALETTE["dark_circuit"])
PANEL = hex_rgb(PALETTE["night_panel"])
WHITE = hex_rgb(PALETTE["ghost_white"])
SOFT = hex_rgb(PALETTE["soft_circuit"])
CYAN = hex_rgb(PALETTE["cyan_flash"])
RED = hex_rgb(PALETTE["glitch_red"])
BLUE = hex_rgb(PALETTE["signal_blue"])
GREEN = hex_rgb(PALETTE["neon_fluorescent"])
EDGE = hex_rgb(PALETTE["circuit_edge"])
PURE = hex_rgb(PALETTE["pure_ghost"])
SOFT_CYAN = hex_rgb(PALETTE["soft_cyan"])
NAVY = hex_rgb(PALETTE["deep_navy"])


def source_image():
    image = Image.open(SOURCE).convert("RGB")
    image = ImageOps.fit(image, (SIZE, SIZE), method=Image.Resampling.LANCZOS, centering=(0.5, 0.48))
    image = ImageEnhance.Contrast(image).enhance(1.08)
    image = ImageEnhance.Color(image).enhance(0.82)
    return image


def base_canvas():
    image = Image.new("RGB", (SIZE, SIZE), VOID)
    draw = ImageDraw.Draw(image)
    draw.rectangle((8, 8, SIZE - 9, SIZE - 9), outline=EDGE, width=1)
    draw.line((16, 28, SIZE - 16, 28), fill=SOFT_CYAN, width=1)
    draw.line((16, SIZE - 28, SIZE - 16, SIZE - 28), fill=SOFT_CYAN, width=1)
    draw.text((17, 14), "PORTRAIT.SCAN // ACTIVE", fill=SOFT, font=None)
    draw.text((17, SIZE - 22), "IDENTITY VERIFIED", fill=CYAN, font=None)
    return image


def clean_frame():
    src = source_image()
    canvas = base_canvas()
    # Keep the real portrait dominant and slightly darken it into the locked dark system palette.
    tinted = Image.blend(src, Image.new("RGB", src.size, NAVY), 0.18)
    tinted = ImageEnhance.Contrast(tinted).enhance(1.18)
    canvas.paste(tinted, (0, 0))
    draw = ImageDraw.Draw(canvas)
    for y in range(0, SIZE, 4):
        draw.line((0, y, SIZE, y), fill=(0, 120, 135), width=1)
    draw.rectangle((7, 7, SIZE - 8, SIZE - 8), outline=CYAN, width=1)
    draw.line((18, 36, 72, 36), fill=PURE, width=2)
    draw.line((SIZE - 72, SIZE - 36, SIZE - 18, SIZE - 36), fill=PURE, width=2)
    return canvas


def ascii_frame():
    src = source_image().convert("L")
    # Use a compact terminal raster while preserving the portrait silhouette.
    cols, rows = 74, 44
    small = src.resize((cols, rows), Image.Resampling.BILINEAR)
    chars = " .:-=+*#%@"
    canvas = Image.new("RGB", (SIZE, SIZE), VOID)
    draw = ImageDraw.Draw(canvas)
    for y in range(rows):
        for x in range(cols):
            value = small.getpixel((x, y))
            char = chars[int(value / 256 * len(chars)) if value < 255 else -1]
            if value > 175:
                color = PURE
            elif value > 105:
                color = CYAN
            else:
                color = SOFT_CYAN
            draw.text((10 + x * 4, 40 + y * 5), char, fill=color, font=None)
    draw.rectangle((7, 7, SIZE - 8, SIZE - 8), outline=CYAN, width=1)
    draw.text((17, 14), "ASCII.IDENTITY // SCANLINE", fill=PURE, font=None)
    draw.text((17, SIZE - 22), "RASTER LOCK // 02", fill=CYAN, font=None)
    for y in range(34, SIZE - 30, 6):
        draw.line((10, y, SIZE - 10, y), fill=(0, 80, 95), width=1)
    return canvas


def particle_frame(seed):
    rng = random.Random(seed)
    src = source_image().convert("L")
    canvas = Image.new("RGB", (SIZE, SIZE), VOID)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((7, 7, SIZE - 8, SIZE - 8), outline=EDGE, width=1)
    draw.text((17, 14), "PARTICLE.FIELD // RECONSTRUCT", fill=PURE, font=None)
    draw.text((17, SIZE - 22), "SIGNAL RETURN // 03", fill=CYAN, font=None)
    for _ in range(18000):
        x = rng.randrange(SIZE)
        y = rng.randrange(SIZE)
        lum = src.getpixel((x, y))
        threshold = 28 + int(lum * 0.62)
        if rng.randrange(256) < threshold:
            if lum > 185:
                color = PURE
            elif lum > 115:
                color = CYAN
            else:
                color = SOFT_CYAN
            if rng.random() < 0.02:
                color = RED
            size = 1 if rng.random() < 0.94 else 2
            draw.rectangle((x, y, x + size, y + size), fill=color)
    # Faint guide marks retain the instrument-panel feel without overwhelming the portrait.
    for x in (36, 96, 224, 284):
        draw.line((x, 34, x, SIZE - 34), fill=(0, 50, 65), width=1)
    for y in (58, 132, 206, 280):
        draw.line((18, y, SIZE - 18, y), fill=(0, 50, 65), width=1)
    return canvas


def wireframe_frame():
    src = source_image().convert("L")
    edges = src.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.GaussianBlur(0.35))
    edges = ImageEnhance.Contrast(edges).enhance(2.8)
    canvas = Image.new("RGB", (SIZE, SIZE), VOID)
    pixels = edges.load()
    out = canvas.load()
    for y in range(SIZE):
        for x in range(SIZE):
            value = pixels[x, y]
            if value > 45:
                if value > 165:
                    out[x, y] = PURE
                elif value > 95:
                    out[x, y] = CYAN
                else:
                    out[x, y] = SOFT_CYAN
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((7, 7, SIZE - 8, SIZE - 8), outline=CYAN, width=1)
    draw.text((17, 14), "WIREFRAME.MAP // VERIFY", fill=PURE, font=None)
    draw.text((17, SIZE - 22), "GEOMETRY RETURN // 04", fill=CYAN, font=None)
    for offset in (0, 1):
        draw.line((18, 42 + offset, SIZE - 18, 42 + offset), fill=EDGE, width=1)
    return canvas


def save_frame(image, path):
    image.convert("RGB").save(path, "PNG", optimize=True)


def main():
    frames = [
        clean_frame(),
        clean_frame(),
        ascii_frame(),
        ascii_frame(),
        particle_frame(11),
        particle_frame(23),
        particle_frame(37),
        wireframe_frame(),
        wireframe_frame(),
        clean_frame(),
        clean_frame(),
    ]
    fallback = clean_frame()
    save_frame(fallback, FALLBACK)
    indexed = [frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=96) for frame in frames]
    indexed[0].save(
        GIF,
        save_all=True,
        append_images=indexed[1:],
        duration=[900, 900, 1050, 1050, 800, 800, 800, 950, 950, 1000, 1000],
        loop=0,
        optimize=True,
        disposal=2,
    )
    print(f"GIF={GIF}")
    print(f"PNG={FALLBACK}")
    print(f"FRAMES={len(frames)}")
    print(f"GIF_BYTES={GIF.stat().st_size}")
    print(f"PNG_BYTES={FALLBACK.stat().st_size}")


if __name__ == "__main__":
    main()
