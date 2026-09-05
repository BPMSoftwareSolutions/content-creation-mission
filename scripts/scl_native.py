"""Inspect a bounded native graph neighborhood without changing its edge language."""
import graphviz
import svgwrite
from scl import need, resolve_sources, graph_hash
from compile_infographics import run_dot, dot_curve, edge_path, shape, text, paragraph, font, BG, INK, MUTED


def native_view(g, focus=None):
    roots = [r for r in g.records if r.kind=='policy' and r.nativeType=='consumer-execution-embodiment-plan.v3']
    need(len(roots)==1,'NO_NATIVE_CANONICAL_GRAPH')
    src=next(s for s in g.sources if s.id==roots[0].sourceRef)
    native=resolve_sources([src])[src.id]['canonicalGraph']
    cells={c['cellId']:c for c in native['cells']}; focus=focus or native['rootCellId']
    need(focus in cells,'UNKNOWN_NATIVE_CELL')
    # A bounded lens is explicit. All records stay in SCL and can be focused next.
    children=sorted(c['cellId'] for c in cells.values() if c.get('parentCellId')==focus)
    neighbors=sorted({e[k]['cellId'] for e in native['edges'] if focus in (e['from']['cellId'],e['to']['cellId']) for k in ('from','to')}-{focus})
    visible=list(dict.fromkeys([focus]+children+neighbors))[:12]; selected=set(visible)
    edges=[e for e in native['edges'] if e['from']['cellId'] in selected and e['to']['cellId'] in selected]
    aliases={c:'c'+str(i) for i,c in enumerate(visible)}
    dot=graphviz.Digraph(graph_attr={'rankdir':'LR','nodesep':'.8','ranksep':'1.6','splines':'spline','pad':'.2'})
    for c in visible:dot.node(aliases[c],label='',shape='box',width=str(790/72),height=str(240/72),fixedsize='true')
    def side(endpoint):return 'w' if endpoint['portId']==cells[endpoint['cellId']]['input']['portId'] else 'e'
    for i,e in enumerate(edges):
        dot.edge(aliases[e['from']['cellId']]+':'+side(e['from']),aliases[e['to']['cellId']]+':'+side(e['to']),
                 id='r'+str(i),label=e['kind']+(' / '+e['selectsVariant'] if e.get('selectsVariant') else ''),fontsize='15',fontname='Segoe UI')
    raw=run_dot(dot);bb=list(map(float,raw['bb'].split(',')));w=max(1320,bb[2]+100);h=bb[3]+300;offset=((w-bb[2])/2,185)
    boxes={}
    for obj in raw.get('objects',[]):
        cid=visible[int(obj['name'][1:])];x,y=map(float,obj['pos'].split(','));boxes[cid]=[x-395+offset[0],bb[3]-y-120+offset[1]]
    d=svgwrite.Drawing(size=(w,h),viewBox=f'0 0 {w} {h}',debug=False)
    d.attribs.update({'role':'img','aria-label':'Native canonical topology / '+g.title})
    d.add(d.rect((0,0),(w,h),fill=BG));text(d,d,'SIDEFX / NATIVE CIRCUIT LENS',40,43,17,'#9de4cb',True)
    text(d,d,'Open the cell. Keep its exact relationships.',40,100,35,INK,True)
    text(d,d,f'{len(visible)} / {len(cells)} cells · {len(edges)} / {len(native["edges"])} routes · DECLARED / no execution animation',40,140,17,MUTED)
    marker=d.marker(id='native-arrow',insert=(8,4),size=(8,8),orient='auto',markerUnits='userSpaceOnUse');marker.add(d.path(d='M0 0 L8 4 L0 8 Z',fill='#9eb4ca'));d.defs.add(marker)
    route_map={o['id']:o for o in raw.get('edges',[])}
    for i,e in enumerate(edges):
        obj=route_map['r'+str(i)];points=dot_curve(obj['pos'],offset,bb[3]);kind=e['kind']
        group=d.g(id='native-route-'+str(i),**{'data-native-edge':e['edgeId'],'data-kind':kind,'data-from-port':e['from']['portId'],'data-to-port':e['to']['portId']})
        group.set_desc(title=e['edgeId'],desc=str(e))
        color='#c3aeff' if kind in ('selection','recurrence') else '#e0b675' if kind=='cancellation' else '#9eb4ca'
        path=d.path(d=edge_path({'kind':'bezier','points':points}),fill='none',stroke=color,stroke_width=2,marker_end=marker.get_funciri())
        if kind in ('return','bounded_return','recurrence','cancellation','altitude_descent'):path.attribs['stroke-dasharray']='7 5'
        group.add(path)
        if obj.get('lp'):
            x,y=map(float,obj['lp'].split(','));text(d,group,kind+(' / '+e['selectsVariant'] if e.get('selectsVariant') else ''),x+offset[0],bb[3]-y+offset[1],15,color,anchor='middle')
        d.add(group)
    for cid in visible:
        c=cells[cid];x,y=boxes[cid];group=d.g(id=aliases[cid],**{'data-native-cell':cid,'data-altitude':c['altitude']})
        group.set_desc(title=cid,desc=c['execution']['authorityId'])
        label=c.get('semanticAddress',cid).split('/operation/')[-1]
        short=label
        while short and font(18,True).getlength(short+'…')>770:short=short[:-1]
        text(d,group,short+'…' if short!=label else label,x,y+26,18,INK,True)
        text(d,group,c['altitude'].upper()+' / '+c['execution']['kind'],x,y+53,12,'#a5e1cb')
        for j,(role,color) in enumerate([('input','#91c3ff'),('event','#8ddbe4'),('outcome','#a7e5c4')]):
            xx=x+j*285;shape(d,group,role,xx,y+70,220,100,color)
            value=c['input']['contractId'] if role=='input' else c['execution']['authorityId'] if role=='event' else c['outcome']['contractId']
            text(d,group,role.upper(),xx+18,y+94,11,color,True)
            paragraph(d,group,value[:65]+'…' if len(value)>66 else value,xx+18,y+118,183,13,INK)
            if j<2:group.add(d.line((xx+220,y+120),(xx+285,y+120),stroke='#537782',stroke_width=2))
        text(d,group,'DECLARED CELL BOUNDARY / product and experience remain distinct',x,y+210,11,MUTED)
        d.add(group)
    text(d,d,'Native edge kinds and exact input / outcome port identities are preserved. Hidden cells are listed in the receipt.',40,h-32,14,MUTED)
    return dict(svg=d.tostring(),focus=focus,cells=[dict(id=c['cellId'],altitude=c['altitude'],parentId=c.get('parentCellId')) for c in native['cells']],
        receipt=dict(kind='SCL_NATIVE_TOPOLOGY_LENS',graphSha256=graph_hash(g),source=src.model_dump(),
            visibleCellIds=visible,hiddenCellCount=len(cells)-len(visible),omittedDirectChildren=children[len([c for c in children if c in selected]):],
            visibleEdgeIds=[e['edgeId'] for e in edges],hiddenEdgeCount=len(native['edges'])-len(edges),
            visibleEdgeKinds=sorted({e['kind'] for e in edges}),motion='NOT_SUPPORTED_FOR_NATIVE_PROFILE',effects='NONE'))
