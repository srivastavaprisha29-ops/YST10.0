"""Local, deterministic narrated-video renderer. Requires ffmpeg and espeak-ng."""
import argparse
import json
import subprocess
import tempfile
import wave
from pathlib import Path

def run(*args):
    subprocess.run(args, check=True, capture_output=True)

def stamp(seconds):
    ms = round(seconds * 1000)
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def render(scenes, output):
    if not isinstance(scenes, list) or not 1 <= len(scenes) <= 100:
        raise ValueError("Provide 1–100 scenes")
    output = Path(output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        clips, captions, elapsed = [], [], 0.0
        for i, scene in enumerate(scenes):
            title, narration = scene["title"], scene["narration"]
            if not isinstance(title, str) or not isinstance(narration, str) or not narration.strip() or len(narration) > 2000 or len(title) > 120:
                raise ValueError("Invalid scene text")
            audio, clip, label = root/f"{i}.wav", root/f"{i}.mp4", root/f"{i}.txt"
            label.write_text(title, encoding="utf-8")
            run("espeak-ng", "-s", "150", "-w", str(audio), "--", narration)
            with wave.open(str(audio)) as w:
                duration = w.getnframes()/w.getframerate()
            # Use relative safe filenames and disable drawtext expansion.
            vf = f"drawtext=textfile={label}:expansion=none:fontcolor=white:fontsize=42:x=(w-tw)/2:y=(h-th)/2"
            run("ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=0x171b26:s=1280x720:r=25", "-i", str(audio), "-vf", vf, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "48000", "-ac", "1", "-shortest", str(clip))
            clips.append(clip)
            captions.append(f"{i+1}\n{stamp(elapsed)} --> {stamp(elapsed+duration)}\n{narration}\n")
            elapsed += duration
        manifest = root/"concat.txt"
        manifest.write_text("".join(f"file '{p.name}'\n" for p in clips))
        run("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "1", "-i", str(manifest), "-c", "copy", "-movflags", "+faststart", str(output))
        output.with_suffix(".srt").write_text("\n".join(captions), encoding="utf-8")
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("storyboard", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(render(json.loads(args.storyboard.read_text()), args.output))
