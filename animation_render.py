"""Deterministic local animation of authorized still artwork, no AI credits."""
import math
import subprocess
from pathlib import Path
from PIL import Image

def render(source, output, seconds=5, fps=24, width=1280, height=720, motion="pan", pixel=False):
    if not 0<seconds<=600 or not 1<=fps<=60 or not 2<=width<=3840 or not 2<=height<=2160 or width%2 or height%2:
        raise ValueError("Invalid rendering parameters")
    if motion not in {"pan","zoom","hold"}:
        raise ValueError("Unknown motion")
    frames=round(seconds*fps)
    if frames<1:
        raise ValueError("Duration too short")
    if pixel and motion!="hold":
        raise ValueError("Pixel mode currently supports stationary integer-scaled artwork only")
    with Image.open(source) as im:
        art=im.convert("RGB")
    if pixel:
        scale=min(width//art.width,height//art.height)
        if scale<1:
            raise ValueError("Pixel artwork exceeds canvas")
        art=art.resize((art.width*scale,art.height*scale),Image.Resampling.NEAREST)
    else:
        scale=max(width/art.width,height/art.height)*(1.12 if motion!="hold" else 1)
        art=art.resize((math.ceil(art.width*scale),math.ceil(art.height*scale)),Image.Resampling.LANCZOS)
    cmd=["ffmpeg","-v","error","-n","-f","rawvideo","-pix_fmt","rgb24","-s",f"{width}x{height}","-r",str(fps),"-i","-","-an","-c:v","libx264","-crf","16","-pix_fmt","yuv420p",str(output)]
    with subprocess.Popen(cmd,stdin=subprocess.PIPE) as proc:
        for i in range(frames):
            t=i/max(1,frames-1); t=t*t*(3-2*t)
            if pixel:
                frame=Image.new("RGB",(width,height))
                frame.paste(art,((width-art.width)//2,(height-art.height)//2))
            else:
                w,h=art.size
                if motion=="zoom":
                    z=1+0.10*t
                    cw,ch=round(width/z),round(height/z)
                else:
                    cw,ch=width,height
                x=round((w-cw)*(0.25+0.5*t if motion=="pan" else 0.5))
                y=(h-ch)//2
                frame=art.crop((x,y,x+cw,y+ch)).resize((width,height),Image.Resampling.LANCZOS)
            proc.stdin.write(frame.tobytes())
        proc.stdin.close()
        if proc.wait()!=0:
            raise RuntimeError("FFmpeg failed")
    return Path(output)
