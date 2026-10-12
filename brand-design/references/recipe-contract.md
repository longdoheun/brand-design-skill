# Parameterized vector recipe

`scripts/render_geometry.py --brief brief.json --recipe recipe.json --output output/` uses Python 3.10+ and the standard library. No font, network access, web runtime, or example project is required.

Use repeatable `--set NAME=EXPRESSION` arguments to explore existing parameters without modifying the source recipe, e.g. `--set angle=15 --output explorations/view-15/` for a recipe with an adjustable `angle`. Structural variants should have separate output directories. Unknown parameters fail, and overrides are recorded in the resolved manifest. The renderer cannot interpret natural-language hard constraints; check that an override is allowed by the brief before using it.

## Fields

- `version`: currently `1`.
- `parameters`: numeric values or arithmetic expressions referring to other parameters. Resolution is order-independent; unknown names and cycles fail. Allowed operations: `+ - * / **`, unary signs, `sqrt`, `sin`, `cos`, `radians`, and `pi`. Coordinates use SVG's downward-positive y axis. Formulas describe the design, not physical simulation.
- `view_box`: `[x, y, width, height]`, with positive dimensions. Numeric expressions are allowed. Include safety space; the renderer does not calculate or fix clipping for arbitrary paths.
- `construction_view_box`: optional bounds for guides that extend beyond the finished silhouette. This changes only the diagram viewport, not the shared coordinates or production viewport.
- `variants`: named palettes with `#RRGGBB` values. Shape colors use `@palette_key`, or `none`. Each variant must provide the referenced colors.
- `shapes`: production geometry. Nodes have `tag`, `attrs`, optional `transform`, and, for `g`, `children`. Supported tags: `g`, `path`, `rect`, `circle`, `ellipse`, `line`, `polygon`, `polyline`. Unused SVG features, scripts, arbitrary XML, text, and external resources are rejected.
- `guides`: construction geometry in the same coordinate system and parameter namespace. Use `@guide` for its color. Production files omit it. The construction file shows production geometry plus these actual guides; its palette is separate from the exported variants.
- `rationale`: entries with `philosophy` (an ID from the brief), `rule`, `parameters`, `observable_result`, `check`, and `status` (`implemented` or `pending`). Semantic attribution is authored by the designer, not inferred by the renderer. Philosophies with no entry remain unresolved in the output manifest.

## Expressions and transformations

Numeric attributes accept a number or an expression string. In `d` and `points`, write expressions in braces, e.g. `M {cx} {cy-r} A {r} {r} 0 0 1 {cx} {cy+r}`. Font outlines can be added as ordinary paths by a separate licensed outlining tool.

Transforms are a list of operations, applied with SVG transform-list semantics:

```json
{
  "tag": "g",
  "transform": [
    { "translate": ["origin_x", "origin_y"] },
    { "rotate": ["angle_deg", "cx", "cy"] }
  ],
  "children": [
    {
      "tag": "circle",
      "attrs": { "cx": "cx", "cy": "cy", "r": "radius", "fill": "@ink" }
    }
  ]
}
```

Allowed transforms: `translate` (2 args), `scale` (1 or 2), `rotate` (1 or 3), `matrix` (6). A matrix can express a designer-chosen affine projection; the helper does not implement 3D modeling. Use compound paths with `fill-rule: evenodd` for negative-space subtraction, or generate boolean geometry with an appropriate external vector tool. Arbitrary shape booleans, collision solving, kerning, and automatic logo aesthetics are outside this helper.

## Outputs and useful checks

Outputs are `<slug>-symbol-<variant>.svg`, `<slug>-construction.svg`, and `<slug>-resolved.json`. The last includes the brief, evaluated parameters, explicit overrides, effective recipe SHA-256, and unresolved philosophy IDs. The diagram and silhouette use the same shape builder.

Verify a changed primitive also changes its guide; preserve specified tangent relationships and constant widths in the source model. Render at intended sizes to catch clipping, a filled-in counter, optical imbalance, and unreadable spacing. Keep optical compensation as a named variable instead of hiding it in an unexplained path edit. Reject unsupported data rather than silently ignoring it.
