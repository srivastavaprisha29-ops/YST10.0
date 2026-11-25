# Video generation quality program

Do not launch public generation or promise universal style fidelity. Prioritize measured visual quality over billing and UI expansion.

## Benchmark protocol
Use original fictional characters and authorized references. For each benchmark case, record model/checkpoint, license, workflow version, seed, resolution, duration, hardware, wall time, peak VRAM, failures and human review. Compare identical prompts and reference assets across compatible providers. Include text-only and reference-conditioned runs. Retain failed samples. Do not report unmeasured metrics as results.

## Gates
1. Actual playable clips with verified duration and decoding.
2. Human review of aesthetic fidelity, prompt adherence and motion, using a 1–5 rubric with written reasons. Initial target median >=4 for each supported style; report sample size and individual failures.
3. Recurring fictional character and room continuity across multiple shots; evaluate dialogue timing separately.
4. Long-form assembly: first a 60-second episode, then 10 minutes, then throughput tests. Measure cost per finished minute and separately per synthetic minute.
5. Safety: no public generation until tested input/output moderation, reference authorization, privacy isolation and prohibited likeness/nudity controls are in place.
6. Capacity: six hours of finished output per day is a target, not a guarantee. Measure on specified hardware.

## Engineering order
Implement a local ComfyUI adapter with explicitly approved workflows; then reference-conditioned keyframes, image-to-video, deterministic layered animation, fictional character rigs, audio-driven mouth shapes, scene continuity checks, selective regeneration and long-form assembly. Evaluate each model's commercial license before deployment. Do not silently substitute styles or claim safety based on prompt filters alone.

## Status
Benchmark specifications only; no generated samples or measured results yet.
