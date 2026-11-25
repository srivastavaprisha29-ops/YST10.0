"""Transparent diagnostic metrics, not a learned aesthetic score."""
from PIL import Image
from reference_assets import palette

def rgb(hex_color):
    return tuple(int(hex_color[i:i+2],16) for i in (1,3,5))

def palette_distance(reference, candidate):
    def directed(a,b):
        return sum(x["weight"] * min(sum((u-v)**2 for u,v in zip(rgb(x["hex"]),rgb(y["hex"])))**0.5 for y in b) for x in a)
    return (directed(reference,candidate)+directed(candidate,reference))/(2*255*3**0.5)

def inspect_frame(path, reference_palette=None, target_size=None):
    with Image.open(path) as src:
        image=src.convert("RGB")
    result={"width":image.width,"height":image.height,"palette":palette(image)}
    if target_size:
        result["resolution_matches"]=image.size==tuple(target_size)
    if reference_palette:
        result["palette_distance"]=palette_distance(reference_palette,result["palette"])
    result["requires_human_review"]=True
    return result
