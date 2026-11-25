# Research discovery

Set YST_USER_AGENT to an identifiable application User-Agent with contact URL, respecting Wikimedia API policies. Run:

```sh
python3 research.py "semiconductors"
python3 planner.py "semiconductors" --sources output/research.notes.json
python3 engine.py output/storyboard.json output/video.mp4
python3 -m unittest discover -s tests
```

The Wikimedia Action API provides keyless encyclopedia discovery. The engine preserves URLs, revision IDs when supplied, retrieval timestamps and excerpts. The notes file matches the existing planner's input contract. Multiple Wikipedia pages are not independent corroboration. Review primary sources and attribution requirements before publishing. No automatic claim entailment, credibility scoring, competitor analysis or general web search is implemented yet. Live API and local model tests remain necessary.
