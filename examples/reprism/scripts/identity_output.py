"""Shared SVG and licensed typography output for the Reprism example."""

import importlib.util
import json
from hashlib import sha256
from pathlib import Path
from xml.etree import ElementTree as ET
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

SVG="http://www.w3.org/2000/svg"
ET.register_namespace("",SVG)
EXAMPLE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("geometry",EXAMPLE.parents[1]/"brand-design/scripts/render_geometry.py")
geometry=importlib.util.module_from_spec(spec)
spec.loader.exec_module(geometry)


def path(polygon):
    if polygon.geom_type=="MultiPolygon":
        return "".join(path(part) for part in polygon.geoms)
    return "".join("M"+"L".join(f"{x:.4f} {y:.4f}" for x,y in ring.coords)+"Z"
                   for ring in [polygon.exterior,*polygon.interiors])


def stage(content,description,width=80,height=82):
    return (f'<svg xmlns="{SVG}" viewBox="-5 -5 {width} {height}" role="img" aria-labelledby="title desc">'
            f'<title id="title">Reprism construction</title><desc id="desc">{description}</desc>{content}</svg>\n')


def export_identity(design,brief,p,recipe,evidence,stages,output):
    files=geometry.render(brief,recipe)
    files.update(stages)
    files["render-recipe.json"]=json.dumps(recipe,indent=2)+"\n"
    font_path=EXAMPLE/"assets/fonts/Manrope.ttf"
    font_hash=sha256(font_path.read_bytes()).hexdigest()
    if font_hash!="3ae11c49db0455a3cc33e37d380f20fdb8c7f8b41dc07625c177e3d87a9d6ae6":
        raise ValueError("Font differs from its provenance record.")
    font=instantiateVariableFont(TTFont(font_path),{"wght":p["type_weight"]})
    glyphs=font.getGlyphSet();cmap=font.getBestCmap();cap=p["source_cap"];pad=p["padding"]
    mark_width=recipe["view_box"][2]-2*pad;type_scale=cap/1440
    cursor=mark_width+p["word_gap"];outlines=[];maxx=0;miny=0;maxy=cap
    for letter in brief["name"][1:]:
        glyph=glyphs[cmap[ord(letter)]];bounds=BoundsPen(glyphs);glyph.draw(bounds)
        origin=cursor-(bounds.bounds[0]*type_scale if not outlines else 0)
        pen=SVGPathPen(glyphs,ntos=lambda v:f"{v:.4f}".rstrip("0").rstrip("."))
        glyph.draw(TransformPen(pen,(type_scale,0,0,-type_scale,origin+pad,cap+pad)))
        outlines.append(pen.getCommands())
        maxx=max(maxx,origin+bounds.bounds[2]*type_scale+pad)
        miny=min(miny,cap+pad-bounds.bounds[3]*type_scale)
        maxy=max(maxy,cap+pad-bounds.bounds[1]*type_scale)
        cursor+=glyph.width*type_scale+p["tracking"]
    if miny<0:raise ValueError("Typography extends beyond its safety inset.")
    for variant,palette in design["variants"].items():
        root=ET.fromstring(files[f'{brief["slug"]}-symbol-{variant}.svg'])
        root.set("viewBox",f"0 0 {maxx+pad:.4f} {maxy+pad:.4f}")
        group=ET.SubElement(root,f"{{{SVG}}}g",{"fill":palette["type"]})
        for data in outlines:ET.SubElement(group,f"{{{SVG}}}path",{"d":data})
        files[f'{brief["slug"]}-wordmark-{variant}.svg']=ET.tostring(root,encoding="unicode")+"\n"
    evidence.update({"font_sha256":font_hash,"wordmark_height":maxy+pad,"cap_height":cap,
                     "design_sha256":sha256(json.dumps(design,sort_keys=True).encode()).hexdigest()})
    files["geometry-evidence.json"]=json.dumps(evidence,indent=2)+"\n"
    output.mkdir(parents=True,exist_ok=True)
    for filename,content in files.items():
        if filename.endswith(".svg"):ET.fromstring(content)
        (output/filename).write_text(content,encoding="utf-8")
    return files
