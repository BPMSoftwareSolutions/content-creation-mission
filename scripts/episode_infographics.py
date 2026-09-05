"""Render source-bound infographic cutaways into an episode using the shared flow plan."""
import argparse
import copy
import io
import json
import math
import subprocess
from pathlib import Path

import cairosvg
import numpy as np
from lxml import etree
from PIL import Image, ImageDraw, ImageFilter

from capability_page_contract import Circuit, Inputs, load_circuit, require
from infographic_contract import ROOT, read, digest
from render_episode_one import font, txt, wrap

W, H = 1920, 1080
EDIT = ROOT / 'declarations/episode-01-infographic-edit.json'
CACHE = ROOT / 'outputs/episode-infographic-cache'
SVG = 'http://www.w3.org/2000/svg'


class Arc:
    """Dense arc-length table over the exact cubic controls; no replacement layout."""
    def __init__(self, projection, edge):
        route = projection['layout']['paths'][edge['id']]
        controls = np.array(route['points'], dtype=float)
        points = []
        source = projection['layout']['junctionGlyphs'].get(edge['source'], {}).get('hub')
        target = projection['layout']['junctionGlyphs'].get(edge['target'], {}).get('hub')
        if source:
            points.append(source)
        if route['kind'] == 'bezier':
            t = np.linspace(0, 1, 513)[:, None]
            for start in range(0, len(controls)-3, 3):
                a, b, c, z = controls[start:start+4]
                points.extend(((1-t)**3*a+3*(1-t)**2*t*b+3*(1-t)*t*t*c+t**3*z).tolist())
        else:
            points.extend(controls.tolist())
        if target:
            points.append(target)
        self.points = np.array(points)
        self.distances = np.r_[0., np.cumsum(np.linalg.norm(np.diff(self.points, axis=0), axis=1))]
        self.length = float(self.distances[-1])

    def point(self, distance):
        s = np.clip(distance, 0, self.length)
        return np.array([np.interp(s, self.distances, self.points[:, i]) for i in (0, 1)])


