# Reprism — reference, record, refine

Reprism supports exercise decisions through measured movement, accumulated records, and interpretable statistical feedback. Tracking and 3D replay are tools for that purpose. The signature expresses **a stable reference supporting a record that can be compared and refined**.

The numerical observations are illustrative normalized design values. They are not user records, exercise prescriptions, or evidence of training effectiveness. The geometry implements a brand metaphor; audience interpretation still needs visual judgment.

## Philosophy → construction

| Brand intent                    | Actual construction rule                                              | Visible result                                                                              |
| ------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Support the person's training   | Keep a stable outer R regardless of record values or statistical gain | An enclosing frame and a steady vertical anchor                                             |
| Learn from accumulated evidence | Compute an exponential moving average before drawing the record trace | One continuous inner curve derived from multiple observations                               |
| Connect evidence to adjustment  | Position the inner curve by its deviation from a fixed target         | A target-relative record that approaches the reference as the illustrative summary improves |

The direction replaces a viewpoint-focused metaphor with data-informed exercise support. Earlier geometric and projection studies are preserved under `archive/`.

## Reference geometry

The base unit is `u=3`. Cap height is `24u=72`, outer circular radius is `9u=27`, and reference weight is `3u=9`. The internal boundary radius is `27−9=18`.

The diagonal uses a true perpendicular offset of half the reference weight. Its angle follows the chosen endpoints rather than an arbitrary 45° constraint. The source model stays unchanged when observations or smoothing gain vary. The reference is painted over its joining record links, preserving the visual frame as well as its geometry.

## Statistical construction

The illustrative observations are deviations `[4, 2, 1, 0.5]`. With smoothing gain `α=0.5`:

```text
z₀ = d₀
zₖ = (1 − α) zₖ₋₁ + α dₖ
z = [4, 3, 2, 1.25]
```

This is an exponential moving average. It records accumulation explicitly rather than assuming that a single latest value represents the trend. The gain is a design parameter, not a recommended exercise adjustment rate.

The target radius is derived from the available counter and the required visual separation:

```text
r* = counter radius − minimum gap − record weight / 2
r* = 18 − 4 − 2 = 12
```

The summary values determine the record radii `[8, 9, 10, 10.75]` using `rₖ = r* − zₖ`. Between records, a bounded smoothstep interpolates the deviation. For phase `t`:

```text
C(t) = (cx, cy) + (r* − z(t)) · (cos(−π/2 + πt), sin(−π/2 + πt))
smoothstep(f) = 3f² − 2f³
```

Endpoint-flat interpolation makes the arc tangent to its horizontal joining links and avoids abrupt direction changes at record boundaries. The trace's constant-width band is generated around this curve. Both links join the reference spine, producing one connected R with two readable counters. More adverse observation values can move the trace away from the target; the model does not manufacture improvement irrespective of its inputs.

## Optical constraints

The record weight is `4` source units: approximately **1.12 CSS px** at a 28px full wordmark height. The selected curved-lane clearance is approximately **5.25 units / 1.47px** at that size. These measurements concern the curved region; the joining links intentionally meet the reference spine.

The target itself stays out of production artwork. Guides and sample markers appear only in the construction assets. The diagram is evidence of the actual source model, not a decorative grid over a finished drawing.

Circular arcs and the record curve are sampled at 384 steps; export simplification is bounded by a 0.006-unit parameter. Real browser inspection checks dark/light surfaces, monochrome, and 28/32/40px header sizes. Geometry tests alone do not prove aesthetic quality.

## One wordmark, one construction system

The complete `Reprism` signature uses original geometric lettering. It is not a custom R placed next to an unrelated stock typeface. Its shared grammar is explicit:

| Relationship | Construction | Purpose |
| --- | --- | --- |
| R → e → p | The same 27-unit circular bowl and 18-unit inner radius; p carries the shared circular bowl on a continuous upright | Carry recognition across the name rather than isolating it in the initial |
| All letters | A 9-unit construction stroke | A consistent visual weight |
| Lowercase height | `x-height = 2 × bowl radius = 54` against a 72-unit capital | Relate the lowercase proportions to the symbol's real circle |
| r → m | 18-unit outer arches, with 9-unit counters | Extend the curve grammar without forcing every letter into a full circle |
| i | A 9-unit stem and circular 9-unit dot | Keep small forms on the same dimensional system |
| s | Tangent-continuous cubic transitions and a width of 49 units | Preserve a readable letter where a literal circle recipe would become awkward |
| Optical fit | 0.75-unit overshoot for e and s; width/height fitting of s and vertical fitting of e | Match the perceived baseline and height of curved and flat forms |
| Spacing | Re: 5.25 units; pr: 6 units; ep/ri/is/sm: 5 units, all expressed relative to the base unit | Balance each adjacent pair rather than apply uniform tracking |

