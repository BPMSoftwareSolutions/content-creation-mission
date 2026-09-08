"""Lay out complete source graphs with Graphviz and the established SCL shapes."""
import hashlib,json
from functools import lru_cache
import graphviz,svgwrite
from lxml import etree
from compile_infographics import run_dot,dot_curve,edge_path,shape,text,font,wrap,GRAMMAR
from enhance_infographics import material_sprite
from scl_render import materials

BG='#071722';INK='#e8efee';MUTED='#91acb5'
SUPPORT={'provider-binding','scenario-call','scenario-return','argument-dependency','conditional-argument'}
RETURNS={'return','recurrence','bounded_return','BOUNDED_RETURN','scenario-return'}
def color(edge):
    if edge['kind'] in RETURNS:return '#b8a0e9'
    if edge['kind'] in ('selection','BRANCH_ROUTE','conditional-argument'):return '#ddb877'
    if edge['kind'] in ('provider-binding','altitude_descent','ALTITUDE_DESCENT'):return '#82a8f9'
    if edge['kind']=='cancellation':return '#efaa91'
    return '#85bcc3'

@lru_cache(None)
def sprite(kind,w,h):
    drawing=svgwrite.Drawing(debug=False);group=drawing.g();shape(drawing,group,kind,0,0,w,h,'#9ce4e7')
    raw,_=material_sprite(etree.fromstring(group.tostring().encode()),[0,0,w,h],kind,materials()[kind])
    return raw

