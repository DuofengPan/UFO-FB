# Third-party notices

The BSD-3-Clause license at the repository root applies to original UFO-FB-adapt
material and to ORCS-derived material (which remains under the upstream ORCS
BSD-3-Clause copyright). Third-party material retains its upstream terms.

## ORCS (structural provenance)

This project’s package layout, adaptation ethos (frozen base + LoRA adapter on
the decoder path; `augmentation` as the only extension seam; privileged critic),
and selected infrastructure patterns are adapted from:

- Repository: [lok-i/orcs](https://github.com/lok-i/orcs)
- Author: Lokesh Krishna
- License: BSD-3-Clause; see `LICENSE` and `NOTICE`
- Related paper lineage: ViBe (arXiv:2609.09918)

## UFO / BFM-Zero (frozen base policy)

The frozen foundation policy loaded for adaptation comes from the UFO / BFM
training stack (FBcprAux / FB latent `z`, actor conditioned on proprio + `z`).
Checkpoint artifacts are **not** vendored in this git repository; point
`UFO_FB_CHECKPOINT` (or config) at a local `runs/.../checkpoint` directory.

## Vendored: rsl_rl (lok-i fork)

Embedded at `_vendor/rsl_rl` and **committed in this repository** (not
fetched at install time). Pin recorded in `deps.lock.json`.

- Source: [lok-i/rsl_rl](https://github.com/lok-i/rsl_rl) (ORCS-validated fork of ETH/NVIDIA RSL-RL)
- SHA: `215b6f4ceda569d2ca39df64dd679b9af15375cb`
- License: BSD-3-Clause (see `_vendor/rsl_rl/LICENSE`)
- Why fork: includes `SonicWithAdapterModel` / `MLPWithAdapter` used by ORCS/ViBe.
  UFO-FB-adapt implements an FB-side LoRA wrap in-tree, but keeps this fork for
  PPO / future training parity with ORCS.

**Not vendored (intentionally):**

- `orcs` Python package — **not a runtime dependency**; only ethos/structure attributed.
- `mocke` (SONIC weights/code) — UFO-FB is the frozen base instead.
- ORCS `assets` / motion datasets — pulled only when a physics task needs them (Phase 4+).

## MimicKit (dodge reward)

`humanoidverse/adapt_fb/tasks/dodge/mdp/rewards.py::ball_clearance` adapts MimicKit's
`compute_dodge_reward` (via ORCS's dodge port).

- Source: [xbpeng/MimicKit](https://github.com/xbpeng/MimicKit)
- License: Apache-2.0; see `LICENSES/Apache-2.0.txt`
- Citation: Xue Bin Peng, *MimicKit*, arXiv:2510.13794 / related dodgeball notes in ORCS

## Other

Additional notices will be appended when vision encoders or further third-party
code are imported.
