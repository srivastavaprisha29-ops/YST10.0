# Research-backed video development

VBench (CVPR 2024): https://arxiv.org/abs/2311.17982 — separate subject/background consistency, motion and frame quality. Current temporal_quality.py is a simple pixel-change diagnostic, not VBench or a reliable flicker detector. Camera motion and cuts confound it.

Wan2.2: https://github.com/Wan-Video/Wan2.2 — benchmark TI2V-5B for local text/image-to-video; assess hardware and licence. LTX-Video: https://github.com/Lightricks/LTX-Video — benchmark multi-keyframe conditioning. ByTheWay (CVPR 2025): https://openaccess.thecvf.com/content/CVPR2025/papers/Bu_ByTheWay_Boost_Your_Text-to-Video_Generation_Model_to_Higher_Quality_in_CVPR_2025_paper.pdf — investigate training-free improvements on supported baselines, not assumed portable.

animation_render.py implements real deterministic still-image pan/zoom/hold via Pillow and FFmpeg. Pixel mode uses integer nearest-neighbor scaling with a static canvas; codec chroma subsampling can still alter colors. This is not generative motion or character animation. Trusted offline operators only; public safety gates remain pending. Test locally with authorized art, measure throughput and inspect rendered frames before adoption. No live GPU results claimed.
