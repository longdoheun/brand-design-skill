# Brand Design Skill

A Codex skill for developing vector logos from brand philosophy, geometric constraints, and practical usage requirements.

The workflow connects **intent → geometric operation → parameters → visual result → verification**. It helps keep construction logic reproducible while leaving room for optical judgment. No brand name, letter, palette, typeface, or proportion is built into the general workflow.

## What is included

- **[Design skill](brand-design/SKILL.md):** guidance for turning a brief into a shape grammar, exploring variations, and reviewing the result.
- **[Brief format](brand-design/references/brief-contract.md):** how to separate philosophies, hard constraints, exploratory rules, and assumptions.
- **[Geometry renderer](brand-design/scripts/render_geometry.py):** a dependency-free Python tool for parameterized SVG primitives, compound paths, affine transformations, and construction guides.
- **[Recipe format](brand-design/references/recipe-contract.md):** supported expressions, shapes, palettes, and recorded rationale.
- **[Reprism example](examples/reprism/case-study.md):** a complete worked design study with source parameters, a Boolean geometry extension, outlined typography, and generated assets.

## Install in Codex

Clone this repository and copy the `brand-design` directory into your user skills directory: `$CODEX_HOME/skills` if configured, otherwise `~/.codex/skills`.

```sh
git clone https://github.com/longdoheun/brand-design-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R brand-design-skill/brand-design "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Invoke it as `$brand-design`. The installed skill does not depend on the example directory. When updating an existing installation, replace the installed skill with the latest version rather than mixing files from different versions.

## Start a design

Provide a short brief in ordinary language; structured JSON is optional. Include the brand name, a few design philosophies, geometric rules, and intended applications. Existing assets and things to preserve or avoid are useful when revising a brand.

```text
$brand-design
Brand: A new learning platform
Philosophies: Curiosity, gradual discovery, calm confidence
Rules: Use a shared grid and meaningful negative space
Application: A 32px web header, on light and dark surfaces
Avoid: Book and lightbulb pictograms
Explore: An open form and a more compact form, with an outlined wordmark
```

The skill guides the design reasoning. The renderer executes an explicit geometry recipe; it does not infer symbolism or judge aesthetic quality automatically.

## Generate and vary geometry

The general renderer requires **Python 3.10+**, with no additional packages or network access. Supply your own brief and recipe:

```sh
python brand-design/scripts/render_geometry.py \
  --brief path/to/brief.json \
  --recipe path/to/recipe.json \
  --output output/base
```

Use repeatable `--set NAME=EXPRESSION` arguments to vary existing adjustable parameters. For example, a recipe with an `angle` parameter can be explored with `--set angle=15 --output output/view-15`. Check the brief's hard constraints before changing a parameter.

Outputs include palette variants, a separate construction SVG, and a JSON manifest of resolved parameters and philosophy mappings. Mappings that are missing or pending remain explicitly unresolved. Rendered inspection is still necessary to assess counters, clipping, optical weight, and small-size legibility.

## Reprism: shared-axis projection

Reprism is a worked example of an exercise motion-tracking and replay brand. Its symbol derives two views of the **same R source**, joined around a shared axis. An orthographic fold changes the upper counter and rim, while a controlled negative seam keeps the views distinct in monochrome. The finished signature contains no construction guides, attached arrow, or start-point decoration.

![Reprism shared-axis projection wordmark](examples/reprism/preview.png)

See the [case study](examples/reprism/case-study.md), [design parameters](examples/reprism/design.json), and [generated SVGs](examples/reprism/generated/). The previous geometric baseline is preserved in `examples/reprism/archive/v2/`.

This example uses Boolean geometry and font outlining beyond the general renderer. To reproduce it, install its build-time requirements in a virtual environment:

```sh
python -m venv .venv
.venv/bin/python -m pip install -r examples/reprism/requirements.txt
.venv/bin/python examples/reprism/scripts/generate_projection.py \
  --output output/reprism
```

`--fold 30` or `--fold 54` explores another viewpoint. Use this example generator to change the fold: its exported `render-recipe.json` is flattened geometry for the general renderer, not the authoritative Boolean source. The example's font, colors, proportions, and construction are project-specific choices.

## Verify

Run the general renderer's tests with:

```sh
python -m unittest discover -s brand-design/scripts -p 'test_*.py'
```

The Reprism example also includes geometry checks for its fixed axis, foreshortening, topology, clearance, and reproducibility. With its build-time requirements installed, run:

```sh
.venv/bin/python -m unittest discover -s examples/reprism/scripts -p 'test_*.py'
```

These checks verify construction properties; they do not establish how an audience interprets the logo. The example is a proposed identity asset, not an application deployment.

## References and font attribution

The skill's [construction reference](brand-design/references/geometric-construction.md) links to primary design cases from Google, Pentagram, and IBM. They are references, not affiliated brands or reusable proprietary artwork.

The Reprism wordmark uses Manrope, distributed under the [SIL Open Font License](examples/reprism/assets/fonts/OFL.txt). Its font source, FONTLOG, and SHA-256 provenance are included with the example. Runtime SVG usage requires no font installation.