class Plate:
    def __init__(self, product, crop):
        self.projection = p = product['projection']; self.crop = crop
        self.scale = min(1792 / crop[2], 704 / crop[3])
        self.size = (round(crop[2]*self.scale), round(crop[3]*self.scale))
        self.offset = ((W-self.size[0])//2, 238+(704-self.size[1])//2)
        self.root = etree.fromstring(product['enhancedSvg'].encode())
        self.root.set('viewBox', ' '.join(map(str, crop)))
        self.root.set('width', str(self.size[0])); self.root.set('height', str(self.size[1]))
        self.background = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=etree.tostring(self.root)))).convert('RGBA')
        chosen = {id for beat in p['animationBeats'] for id in beat['edgeIds']}
        edges = [e for e in p['edges'] if e['id'] in chosen and e['type'] in ('transition', 'product-transfer')]
        self.arcs = {edge['id']: Arc(p, edge) for edge in edges}
        payload = json.dumps({'projection': p, 'lengths': {id: arc.length for id, arc in self.arcs.items()}})
        result = subprocess.run(['node', str(ROOT/'scripts/export_episode_flow.cjs')], input=payload, capture_output=True, text=True, check=True)
        shared = json.loads(result.stdout); self.plan = shared['plan']
        self.balls = []
        diameter = round(72*self.scale)
        for angle in range(0, 360, 6):
            body = shared['artwork']['body'].replace('data-flow-roll="sphere"', f'data-flow-roll="sphere" transform="rotate({angle})"')
            svg = f'<svg xmlns="{SVG}" viewBox="-36 -36 72 72" width="{diameter}" height="{diameter}"><defs>{shared["artwork"]["definitions"]}</defs>{body}</svg>'
            self.balls.append(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert('RGBA'))
        self.glows = {}

    def xy(self, point):
        return ((point[0]-self.crop[0])*self.scale, (point[1]-self.crop[1])*self.scale)

    def glow(self, id, color='#d3f0ff'):
        key = (id, color)
        if key not in self.glows:
            root = etree.Element(f'{{{SVG}}}svg', nsmap=self.root.nsmap, attrib=dict(self.root.attrib))
            for defs in self.root.findall(f'{{{SVG}}}defs'):
                root.append(copy.deepcopy(defs))
            group = self.root.xpath('//*[@id=$id]', id=id)[0]
            out = etree.SubElement(root, f'{{{SVG}}}g')
            for child in group:
                if etree.QName(child).localname not in ('rect', 'path', 'circle', 'ellipse', 'line', 'polygon', 'polyline'):
                    continue
                shape = copy.deepcopy(child); shape.set('fill', 'none'); shape.set('stroke', color)
                shape.set('stroke-width', '5'); shape.attrib.pop('id', None); out.append(shape)
            mask = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=etree.tostring(root)))).convert('RGBA')
            bbox = mask.getbbox()
            if bbox:
                bbox = (max(0,bbox[0]-22),max(0,bbox[1]-22),min(mask.width,bbox[2]+22),min(mask.height,bbox[3]+22))
                mask = mask.crop(bbox)
                halo = mask.filter(ImageFilter.GaussianBlur(7)); halo.alpha_composite(mask)
                self.glows[key] = (halo, bbox[:2])
            else:
                self.glows[key] = (Image.new('RGBA',(1,1)), (0,0))
        return self.glows[key]

    def anchor(self, name):
        if name == 'start': return 0.
        if name == 'end': return self.plan['duration']
        _, id, field = name.split(':')
        return self.plan['nodes'][id][field]

    def frame(self, time, highlights=(), animate=True):
        image = self.background.copy(); d = ImageDraw.Draw(image)
        if animate:
            for id, timing in self.plan['nodes'].items():
                if timing['start'] <= time < timing['release']:
                    halo, at = self.glow(id); image.alpha_composite(halo, at)
            for flight in self.plan['flights']:
                arc = self.arcs[flight['id']]; distance = max(0, min(arc.length, (time-flight['start'])*self.plan['speed']))
                if flight['start'] <= time < flight['end']:
                    trail = [self.xy(arc.point(s)) for s in np.linspace(max(0, distance-90), distance, 24)]
                    d.line(trail, fill=(220,240,255,175), width=3)
                    self.ball(image, arc.point(distance), distance)
                elif time >= flight['end']:
                    node = self.plan['nodes'][flight['target']]
                    if self.projection['layout']['junctionGlyphs'].get(flight['target'], {}).get('hub') and time < node['release']:
                        self.ball(image, arc.point(arc.length), arc.length)
            for id in self.plan['roots']:
                timing = self.plan['nodes'][id]
                if timing['start'] <= time < timing['release']:
                    edge = next(f for f in self.plan['flights'] if f['source'] == id)
                    self.ball(image, self.arcs[edge['id']].point(0), 0)
            for node in self.projection['junctions']:
                if node['type'] != 'convergence' or node['id'] not in self.plan['nodes']: continue
                timing = self.plan['nodes'][node['id']]; arrived = sum(t <= time for t in timing['arrivals'])
                if arrived and time < timing['release']:
                    x,y = self.xy(self.projection['layout']['junctionGlyphs'][node['id']]['hub'])
                    label = f'{arrived} / {timing["required"]}' + (' · WAIT' if arrived < timing['required'] else ' · MERGE')
                    d.text((x,y-38*self.scale), label, font=font(max(14,round(17*self.scale)),True), anchor='mm',fill='#e9f3ff')
        for id in highlights:
            node = next((n for n in self.projection['nodes']+self.projection['junctions'] if n['id'] == id),None)
            halo, at = self.glow(id, '#efbe77' if node and node['basis']=='GAP' else '#d3f0ff'); image.alpha_composite(halo, at)
        return image

    def ball(self, image, point, distance):
        angle = distance/14*180/math.pi
        ball = self.balls[round(angle/6)%len(self.balls)]
        x,y = self.xy(point); image.alpha_composite(ball,(round(x-ball.width/2),round(y-ball.height/2)))


