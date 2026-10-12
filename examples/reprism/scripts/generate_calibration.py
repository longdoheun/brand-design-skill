"""Construct a stable reference R and a statistically summarized record trace."""

import argparse
import json
import math
from pathlib import Path
from shapely.geometry import Polygon,box,LineString
from identity_output import EXAMPLE,geometry,path,stage,export_identity


def summarize(observations,alpha):
    if not 0<alpha<=1 or len(observations)<2:
        raise ValueError("Use at least two observations and smoothing alpha in (0,1].")
    if any(not isinstance(v,(int,float)) or isinstance(v,bool) or not math.isfinite(v) or v<0 for v in observations):
        raise ValueError("Design observations must be finite nonnegative deviations.")
    result=[float(observations[0])]
    for value in observations[1:]:result.append((1-alpha)*result[-1]+alpha*value)
    return result


def interpolate(t,values):
    # Endpoint-flat smoothstep preserves tangency to the horizontal return links.
    if not 0<=t<=1:raise ValueError("Curve phase must be in [0,1].")
    position=t*(len(values)-1);index=min(int(position),len(values)-2);f=position-index
    blend=f*f*(3-2*f)
    return values[index]+(values[index+1]-values[index])*blend


def model(design):
    p=geometry.Parameters(design["parameters"]).values
    cap,w,r=p["source_cap"],p["stroke"],p["radius"]
    segments=int(p["arc_segments"]);rw=p["record_stroke"];gap=p["minimum_lane_gap"]
    if segments<64 or not 0<w<r or not 0<rw<2*p["target_radius"] or gap<=0:
        raise ValueError("Invalid reference or record dimensions.")
    summary=summarize(design["observed_deviations"],p["smoothing_alpha"])
    if max(summary)>=p["target_radius"]-rw/2:
        raise ValueError("The record trace would close its inner counter.")

    def bowl(radius,left):
        arc=[(r+radius*math.cos(-math.pi/2+i*math.pi/segments),
              r+radius*math.sin(-math.pi/2+i*math.pi/segments)) for i in range(segments+1)]
        return Polygon([(left,r-radius),*arc,(left,r+radius)])
    start=(r,2*r-w/2);end=(p["leg_tip_x"],cap)
    dx,dy=end[0]-start[0],end[1]-start[1];length=math.hypot(dx,dy);nx,ny=-dy/length,dx/length
    leg=Polygon([(start[0]+nx*w/2,start[1]+ny*w/2),(start[0]-nx*w/2,start[1]-ny*w/2),
                 (end[0]-nx*w/2,end[1]-ny*w/2),(end[0]+nx*w/2,end[1]+ny*w/2)])
    leg=leg.intersection(box(-cap,-cap,2*cap,cap))
    reference=bowl(r,0).union(box(0,0,w,cap)).union(leg).difference(bowl(p["counter_radius"],w))

    def point(t):
        radius=p["target_radius"]-interpolate(t,summary)
        angle=-math.pi/2+math.pi*t
        return (r+radius*math.cos(angle),r+radius*math.sin(angle))
    points=[point(i/segments) for i in range(segments+1)]
    chain=[(w-1,points[0][1]),*points,(w-1,points[-1][1])]
    record=LineString(chain).buffer(rw/2,cap_style=2,join_style=1)
    combined=reference.union(record)
    if not combined.is_valid or combined.geom_type!="Polygon" or len(combined.interiors)!=2:
        raise ValueError("The intended connected R must retain two readable counters.")
    lane=record.intersection(box(r,-cap,2*cap,2*cap))
    clearance=reference.distance(lane)
    wordmark_height=cap+p['descender']+2*p["padding"]
    if min(clearance,rw)*28/wordmark_height<1:
        raise ValueError("Record weight or curved-lane clearance is below 1px at 28px height.")
    tolerance=p["simplify_tolerance"]
    reference_out=reference.simplify(tolerance,preserve_topology=True)
    record_out=record.simplify(tolerance,preserve_topology=True)
    evidence={"data_status":design["data_status"],"observed_deviations":design["observed_deviations"],
              "statistical_summary":summary,"smoothing_alpha":p["smoothing_alpha"],
              "target_radius":p["target_radius"],"lane_clearance":clearance,
              "lane_at_28px":clearance*28/wordmark_height,"record_weight_at_28px":rw*28/wordmark_height,
              "connected_components":1,"counter_count":2,"export_tolerance_units":tolerance,
              "leg_angle_deg":math.degrees(math.atan2(dy,dx))}
    return p,reference_out,record_out,points,point,evidence


