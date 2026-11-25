"""Deterministic compositing of prepared transparent artwork; offline only."""
from PIL import Image
from motion_timeline import sample_keys

def compose(background, layers, t):
    canvas=background.convert("RGBA").copy()
    for layer in sorted(layers,key=lambda l:l.get("z",0)):
        art=layer["image"].convert("RGBA")
        x=round(sample_keys(layer.get("x",[(0,0)]),t))
        y=round(sample_keys(layer.get("y",[(0,0)]),t))
        angle=sample_keys(layer.get("angle",[(0,0)]),t)
        opacity=sample_keys(layer.get("opacity",[(0,1)]),t)
        if not 0<=opacity<=1: raise ValueError("Invalid opacity")
        if angle:
            art=art.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
        if opacity!=1:
            art.putalpha(art.getchannel("A").point(lambda v:round(v*opacity)))
        canvas.alpha_composite(art,dest=(x,y))
    return canvas
