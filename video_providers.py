"""Trusted-operator-only local ComfyUI workflow adapter and budget-aware routing."""
import copy
import json
import time
import urllib.request
import urllib.parse
from dataclasses import dataclass
from pathlib import Path
import subprocess

@dataclass(frozen=True)
class Provider:
    name: str
    modes: tuple
    styles: tuple
    remaining_seconds: int
    cost_per_second_cents: float
    quality: float
    authorized: bool = False

def select(providers, mode, style, seconds, budget_cents):
    if seconds <= 0 or budget_cents < 0:
        raise ValueError("Invalid duration or budget")
    eligible = [p for p in providers if p.authorized and mode in p.modes
        and style in p.styles and p.remaining_seconds >= seconds
        and 0 <= p.cost_per_second_cents * seconds <= budget_cents]
    if not eligible:
        raise RuntimeError("No compatible authorized capacity; queue or request approval")
    return max(eligible, key=lambda p: (p.quality, -p.cost_per_second_cents))

class ComfyLocal:
    base = "http://127.0.0.1:8188"
    def request(self, path, payload=None):
        req = urllib.request.Request(self.base+path,
            data=json.dumps(payload).encode() if payload is not None else None,
            headers={"Content-Type":"application/json"})
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.load(response)

    def submit(self, workflow, bindings, *, operator_approved=False):
        if not operator_approved:
            raise PermissionError("Only trusted, reviewed offline workflows are allowed")
        graph = copy.deepcopy(workflow)
        for node, field, value in bindings:
            if field not in graph[node]["inputs"]:
                raise ValueError("Unknown workflow input")
            graph[node]["inputs"][field] = value
        result = self.request("/prompt", {"prompt":graph})
        return result["prompt_id"]

    def wait(self, job_id, timeout=1800):
        deadline = time.monotonic()+timeout
        while time.monotonic()<deadline:
            row = self.request("/history/"+urllib.parse.quote(job_id,safe="")).get(job_id)
            if row:
                status=row.get("status",{})
                if status.get("status_str")=="error":
                    raise RuntimeError("Workflow failed")
                if status.get("completed"):
                    return row["outputs"]
            time.sleep(3)
        raise TimeoutError("Job may still be running; retain ID and resume polling")

    def download_video(self, entry, target):
        if entry.get("type")!="output" or Path(entry["filename"]).suffix.lower() not in (".mp4",".webm",".mov"):
            raise ValueError("Expected video output")
        query=urllib.parse.urlencode({k:entry.get(k,"") for k in ("filename","subfolder","type")})
        target=Path(target)
        if target.exists():
            raise FileExistsError(target)
        try:
            with urllib.request.urlopen(self.base+"/view?"+query,timeout=60) as response, target.open("xb") as out:
                total=0
                while chunk:=response.read(1024*1024):
                    total+=len(chunk)
                    if total>1024**3:
                        raise ValueError("Output exceeds 1 GiB")
                    out.write(chunk)
            info=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(target)]))
            if not any(s.get("codec_type")=="video" for s in info["streams"]):
                raise ValueError("Missing video stream")
            return info
        except Exception:
            target.unlink(missing_ok=True)
            raise
