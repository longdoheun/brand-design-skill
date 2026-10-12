# Reprism identity and reference decisions

## Observed starting point

The existing Reprism app mark names its symbol “A flowing R-shaped repetition arrow.” It has a rounded mint R, an open bowl, a diagonal arrow, a white starting dot, and a dark rounded-square app mask. The application uses `#66E2A6`, `#F4F7F6`, and dark surfaces. Its tagline is “See every rep clearly.” No prior formal identity manual was found. The app tile remains a separate asset; the current web proposal refines the R geometry rather than changing the app icon.

The new interpretation is **a repetition made visible**: the R conveys movement; the start point and clear wordmark support readable tracking. This is a proposed Reprism rationale, not a claim about the original designer's intent. Avoid literal dumbbells, anatomy illustrations, and a rainbow prism within the signature.

## Primary references reviewed on 2026-10-12

| Source | Principle applied to Reprism | Boundary |
| --- | --- | --- |
| [Linear Brand Guidelines](https://linear.app/brand) | Separate wordmark use from compact icon use; leave breathing room; retain one exact brand spelling. | Do not copy its symbol or proprietary lettering. |
| [IBM Design Language: 8-bar](https://www.ibm.com/design/language/ibm-logos/8-bar/) | Judge light/dark weight optically and align using meaningful letter geometry; define clearspace. | IBM's stripe ratios and minimum dimensions are specific to IBM. |
| [Manrope official source](https://github.com/google/fonts/tree/main/ofl/manrope) and [license](https://github.com/google/fonts/blob/main/ofl/manrope/OFL.txt) | Use a documented open-source geometric sans; preserve the license and font provenance. | Manrope is the source typeface, not custom lettering claimed as original. |
| [Google's geometric construction case](https://design.google/library/evolving-google-identity) and [Pentagram's MIT Media Lab grid](https://www.pentagram.com/work/mit-media-lab) | Build a coherent shape grammar and inspect its optical result. | No borrowed glyphs or claim that mathematical purity guarantees quality. |

These are design references, not affiliation or endorsement. Reprism's ratios, colors, and layout choices below are project decisions.

## Full-wordmark construction

- Use base unit `u=6`. The cap height is `12u=72`, stem width `2u=12`, bowl center `(4u,4u)=(24,24)`, and concentric radii `4u=24` / `2u=12`. A 45° band of width `2u` joins an integrated right-triangle arrowhead of side `3u=18`. Its tip is `(9u,12u)=(54,72)`.
- The point is a circle of radius `0.5u=3`, centered at `(u,u)=(6,6)`. All web R elements are filled shapes; no mismatched rounded stroke caps are attached at the leg. Single-color variants keep a continuous silhouette.
- Follow it with outlined Manrope `eprism`, weight 700. Typography scale is 0.05 (1440-unit cap height → 72). Use a 6-unit optical gap after the R and -1-unit tracking between the remaining glyph advances.
- Include the p descender and i dot in the viewBox rather than clipping to the cap height. Add a 2-unit internal safety inset.
- Keep the SVG transparent. Application layout supplies padding and background.
- Header recommendation: 32 CSS px full artwork height; 28 minimum, 40 for more spacious headers. These are practical tested choices, not industry-wide standards. External clearspace: at least 0.5× cap height on each side.

| Variant | R / arrow | Type | Start point | Intended surface |
| --- | --- | --- | --- | --- |
| Primary | `#66E2A6` / same | `#F4F7F6` | `#F4FFF9` | Dark |
| Light | `#147A55` / same | `#172129` | `#172129` | Light |
| Mono | `#172129` | same | same | Light / print |
| Inverse | `#F4F7F6` | same | same | Dark |

## Source and reproducibility

The self-contained package stores `assets/fonts/Manrope.ttf`, its OFL and FONTLOG, and a SHA-256 source record. `scripts/generate_wordmark.py` instantiates the variable font at 700 and exports glyph paths, symbols, and a construction diagram to `assets/logos/` or an explicit destination. Paths are resolved relative to the script, so it works from any working directory. Python 3.10+ and FontTools 4.65.0 are required only for generation; delivered SVGs require no font loading or network access.

`assets/logos/reprism-construction.svg` shows the actual geometric scaffold. The wordmarks and symbols beside it are production files without guides. The construction SVG includes labels; the production signatures contain only vector paths and shapes.

Avoid stretching, compressing, arbitrary letter-spacing changes, cropping the descender, placing the dark app square behind the web signature, or introducing another R before the signature. Ensure an embedded image has an accessible `alt="Reprism"`; decorative duplicates should have empty alt text.
