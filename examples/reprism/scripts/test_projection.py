"""Numerical checks for the example's source, projection, negative space, and assets."""

import copy
import json
import math
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

from shapely.geometry import Point
from generate_projection import EXAMPLE, model, generate, geometry


class ProjectionTests(unittest.TestCase):
    def setUp(self):
        self.design=json.loads((EXAMPLE/"design.json").read_text())
        self.brief=json.loads((EXAMPLE/"brief.json").read_text())

    def test_fixed_axis_and_normal_foreshortening(self):
        p,_,_,_,_,_,metrics=model(self.design["parameters"])
        a,b,d,e,tx,ty=metrics["projection_matrix"]
        phi=math.radians(p["axis_deg"]);theta=math.radians(p["fold_deg"])
        v=(math.cos(phi),math.sin(phi));n=(-v[1],v[0]);c=p["radius"]
        for t in [-30,-10,0,10,30]:
            x,y=c+t*v[0],c+t*v[1]
            self.assertAlmostEqual(a*x+b*y+tx,x,places=10)
            self.assertAlmostEqual(d*x+e*y+ty,y,places=10)
        x,y=c+10*n[0],c+10*n[1]
        self.assertAlmostEqual(a*x+b*y+tx,c+10*math.cos(theta)*n[0],places=10)
        self.assertAlmostEqual(d*x+e*y+ty,c+10*math.cos(theta)*n[1],places=10)

    def test_real_negative_space_and_counter(self):
        p,front,facet,source,_,normalize,metrics=model(self.design["parameters"])
        self.assertEqual(metrics["face_count"],2)
        self.assertTrue(front.is_valid and facet.is_valid)
        self.assertGreaterEqual(front.distance(facet)*28/100,1)
        y=p["radius"]+(6-p["radius"])*math.tan(math.radians(p["axis_deg"]))
        seam_point=Point(6,y)
        self.assertTrue(source.contains(seam_point))
        self.assertFalse(front.contains(normalize(seam_point)))
        self.assertFalse(facet.contains(normalize(seam_point)))
        a,b,d,e,tx,ty=metrics["projection_matrix"]
        def projected_point(x,y):return normalize(Point(a*x+b*y+tx,d*x+e*y+ty))
        self.assertTrue(facet.contains(projected_point(24,6)))
        self.assertFalse(facet.contains(projected_point(24,18)))

    def test_view_changes_without_changing_source(self):
        _,_,facet,source,_,_,metrics=model(self.design["parameters"])
        changed=copy.deepcopy(self.design["parameters"]);changed["fold_deg"]=54
        _,_,facet2,source2,_,_,metrics2=model(changed)
        self.assertTrue(source.equals(source2))
        self.assertFalse(facet.equals(facet2))
        self.assertNotEqual(metrics["projection_matrix"],metrics2["projection_matrix"])
        with self.assertRaises(ValueError):
            invalid=copy.deepcopy(changed);invalid["seam"]=0.2;model(invalid)

    def test_reproduction_and_vector_delivery(self):
        with tempfile.TemporaryDirectory() as directory:
            first=Path(directory)/"first";second=Path(directory)/"second"
            generate(self.design,self.brief,first);generate(self.design,self.brief,second)
            self.assertEqual(sorted(p.name for p in first.iterdir()),sorted(p.name for p in second.iterdir()))
            for item in first.iterdir():
                self.assertEqual(item.read_bytes(),(second/item.name).read_bytes())
                if item.suffix==".svg":
                    root=ET.parse(item).getroot()
                    self.assertTrue(all(e.tag.startswith("{http://www.w3.org/2000/svg}") for e in root.iter()))
                    self.assertFalse(any(e.tag.endswith(("text","script")) for e in root.iter()))
                    self.assertFalse(any("href" in k for e in root.iter() for k in e.attrib))
            recipe=json.loads((first/"render-recipe.json").read_text())
            replay=geometry.render(self.brief,recipe)
            for name,content in replay.items():
                self.assertEqual((first/name).read_text(),content)
            manifest=json.loads((first/"reprism-resolved.json").read_text())
            self.assertEqual(manifest["unresolved_philosophies"],[])


if __name__=="__main__":
    unittest.main()