def render_topology(view,texture_writer):
    nodes=view['nodes'];byid={n['id']:n for n in nodes};aliases={n['id']:'n'+str(i) for i,n in enumerate(nodes)}
    dims={n['id']:(270,176 if n['kind']=='decision' else 135) for n in nodes}
    dot=graphviz.Digraph(graph_attr={'rankdir':'LR','nodesep':'.55','ranksep':'1.0','splines':'spline','pad':'.35','nslimit':'3','nslimit1':'3'},node_attr={'fixedsize':'true'},edge_attr={'fontname':'Segoe UI','fontsize':'11'})
    for n in nodes:
        w,h=dims[n['id']];dot.node(aliases[n['id']],label='',shape='diamond' if n['kind']=='decision' else 'box',width=str(w/72),height=str((h+45)/72))
    def side(e,end):
        n=byid[e['source'] if end=='from' else e['target']];port=e.get('facts',{}).get(end,{}).get('portId')
        if port:return 'w' if port==n['facts'].get('input',{}).get('portId') else 'e'
        return 'e' if end=='from' else 'w'
    for i,e in enumerate(view['edges']):
        label=e['label'];label=label[:47]+'…' if len(label)>48 else label
        dot.edge(aliases[e['source']]+':'+side(e,'from'),aliases[e['target']]+':'+side(e,'to'),id='e'+str(i),label=label,constraint='false' if e['kind'] in RETURNS or e['kind']=='provider-binding' else 'true')
    raw=run_dot(dot);bounds=list(map(float,raw.get('bb','0,0,800,400').split(',')));width=max(860,bounds[2]+80);height=max(260,bounds[3]+65);offset=((width-bounds[2])/2,20)
    drawing=svgwrite.Drawing(size=(width,height),viewBox=f'0 0 {width} {height}',debug=False)
    drawing.attribs.update({'role':'group','aria-label':view['label']})
    drawing.add(drawing.rect((0,0),(width,height),fill=BG))
    marker=drawing.marker(id=view['id']+'-arrow',insert=(9,4),size=(10,8),orient='auto',markerUnits='userSpaceOnUse');marker.add(drawing.path(d='M0 0 L9 4 L0 8',fill='none',stroke='#a3c3cd',stroke_width=1.8));drawing.defs.add(marker)
    curves={e['id']:e for e in raw.get('edges',[])}
    for i,e in enumerate(view['edges']):
        obj=curves['e'+str(i)];points=dot_curve(obj['pos'],offset,bounds[3]);group=drawing.g(id=e['id'],**{'data-route':e['id'],'data-source':e['source'],'data-target':e['target'],'role':'button','tabindex':'0','aria-label':e['kind']+': '+e['label']})
        group.set_desc(title=e['identity'],desc=e['kind']+' / '+e['label'])
        path=drawing.path(d=edge_path({'points':points,'kind':'bezier'}),fill='none',stroke=color(e),stroke_width=2)
        path.attribs['class']='route-path'
        if e['kind']!='provider-binding':path.attribs['marker-end']=marker.get_funciri()
        if e['kind'] in RETURNS or e['kind']=='provider-binding':path.attribs['stroke-dasharray']='7 5'
        group.add(path)
        if obj.get('lp'):
            x,y=map(float,obj['lp'].split(','));label=e['label'][:47]+'…' if len(e['label'])>48 else e['label'];text(drawing,group,label,x+offset[0],bounds[3]-y+offset[1],12,color(e),anchor='middle')
        drawing.add(group)
    boxes={}
    for obj in raw.get('objects',[]):
        if not obj['name'].startswith('n'):continue
        n=nodes[int(obj['name'][1:])];w,h=dims[n['id']];x,y=map(float,obj['pos'].split(','));x=x-w/2+offset[0];y=bounds[3]-y-h/2+offset[1];boxes[n['id']]=[x,y,w,h]
        kind=n['kind'];canonical=kind if kind!='unresolved' else 'rejection';spec=(GRAMMAR['nodeTypes']|GRAMMAR['junctionTypes'])[canonical];c=spec['color']
        group=drawing.g(id=n['id'],**{'data-entity':n['id'],'data-type':canonical,'role':'button','tabindex':'0','aria-label':kind+': '+n['label']});group.set_desc(title=n['label'],desc=n['identity'])
        shape(drawing,group,canonical,x,y,w,h,c)
        texture=texture_writer(canonical,w,h,sprite(canonical,w,h));group.add(drawing.image(href=texture,insert=(x,y),size=(w,h),preserveAspectRatio='none',**{'class':'material'}))
        if canonical in ('fan-out','convergence','termination'):
            text(drawing,group,spec['label'].upper(),x+w/2,y-13,11,c,True,'middle');baseline=y+h+25
        else:
            pad=55 if canonical=='decision' else 28
            text(drawing,group,spec['label'].upper(),x+w/2,y+30,11,c,True,'middle')
            rows=wrap(n['label'],w-pad*2,17,True);rows=rows[:3]
            if len(wrap(n['label'],w-pad*2,17,True))>3:rows[-1]=rows[-1][:-1]+'…'
            for j,line in enumerate(rows):text(drawing,group,line,x+w/2,y+58+j*23,17,INK,True,'middle')
            baseline=y+h+23
        if canonical in ('fan-out','convergence','termination'):
            label=n['label'][:40]+'…' if len(n['label'])>41 else n['label'];text(drawing,group,label,x+w/2,baseline,15,INK,True,'middle')
        else:
            label=n['detail'];label=label[:42]+'…' if len(label)>43 else label;text(drawing,group,label,x+w/2,baseline,11,MUTED,anchor='middle')
        drawing.add(group)
    # Graphviz positions are measured, not estimated. A dropped object is a build failure.
    if set(boxes)!=set(byid):raise ValueError('TOPOLOGY_LAYOUT_OMITTED_NODE')
    for i,(aid,a) in enumerate(boxes.items()):
        for bid,b in list(boxes.items())[i+1:]:
            if a[0]<b[0]+b[2]-.1 and a[0]+a[2]>b[0]+.1 and a[1]<b[1]+b[3]-.1 and a[1]+a[3]>b[1]+.1:raise ValueError('TOPOLOGY_NODE_OVERLAP:'+aid+':'+bid)
    return {'svg':drawing.tostring(),'layout':{'width':width,'height':height,'boxes':boxes},'geometry':{'nodes':len(boxes),'routes':len(curves),'overlaps':0}}
