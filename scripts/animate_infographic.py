"""Manim traces compiled paths and reveals the exact SVG groups, without redrawing meaning."""
import copy
import io
import math
import subprocess
from pathlib import Path

import cairosvg
import imageio_ffmpeg
import networkx as nx
import numpy as np
from lxml import etree
from PIL import Image
from manim import Scene,ImageMobject,Text,Rectangle,VMobject,Dot,FadeIn,FadeOut,Create,MoveAlongPath,AnimationGroup,linear,tempconfig

from infographic_contract import ROOT,read,write,digest,validate

DEST=ROOT/'samples/infographic-grammar/scenario-target'
P=read(DEST/'projection.json');G=P['layout'];W,H=G['width'],G['height'];SCALE=1920/W
ASSETS=ROOT/'outputs/infographic-motion-assets';ASSETS.mkdir(parents=True,exist_ok=True)

def point(x,y):return np.array([(x/W-.5)*16,(.5-y/H)*(H/W*16),0.])

def prepare():
    root=etree.parse(str(DEST/'infographic.svg')).getroot();background=copy.deepcopy(root)
    for group in background.xpath('//*[@data-entity or @data-edge]'):group.set('opacity','.2')
    cairosvg.svg2png(bytestring=etree.tostring(background),write_to=str(ASSETS/'background.png'),output_width=1920)
    for id,box in G['boxes'].items():
        isolated=etree.Element(root.tag,nsmap=root.nsmap,attrib=dict(root.attrib))
        for child in root:
            if etree.QName(child).localname=='defs' or child.get('id')==id:isolated.append(copy.deepcopy(child))
        # Rasterize each original group separately; crop only its measured geometry.
        image=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=etree.tostring(isolated),output_width=1920)))
        x,y,w,h=box;crop=[math.floor((x-10)*SCALE),math.floor((y-16)*SCALE),math.ceil((x+w+10)*SCALE),math.ceil((y+h+32)*SCALE)]
        image.crop(crop).save(ASSETS/(id+'.png'));G.setdefault('motionCrops',{})[id]=crop
    for edge in P['edges']:
        isolated=etree.Element(root.tag,nsmap=root.nsmap,attrib=dict(root.attrib))
        for child in root:
            if etree.QName(child).localname=='defs' or child.get('id')==edge['id']:isolated.append(copy.deepcopy(child))
        cairosvg.svg2png(bytestring=etree.tostring(isolated),write_to=str(ASSETS/(edge['id']+'.png')),output_width=1920)

