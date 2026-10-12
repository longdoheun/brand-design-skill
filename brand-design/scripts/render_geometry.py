"""Render a brand-neutral geometric logo recipe. Python 3.10+, no dependencies."""

import argparse
import ast
import copy
import hashlib
import json
import math
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

OPERATORS = {ast.Add: lambda a, b: a+b, ast.Sub: lambda a, b: a-b,
             ast.Mult: lambda a, b: a*b, ast.Div: lambda a, b: a/b,
             ast.Pow: lambda a, b: a**b}
FUNCTIONS = {"sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "radians": math.radians}
COMMON = {"fill", "stroke", "stroke-width", "fill-rule", "stroke-linecap", "stroke-linejoin",
          "opacity", "fill-opacity", "stroke-opacity", "stroke-dasharray"}
ATTRIBUTES = {
    "g": set(), "path": {"d"}, "rect": {"x", "y", "width", "height", "rx", "ry"},
    "circle": {"cx", "cy", "r"}, "ellipse": {"cx", "cy", "rx", "ry"},
    "line": {"x1", "y1", "x2", "y2"}, "polygon": {"points"}, "polyline": {"points"},
}
ENUMS = {"fill-rule": {"nonzero", "evenodd"}, "stroke-linecap": {"butt", "round", "square"},
         "stroke-linejoin": {"miter", "round", "bevel"}}


def number(value):
    value = float(value)
    if not math.isfinite(value) or abs(value) > 1e9:
        raise ValueError("Geometry values must be finite and within ±1e9.")
    return f"{value:.6f}".rstrip("0").rstrip(".") if value else "0"


class Parameters:
    def __init__(self, definitions):
        if not isinstance(definitions, dict):
            raise ValueError("parameters must be an object.")
        if any(not re.fullmatch(r"[a-z][a-z0-9_]*", key) or key in FUNCTIONS or key == "pi"
               for key in definitions):
            raise ValueError("Use lowercase parameter names; math function names are reserved.")
        self.definitions = definitions
        self.values = {}
        self.active = set()
        for key in definitions:
            self.resolve(key)

    def resolve(self, key):
        if key == "pi":
            return math.pi
        if key in self.values:
            return self.values[key]
        if key not in self.definitions or key in self.active:
            raise ValueError(f"Unknown or cyclic parameter: {key}")
        self.active.add(key)
        value = self.evaluate(self.definitions[key])
        self.active.remove(key)
        self.values[key] = value
        return value

    def evaluate(self, expression):
        if isinstance(expression, (int, float)) and not isinstance(expression, bool):
            number(expression)
            return float(expression)
        if not isinstance(expression, str) or len(expression) > 1024:
            raise ValueError("Expected a numeric value or a short arithmetic expression.")
        tree = ast.parse(expression, mode="eval")
        if sum(1 for _ in ast.walk(tree)) > 128:
            raise ValueError("Expression is too complex.")

        def visit(node):
            if isinstance(node, ast.Constant) and type(node.value) in (int, float):
                return float(node.value)
            if isinstance(node, ast.Name):
                return self.resolve(node.id)
            if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
                return OPERATORS[type(node.op)](visit(node.left), visit(node.right))
            if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
                return (-1 if isinstance(node.op, ast.USub) else 1) * visit(node.operand)
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                    and node.func.id in FUNCTIONS and len(node.args) == 1 and not node.keywords):
                return FUNCTIONS[node.func.id](visit(node.args[0]))
            raise ValueError("Unsupported expression; attributes, imports, and arbitrary calls are forbidden.")

        result = visit(tree.body)
        number(result)
        return float(result)

    def template(self, text):
        if not isinstance(text, str):
            raise ValueError("Path data and point lists must be strings.")
        result = re.sub(r"\{([^{}]+)\}", lambda match: number(self.evaluate(match[1])), text)
        if "{" in result or "}" in result:
            raise ValueError("Unbalanced expression braces.")
        return result


