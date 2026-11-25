# Local AI script and storyboard generation

Install Ollama and start its local service. Pull a compatible model, for example:

```sh
ollama pull qwen2.5:7b
python3 planner.py "How semiconductors work" --scenes 6
python3 engine.py output/storyboard.json output/video.mp4
python3 -m unittest discover -s tests
```

Optional: provide --sources notes.json, a JSON array of human-reviewed research notes with URLs and relevant excerpts. The planner preserves source IDs and writes a source sidecar. References are validated for existence, not factual entailment. All claims are marked unverified. No automatic web retrieval or factual verification is present yet.

The local model requires sufficient RAM and storage. Model installation and local inference have not been tested in this environment. No paid API is required. The visual prompts are stored for future image/video generation; the current renderer still renders title cards.
