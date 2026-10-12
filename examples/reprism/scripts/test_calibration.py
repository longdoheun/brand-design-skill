"""Check statistical construction, stable reference, clearance, and vector reproduction."""

import copy
import json
import math
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET
from generate_calibration import EXAMPLE,geometry,model,generate,summarize
from lettering import glyphs,layout
from shapely.affinity import scale


class CalibrationTests(unittest.TestCase):
    def setUp(self):
        self.design=json.loads((EXAMPLE/"design.json").read_text())
        self.brief=json.loads((EXAMPLE/"brief.json").read_text())

    def test_statistical_summary_and_adverse_inputs(self):
        self.assertEqual(summarize([4,2,1,.5],.5),[4,3,2,1.25])
        self.assertEqual(summarize([1,3,5],.5),[1,2,3.5])
        self.assertEqual(summarize([2,2,2],.2),[2,2,2])
        self.assertEqual(summarize([4,2,1],1),[4,2,1])
        for values,alpha in [([4],.5),([4,-1],.5),([4,float('nan')],.5),([4,2],0)]:
            with self.assertRaises(ValueError):summarize(values,alpha)

    def test_records_and_gain_do_not_move_reference(self):
        _,reference,record,*_=model(self.design)
        changed=copy.deepcopy(self.design)
        changed["parameters"]["smoothing_alpha"]=.75
        changed["observed_deviations"]=[3,2,2,1]
        _,reference2,record2,*_=model(changed)
        self.assertTrue(reference.equals(reference2))
        self.assertFalse(record.equals(record2))

    def test_target_relative_coordinates_and_tangency(self):
        p,_,_,_,point,_=model(self.design)
        for i,expected in enumerate([8,9,10,10.75]):
            x,y=point(i/3)
            self.assertAlmostEqual(math.hypot(x-p["radius"],y-p["radius"]),expected,places=9)
        for t,near in [(0,.0001),(1,.9999)]:
            x,y=point(t);xx,yy=point(near)
            self.assertLess(abs((yy-y)/(xx-x)),.002)

    def test_connected_geometry_and_real_comparison_lane(self):
        _,reference,record,_,_,evidence=model(self.design)
        combined=reference.union(record)
        self.assertTrue(combined.is_valid)
        self.assertEqual(combined.geom_type,'Polygon')
        self.assertEqual(len(combined.interiors),2)
        self.assertGreaterEqual(evidence['lane_at_28px'],1)
        self.assertGreaterEqual(evidence['record_weight_at_28px'],1)
        invalid=copy.deepcopy(self.design)
        invalid['parameters']['record_stroke']=1
        with self.assertRaises(ValueError):model(invalid)

    def test_portable_vector_reproduction(self):
        with tempfile.TemporaryDirectory() as folder:
            first=Path(folder)/'first';second=Path(folder)/'second'
            generate(self.design,self.brief,first);generate(self.design,self.brief,second)
            for item in first.iterdir():
                self.assertEqual(item.read_bytes(),(second/item.name).read_bytes())
                if item.suffix=='.svg':
                    root=ET.parse(item).getroot()
                    self.assertTrue(all(e.tag.startswith('{http://www.w3.org/2000/svg}') for e in root.iter()))
                    self.assertFalse(any(e.tag.endswith(('text','script')) for e in root.iter()))
                    self.assertFalse(any('href' in k for e in root.iter() for k in e.attrib))
            recipe=json.loads((first/'render-recipe.json').read_text())
            for name,value in geometry.render(self.brief,recipe).items():
                self.assertEqual((first/name).read_text(),value)
            manifest=json.loads((first/'reprism-resolved.json').read_text())
            self.assertEqual(manifest['unresolved_philosophies'],[])

    def test_letterform_topology_and_shared_bowl(self):
        p,*_=model(self.design);letters=glyphs(p)
        for letter,shape in letters.items():
            self.assertTrue(shape.is_valid,letter)
            self.assertFalse(shape.is_empty,letter)
        for letter in 'ep':self.assertEqual(len(letters[letter].interiors),1)
        for letter in 'rsm':
            self.assertEqual(letters[letter].geom_type,'Polygon')
            self.assertEqual(len(letters[letter].interiors),0)
        self.assertEqual(len(letters['i'].geoms),2)
        # The p bowl repeats the R's dimensions at the lowercase centre.
        self.assertAlmostEqual(letters['p'].bounds[2],2*p['radius'])
        counter=letters['p'].interiors[0]
        self.assertAlmostEqual(counter.bounds[2],2*p['radius']-p['stroke'])
        self.assertAlmostEqual(counter.bounds[0],p['stroke'])
        self.assertAlmostEqual(letters['p'].bounds[3],p['source_cap']+p['descender'])

    def test_whole_wordmark_spacing_and_scaling(self):
        p,reference,*_=model(self.design)
        params=geometry.Parameters(self.design['parameters'])
        pairs={key:params.evaluate(value) for key,value in self.design['pair_gaps'].items()}
        placed,_=layout(p,reference.bounds[2],pairs)
        for (a,left),(b,right) in zip(placed,placed[1:]):
            self.assertAlmostEqual(right.bounds[0]-left.bounds[2],pairs[a+b])
            self.assertGreaterEqual(left.distance(right)*28/100,1)
        changed=copy.deepcopy(self.design);changed['parameters']['unit']=4
        enlarged=geometry.Parameters(changed['parameters']).values
        original_glyphs=glyphs(p);larger_glyphs=glyphs(enlarged)
        for letter,shape in original_glyphs.items():
            self.assertLess(scale(shape,xfact=4/3,yfact=4/3,origin=(0,0)).hausdorff_distance(larger_glyphs[letter]),.02)
        with self.assertRaises(ValueError):layout(p,reference.bounds[2],{**pairs,'ep':-1})


if __name__=='__main__':unittest.main()