def color(value, palette):
    if not isinstance(value, str):
        raise ValueError("Colors must be strings.")
    if value.startswith("@"):
        value = palette[value[1:]]
    if value != "none" and not re.fullmatch(r"#[0-9A-Fa-f]{6}", value):
        raise ValueError("Use #RRGGBB colors, palette references, or none.")
    return value


def shape(spec, params, palette):
    if not isinstance(spec, dict) or set(spec) - {"tag", "attrs", "transform", "children"}:
        raise ValueError("Unsupported shape field.")
    tag = spec["tag"]
    if tag not in ATTRIBUTES:
        raise ValueError(f"Unsupported SVG element: {tag}")
    element = ET.Element(tag)
    if not isinstance(spec.get("attrs", {}), dict):
        raise ValueError("attrs must be an object.")
    for key, value in spec.get("attrs", {}).items():
        if key not in COMMON | ATTRIBUTES[tag]:
            raise ValueError(f"Unsupported {tag} attribute: {key}")
        if key in {"fill", "stroke"}:
            output = color(value, palette)
        elif key in ENUMS:
            if value not in ENUMS[key]:
                raise ValueError(f"Invalid {key}.")
            output = value
        elif key in {"d", "points", "stroke-dasharray"}:
            output = params.template(value)
            allowed = r"[MmLlHhVvCcSsQqTtAaZz0-9eE+.,\s-]+" if key == "d" else r"[0-9eE+.,\s-]+"
            if not re.fullmatch(allowed, output):
                raise ValueError(f"Invalid vector data in {key}.")
        else:
            numeric = params.evaluate(value)
            if key in {"r", "rx", "ry", "width", "height", "stroke-width"} and numeric < 0:
                raise ValueError(f"{key} cannot be negative.")
            if key.endswith("opacity") and not 0 <= numeric <= 1:
                raise ValueError("Opacity must be in [0,1].")
            output = number(numeric)
        element.set(key, output)
    transforms = []
    for operation in spec.get("transform", []):
        if not isinstance(operation, dict) or len(operation) != 1:
            raise ValueError("Each transform must have one operation.")
        name, arguments = next(iter(operation.items()))
        lengths = {"translate": {2}, "scale": {1, 2}, "rotate": {1, 3}, "matrix": {6}}
        if name not in lengths or not isinstance(arguments, list) or len(arguments) not in lengths[name]:
            raise ValueError("Invalid transform or argument count.")
        transforms.append(f'{name}({" ".join(number(params.evaluate(v)) for v in arguments)})')
    if transforms:
        element.set("transform", " ".join(transforms))
    if "children" in spec and tag != "g":
        raise ValueError("Only groups may contain children.")
    for child in spec.get("children", []):
        element.append(shape(child, params, palette))
    return element


