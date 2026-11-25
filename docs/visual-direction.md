# Aesthetic-first visual engine

Users may supply text-only art direction or a moodboard of authorized reference images. Presets are optional. Store project-level style, palette, medium, motion, negative constraints, recurring fictional character IDs and set IDs. Reference IDs must resolve to validated assets before generation; the current contract does not upload or condition on images yet.

For illustrated dialogue, use reusable character layers, backgrounds, expressions, mouth shapes, blinking and camera cuts rather than regenerating every frame. For paintings use subtle layer motion; for pixel art preserve pixel edges; for cinematic footage use compatible video inference. No silent fallback to a different aesthetic.

Safety requirements before public generation: reject nudity and sexual content, reject unauthorized real-person likeness replication and face swapping, validate uploaded media, moderate prompts and outputs, keep references private by default, and require appropriate asset rights. These are requirements, not implemented enforcement. Do not enable public generation until enforcement is tested.

The initial Python module defines creative direction and capability-aware routing only. Actual provider adapters, reference ingestion, moderation, character animation and quality tests remain to be implemented. No universal style fidelity is promised.