The construction stroke is shared; optical fitting slightly changes the final weights of e and s. These adjustments are disclosed rather than described as perfectly uniform geometry. The p extends 24 units below the baseline. The i dot ends 9 units above the lowercase stems.

The statistical trace remains distinctive to R. Repeating it in every letter would crowd the name and make the word harder to read. The other letters carry the relationship through their construction, not through repeated decoration. `generated/reprism-lettering.svg` overlays the real letterforms with the shared metrics and source bowl circles.

## Relationship to the product

The signature preserves the application's mint (`#66E2A6`), warm white (`#F4F7F6`), and dark (`#0B0E12`) palette. Its restrained geometric forms support an interface containing anatomical models, exercise controls, and quantitative records. The logo establishes identity while the model and workout information remain the main content. The identity is applied in the companion Reprism application. The asset preview does not constitute a usability study.

The benefit remains exercise assistance informed by evidence. The 3D renderer and motion tracker support that benefit; neither becomes the sole meaning of the brand. All production SVGs are transparent, outlined, and self-contained.

## Production color strategy

The production signature uses one foreground across R, its record trace, and all of `eprism`. The earlier accent-R/neutral-name study separated the initial visually; the production revision makes the complete name one identifier at compact header sizes. This is a deliberate design choice, not a claim that every brand must use one color.

| Surface | Reference, record, and lettering | Reason |
| --- | --- | --- |
| Dark `#0B0E12` | `#66E2A6` | Reuse the product's established mint across the complete name |
| Light `#F4F7F6` | `#147A55` | Adapt the foreground for contrast instead of carrying pale mint onto a light surface |
| One-ink reproduction | `#172129` | Keep the structure recognizable without color variation |
| Inverse | `#F4F7F6` | Provide a quiet neutral signature on dark surfaces |

The internal record remains distinct through its actual negative-space lane, rather than a second tint. `design.json.color_policy` records the palette source, roles, reasons, surfaces, and review criteria; `variants` provides executable production colors. Green is selected from the existing product palette, not as universal evidence of scientific rigor.

The project's foreground/background design target is 4.5:1; mint on the selected dark surface measures approximately 11.97:1, and dark green on the selected light surface 4.94:1. These are nominal solid-color measurements using the [W3C contrast method](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), not proof of aesthetic quality or a blanket accessibility certification. W3C exempts logotypes from ordinary text thresholds. Blue guides and white lettering in construction overlays are explanatory and do not add production palette roles.

## Applied revision

The R's leg endpoint moves from 63 to 54 units; its angle follows the actual endpoints, making the capital less wide relative to the lowercase bowls. The p uses a circular counter, preserving the shared radius while making the lowercase form less rigid. The first pair's clear gap is 5.25 units; the other pair-specific gaps remain unchanged.

The application uses the full signature in its header, authentication screens, and launch splash. The installed icon and favicon use the same R, centered on a flat dark square. Icon artwork fits inside the central maskable-safe region; raster outputs are opaque PNGs at 192, 512, and 180 pixels. Small screens keep the wordmark visible while navigation moves to its own row. This revision is intended for application use; the earlier studies remain available in repository history.

## Reproduction

- `brief.json` records purpose, philosophies, and constraints.
- `design.json` provides source dimensions, observations, smoothing gain, and palettes.
- `scripts/generate_calibration.py` computes reference and record geometry.
- `scripts/identity_output.py` shares vector export and complete signature layout.
- `scripts/lettering.py` constructs the six original lowercase letterforms from shared modules and optical parameters.
- `generated/geometry-evidence.json` records observations, statistical summaries, gap measurements, dimensions, and source hashes.
- `generated/render-recipe.json` replays the flattened assets through the general renderer. Rerun the example builder to change the underlying statistics.
- `preview.html` opens the standalone asset board using relative local paths.

Install the pinned requirements from `requirements.txt` in a virtual environment, then run the example builder. `--alpha` varies smoothing without changing the reference. Tests cover independently calculated summaries, target-relative geometry, frame invariance, real clearance, readable letter counters, connected arches, non-overlapping pair spacing, scale covariance, valid vector delivery, and repeatable output.

## References and attribution

[Google's geometric identity case](https://design.google/library/evolving-google-identity), [Pentagram's MIT Media Lab identity](https://www.pentagram.com/work/mit-media-lab), and [IBM's logo guidance](https://www.ibm.com/design/language/ibm-logos/8-bar/) inform construction and optical review. They do not prescribe this symbol or establish its exercise efficacy. Earlier studies used Manrope; its source, license, and provenance remain in `assets/fonts/` for those archived assets. The current original lettering does not require that font.
