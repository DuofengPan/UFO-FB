"""Phase 6: obs bridge dims + artifact path resolution."""

from __future__ import annotations

import torch

from humanoidverse.adapt_fb.core.obs_bridge import (
    HISTORY_KEYS,
    ActorHistoryBuffer,
    build_actor_obs,
    policy_to_mjlab_action,
)


def test_history_keys_sorted_ufo_order():
    assert HISTORY_KEYS == (
        "actions",
        "base_ang_vel",
        "dof_pos",
        "dof_vel",
        "projected_gravity",
    )


def test_build_actor_obs_shapes():
    b = 2
    hist = ActorHistoryBuffer(b, device="cpu")
    from humanoidverse.adapt_fb.core.obs_bridge import ProprioSnapshot

    snap = ProprioSnapshot(
        dof_pos=torch.zeros(b, 29),
        dof_vel=torch.zeros(b, 29),
        projected_gravity=torch.zeros(b, 3),
        base_ang_vel=torch.zeros(b, 3),
        actions=torch.zeros(b, 29),
    )
    obs = build_actor_obs(snap, hist)
    assert obs["state"].shape == (b, 64)
    assert obs["last_action"].shape == (b, 29)
    assert obs["history_actor"].shape == (b, 372)
    # second step advances history
    obs2 = build_actor_obs(snap, hist)
    assert obs2["history_actor"].shape == (b, 372)


def test_history_newest_at_index_zero():
    """UFO HVHistoryHandler stores newest at index 0."""
    hist = ActorHistoryBuffer(1, device="cpu")
    for i in range(4):
        snap = {k: torch.full((1, d), float(i + 1)) for k, d in hist._dims.items()}
        hist.add(snap)
    # After 4 pushes with values 1..4, index 0 must be newest (=4).
    assert float(hist._buf["actions"][0, 0, 0]) == 4.0
    assert float(hist._buf["actions"][0, 3, 0]) == 1.0
    # peek must not advance
    from humanoidverse.adapt_fb.core.obs_bridge import ProprioSnapshot

    snap = ProprioSnapshot(
        dof_pos=torch.zeros(1, 29),
        dof_vel=torch.zeros(1, 29),
        projected_gravity=torch.zeros(1, 3),
        base_ang_vel=torch.zeros(1, 3),
        actions=torch.zeros(1, 29),
    )
    build_actor_obs(snap, hist, advance_history=False)
    assert float(hist._buf["actions"][0, 0, 0]) == 4.0


def test_policy_to_mjlab_action_scale():
    a = torch.ones(1, 29)
    assert torch.allclose(policy_to_mjlab_action(a), a * 5.0)


def test_resolve_artifacts_sibling_or_skip():
    from humanoidverse.adapt_fb.core.artifacts import default_checkpoint_candidates, resolve_artifacts

    # Skip if workstation has no UFO sibling checkout.
    if not any(p.is_dir() for p in default_checkpoint_candidates()):
        return
    arts = resolve_artifacts()
    assert (arts.checkpoint_dir / "model" / "config.json").is_file()
    assert arts.goal_pkl.is_file()
