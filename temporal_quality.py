"""Frame-level diagnostics; not an implementation of VBench."""
from PIL import Image, ImageChops, ImageStat

def delta(a,b):
    a=a.convert("RGB").resize((96,96))
    b=b.convert("RGB").resize((96,96))
    return sum(ImageStat.Stat(ImageChops.difference(a,b)).mean)/(3*255)

def inspect_frames(frames):
    if len(frames)<3:
        raise ValueError("At least three frames required")
    adjacent=[delta(a,b) for a,b in zip(frames,frames[1:])]
    return {"mean_frame_change":sum(adjacent)/len(adjacent),
            "max_frame_change":max(adjacent),
            "change_variation":sum(abs(a-b) for a,b in zip(adjacent,adjacent[1:]))/(len(adjacent)-1),
            "human_review_required":True}
