from __future__ import annotations

import io
import sys
import unittest
from unittest.mock import patch

from humanoidverse.agents.presets import build_agent_preset
from humanoidverse.train import _default_update_z_every_step, build_ufo_mjlab_config, canonical_agent_name, parse_args


class AgentAliasesTest(unittest.TestCase):
    def _parse(self, *args: str):
        stderr = io.StringIO()
        with patch.object(sys, "argv", ["train.py", *args]), patch("sys.stderr", stderr):
            parsed = parse_args()
        return parsed, stderr.getvalue()

    def test_canonical_agent_name_is_fb(self) -> None:
        self.assertEqual(canonical_agent_name("fb"), "fb")

    def test_removed_presets_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            canonical_agent_name("tech")
        with self.assertRaises(ValueError):
            canonical_agent_name("tldr")

    def test_agent_fb_parses(self) -> None:
        args, warning = self._parse("--agent", "fb")
        self.assertEqual(args.agent, "fb")
        self.assertEqual(args.update_z_every_step, 100)
        self.assertEqual(warning, "")

    def test_fb_default_update_z_every_step(self) -> None:
        self.assertEqual(_default_update_z_every_step("fb"), 100)

    def test_fb_preset_uses_fb_wandb_group(self) -> None:
        selected = build_agent_preset(
            agent="fb",
            device="cpu",
            compile=False,
            update_z_every_step=100,
            lr_scale=1.0,
            clip_grad_norm=0.0,
            cartwheel_aux_safe=False,
            wandb_project="test",
        )
        self.assertEqual(selected["wandb_group"], "ufo_fb")
        self.assertEqual(selected["agent_cfg"].name, "FBcprAuxAgent")
        self.assertEqual(selected["agent_cfg"].train.update_z_every_step, 100)

    def test_fb_build_config_uses_public_names(self) -> None:
        cfg = build_ufo_mjlab_config(
            device="cpu",
            work_dir="/tmp/ufo_agent_alias_test",
            num_envs=1,
            num_env_steps=1,
            seed=1,
            use_wandb=False,
            wandb_run_name=None,
            smoke=True,
            agent="fb",
        )
        self.assertEqual(cfg.wandb_gname, "ufo_fb")
        self.assertEqual(cfg.wandb_run_name, "ufo_fb")
        self.assertEqual(cfg.tags["agent"], "fb")


if __name__ == "__main__":
    unittest.main()
