# Reprism — reference, record, refine

Reprism supports exercise decisions through measured movement, accumulated records, and interpretable statistical feedback. Tracking and 3D replay are tools for that purpose. This proposed signature expresses **a stable reference supporting a record that can be compared and refined**.

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

## Wordmark and surfaces

The R is the first letter of `Reprism`; the remaining letters use outlined Manrope 700. The 6-unit R/e gap and −1-unit tracking are named spacing choices. All production SVGs are transparent and self-contained.

| Surface | Reference | Record    | Type      |
| ------- | --------- | --------- | --------- |
| Dark    | `#66E2A6` | `#91EDBF` | `#F4F7F6` |
| Light   | `#147A55` | `#327E60` | `#172129` |
| Mono    | `#172129` | `#172129` | `#172129` |
| Inverse | `#F4F7F6` | `#F4F7F6` | `#F4F7F6` |

These colors and ratios belong to this brand example, not the generic skill. Existing app icons and application navigation are separate integration work.

## Reproduction

- `brief.json` records purpose, philosophies, and constraints.
- `design.json` provides source dimensions, observations, smoothing gain, and palettes.
- `scripts/generate_calibration.py` computes reference and record geometry.
- `scripts/identity_output.py` shares vector export and licensed typography handling.
- `generated/geometry-evidence.json` records observations, statistical summaries, gap measurements, dimensions, and source hashes.
- `generated/render-recipe.json` replays the flattened assets through the general renderer. Rerun the example builder to change the underlying statistics.
- `preview.html` opens the standalone asset board using relative local paths.

Install the pinned requirements from `requirements.txt` in a virtual environment, then run the example builder. `--alpha` varies smoothing without changing the reference. Tests cover independently calculated summaries, target-relative geometry, frame invariance, real clearance, topology, valid vector delivery, and repeatable output.

## References and attribution

[Google's geometric identity case](https://design.google/library/evolving-google-identity), [Pentagram's MIT Media Lab identity](https://www.pentagram.com/work/mit-media-lab), and [IBM's logo guidance](https://www.ibm.com/design/language/ibm-logos/8-bar/) inform construction and optical review. They do not prescribe this symbol or establish its exercise efficacy. Manrope's source, license, and provenance remain in `assets/fonts/`.
