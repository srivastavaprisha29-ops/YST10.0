# YST10.0 — AI YouTube Production Studio

YST10.0 is an open-development project for an end-to-end faceless YouTube video production platform. The goal is to connect research, fact-checking, scripting, storyboarding, media production, voiceover, timeline editing, export, and publishing within one workspace.

## Product principles

- No opaque coins or credits: show users their **finished-video-minute allowances**.
- Provide a useful free tier; allow the founder's account to access all product features without a subscription fee.
- Do not conflate free account access with free compute: GPU hosting, storage and third-party APIs still have costs.
- Do not claim that any provider offers six hours of free daily cinematic generation without verification.
- Support modular, authorized provider integrations with documented API permissions and licensing.
- Keep API keys on the server; never expose credentials in the browser.
- Track output duration, source licenses, job retries, cost, progress, and render status.

## Production workflow

1. **Discover and Research:** collect sources and topics, with citations and fact-check flags.
2. **Script:** produce editable outlines, narration, hooks, and scene text.
3. **Storyboard:** break scripts into timed shots and media requirements.
4. **Visual Studio:** generate images and footage, retrieve licensed stock media, and build programmatic motion graphics.
5. **Audio:** voice narration, music where properly licensed, sound effects, and subtitles.
6. **Timeline:** assemble clips, timing, transitions, captions, and voiceover.
7. **Render and QA:** background jobs create MP4 exports with documented settings.
8. **Publish:** export metadata, thumbnails, and optionally integrate YouTube OAuth upload.

## Architecture proposal

- Frontend: Next.js, TypeScript, Tailwind CSS
- API: FastAPI, Python
- Database: PostgreSQL
- Queue: Redis + Celery or another durable task scheduler
- Storage: S3-compatible object storage, configurable local mode
- Media processing: FFmpeg and Remotion
- Optional generation workers: self-hosted open-weight models on provisioned GPU hardware
- Authentication and billing: server-side role and entitlement enforcement, with payment-provider integration later

### Provider router

The router must select among configured, explicitly authorized providers based on compatibility, estimated cost, queue time, capacity, commercial licensing, and quality. Provider-specific rate limits cannot be bypassed. The system may fall back to local motion graphics or appropriately licensed stock media when AI video generation is unavailable, but must label the substitution clearly.

### Time-based allowances

Billing-facing allowances should be expressed in **finished video minutes**, with a clearly defined policy for premium fully synthetic clips, scene regeneration, resolution, and concurrent jobs. Failed renders or downloads of existing projects should not consume a new final-render allowance. Track compute cost internally even if customers never see credits.

## Founder's six-hour goal

Six hours of *finished videos per day* is a target, not current capacity. Benchmark real workloads before committing to throughput, price, or customer plans. Completely free unrestricted GPU inference is not a realistic assumption.

## Initial milestones

- [ ] Scaffold Next.js frontend and FastAPI service
- [ ] Create projects, scripts and storyboard data models
- [ ] Implement job lifecycle and status UI
- [ ] Implement a working zero-paid-API-cost demo: script -> timed slides/graphics -> narration -> captions -> MP4
- [ ] Measure render duration, storage size and infrastructure costs
- [ ] Introduce provider-adapter interface and local inference support
- [ ] Implement authentication, founder privileges and user entitlements
- [ ] Introduce payments only after cost benchmarking and abuse protection
- [ ] Add optional YouTube publishing integration

## Security and commercialization

Do not commit API keys, provider tokens, payments credentials or private user information. This is a public repository, so proprietary commercial logic should not be added here without an explicit decision about visibility and licensing. No third-party AI service's free-trial or quota policies should be evaded.

## Status

**Planning baseline.** Functional video generation has not yet been implemented or benchmarked.
