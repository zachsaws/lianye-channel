import json,subprocess
from pathlib import Path
q=Path(__file__).resolve().parents[1]/'qa'
for name in ['route','story']:
 d=q/f'motion-{name}';frames=json.loads((d/'frames.json').read_text());out=[]
 for i,f in enumerate(frames):
  duration=max(.04,min(4.5,(frames[i+1]['time']-f['time'])if i+1<len(frames) else 1.0))
  out += [f"file '{f['file']}'",f'duration {duration:.5f}']
 out += [f"file '{frames[-1]['file']}'"]
 (d/'concat.txt').write_text('\n'.join(out)+'\n')
 subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(d/'concat.txt'),'-vf','fps=20,pad=ceil(iw/2)*2:ceil(ih/2)*2','-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(q/f'motion-{name}.mp4')],check=True)
print('real-browser recordings encoded')
