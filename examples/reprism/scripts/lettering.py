"""Original Reprism lettering from the symbol's stroke and circular module.

This is a scoped alphabet, not a font: it supports only the six lowercase
letters in the signature. Coordinates are SVG-oriented (positive y down).
"""

import math
from shapely.geometry import Point, Polygon, LineString, box
from shapely.affinity import scale, translate
from shapely.ops import unary_union


def cubic(a, b, c, d, steps=96):
    return [tuple((1-t)**3*a[j]+3*(1-t)**2*t*b[j]+3*(1-t)*t*t*c[j]+t**3*d[j]
                  for j in range(2)) for t in (i/steps for i in range(steps+1))]


def glyphs(p):
    w, r, h, cap = p['stroke'], p['radius'], p['x_height'], p['source_cap']
    top=cap-h; mid=cap-h/2; a=p['arch_radius']; over=p['optical_overshoot']
    if h != 2*r or not w<a<r or p['descender']<=0:
        raise ValueError('Lettering requires the shared circular module and open arches.')
    def circle(radius):
        return Point(r,mid).buffer(radius,quad_segs=int(p['arc_segments'])//4)
    ring=circle(r).difference(circle(r-w))
    # e: circular counter, level crossbar, and a lower-right reading aperture.
    aperture=Polygon([(r,mid),(3*r,mid),(3*r,mid+1.25*w),(r,mid+1.25*w)])
    e=ring.difference(aperture).union(box(w/2,mid-w/2,2*r,mid+w/2))
    e=scale(e,xfact=1,yfact=(h+2*over)/h,origin=(r,mid))
    # The p repeats the circular module with a rounded counter. Its upright
    # carries the bowl without turning the lowercase form into a miniature D.
    letter_p=ring.union(box(0,top,w,cap+p['descender']))
    def arch(cx):
        angles=[math.pi+i*math.pi/192 for i in range(193)]
        outer=[(cx+a*math.cos(t),top+a+a*math.sin(t)) for t in angles]
        inner=[(cx+(a-w)*math.cos(t),top+a+(a-w)*math.sin(t)) for t in reversed(angles)]
        # Exact joins avoid near-zero seams caused by sin(2π) rounding.
        outer[0]=(cx-a,top+a);outer[-1]=(cx+a,top+a)
        inner[0]=(cx+a-w,top+a);inner[-1]=(cx-a+w,top+a)
        return Polygon([*outer,*inner])
    letter_r=arch(a).union(box(0,top,w,cap))
    second=2*a-w
    letter_m=unary_union([arch(a),arch(a+second),box(0,top,w,cap),
                          box(second,top+a,second+w,cap),
                          box(2*second,top+a,2*second+w,cap)])
    letter_i=box(0,top,w,cap).union(Point(w/2,w/2).buffer(w/2,quad_segs=48))
    # s uses tangent continuous cubic transitions; its width is an optical
    # correction, not a claim that every alphabetic form is a perfect circle.
    sw=p['s_width']; k=sw/49
    segments=[((42,28),(31,17),(6,19),(6,32)),
              ((6,32),(6,45),(43,40),(43,57)),
              ((43,57),(43,70),(17,75),(5,63))]
    points=[]
    for segment in segments:
        sampled=cubic(*[(x*k,top+(y-18)*h/54) for x,y in segment])
        points.extend(sampled[1:] if points else sampled)
    letter_s=LineString(points).buffer(w/2,cap_style=2,join_style=1)
    # Fit the curved top and bottom to the same optical overshoot as the e.
    y0,y1=letter_s.bounds[1],letter_s.bounds[3]
    x0,x1=letter_s.bounds[0],letter_s.bounds[2]
    letter_s=scale(letter_s,xfact=sw/(x1-x0),yfact=(h+2*over)/(y1-y0),origin=(x0,y0))
    letter_s=translate(letter_s,yoff=top-over-y0)
    result={'e':e,'p':letter_p,'r':letter_r,'i':letter_i,'s':letter_s,'m':letter_m}
    return {letter:translate(shape,xoff=-shape.bounds[0]).simplify(p['simplify_tolerance'],preserve_topology=True)
            for letter,shape in result.items()}


def layout(p,mark_width,pairs):
    letters=glyphs(p);cursor=mark_width+pairs['Re'];placed=[];gaps={}
    if any(not math.isfinite(value) or value<=0 for value in pairs.values()):
        raise ValueError('All optical pair gaps must be finite and positive.')
    previous='R'
    for letter in 'eprism':
        if previous!='R':cursor+=pairs[previous+letter]
        shape=translate(letters[letter],xoff=cursor)
        if not shape.is_valid:raise ValueError(f'Invalid letter: {letter}')
        placed.append((letter,shape));gaps[previous+letter]=pairs[previous+letter]
        cursor=shape.bounds[2];previous=letter
    return placed, {'lettering':'Original geometric lettering; no runtime font',
                    'stroke_note':'Shared construction stroke; e has vertical and s has width/height optical fitting.',
                    'x_height':p['x_height'],'shared_stroke':p['stroke'],
                    'bowl_radius':p['radius'],'arch_radius':p['arch_radius'],
                    'optical_overshoot':p['optical_overshoot'],'pair_gaps':gaps,
                    'glyph_bounds':{letter:list(shape.bounds) for letter,shape in placed}}