class CircuitMotion(Scene):
    def construct(self):
        self.camera.background_color='#07131e'
        self.add(ImageMobject(str(ASSETS/'background.png')).scale_to_fit_width(16))
        nodes={n['id']:n for n in P['nodes']+P['junctions']};edges={e['id']:e for e in P['edges']}
        sprites={}
        for id,crop in G['motionCrops'].items():
            x1,y1,x2,y2=crop;sprites[id]=ImageMobject(str(ASSETS/(id+'.png'))).scale_to_fit_width((x2-x1)/1920*16).move_to(point((x1+x2)/2/SCALE,(y1+y2)/2/SCALE))
        self.phase_text=None;self.timeline=[];shown=set();traced=set()
        def stamp(kind,ids):self.timeline.append({'seconds':round(float(self.time),3),'action':kind,'ids':ids})
        def reveal(ids):
            ids=[id for id in ids if id not in shown]
            if ids:self.play(*[FadeIn(sprites[id]) for id in ids],run_time=.6);shown.update(ids);stamp('reveal',ids)
        def trace(ids):
            jobs=[];dots=[];paths=[]
            for id in ids:
                if id in traced:continue
                spec=G['paths'][id];coords=np.array([point(x,y) for x,y in spec['points']]);path=VMobject(stroke_color='#b6a4ff',stroke_width=3)
                if spec['kind']=='bezier':path.set_points(coords)
                else:path.set_points_as_corners(coords)
                dot=Dot(coords[0],radius=.045,color='#f4edff');self.add(dot);dots.append(dot);paths.append(path)
                jobs.extend([Create(path),MoveAlongPath(dot,path,rate_func=linear)]);traced.add(id)
            if jobs:
                self.play(*jobs,run_time=1);self.remove(*dots,*paths)
                # Restore the original edge group, including arrowheads and its exact labels.
                for id in ids:self.add(ImageMobject(str(ASSETS/(id+'.png'))).scale_to_fit_width(16))
                stamp('arrive',ids)
        for i,beat in enumerate(P['animationBeats']):
            # The footer is the only text Manim authors; all circuit labels are original SVG pixels.
            if self.phase_text:self.remove(self.phase_text)
            cover=Rectangle(width=15.9,height=.4,fill_color='#07131e',fill_opacity=1,stroke_width=0).move_to(point(W/2,G['legendY']+102))
            label=Text(f'{i+1:02d}  {beat["phase"].upper()}  /  {beat["caption"]}',font='Segoe UI',font_size=18,color='#f2f0e9')
            if label.width>15.2:label.scale_to_fit_width(15.2)
            label.move_to(cover);self.add(cover,label);self.phase_text=label;stamp('phase',[beat['phase']])
            pending=set(beat['entityIds']);support=[id for id in pending if nodes[id]['layer']=='support'];reveal(support);pending-=set(support)
            info=[id for id in beat['edgeIds'] if edges[id]['type'] not in ('transition','product-transfer','retry')]
            if info:
                self.play(*[FadeIn(ImageMobject(str(ASSETS/(id+'.png'))).scale_to_fit_width(16)) for id in info],run_time=.4);stamp('information-attachment',info)
            while pending:
                ready=[]
                for id in sorted(pending):
                    incoming=[e for e in P['edges'] if e['target']==id and e['type'] in ('transition','product-transfer')]
                    parents=[e['source'] for e in incoming]
                    if not parents or all(parent in shown for parent in parents):ready.append(id)
                if not ready:raise ValueError('MOTION_CANNOT_RESOLVE_PENDING:'+str(sorted(pending)))
                inbound=[e['id'] for e in P['edges'] if e['target'] in ready and e['type'] in ('transition','product-transfer')]
                if not set(inbound)<=set(beat['edgeIds']):raise ValueError('MOTION_EDGE_PHASE_MISMATCH:'+str(inbound))
                trace(inbound);reveal(ready);pending-=set(ready)
                if any(nodes[id]['type']=='convergence' for id in ready):self.wait(.7)
            self.wait(1.6 if i<4 else 4)
        write(DEST/'motion-timeline.json',{'meaning':'Illustrative target timing, not execution telemetry.','contractSha256':P['contractSha256'],'events':self.timeline,'durationSeconds':round(float(self.time),3)})

def main():
    p=validate(read('declarations/infographics/scenario-target.json'))
    if digest(ROOT/'declarations/infographics/scenario-target.json')!=P['contractSha256']:raise ValueError('STALE_MOTION_CONTRACT')
    prepare()
    with tempconfig({'pixel_width':1920,'pixel_height':1080,'frame_width':16,'frame_height':9,'frame_rate':24,'media_dir':str(ASSETS/'manim'),'output_file':'circuit-motion','disable_caching':True,'verbosity':'WARNING','progress_bar':'none','write_to_movie':True}):
        scene=CircuitMotion();scene.render();source=Path(scene.renderer.file_writer.movie_file_path)
    result=DEST/'circuit-motion.mp4'
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-i',str(source),'-c','copy','-movflags','+faststart',str(result)],capture_output=True,check=True)
    import av
    with av.open(str(result)) as media:
        stream=media.streams.video[0];frames=sum(1 for _ in media.decode(video=0));duration=frames/float(stream.average_rate)
    write(DEST/'motion-receipt.json',{'status':'RENDERED_AND_DECODED','renderer':'Manim 0.21.0 / Cairo + FFmpeg','contractSha256':P['contractSha256'],'staticSvgSha256':digest(DEST/'infographic.svg'),'videoSha256':digest(result),'timelineSha256':digest(DEST/'motion-timeline.json'),'width':1920,'height':1080,'frames':frames,'fps':24,'durationSeconds':duration,'evidence':'Media rendering proof only. No capability execution is asserted.'})
    print('MANIM_RENDERED',frames,'frames',round(duration,2),'seconds',flush=True)

if __name__=='__main__':main()
