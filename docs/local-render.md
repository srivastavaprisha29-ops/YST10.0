# First local rendering milestone

Install Python 3, FFmpeg (with drawtext and libx264), espeak-ng, and a system font. On Ubuntu: `sudo apt install ffmpeg espeak-ng fonts-dejavu-core`.

Run `python3 engine.py examples/storyboard.json output/demo.mp4`.

The renderer accepts editable JSON scenes and creates a narrated 720p MP4 plus a separate SRT subtitle file. It uses deterministic title cards, not generative cinematic footage. Narration is local synthetic speech; subtitles are scene-level estimates. No API key or paid API is required. Hardware and electricity are not free.

The GitHub Actions smoke test checks whether rendering succeeds and uploads a sample. CI is for testing, not production generation. Next: local language-model storyboard adapter, browser UI, durable jobs, better graphics, and timing validation.
