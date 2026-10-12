"""Shared SVG export for the Reprism symbol and original whole-word lettering."""

import importlib.util
import json
from hashlib import sha256
from pathlib import Path
from xml.etree import ElementTree as ET
from lettering import layout

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
    cap=p['source_cap'];pad=p['padding'];mark_width=recipe['view_box'][2]-2*pad
    if brief['name']!='Reprism':raise ValueError('This lettering builder is scoped to Reprism.')
    pair_resolver=geometry.Parameters(design['parameters'])
    placed,type_evidence=layout(p,mark_width,{key:pair_resolver.evaluate(value) for key,value in design['pair_gaps'].items()})
    maxx=placed[-1][1].bounds[2];maxy=max(shape.bounds[3] for _,shape in placed)
    if min(shape.bounds[1] for _,shape in placed)<0:raise ValueError('Lettering exceeds its safety inset.')
    for variant,palette in design["variants"].items():
        root=ET.fromstring(files[f'{brief["slug"]}-symbol-{variant}.svg'])
        root.set("viewBox",f"0 0 {maxx+2*pad:.4f} {maxy+2*pad:.4f}")
        root.find(f'{{{SVG}}}desc').text='Reprism: reference, record, refine. A shared circular and stroke grammar across the whole signature.'
        group=ET.SubElement(root,f"{{{SVG}}}g",{"fill":palette["type"],'fill-rule':'evenodd','transform':f'translate({pad} {pad})'})
        for letter,shape in placed:ET.SubElement(group,f"{{{SVG}}}path",{"d":path(shape),'data-letter':letter})
        files[f'{brief["slug"]}-wordmark-{variant}.svg']=ET.tostring(root,encoding="unicode")+"\n"
    # The construction board includes the actual production lettering, with
    # shared circles and horizontal metrics drawn separately from the artwork.
    guides=''.join(f'<line x1="0" y1="{y}" x2="{maxx}" y2="{y}" stroke="#83CDE9" stroke-width=".3" stroke-dasharray="1 2"/>' for y in [0,cap-p['x_height'],cap,cap+p['descender']])
    glyph_content=''.join(f'<path fill="#F4F7F6" fill-rule="evenodd" d="{path(shape)}"/>' for _,shape in placed)
    circles=''.join(f'<circle cx="{shape.bounds[0]+p["radius"]}" cy="{cap-p["radius"]}" r="{p["radius"]}" fill="none" stroke="#66E2A6" stroke-width=".4"/>' for letter,shape in placed if letter in 'ep')
    circles+=f'<circle cx="{p["radius"]}" cy="{p["radius"]}" r="{p["radius"]}" fill="none" stroke="#66E2A6" stroke-width=".4"/>'
    symbol=ET.fromstring(files['reprism-symbol-primary.svg']).find(f'{{{SVG}}}g')
    # Remove its production inset to align the diagram with the baseline grid.
    symbol.set('transform','translate(0 0)')
    files['reprism-lettering.svg']=stage(ET.tostring(symbol,encoding='unicode')+glyph_content+guides+circles,'Shared stroke, circular bowls, x-height, baseline, and pair-specific spacing',maxx+10,maxy+10)
    evidence.update({**type_evidence,"wordmark_height":maxy+2*pad,"cap_height":cap,
                     "design_sha256":sha256(json.dumps(design,sort_keys=True).encode()).hexdigest()})
    files["geometry-evidence.json"]=json.dumps(evidence,indent=2)+"\n"
    output.mkdir(parents=True,exist_ok=True)
    for filename,content in files.items():
        if filename.endswith(".svg"):ET.fromstring(content)
        (output/filename).write_text(content,encoding="utf-8")
    return files
