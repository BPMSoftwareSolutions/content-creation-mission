"""Create and bind the lightweight web derivative of the full-quality film."""
import json, shutil, subprocess
import imageio_ffmpeg
from produce_episode_two import ROOT, OUT, SITE, dump, digest, public_data

def main():
    source=OUT/'episode-02-directed.mp4';web=OUT/'episode-02-web.mp4';receipt=OUT/'web-film.receipt.json'
    cached=json.loads(receipt.read_text()) if receipt.exists() else {}
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    if not (web.exists() and cached.get('sourceSha256')==digest(source) and cached.get('webSha256')==digest(web)):
        subprocess.run([ff,'-hide_banner','-loglevel','error','-y','-i',str(source),'-vf','scale=1280:720','-c:v','libx264','-preset','fast','-crf','24','-c:a','aac','-b:a','96k','-movflags','+faststart',str(web)],check=True)
    subprocess.run([ff,'-hide_banner','-loglevel','error','-xerror','-i',str(web),'-f','null','-'],check=True)
    dump(receipt,{'sourceSha256':digest(source),'webSha256':digest(web),'webBytes':web.stat().st_size,'format':'1280x720 H264 AAC; full timeline; no editorial changes','decode':'PASS'})
    shutil.copy2(web,SITE/'episode-02.mp4')
    release=json.loads((OUT/'release.json').read_text(encoding='utf-8'));release['webFilmSha256']=digest(web)
    dump(OUT/'release.json',release);dump(ROOT/'release-site/app/episode-two.json',public_data(release))
    print('WEB DERIVATIVE VERIFIED',web.stat().st_size,flush=True)

if __name__=='__main__':main()
