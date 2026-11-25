"""Keyless discovery and provenance; not an automatic truth verifier."""
import argparse
import json
import os
import urllib.request
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

def request(params):
    url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(params)
    agent = os.environ.get("YST_USER_AGENT")
    if not agent:
        raise RuntimeError("Set YST_USER_AGENT to your application name and contact URL")
    req = urllib.request.Request(url, headers={"User-Agent": agent})
    with urllib.request.urlopen(req, timeout=25) as response:
        data = json.loads(response.read(4_000_000))
    if "error" in data:
        raise RuntimeError(str(data["error"]))
    return data

def normalize(data):
    pages = data.get("query", {}).get("pages", [])
    result = []
    for page in sorted(pages, key=lambda p: p.get("index", 999)):
        if not page.get("extract") or not page.get("fullurl"):
            continue
        result.append({"id":len(result)+1, "title":page["title"],
                       "url":page["fullurl"], "revision":page.get("lastrevid"),
                       "excerpt":page["extract"][:4000],
                       "retrieved_at":datetime.now(timezone.utc).isoformat(),
                       "source_type":"encyclopedia", "review_status":"unverified"})
    return result

def discover(topic, limit=5):
    if not topic.strip() or len(topic)>500 or not 1<=limit<=10:
        raise ValueError("Invalid topic or limit")
    return normalize(request({"action":"query","generator":"search","gsrsearch":topic,
        "gsrnamespace":0,"gsrlimit":limit,"prop":"extracts|info","exintro":1,
        "explaintext":1,"exlimit":limit,"inprop":"url","format":"json","formatversion":2}))

def notes(sources):
    return [f"{s['title']} | {s['url']} | revision {s['revision']} | {s['excerpt']}" for s in sources]

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("topic")
    p.add_argument("--output",type=Path,default=Path("output/research.json"))
    args=p.parse_args()
    sources=discover(args.topic)
    if not sources:
        raise SystemExit("No evidence retrieved; try a different topic")
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(sources,indent=2,ensure_ascii=False))
    args.output.with_suffix(".notes.json").write_text(json.dumps(notes(sources),indent=2,ensure_ascii=False))
