"""Check geometry dependencies and brand independence without extra packages."""

import copy
import unittest
from xml.etree import ElementTree as ET

from render_geometry import Parameters, render


def fixture():
    brief = {"name": "Test Orbit", "slug": "test-orbit",
             "philosophies": [{"id": "shared-origin", "statement": "Two views of one source."}]}
    circle = {"tag": "circle", "attrs": {"cx": "cx", "cy": "cy", "r": "radius",
                                           "fill": "none", "stroke": "@ink", "stroke-width": "weight"}}
    recipe = {
        "version": 1,
        "parameters": {"radius": "3*unit", "unit": 5, "cx": "5*unit", "cy": "5*unit",
                       "weight": "unit/2", "angle": 30},
        "view_box": [0, 0, "10*unit", "10*unit"],
        "variants": {"primary": {"ink": "#6B4C9A"}, "mono": {"ink": "#111111"}},
        "shapes": [circle, {"tag": "g", "transform": [{"matrix": ["cos(radians(angle))", 0, 0, 1,
                            "cx*(1-cos(radians(angle)))", 0]}], "children": [copy.deepcopy(circle)]}],
        "guides": [{"tag": "circle", "attrs": {"cx": "cx", "cy": "cy", "r": "radius",
                    "fill": "none", "stroke": "@guide", "stroke-width": "unit/20"}}],
        "rationale": [{"philosophy": "shared-origin", "rule": "Use an affine view of the same circle.",
                       "parameters": ["radius", "angle"], "observable_result": "Two related views.",
                       "check": "Shared radius and transform origin; visual reading still needs review.",
                       "status": "implemented"}],
    }
    return brief, recipe


class GeometryTests(unittest.TestCase):
    def test_dependencies_and_invalid_expressions(self):
        params = Parameters({"weight": "2*unit", "unit": 6, "diagonal": "weight/sqrt(2)"})
        self.assertAlmostEqual(params.values["diagonal"], 12/2**0.5)
        for invalid in ("__import__('os').system('true')", "(1).__class__", "unknown", "sqrt(-1)", "1/0"):
            with self.assertRaises((ValueError, ArithmeticError)):
                params.evaluate(invalid)
        with self.assertRaises(ValueError):
            Parameters({"a": "b", "b": "a"})

    def test_other_brand_and_projection(self):
        brief, recipe = fixture()
        files = render(brief, recipe)
        self.assertEqual(files, render(copy.deepcopy(brief), copy.deepcopy(recipe)))
        root = ET.fromstring(files["test-orbit-symbol-primary.svg"])
        ns = {"s": "http://www.w3.org/2000/svg"}
        circles = root.findall(".//s:circle", ns)
        self.assertEqual([c.attrib["r"] for c in circles], ["15", "15"])
        matrix = root.find("s:g", ns).attrib["transform"]
        self.assertIn("0.866025", matrix)
        self.assertTrue(all("Reprism" not in value for value in files.values()))

    def test_variation_updates_production_and_guides(self):
        brief, recipe = fixture()
        original = render(brief, recipe)
        changed = render(brief, recipe, {"unit": "8"})
        self.assertEqual(recipe["parameters"]["unit"], 5)
        self.assertNotEqual(original, changed)
        ns = {"s": "http://www.w3.org/2000/svg"}
        for filename in ("test-orbit-symbol-primary.svg", "test-orbit-construction.svg"):
            root = ET.fromstring(changed[filename])
            self.assertEqual(root.attrib["viewBox"], "0 0 80 80")
            self.assertTrue(all(c.attrib["r"] == "24" for c in root.findall(".//s:circle", ns)))

    def test_structural_variation_changes_projection(self):
        brief, recipe = fixture()
        original = render(brief, recipe)
        changed = render(brief, recipe, {"angle": "60"})
        root = ET.fromstring(changed["test-orbit-symbol-primary.svg"])
        ns = {"s": "http://www.w3.org/2000/svg"}
        self.assertIn("matrix(0.5 0 0 1 12.5 0)", root.find("s:g", ns).attrib["transform"])
        self.assertNotEqual(original["test-orbit-symbol-primary.svg"], changed["test-orbit-symbol-primary.svg"])
        with self.assertRaises(ValueError):
            render(brief, recipe, {"unknown_axis": 10})

    def test_construction_bounds_do_not_resize_production(self):
        brief, recipe = fixture()
        recipe["construction_view_box"] = [-5, -5, 60, 60]
        files = render(brief, recipe)
        self.assertEqual(ET.fromstring(files["test-orbit-construction.svg"]).attrib["viewBox"], "-5 -5 60 60")
        self.assertEqual(ET.fromstring(files["test-orbit-symbol-primary.svg"]).attrib["viewBox"], "0 0 50 50")

    def test_unresolved_philosophy_is_not_hidden(self):
        import json
        brief, recipe = fixture()
        recipe["rationale"][0]["status"] = "pending"
        manifest = json.loads(render(brief, recipe)["test-orbit-resolved.json"])
        self.assertEqual(manifest["unresolved_philosophies"], ["shared-origin"])
        implemented_part = copy.deepcopy(recipe["rationale"][0])
        implemented_part["status"] = "implemented"
        recipe["rationale"].append(implemented_part)
        manifest = json.loads(render(brief, recipe)["test-orbit-resolved.json"])
        self.assertEqual(manifest["unresolved_philosophies"], ["shared-origin"])

    def test_invalid_geometry_and_external_resources(self):
        for mutation in (
            lambda r: r["shapes"][0]["attrs"].update({"r": -1}),
            lambda r: r["shapes"][0]["attrs"].update({"fill": "url(https://example.com/a)"}),
            lambda r: r["shapes"][0].update({"tag": "script"}),
            lambda r: r.update({"view_box": [0, 0, 0, 1]}),
            lambda r: r["rationale"][0].update({"parameters": ["absent"]}),
        ):
            brief, recipe = fixture()
            mutation(recipe)
            with self.assertRaises(ValueError):
                render(brief, recipe)


if __name__ == "__main__":
    unittest.main()
