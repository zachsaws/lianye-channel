import json,subprocess,sys
from pathlib import Path
q=Path(__file__).resolve().parents[1]/'qa'
names=sys.argv[1:] or ['hero','network','software','launch']
for name in names:
 d=q/f'motion-{name}';a=json.loads((d/'frames.json').read_text());rows=[]
 for i,f in enumerate(a):
  dt=max(.04,min(6,a[i+1]['time']-f['time'])) if i+1<len(a) else 1
  rows.extend(["file '"+f['file']+"'",f'duration {dt:.5f}'])
 rows.append("file '"+a[-1]['file']+"'");(d/'concat.txt').write_text('\n'.join(rows)+'\n')
 subprocess.run(['/opt/homebrew/bin/ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(d/'concat.txt'),'-vf','fps=20,pad=ceil(iw/2)*2:ceil(ih/2)*2','-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(q/f'{name}-motion.mp4')],check=True)
if 'hero' in names:subprocess.run(['/opt/homebrew/bin/ffmpeg','-y','-loglevel','error','-i',str(q/'hero-motion.mp4'),'-filter_complex','[0:v]fps=8,scale=900:-2:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128:stats_mode=diff[p];[s1][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle','-loop','0',str(q/'hero-motion.gif')],check=True)
print('4 real browser recordings and default-hero GIF encoded')
