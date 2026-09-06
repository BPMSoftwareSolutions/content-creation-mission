"""Render individually authored SVG elements. There is no subsection layout fallback."""
import html
from PIL import ImageFont
from production_store import read

def section_spec(store,revision,scene):
    direction=read(store.resolve(revision['sectionDirectionRef']))
    plans=[p for p in direction['sections'] if p['key']==scene['sectionVisualId']]
    if len(plans)!=1:raise ValueError('A subsection needs exactly one art-direction record')
    for field in ('format','purpose','composition','camera','motion','assetPrompt'):
        if not plans[0].get(field):raise ValueError('Missing subsection direction: '+field)
    compositions=read(store.resolve(revision['sectionCompositionRef']))['sections']
    if scene['sectionVisualId'] not in compositions:raise ValueError('Authored section composition missing; no layout fallback')
    if not compositions[scene['sectionVisualId']].get('elements'):raise ValueError('Empty subsection composition; no layout fallback')
    return plans[0],compositions[scene['sectionVisualId']]

def value_at(state,ref):
    value=state
    for key in ref.split('.'):value=value[int(key)] if isinstance(value,list) else value[key]
    return str(value)

def text_node(element,state,p):
    value=value_at(state,element['ref']) if 'ref' in element else element['value']
    size=element['size'];font=ImageFont.truetype(p['boldFontFile'] if element.get('weight',400)>=600 else p['fontFile'],size)
    width=element.get('width',1840-element['x']);lines=[]
    for paragraph in value.split('\n'):
        line=''
        for word in paragraph.split():
            candidate=(line+' '+word).strip()
            if font.getlength(word)>width:raise ValueError('Unbreakable text overflow: '+word)
            if line and font.getlength(candidate)>width:lines.append(line);line=word
            else:line=candidate
        if line:lines.append(line)
    if element['y']+(len(lines)-1)*size*1.15>850:
        raise ValueError('Text intrudes into caption area: '+value)
    x=element['x'];y=element['y'];transform=f' transform="rotate({element["rotation"]} {x} {y})"' if element.get('rotation') else ''
    return ''.join(f'<text x="{x}" y="{y+i*size*1.15}" font-family="{p["fontFamily"]}" font-size="{size}" font-weight="{element.get("weight",400)}" fill="{element["fill"]}"{transform}>{html.escape(line)}</text>' for i,line in enumerate(lines))

def svg_composition(revision,scene,state,state_index,plan,spec,p,clean=False):
    light=plan['palette']=='light';base='#fff9ed' if light else '#08131f'
    result=['<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">']
    if clean:result.append(f'<rect width="1920" height="1080" fill="{base}"/>')
    for shade in spec['shade']:
        result.append('<rect '+' '.join(f'{k}="{v}"' for k,v in shade.items())+'/>')
    for e in spec['elements']:
        if 'states' in e and state_index not in e['states']:continue
        if e['type']=='text':result.append(text_node(e,state,p));continue
        if e['type'] not in ('path','rect','circle','ellipse','line','polyline'):raise ValueError('Unsupported authored SVG primitive')
        names={'strokeWidth':'stroke-width','dash':'stroke-dasharray'}
        shape=dict(e)
        if shape['type'] in ('path','line','polyline'):shape.setdefault('fill','none')
        attrs=' '.join(f'{names.get(k,k)}="{html.escape(str(v),quote=True)}"' for k,v in shape.items() if k not in ('type','states'))
        result.append(f'<{e["type"]} {attrs}/>' )
    label=scene['status'];font=ImageFont.truetype(p['boldFontFile'],48)
    width=min(1690,font.getlength(label)+44)
    result.append(f'<rect x="55" y="31" width="{width}" height="81" rx="9" fill="{base}" fill-opacity=".95"/>')
    result.append(text_node({'value':label,'x':76,'y':87,'size':48,'weight':700,'fill':'#735430' if light else '#ffd097','width':1650},state,p))
    result.append('</svg>');return ''.join(result)