class EpisodeInfographics:
    def __init__(self, edit=EDIT):
        self.inputs = Inputs(); self.edit = read(self.inputs.file(edit))
        require(self.edit['version']=='episode-infographic-edit.v1','EPISODE_EDIT_VERSION')
        self.timeline = read(self.inputs.file(self.edit['timeline']['path'],self.edit['timeline']['sha256']))
        self.inputs.file('templates/circuit-flow.js', self.edit['flowEngineSha256'])
        self.inputs.file('scripts/export_episode_flow.cjs'); self.inputs.file('scripts/episode_infographics.py')
        self.inputs.file('scripts/render_episode_one.py')
        self.plates = {}
        for key, spec in self.edit['circuits'].items():
            product = load_circuit(Circuit.model_validate(spec['binding']),self.edit['capabilityId'],self.inputs)
            self.plates[key] = Plate(product, spec['crop'])
        self.chapters = {c['id']: c for c in self.timeline['chapters']}
        for id, spec in self.edit['chapters'].items():
            chapter = self.chapters[id]
            require(spec['reality']==chapter['reality'],'EPISODE_REALITY_MISMATCH')
            ends = 0
            for scene in spec['scenes']:
                require(abs(scene['start']-ends)<.001 and scene['end']>scene['start'],'EPISODE_SCENE_GAP')
                ends = scene['end']; require(scene['circuit'] in self.plates,'UNKNOWN_EPISODE_CIRCUIT')
            require(abs(ends-chapter['duration'])<.001,'EPISODE_SCENE_DURATION')
            for key, knots in spec['flowCues'].items():
                times = [t for t,_ in knots]; values = [self.plates[key].anchor(a) for _,a in knots]
                require(times == sorted(times) and len(set(times)) == len(times),'EPISODE_CUE_ORDER')
                require(values == sorted(values),'EPISODE_FLOW_REVERSES')
        CACHE.mkdir(parents=True,exist_ok=True)

    def flow_time(self, spec, key, time):
        knots = spec['flowCues'].get(key)
        if not knots: return 0
        return float(np.interp(time,[t for t,_ in knots],[self.plates[key].anchor(a) for _,a in knots]))

    def frame(self, chapter, local):
        spec = self.edit['chapters'][chapter['id']]
        scene = next((s for s in spec['scenes'] if s['start'] <= local < s['end']),spec['scenes'][-1])
        plate = self.plates[scene['circuit']]
        cue = next((c for c in reversed(spec['captions']) if local>=c['at']),spec['captions'][0])
        highlights = [id for c in spec.get('highlights',[]) if c['circuit']==scene['circuit'] and c['start']<=local<c['end'] for id in c['ids']]
        image = Image.new('RGBA',(W,H),'#07131e'); d=ImageDraw.Draw(image)
        color={'CURRENT':'#73ded5','GAP':'#efbe77','TARGET':'#b6a4ff'}[spec['reality']]
        txt(d,(64,32),'SIDEFX  /  THE FUTURE OF AGENTIC ENGINEERING',20,'#83dad3',True)
        d.text((1856,36),'S01 / E01  ·  '+chapter['section'].upper(),font=font(18,True),fill='#a7bdc9',anchor='ra')
        txt(d,(64,90),scene['title'],51,'#f2f1eb',True)
        txt(d,(64,162),scene['subtitle'],23,color)
        d.line((64,210,1856,210),fill='#2c4656',width=1)
        material=plate.frame(self.flow_time(spec,scene['circuit'],local),highlights,scene.get('animate',True))
        image.alpha_composite(material,plate.offset)
        d=ImageDraw.Draw(image);d.line((64,962,1856,962),fill='#2c4656',width=1)
        txt(d,(64,982),cue['text'],25,color,True)
        txt(d,(64,1027),'SOURCE-BOUND CIRCUIT  ·  '+scene['basisLabel'],17,'#a7bdc9')
        d.text((1856,1030),'ILLUSTRATIVE MOTION / NO LIVE EXECUTION',font=font(15),fill='#a7bdc9',anchor='ra')
        return image.convert('RGB')

    def receipt(self):
        return {'version':'episode-infographic-render.v1','editPath':EDIT.relative_to(ROOT).as_posix(),
                'editSha256':digest(EDIT),'inputs':dict(sorted(self.inputs.hashes.items())),
                'chapters':self.edit['chapters'],'plans':{key:plate.plan for key,plate in self.plates.items()},
                'meaning':'Illustrative rendering, never live capability execution.'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--preview',action='store_true');args=parser.parse_args()
    editor=EpisodeInfographics()
    if args.preview:
        frames=[]
        for chapter,time in [('open-event',4),('open-event',7.2),('open-event',13),('open-event',20),('evidence',5.9),('evidence',19)]:
            frame=editor.frame(editor.chapters[chapter],time)
            frame.save(CACHE/f'{chapter}-{time}.png')
            frames.append(frame.resize((960,540),Image.Resampling.LANCZOS))
        sheet=Image.new('RGB',(1920,1620))
        for i,frame in enumerate(frames):sheet.paste(frame,(i%2*960,i//2*540))
        sheet.save(ROOT/'evaluations/episode-01-infographic-preview.jpg',quality=94)
    (CACHE/'render-plan.json').write_text(json.dumps(editor.receipt(),indent=2)+'\n',encoding='utf-8')
    print('Validated three infographic plates and two chapter edits.',flush=True)


if __name__=='__main__':main()
