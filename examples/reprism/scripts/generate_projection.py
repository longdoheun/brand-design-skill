"""Rebuild the shared-axis Reprism study, including vector typography and evidence."""

import argparse
import importlib.util
import json
import math
from hashlib import sha256
from pathlib import Path
from xml.etree import ElementTree as ET

from shapely.geometry import Polygon, box
from shapely.affinity import affine_transform, translate, scale
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)
EXAMPLE = Path(__file__).resolve().parents[1]
REPOSITORY = EXAMPLE.parents[1]
spec = importlib.util.spec_from_file_location("geometry", REPOSITORY / "brand-design/scripts/render_geometry.py")
geometry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(geometry)


def path(polygon):
    if polygon.geom_type == "MultiPolygon":
        return "".join(path(part) for part in polygon.geoms)
    return "".join("M" + "L".join(f"{x:.4f} {y:.4f}" for x,y in ring.coords) + "Z"
                   for ring in [polygon.exterior, *polygon.interiors])


def model(parameters):
    p = geometry.Parameters(parameters).values
    unit, radius, stroke = p["unit"], p["radius"], p["stroke"]
    cap, counter_radius = p["source_cap"], p["counter_radius"]
    segments = int(p["arc_segments"])
    if unit <= 0 or not 0 < counter_radius < radius or segments < 32:
        raise ValueError("Invalid source dimensions or arc resolution.")
    if not 0 < p["fold_deg"] < 80 or not 0 < p["seam"] < stroke:
        raise ValueError("Fold and seam must preserve a readable source.")

    def bowl(r, left):
        arc = [(radius + r*math.cos(-math.pi/2+i*math.pi/segments),
                radius + r*math.sin(-math.pi/2+i*math.pi/segments)) for i in range(segments+1)]
        return Polygon([(left, radius-r), *arc, (left, radius+r)])

    offset = stroke/(2*math.sqrt(2))
    leg = Polygon([(4*unit-offset,7*unit+offset),(4*unit+offset,7*unit-offset),
                   (9*unit+offset,12*unit-offset),(9*unit-offset,12*unit+offset)])
    leg = leg.intersection(box(-cap,-cap,2*cap,cap))
    source = bowl(radius,0).union(box(0,0,stroke,cap)).union(leg).difference(bowl(counter_radius,stroke))

    # Orthographic projection of a plane rotated in 3D about its shared in-plane axis:
    # T = vv^T + cos(theta) nn^T. Axis direction v remains fixed; normal n foreshortens.
    phi, theta = math.radians(p["axis_deg"]), math.radians(p["fold_deg"])
    v = (math.cos(phi),math.sin(phi)); n = (-v[1],v[0]); center = (radius,radius)
    a = v[0]*v[0]+math.cos(theta)*n[0]*n[0]
    b = v[0]*v[1]+math.cos(theta)*n[0]*n[1]
    e = v[1]*v[1]+math.cos(theta)*n[1]*n[1]
    matrix = [a,b,b,e,radius*(1-a-b),radius*(1-b-e)]
    projected = affine_transform(source,matrix)

    def halfplane(side):
        def point(t,s):
            return (center[0]+v[0]*t+n[0]*s,center[1]+v[1]*t+n[1]*s)
        extent=4*cap
        return Polygon([point(-extent,side*p["seam"]/2),point(extent,side*p["seam"]/2),
                        point(extent,side*extent),point(-extent,side*extent)])

    front = source.intersection(halfplane(1))
    facet = projected.intersection(halfplane(-1))
    combined = front.union(facet)
    if any(not g.is_valid or g.is_empty for g in [source,front,facet]) or combined.geom_type != "MultiPolygon":
        raise ValueError("The chosen parameters do not yield two valid separated faces.")
    if len(combined.geoms) != 2:
        raise ValueError("The intended mark must have exactly two faces.")
    minx,miny,maxx,maxy = combined.bounds
    normalization=p["output_cap"]/(maxy-miny)

    def normalize(g):
        return scale(translate(g,xoff=-minx,yoff=-miny),normalization,normalization,origin=(0,0))

    # Measured clearance uses unsimplified geometry; export error is bounded separately.
    gap=front.distance(facet)*normalization
    if gap*28/100 < 1:
        raise ValueError("Nominal seam clearance falls below 1px at 28px wordmark height.")
    tol=p["simplify_tolerance"]
    front_out=normalize(front).simplify(tol,preserve_topology=True)
    facet_out=normalize(facet).simplify(tol,preserve_topology=True)
    metrics={"projection_matrix":matrix,"normalization_scale":normalization,
             "source_cap":cap,"source_stroke":stroke,"source_counter_area":bowl(counter_radius,stroke).area,
             "seam_units":gap,"seam_at_28px":gap*28/100,"seam_at_32px":gap*32/100,
             "face_count":len(combined.geoms),"export_tolerance_units":tol,
             "arc_sagitta_bound_units":radius*(1-math.cos(math.pi/(2*segments)))}
    return p,front_out,facet_out,source,projected,normalize,metrics


