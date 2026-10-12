"""Generate the geometric Reprism signature from bundled, licensed assets."""

import argparse
import math
import sys
from hashlib import sha256
from pathlib import Path
from xml.etree import ElementTree as ET

if sys.version_info < (3, 10):
    raise SystemExit("Use Python 3.10 or newer with build-time fonttools==4.65.0.")

try:
    from fontTools.ttLib import TTFont
    from fontTools.varLib.instancer import instantiateVariableFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.pens.boundsPen import BoundsPen
except ImportError:
    raise SystemExit("Install build-time fonttools==4.65.0 in an isolated Python environment.")


SKILL = Path(__file__).resolve().parents[1]
FONT = SKILL / "assets/fonts/Manrope.ttf"
FONT_HASH = "3ae11c49db0455a3cc33e37d380f20fdb8c7f8b41dc07625c177e3d87a9d6ae6"


def number(value):
    return f"{value:.3f}".rstrip("0").rstrip(".")


def mark(color, dot):
    # u=6: cap=12u, stem=2u, outer radius=4u, inner radius=2u.
    bowl = "M0 0H24A24 24 0 0 1 24 48H12V72H0Z M12 12V36H24A12 12 0 0 0 24 12Z"
    # A 12-unit-wide band follows the 45-degree line from (24,42) to (48,66).
    offset = 6 / math.sqrt(2)
    corners = [(24-offset, 42+offset), (24+offset, 42-offset),
               (48+offset, 66-offset), (48-offset, 66+offset)]
    leg = "M" + "L".join(f"{number(x)} {number(y)}" for x, y in corners) + "Z"
    return (
        f'<g fill="{color}"><path fill-rule="evenodd" d="{bowl}"/>'
        f'<path d="{leg}"/><path d="M54 54V72H36Z"/></g>'
        f'<circle cx="6" cy="6" r="3" fill="{dot}"/>'
    )


def svg(content, width, height, description):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {number(width)} {height}" '
        'role="img" aria-labelledby="title desc">\n'
        '<title id="title">Reprism</title>\n'
        f'<desc id="desc">{description}</desc>\n{content}\n</svg>\n'
    )


def construction():
    return svg(
        '<defs><pattern id="grid" x="120" y="60" width="19.8" height="19.8" patternUnits="userSpaceOnUse">'
        '<path d="M19.8 0H0V19.8" fill="none" stroke="#26313B" stroke-width=".6"/>'
        '</pattern></defs><rect width="560" height="360" fill="#12171D"/>'
        '<rect x="100" y="40" width="224" height="280" fill="url(#grid)"/>'
        '<g transform="translate(120 60) scale(3.3)">'
        + mark("#66E2A6", "#F4FFF9") +
        '<g fill="none" stroke="#83CDE9" stroke-width=".3" stroke-dasharray="1 1">'
        '<circle cx="24" cy="24" r="24"/><circle cx="24" cy="24" r="12"/>'
        '<path d="M0 0H60M0 72H60M24 42L54 72M24 -6V78"/></g></g>'
        '<g fill="#F4F7F6" font-family="system-ui,sans-serif" font-size="13">'
        '<text x="350" y="105">u = 6</text><text x="350" y="141">Cap height = 12u</text>'
        '<text x="350" y="177">Stem = 2u</text><text x="350" y="213">Radii = 4u / 2u</text>'
        '<text x="350" y="249">Leg = 45°</text><text x="350" y="285">Arrow = 3u</text>'
        '</g>', 560, 360, "Construction grid: circular bowl, constant thickness, 45-degree leg"
    )


def generate(output):
    if sha256(FONT.read_bytes()).hexdigest() != FONT_HASH:
        raise SystemExit("Bundled font differs from its documented SHA-256; review the source first.")
    font = instantiateVariableFont(TTFont(FONT), {"wght": 700})
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    scale = 72 / 1440
    cursor = 54 + 6
    paths = []
    max_x = 0
    for letter in "eprism":
        glyph = glyphs[cmap[ord(letter)]]
        bounds = BoundsPen(glyphs)
        glyph.draw(bounds)
        origin = cursor - (bounds.bounds[0] * scale if letter == "e" else 0)
        pen = SVGPathPen(glyphs, ntos=number)
        glyph.draw(TransformPen(pen, (scale, 0, 0, -scale, origin + 2, 74)))
        paths.append(f'<path d="{pen.getCommands()}"/>')
        max_x = max(max_x, origin + bounds.bounds[2] * scale + 2)
        cursor += glyph.width * scale - 1
    variants = {
        "": ("#66E2A6", "#F4F7F6", "#F4FFF9"),
        "-light": ("#147A55", "#172129", "#172129"),
        "-mono": ("#172129",) * 3,
        "-mono-inverse": ("#F4F7F6",) * 3,
    }
    output.mkdir(parents=True, exist_ok=True)
    files = {}
    for suffix, (color, ink, dot) in variants.items():
        content = '<g transform="translate(2 2)">' + mark(color, dot) + '</g>'
        files[f"reprism-symbol{suffix}.svg"] = svg(content, 58, 76, "Geometric repetition-arrow R")
        content += f'<g fill="{ink}">{"".join(paths)}</g>'
        files[f"reprism-wordmark{suffix}.svg"] = svg(content, max_x + 2, 100,
                                                   "Geometric R and outlined Reprism wordmark")
    files["reprism-construction.svg"] = construction()
    for filename, content in files.items():
        ET.fromstring(content)
        (output / filename).write_text(content, encoding="utf-8")
        print(f"{filename}: {len(content.encode())} bytes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=SKILL / "assets/logos")
    args = parser.parse_args()
    generate(args.output.resolve())
