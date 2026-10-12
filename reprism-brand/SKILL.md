---
name: reprism-brand
description: "Design or revise Reprism logos, geometric symbols, wordmarks, and header branding with a consistent identity. Use for Reprism brand work, not general exercise UI changes."
---

# Reprism Brand

Read [the identity reference](references/identity.md) before changing brand geometry. For geometric reconstruction, read [construction principles and cases](references/geometric-construction.md). This package includes its own font, generator, and output assets; it does not require a particular project path. When integrating into an app, inspect that project's current branding and conventions first.

## Identity decisions

- Spell the brand `Reprism`. In the full wordmark, the repetition-arrow **R is the first letter**, followed by `eprism`; avoid repeating an app tile and another capital R.
- Retain a recognizable R and directional repetition motif. The current web proposal uses circular arcs, a constant-width stem, and a 45° leg with an integrated arrowhead. Earlier rounded-stroke geometry is revisable; do not freeze an obsolete path against explicit user feedback.
- Use transparent artwork for web headers. Keep the rounded dark tile for app icons. Do not bake a backdrop, glow, bevel, slogan, or navigation into the wordmark.
- Use mint `#66E2A6` with near-white `#F4F7F6` on dark surfaces. The light variant uses dark text and darker green for legibility. Maintain monochrome versions. Do not infer a rainbow palette from the name.
- The initial outlined typography is Manrope Bold (700). Preserve its license and source record when regenerating; never replace SVG outlines with runtime system-font text.

## Production workflow

1. Inspect `assets/logos/` and the destination project's branding. Prefer revising the canonical vector over generating raster art. App icons are separate deliverables and need not change when a header wordmark changes.
2. Run `python scripts/generate_wordmark.py --output /chosen/output/directory` from the skill folder, or pass an absolute script path from another directory. Without `--output`, it regenerates `assets/logos/`. It uses the bundled licensed font, with no network requests. Python 3.10+ and FontTools 4.65.0 are build-time tooling only; use a temporary environment if unavailable. Do not add them to web application dependencies.
3. Keep the R and lettering optically balanced. Use the reference's current dimensions as a baseline, not an immutable geometric law. Generate a construction diagram from the same dimensions as the production paths. Adjust spacing only after inspecting the actual rendering.
4. Check dark, light, monochrome, and inverse variants at 28, 32, and 40 CSS px in a real browser. Check small counters, the R/e gap, start-point dot, baseline, and clipping. Reserve at least half the cap height around the artwork; keep it away from account/settings controls.
5. Validate SVG XML, confirm there are no external resources or `<text>` elements, and preview the exact delivered assets. Run the skill validator when changing this package.
6. Distinguish asset design from application layout. A placement mock does not mean the live header was changed. Report what was actually integrated, with a preview and source links.

When researching further, use original brand guidelines and font sources. Borrow principles such as optical correction and clearspace, not another brand's shapes, proprietary font, or brand-specific numeric rules.
