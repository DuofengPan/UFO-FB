# `humanoidverse.adapt_fb`

ORCS-style LoRA dodge adaptation on a **frozen** UFO-FB policy.

## Design

| Piece | Source |
|-------|--------|
| Frozen actor + goal `z` | UFO checkpoint / existing `goal_inference` pickle (read-only) |
| Proprio / action / history | UFO `HumanoidVerseMjlabVectorEnv` |
| LoRA + PPO | This package |
| Ball | Optional inject into the same mjlab scene (`--ball`) |

UFO core train / eval / `goal_inference` are **not** modified. Play does not rewrite `goal_reaching.pkl` or videos.

## Play (ORCS-style viewer)

From the UFO repo root:

```bash
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}"

# No ball — UFO host only
python -m humanoidverse.adapt_fb.play --agent initial --ball none --viewer native --device cuda:0

# Ball pinned overhead (inactive threat; for A/B)
python -m humanoidverse.adapt_fb.play --agent initial --ball parked --viewer native --device cuda:0

# Ball thrown at the robot
python -m humanoidverse.adapt_fb.play --agent initial --ball throw --viewer native --device cuda:0
```

Keys: `n`/`b` cycle goal (MuJoCo window or terminal); Space pause; Enter reset; `+/-` speed.

Needs `runs/ufo_fb_8gpu/checkpoint` and `runs/ufo_fb_8gpu/goal_inference/goal_reaching.pkl`
(or `UFO_FB_CHECKPOINT` / `UFO_FB_GOAL_PKL`).

## Attribution

See `NOTICE`, `THIRD_PARTY_NOTICES.md`, `LICENSE`. Vendored `rsl_rl` at `_vendor/rsl_rl`.
