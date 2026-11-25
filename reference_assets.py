"""Local reference ingestion for trusted operators; not public upload moderation."""
import hashlib
import io
import json
import os
from pathlib import Path
from PIL import Image, ImageOps

MAX_BYTES = 15 * 1024 * 1024
MAX_PIXELS = 20_000_000

def ingest(raw: bytes, root: Path, *, rights_confirmed: bool):
    if not rights_confirmed:
        raise ValueError("Reference rights must be confirmed")
    if not raw or len(raw) > MAX_BYTES:
        raise ValueError("Invalid image size")
    with Image.open(io.BytesIO(raw)) as src:
        if src.format not in {"PNG", "JPEG", "WEBP"} or getattr(src, "n_frames", 1) != 1:
            raise ValueError("Only still PNG, JPEG and WebP images are accepted")
        if src.width * src.height > MAX_PIXELS:
            raise ValueError("Image exceeds pixel limit")
        image = ImageOps.exif_transpose(src).convert("RGB")
    image.thumbnail((2048, 2048), Image.Resampling.LANCZOS)
    clean = Image.new("RGB", image.size)
    clean.paste(image)
    buf = io.BytesIO()
    clean.save(buf, format="PNG")
    data = buf.getvalue()
    asset_id = hashlib.sha256(data).hexdigest()
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    target = root / (asset_id + ".png")
    fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "wb") as f:
        f.write(data)
    return {"id": asset_id, "width": clean.width, "height": clean.height,
            "palette": palette(clean), "moderation": "pending",
            "rights_confirmed": True}

def palette(image, colors=6):
    small = image.copy().convert("RGB")
    small.thumbnail((128,128))
    q = small.quantize(colors=colors)
    p = q.getpalette()
    counts = sorted(q.getcolors(), reverse=True)
    total = sum(n for n,_ in counts)
    return [{"hex": "#%02x%02x%02x" % tuple(p[i*3:i*3+3]), "weight": n/total} for n,i in counts]

def save_moodboard(root, name, assets, direction):
    if not name.strip() or len(name)>120 or not assets:
        raise ValueError("Moodboard requires name and references")
    manifest = {"name":name, "references":assets, "direction":direction,
                "generation_ready":False}
    data = json.dumps(manifest, ensure_ascii=False, sort_keys=True).encode()
    key = hashlib.sha256(data).hexdigest()
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(root/(key+".json"), os.O_WRONLY|os.O_CREAT|os.O_TRUNC, 0o600)
    with os.fdopen(fd,"wb") as f:
        f.write(data)
    return key
