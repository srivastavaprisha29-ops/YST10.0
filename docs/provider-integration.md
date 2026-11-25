# Multi-provider inference

Local adapter targets legacy ComfyUI /prompt, /history, /view endpoints. Pin a tested ComfyUI release; prefer its versioned API for production. Run on a private loopback service in offline mode with only reviewed nodes and workflows. The operator approval flag is not a public safety boundary. Do not expose this adapter or accept arbitrary graphs from customers.

Export an API-format workflow from a compatible installed model (Wan, LTX, etc.), review it, and bind known node inputs to prompts, seed and prepared references. The adapter submits, polls and downloads an explicitly selected output entry. ffprobe checks video stream metadata, not full decode or visual quality. Workflow templates, model weights and live GPU tests are not supplied.

Provider selection is a pure function using explicit authorized capacity, style, mode, estimated cost and quality. It does not reserve quota, measure quality or fetch balances. Zero budget prevents estimated paid selection but cannot enforce billing in external workflows. Production requires atomic reservations and verified billing. External candidates: Runway Dev, Replicate, Comfy Router; no credentials or paid connections enabled. Do not automate consumer free trials or bypass provider limits.

Six finished hours/day requires throughput benchmarks, not just additional provider names. Distinguish synthetic footage duration from assembled duration and GPU wall time.
