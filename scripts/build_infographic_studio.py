"""Package the same compiler artifacts into a file://-compatible inspection studio."""
import json
import shutil
import svgwrite
from compile_infographics import OUT,ROOT,GRAMMAR,shape,BG,read

def symbol(type,basis=None):
    d=svgwrite.Drawing(size=(156,126),viewBox='0 0 156 126',debug=False)
    color=(GRAMMAR['nodeTypes']|GRAMMAR['junctionTypes'])[type]['color']
    shape(d,d,type,12,18,132,88,color)
    return d.tostring()

def connector(type):
    d=svgwrite.Drawing(size=(180,60),viewBox='0 0 180 60',debug=False);color='#8b671f' if type=='authority' else '#23464e'
    path='M12 30 H161' if type!='retry' else 'M18 42 V16 H150 V42'
    attrs=dict(fill='none',stroke=color,stroke_width=2.5)
    if type=='dependency':attrs['stroke_dasharray']='8 5'
    if type=='evidence-attachment':attrs['stroke_dasharray']='2 6'
    d.add(d.path(d=path,**attrs))
    if type in ('transition','product-transfer','dependency'):d.add(d.polyline([(150,23),(162,30),(150,37)],fill='none' if type=='dependency' else color,stroke=color,stroke_width=2))
    if type=='product-transfer':d.add(d.polyline([(140,23),(152,30),(140,37)],fill='none',stroke=color,stroke_width=2))
    if type=='retry':d.add(d.polygon([(144,36),(150,46),(156,36)],fill=color))
    if type=='provider-binding':
        for x in (12,157):d.add(d.rect((x,24),(5,12),fill='none',stroke=color,stroke_width=2))
    return d.tostring()

def main():
    products={p.parent.name:{'projection':read(p),'svg':(p.parent/'infographic.svg').read_text(encoding='utf-8').replace('role="img"','role="group"')} for p in OUT.glob('*/projection.json')}
    data={'grammar':GRAMMAR,'products':products,'inventory':read(OUT/'estate-inventory.json'),'symbols':{type:symbol(type) for type in GRAMMAR['nodeTypes']|GRAMMAR['junctionTypes']},'connectors':{type:connector(type) for type in GRAMMAR['edgeTypes']},'modeSymbols':{mode:symbol('provider',mode) for mode in GRAMMAR['evidenceModes']}}
    (OUT/'studio-data.js').write_text('window.INFOGRAPHIC_STUDIO = '+json.dumps(data,ensure_ascii=False).replace('<','\\u003c')+';\n',encoding='utf-8')
    for extension,name in [('html','index.html'),('css','studio.css'),('js','studio.js')]:shutil.copyfile(ROOT/f'templates/infographic-studio.{extension}',OUT/name)
    print('Studio built from',len(products),'projections,',len(data['symbols']),'primitives and',len(data['connectors']),'connectors.')

if __name__=='__main__':main()
