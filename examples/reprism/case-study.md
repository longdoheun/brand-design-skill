# Reprism — shared-axis projection

Reprism is an exercise motion-tracking and replay application. This proposed web signature expresses **one movement, observed from different viewpoints** through two related faces of a single R source. A controlled negative seam distinguishes the faces without relying on color. It is a logo design study, not exercise simulation or evidence of audience interpretation.

## From philosophy to geometry

| Intent                                 | Implemented operation                                      | Visible effect                                                        |
| -------------------------------------- | ---------------------------------------------------------- | --------------------------------------------------------------------- |
| Observe the same movement consistently | Reuse one parameterized R source for both faces            | A recognizable letter with a common geometric origin                  |
| Read a movement from different views   | Project one face of the source around a shared, fixed axis | A subtly foreshortened upper rim and counter                          |
| Make the relationship understandable   | Keep a measured negative seam between faces                | A clean distinction that remains visible in single-color reproduction |

The construction has no attached arrowhead or start-point dot. Mint and the Reprism spelling remain continuous with the application's existing identity. The previous baseline is preserved in `archive/v2/`.

## Source model

All source dimensions derive from `u=6`:

- Cap height `12u=72` and stem/diagonal weight `2u=12`.
- Circular bowl radius `4u=24`, centered at `(24,24)`; counter radius `24−12=12`.
- Diagonal band follows a 45° direction. Its corners use the perpendicular offset `w/(2√2)`, preserving the source weight rather than matching horizontal bounding-box widths.
- Circular arcs are sampled with 256 segments per semicircle. The maximum source sagitta is below 0.0005 source units; topology-preserving export simplification uses a separate 0.008-unit tolerance.

The finished projected strokes intentionally foreshorten. Equal weight is a property of the source plane, not a claim that every projected section retains the same visible width.

## Shared-axis projection

Let the axis through the bowl center have unit direction `v`, and perpendicular direction `n`. Orthographic projection of a plane folded by angle `θ` around that axis is:

```text
T = v vᵀ + cos(θ) n nᵀ
p′ = c + T (p − c)
```

The selected axis is −22°, and the fold is 42°. Every point `c+t·v` stays fixed, while displacement along `n` is multiplied by `cos(42°)`. This is a projection of a planar design surface, not a perspective camera model.

The lower face comes from the source; the upper face comes from the projected copy of that same source. They are clipped to opposite half-planes with a symmetric gap of `0.6u=3.6` along `n`. The gap is actual negative geometry, rather than a colored line placed over the logo. The counter changes with the projection because it belongs to the transformed source.

The result is normalized once to a 72-unit cap height; both faces and their gap receive the same scale. The nominal gap is approximately **1.086 CSS px at a 28px wordmark height**, and **1.241px at 32px**. Actual antialiasing depends on display scale and rendering. Browser review complements these geometric measurements.

## Optical selection

Three fold angles—30°, 42°, and 54°—were rendered with the complete wordmark. The middle option retains more of the counter than the strong fold while making the change in the upper face visible. The −22° axis creates a rising seam without competing with the R leg. These are project-specific visual choices, not universal ideal angles.

The face gap was enlarged to 3.6 units so its nominal clearance exceeds 1px at the smallest intended header size. The symbol's cap height is aligned with the lettering rather than the source plane's unprojected top edge. A 6-unit R/e gap and −1-unit tracking provide an initial optical balance; both are named parameters.

## Typography and surfaces

The remaining `eprism` letters use outlined Manrope at weight 700. The R is the first letter; a second capital R or a boxed app icon is not placed before it. Typeface choice is documented rather than claimed as original lettering.

| Variant        | Front face | Folded face | Type      |
| -------------- | ---------- | ----------- | --------- |
| Primary / dark | `#66E2A6`  | `#91EDBF`   | `#F4F7F6` |
| Light          | `#147A55`  | `#327E60`   | `#172129` |
| Mono           | `#172129`  | `#172129`   | `#172129` |
| Inverse        | `#F4F7F6`  | `#F4F7F6`   | `#F4F7F6` |

Deliverables have transparent backgrounds and outlined production typography. The recommended full wordmark height is 32px; 28px and 40px are also reviewed. Reserve approximately half the cap height as external clearspace. Existing app icons and application navigation are outside this example.

## Reproduce and inspect

`design.json` is the authoritative parameter source. `brief.json` records intent and constraints. `scripts/generate_projection.py` performs the projection, clipping, Boolean operations, font outlining, and exports:

- Production symbols and wordmarks in four palettes.
- Source, projected-view, and construction SVGs.
- `render-recipe.json`, a flattened recipe usable by the shared SVG renderer.
- `geometry-evidence.json`, with the projection matrix, clearance, approximation tolerances, source hashes, and dimensions.
- `reprism-resolved.json`, with the implemented geometry mappings. These statuses do not assert a validated audience response.

To vary the fold or source dimensions, rerun the example builder using an edited design file or `--fold`; editing the flattened recipe's numeric metadata does not recompute its Boolean paths. Install the pinned build-time dependencies in `requirements.txt`. Source fonts and their license remain in `assets/fonts/`.

The numerical tests verify the fixed axis, normal foreshortening, two valid faces, seam clearance, parameter effects, and byte-identical regeneration. The rendered preview shows the complete signature on dark/light surfaces and at header sizes.

## Design references

[Google's identity construction case](https://design.google/library/evolving-google-identity) informs geometry followed by optical review. [Pentagram's MIT Media Lab case](https://www.pentagram.com/work/mit-media-lab) informs common-source shape grammar. [IBM's logo guidance](https://www.ibm.com/design/language/ibm-logos/8-bar/) informs spacing and surface-aware review. [Linear's brand guidelines](https://linear.app/brand) inform compact-symbol versus wordmark use. These sources do not prescribe Reprism's particular shape or measurements.
