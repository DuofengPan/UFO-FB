# `humanoidverse.adapt_fb`

ORCS-style LoRA dodge adaptation on a **frozen** UFO-FB policy.

## Design

| Piece | Source |
|-------|--------|
| Frozen actor + goal `z` | UFO checkpoint / `goal_inference` pickle |
| Proprio / action / history | UFO `HumanoidVerseMjlabVectorEnv` (default play host) |
| LoRA + PPO | This package (`FbWithAdapter` + vendored `rsl_rl`) |
| Ball | Planned on the UFO host; legacy Adapt dodge kept as `--backend dodge` |

UFO core train / eval / algorithms are **not** modified by this package.

## Run (from the UFO repo root)

```bash
# PYTHONPATH = UFO root (or: pip install -e .)
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}"

# Frozen base on UFO env (same obs/action as goal_inference)
python -m humanoidverse.adapt_fb.play --agent initial --viewer native --device cuda:0

# Headless smoke
python -m humanoidverse.adapt_fb.play --agent initial --steps 200 --device cuda:0
```

Needs `runs/ufo_fb_8gpu/checkpoint` and `runs/ufo_fb_8gpu/goal_inference/goal_reaching.pkl`
(or set `UFO_FB_CHECKPOINT` / `UFO_FB_GOAL_PKL`).

## Attribution

ORCS / rsl_rl / MimicKit notices: see `NOTICE`, `THIRD_PARTY_NOTICES.md`, `LICENSE`.
Vendored `rsl_rl` lives at `_vendor/rsl_rl`.
