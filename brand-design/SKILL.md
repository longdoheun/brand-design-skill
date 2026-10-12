---
name: brand-design
description: "Create or refine brand logos and wordmarks from brand philosophies, geometric rules, and visual constraints. Use for reusable identity design and parameterized vector variations, not general UI styling."
---

# Brand Design

Turn the user's philosophy into a reproducible shape grammar, then refine its optical result. Geometry is the underlying logic; the delivered logo should read clearly without its construction diagram. No particular brand, letter, palette, font, or angle is the default.

## Inputs and scope

Accept ordinary language, existing assets, or a structured brief. Read [the brief contract](references/brief-contract.md) when translating the inputs. Extract the brand name, a few prioritized philosophies, requested geometric rules, intended placements/sizes, and things to preserve or avoid. Ask only for missing information that materially changes the direction. Record inferred values as assumptions; do not turn example values into universal requirements.

Separate hard constraints from adjustable starting points. A user-supplied mathematical rule remains a requirement unless they authorize changing it. Explain a legibility conflict with a concrete rendered alternative. Existing brand history, researched evidence, and new proposals must be labeled separately.

Distinguish the brand's benefit to its user from its delivery mechanisms. Prioritize the benefit in the brief; do not let a technology, visualization technique, or the brand's spelling dictate the primary philosophy.

## Philosophy → rule → form

1. Build a traceable mapping for each chosen direction: **philosophy → geometric operation → parameter → visible result → verification**. For example, continuity might use tangent joins, while multiple viewpoints might use transformations of one shared source curve. Do not merely attach meanings to an arbitrary finished shape.
2. Read [geometric construction](references/geometric-construction.md) for reference cases. Choose a small shape grammar, relational dimensions, and meaningful negative space. A grid must control actual coordinates. Neither a golden ratio nor a projection is mandatory. Use primary references when further research is needed; borrow principles, not proprietary marks.
3. Keep structural invariants separate from variant parameters. Variants should explore useful tradeoffs in expression, weight, openness, or viewpoint. The renderer's repeatable `--set NAME=EXPRESSION` overrides explore existing parameters without editing the source recipe; save each structural variation in a separate output directory. Changing only the brand text or color is not evidence of a new brand-specific design. Preserve recognition and hard constraints while varying the requested rules.
4. Use repo-native vectors when producing a logo. Read [the recipe contract](references/recipe-contract.md) for the bundled parameterized SVG renderer. It supports primitives, derived expressions, compound paths, and affine transforms; it is an execution helper, not an autonomous semantic designer. Unsupported geometry can use a scoped custom generator with equally explicit inputs and construction logic.
5. Inspect the silhouette in one color first. Check counters, joins, diagonal weight, alignment, and spacing at actual intended sizes. Keep optical corrections as named parameters with a reason. Do not silently violate hard constraints. An attractive diagram does not demonstrate a usable logo.
6. Design the complete signature, not a first-letter symbol in isolation. Compare the symbol with every letter's stroke, curve, counter, x-height, terminals, and spacing, then check the whole name within the product's visual language. Share a small grammar where it improves coherence; do not mechanically repeat the symbol's special detail in every glyph. Create wordmarks using licensed typefaces or original lettering; choose them from the brief rather than a bundled example. Deliver production SVGs with outlined type and no external resources. The generic renderer makes symbols and construction assets; wordmark layout and font outlining require a separate appropriate tool.

## Color decisions

Record why each color exists, not just its hexadecimal value. Start from the established product palette or the brief's context, choose a strategy (one color, accent plus neutral, or a justified multicolor system), and map each role to an element, source, intended hierarchy, and actual background. A symbol and name may share or differ in color; neither split lettering nor a colored initial is the default. If splitting them, explain what that distinction accomplishes and verify that the name still reads as one signature. Do not assign different colors to letters merely to decorate them or treat a hue as universal evidence of trust, health, or scientific rigor.

Keep palette roles consistent across variants. Check foreground/background contrast on the named surfaces and at the intended size; record the chosen review target separately from any applicable accessibility requirement. Inspect the monochrome variant so recognition and meaning do not depend on hue. Construction-guide colors are explanatory overlays, not additional brand colors. Read the [brief contract](references/brief-contract.md#color-policy) when recording these decisions.

## Output and verification

Save the normalized brief, source recipe/generator, resolved parameters and rationale, production assets, and a real rendered preview. Use only the requested formats and variants. Construction guides belong in a separate file, not in the finished signature.

Verify that another working directory can regenerate the same output, that parameter changes affect both production and construction geometry, and that applicable structural invariants hold. Then inspect actual rendered sizes and surfaces. Numeric checks do not prove perceptual quality or validate the proposed symbolism. Report unresolved mappings as unresolved; do not present them as implemented philosophy.

Do not deploy, alter application navigation, update app icons, or publish to a remote repository merely because logo design was requested. Perform those actions when authorized. State clearly whether the result is a study, a proposed identity, or an integrated asset.

## Example boundary

The companion repository's `examples/reprism/` is a worked data-guided training-support study with its brief, statistical design inputs, scoped geometry/lettering generator and rendered artifacts. It is **not** the generic template or a required dependency. The installed skill works without that folder. Its design inputs are authoritative; the exported renderer recipe contains flattened paths. Use the example only when relevant. Implemented geometry does not establish audience interpretation or product efficacy.
