"""Creative direction contracts for future visual providers."""
from dataclasses import dataclass, field, asdict

PRESETS = {
    "dollhouse": "pastel fashion dollhouse, playful stylized interiors",
    "illustrated_dialogue": "consistent 2D illustrated characters and room",
    "abstract": "conceptual shapes and experimental composition",
    "painting": "visible brushwork and traditional painted textures",
    "pixel": "intentional low resolution pixel art, crisp nearest-neighbor edges",
    "sketch": "hand drawn lines and limited motion",
    "collage": "layered paper, editorial typography and mixed media",
    "natural": "ordinary lighting, candid composition, restrained processing",
    "stop_motion": "handcrafted miniature sets and stepped movement",
    "editorial": "fashion editorial composition and restrained palette",
    "explainer": "flat vector graphics and readable diagrams",
    "cinematic": "cinematic composition and realistic movement",
}
@dataclass
class Direction:
    aesthetic: str
    palette: str = ""
    medium: str = ""
    motion: str = ""
    avoid: str = ""
    reference_ids: list[str] = field(default_factory=list)
    character_ids: list[str] = field(default_factory=list)
    set_id: str = ""
    preset: str = ""
    def prompt(self, scene):
        return "\n".join([f"Scene: {scene}", f"Art direction: {self.aesthetic}",
            f"Preset: {PRESETS.get(self.preset, '')}", f"Palette: {self.palette}",
            f"Medium: {self.medium}", f"Motion: {self.motion}", f"Avoid: {self.avoid}",
            "Preserve the chosen art medium; do not default to photorealism or cinematic lighting."])
    def manifest(self):
        return asdict(self)

def choose_route(direction, scene_kind, capabilities):
    """Select only a compatible available route; never silently substitute."""
    needs_refs = bool(direction.reference_ids or direction.character_ids or direction.set_id)
    preferred = {
        "dialogue": ["layered_animation", "image_to_video"],
        "diagram": ["motion_graphics"],
        "painting": ["layered_animation", "image_to_video"],
        "footage": ["image_to_video", "text_to_video"],
    }.get(scene_kind, ["image_to_video", "text_to_video", "layered_animation"])
    for route in preferred:
        cap = capabilities.get(route, {})
        if cap.get("available") and (not needs_refs or cap.get("reference_conditioning")):
            return route
    raise RuntimeError("No compatible visual route available; request user approval for alternatives")