def generate(design,brief,output):
    p,reference,record,points,point,evidence=model(design)
    pad=p["padding"];cap=p["source_cap"];width=reference.bounds[2]
    rationale=[
        {"philosophy":"training-support","rule":"Hold the reference frame fixed as observation values and smoothing vary.",
         "parameters":["unit","radius","stroke","source_cap"],"observable_result":"A steady outer R supports the internal record.",
         "check":"Changing records must not change the reference geometry.","status":"implemented"},
        {"philosophy":"accumulated-evidence","rule":"Use an exponential moving average of an illustrative observation sequence.",
         "parameters":["smoothing_alpha"],"observable_result":"The inner trace summarizes multiple records rather than tracing raw inputs.",
         "check":"Verify the summary independently and that it drives actual curve coordinates.","status":"implemented"},
        {"philosophy":"guided-improvement","rule":"Express differences relative to a fixed target inside the reference envelope.",
         "parameters":["target_radius","minimum_lane_gap","record_stroke"],"observable_result":"The trace approaches its target as the illustrated summary deviation decreases.",
         "check":"Validate target-minus-summary radii, genuine lane clearance, and a readable mono symbol.","status":"implemented"}
    ]
    recipe={"version":1,"parameters":design["parameters"],"view_box":[0,0,width+2*pad,cap+2*pad],
            "variants":design["variants"],"rationale":rationale,
            "shapes":[{"tag":"g","transform":[{"translate":["padding","padding"]}],"children":[
                {"tag":"path","attrs":{"fill":"@record","d":path(record)}},
                {"tag":"path","attrs":{"fill":"@ink","fill-rule":"evenodd","d":path(reference)}}]}],
            "guides":[{"tag":"g","transform":[{"translate":["padding","padding"]}],
                       "attrs":{"fill":"none","stroke":"@guide","stroke-width":0.25},"children":[
                           {"tag":"path","attrs":{"d":"M{stroke} {radius-target_radius} H{radius} A{target_radius} {target_radius} 0 0 1 {radius} {radius+target_radius} H{stroke}"}},
                           {"tag":"circle","attrs":{"cx":"radius","cy":"radius","r":"counter_radius"}}]}]}
    source=stage(f'<path fill="#87909A" fill-rule="evenodd" d="{path(reference)}"/>'
                 f'<path d="M{p["stroke"]} {p["radius"]-p["target_radius"]}H{p["radius"]} A{p["target_radius"]} {p["target_radius"]} 0 0 1 {p["radius"]} {p["radius"]+p["target_radius"]}H{p["stroke"]}" fill="none" stroke="#83CDE9" stroke-width=".5" stroke-dasharray="1.5 1.5"/>',
                 "Stable reference frame with a fixed internal target")
    marks="".join(f'<circle cx="{point(i/(len(evidence["statistical_summary"])-1))[0]}" cy="{point(i/(len(evidence["statistical_summary"])-1))[1]}" r="1" fill="#83CDE9"/>' for i in range(len(evidence["statistical_summary"])))
    records=stage(f'<path fill="none" stroke="#87909A" stroke-width=".5" d="{path(reference)}"/>'
                  f'<path fill="none" stroke="#66E2A6" stroke-width=".6" d="M'+"L".join(f"{x:.4f} {y:.4f}" for x,y in points)+f'"/>{marks}',
                  "Four illustrative records, statistically summarized within the reference")
    stages={"reprism-reference.svg":source,"reprism-record.svg":records}
    files=export_identity(design,brief,p,recipe,evidence,stages,output)
    print(f'{len(files)} files · summary {evidence["statistical_summary"]} · lane {evidence["lane_at_28px"]:.3f}px at 28px')


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--design",type=Path,default=EXAMPLE/"design.json")
    parser.add_argument("--brief",type=Path,default=EXAMPLE/"brief.json")
    parser.add_argument("--output",type=Path,default=EXAMPLE/"generated")
    parser.add_argument("--alpha",type=float,help="Explore statistical smoothing without changing the reference.")
    args=parser.parse_args();design=json.loads(args.design.read_text());brief=json.loads(args.brief.read_text())
    if args.alpha is not None:design["parameters"]["smoothing_alpha"]=args.alpha
    generate(design,brief,args.output)