def generate(design, brief, output):
    p,front,facet,source,projected,normalize,metrics=model(design["parameters"])
    pad=p["padding"]; mark_width=max(front.bounds[2],facet.bounds[2]); cap=p["output_cap"]
    rationale=[
        {"philosophy":"multiple-views","rule":"Use front and folded projections of exactly the same source across a fixed axis.",
         "parameters":["axis_deg","fold_deg","radius"],"observable_result":"The upper counter and rim change with the view while the lower face remains stable.",
         "check":"Verify fixed points and normal foreshortening of the projection; inspect the silhouette.","status":"implemented"},
        {"philosophy":"repetition","rule":"Reuse the complete geometric source for both observations rather than drawing a second unrelated glyph.",
         "parameters":["unit","stroke","source_cap"],"observable_result":"One recognizable R with related faces.",
         "check":"Both faces must derive from source and affine_transform(source,matrix).","status":"implemented"},
        {"philosophy":"clarity","rule":"Separate views with a controlled negative seam and preserve a readable counter.",
         "parameters":["seam","padding","output_cap"],"observable_result":"The folded relationship survives single-color reproduction at header sizes.",
         "check":"Exactly two valid faces; nominal clearance above 1px at 28px, followed by browser review.","status":"implemented"}
    ]
    recipe={"version":1,"parameters":design["parameters"],"view_box":[0,0,mark_width+2*pad,cap+2*pad],
            "variants":design["variants"],"rationale":rationale,
            "shapes":[{"tag":"g","transform":[{"translate":["padding","padding"]}],"children":[
                {"tag":"path","attrs":{"fill":"@ink","fill-rule":"evenodd","d":path(front)}},
                {"tag":"path","attrs":{"fill":"@facet","fill-rule":"evenodd","d":path(facet)}}]}],
            "guides":[{"tag":"g","transform":[{"translate":["padding","padding"]}],
                       "attrs":{"fill":"none","stroke":"@guide","stroke-width":0.25},"children":[
                           {"tag":"path","attrs":{"d":path(normalize(source))}},
                           {"tag":"path","attrs":{"d":path(normalize(projected))}}]}]}
    all_views=normalize(source.union(projected))
    vx0,vy0,vx1,vy1=all_views.bounds
    recipe["construction_view_box"]=[vx0,vy0,vx1-vx0+2*pad,vy1-vy0+2*pad]
    files=geometry.render(brief,recipe)
    files["render-recipe.json"]=json.dumps(recipe,indent=2)+"\n"

    def stage(content,description):
        return (f'<svg xmlns="{SVG}" viewBox="-5 -5 70 82" role="img" aria-labelledby="title desc">'
                f'<title id="title">Reprism geometry</title><desc id="desc">{description}</desc>{content}</svg>\n')
    files["reprism-source.svg"]=stage(f'<path fill="#87909A" fill-rule="evenodd" d="{path(source)}"/>',
                                      "One circular R source, before projection")
    slope=math.tan(math.radians(p["axis_deg"]))
    line_y0=p["radius"]-p["radius"]*slope
    line_y1=p["radius"]+(60-p["radius"])*slope
    files["reprism-views.svg"]=stage(
        f'<path fill="none" stroke="#66E2A6" stroke-width=".7" d="{path(source)}"/>'
        f'<path fill="none" stroke="#83CDE9" stroke-width=".7" d="{path(projected)}"/>'
        f'<path fill="none" stroke="#F4F7F6" stroke-width=".45" stroke-dasharray="1.4 1.4" '
        f'd="M0 {line_y0}L60 {line_y1}"/>',"Front and folded views preserve the same shared axis")

    font_path=EXAMPLE/"assets/fonts/Manrope.ttf"
    font_hash=sha256(font_path.read_bytes()).hexdigest()
    if font_hash != "3ae11c49db0455a3cc33e37d380f20fdb8c7f8b41dc07625c177e3d87a9d6ae6":
        raise ValueError("Font source differs from its provenance record.")
    font=instantiateVariableFont(TTFont(font_path),{"wght":p["type_weight"]})
    glyphs=font.getGlyphSet(); cmap=font.getBestCmap(); type_scale=cap/1440
    cursor=mark_width+p["word_gap"]; type_paths=[]; maxx=0; miny=0; maxy=cap
    for letter in brief["name"][1:]:
        glyph=glyphs[cmap[ord(letter)]]; bounds=BoundsPen(glyphs); glyph.draw(bounds)
        origin=cursor-(bounds.bounds[0]*type_scale if not type_paths else 0)
        pen=SVGPathPen(glyphs,ntos=lambda value:f"{value:.4f}".rstrip("0").rstrip("."))
        glyph.draw(TransformPen(pen,(type_scale,0,0,-type_scale,origin+pad,cap+pad)))
        type_paths.append(pen.getCommands())
        maxx=max(maxx,origin+bounds.bounds[2]*type_scale+pad)
        miny=min(miny,cap+pad-bounds.bounds[3]*type_scale)
        maxy=max(maxy,cap+pad-bounds.bounds[1]*type_scale)
        cursor+=glyph.width*type_scale+p["tracking"]
    if miny < 0:
        raise ValueError("Typography extends outside the upper safety boundary.")
    for variant,palette in design["variants"].items():
        root=ET.fromstring(files[f'{brief["slug"]}-symbol-{variant}.svg'])
        root.set("viewBox",f"0 0 {maxx+pad:.4f} {maxy+pad:.4f}")
        group=ET.SubElement(root,f"{{{SVG}}}g",{"fill":palette["type"]})
        for data in type_paths:ET.SubElement(group,f"{{{SVG}}}path",{"d":data})
        files[f'{brief["slug"]}-wordmark-{variant}.svg']=ET.tostring(root,encoding="unicode")+"\n"
    metrics.update({"font_sha256":font_hash,"wordmark_height":maxy+pad,"word_gap":p["word_gap"],
                    "cap_height":cap,"design_sha256":sha256(json.dumps(design,sort_keys=True).encode()).hexdigest()})
    files["geometry-evidence.json"]=json.dumps(metrics,indent=2)+"\n"
    output.mkdir(parents=True,exist_ok=True)
    for filename,content in files.items():
        if filename.endswith(".svg"):ET.fromstring(content)
        (output/filename).write_text(content,encoding="utf-8")
    print(f'{len(files)} files · seam {metrics["seam_at_28px"]:.3f}px at 28px · two valid faces')


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--design",type=Path,default=EXAMPLE/"design.json")
    parser.add_argument("--brief",type=Path,default=EXAMPLE/"brief.json")
    parser.add_argument("--output",type=Path,default=EXAMPLE/"generated")
    parser.add_argument("--fold",type=float,help="Explore a different fold angle.")
    args=parser.parse_args()
    design=json.loads(args.design.read_text());brief=json.loads(args.brief.read_text())
    if args.fold is not None:design["parameters"]["fold_deg"]=args.fold
    generate(design,brief,args.output)