def render(brief, recipe, overrides=None):
    if not isinstance(brief, dict) or not isinstance(recipe, dict):
        raise ValueError("Brief and recipe must be JSON objects.")
    if type(recipe.get("version")) is not int or recipe["version"] != 1:
        raise ValueError("Unsupported recipe version.")
    allowed = {"version", "parameters", "view_box", "variants", "shapes", "guides", "rationale"}
    if set(recipe) - allowed:
        raise ValueError("Unsupported recipe field.")
    overrides = overrides or {}
    if not isinstance(overrides, dict) or set(overrides) - set(recipe["parameters"]):
        raise ValueError("Variation overrides must refer to existing parameters.")
    recipe = copy.deepcopy(recipe)
    recipe["parameters"].update(overrides)
    name, slug = brief["name"], brief["slug"]
    if not isinstance(name, str) or not name.strip() or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ValueError("Provide a brand name and a safe lowercase slug.")
    if (not isinstance(brief["philosophies"], list)
            or any(not isinstance(item, dict) or not isinstance(item.get("id"), str)
                   or not item["id"].strip() for item in brief["philosophies"])):
        raise ValueError("Philosophies must have nonempty string IDs.")
    philosophies = {item["id"] for item in brief["philosophies"]}
    if len(philosophies) != len(brief["philosophies"]) or not philosophies:
        raise ValueError("Provide distinct philosophy IDs.")
    params = Parameters(recipe["parameters"])
    if not isinstance(recipe["view_box"], list):
        raise ValueError("view_box must be a list.")
    bounds = [params.evaluate(value) for value in recipe["view_box"]]
    if len(bounds) != 4 or bounds[2] <= 0 or bounds[3] <= 0:
        raise ValueError("view_box must have four numbers and positive dimensions.")
    palettes = recipe["variants"]
    if not isinstance(palettes, dict) or not isinstance(recipe["shapes"], list):
        raise ValueError("variants must be an object and shapes must be a list.")
    if not palettes or not recipe["shapes"]:
        raise ValueError("Provide at least one palette and production shape.")
    implemented = set()
    pending = set()
    for item in recipe.get("rationale", []):
        if item["philosophy"] not in philosophies or item["status"] not in {"implemented", "pending"}:
            raise ValueError("Rationale must reference a philosophy and an explicit mapping status.")
        for field in ("rule", "observable_result", "check"):
            if not isinstance(item[field], str) or not item[field].strip():
                raise ValueError(f"Rationale requires {field}.")
        if any(key not in params.values for key in item["parameters"]):
            raise ValueError("Rationale references unknown parameters.")
        if item["status"] == "implemented":
            implemented.add(item["philosophy"])
        else:
            pending.add(item["philosophy"])

    def svg(palette, guides=False):
        root = ET.Element("svg", {"xmlns": "http://www.w3.org/2000/svg",
                                  "viewBox": " ".join(number(v) for v in bounds),
                                  "role": "img", "aria-labelledby": "title desc"})
        ET.SubElement(root, "title", {"id": "title"}).text = name
        ET.SubElement(root, "desc", {"id": "desc"}).text = (
            "Construction geometry; guides are not part of the production logo" if guides
            else "Brand symbol generated from its geometric recipe")
        for spec in recipe["shapes"]:
            root.append(shape(spec, params, palette))
        if guides:
            for spec in recipe.get("guides", []):
                root.append(shape(spec, params, {**palette, "guide": "#87909A"}))
        return ET.tostring(root, encoding="unicode") + "\n"

    files = {}
    for variant, palette in palettes.items():
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", variant):
            raise ValueError("Use safe lowercase variant names.")
        if not isinstance(palette, dict):
            raise ValueError("Each palette must be an object.")
        for value in palette.values():
            color(value, {})
        files[f"{slug}-symbol-{variant}.svg"] = svg(palette)
    files[f"{slug}-construction.svg"] = svg(next(iter(palettes.values())), guides=True)
    digest = hashlib.sha256(json.dumps(recipe, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    manifest = {"brief": brief, "parameters": params.values, "rationale": recipe.get("rationale", []),
                "parameter_overrides": overrides,
                "unresolved_philosophies": sorted((philosophies - implemented) | pending), "recipe_sha256": digest}
    files[f"{slug}-resolved.json"] = json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--brief", type=Path, required=True)
    parser.add_argument("--recipe", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--set", action="append", default=[], metavar="NAME=EXPRESSION",
                        help="Explore a named parameter without editing the source recipe; repeat as needed.")
    args = parser.parse_args()
    try:
        # Validate and render everything before writing any artifact.
        overrides = {}
        for setting in args.set:
            key, separator, value = setting.partition("=")
            if not separator or not value or key in overrides:
                raise ValueError("Each --set must have a distinct NAME=EXPRESSION.")
            overrides[key] = value
        files = render(json.loads(args.brief.read_text()), json.loads(args.recipe.read_text()), overrides)
    except (ValueError, TypeError, KeyError, SyntaxError, ArithmeticError, OSError) as error:
        parser.exit(2, f"Invalid design input: {error}\n")
    args.output.mkdir(parents=True, exist_ok=True)
    for filename, content in files.items():
        (args.output / filename).write_text(content, encoding="utf-8")
        print(filename)


if __name__ == "__main__":
    if sys.version_info < (3, 10):
        raise SystemExit("Use Python 3.10 or newer.")
    main()
