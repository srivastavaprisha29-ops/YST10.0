"""Frame-accurate action planning for fictional characters and reusable assets."""
from dataclasses import dataclass
from fractions import Fraction

@dataclass(frozen=True)
class Action:
    actor: str
    channel: str
    start: int
    end: int
    kind: str
    target: str = ""

def frame(seconds, fps):
    return round(Fraction(str(seconds))*fps)

def validate(actions, duration_frames, actors):
    if duration_frames<1:
        raise ValueError("Invalid duration")
    channels={"body","face","mouth","gaze","camera","prop"}
    tracks={}
    for a in actions:
        if a.actor not in actors or a.channel not in channels or not 0<=a.start<a.end<=duration_frames:
            raise ValueError("Invalid action")
        tracks.setdefault((a.actor,a.channel),[]).append(a)
    for track in tracks.values():
        track.sort(key=lambda a:a.start)
        if any(a.end>b.start for a,b in zip(track,track[1:])):
            raise ValueError("Conflicting actions on same track")
    return tracks

def sample_keys(keys, t):
    if not keys or any(a[0]>=b[0] for a,b in zip(keys,keys[1:])):
        raise ValueError("Keyframes must be strictly ordered")
    if t<=keys[0][0]: return keys[0][1]
    for (a,x),(b,y) in zip(keys,keys[1:]):
        if t<=b:
            u=(t-a)/(b-a); u=u*u*(3-2*u)
            return x+(y-x)*u
    return keys[-1][1]

def speech_actions(actor, cues, fps):
    """Convert externally aligned viseme intervals into mouth track actions."""
    return [Action(actor,"mouth",frame(c["start"],fps),frame(c["end"],fps),c["viseme"]) for c in cues if frame(c["end"],fps)>frame(c["start"],fps)]
