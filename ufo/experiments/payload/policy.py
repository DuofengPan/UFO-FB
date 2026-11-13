"""只加载原 checkpoint 的 Actor、Backward 和冻结归一化器。"""
import hashlib
import json
from pathlib import Path
import torch
from safetensors import safe_open
from ufo.agents.common.base import BaseModel
from ufo.agents.common.checkpoint import load_build_kwargs
from ufo.agents.fb_cpr_aux.config import FBcprAuxModelConfig
from ufo.agents.fb_cpr_aux.model import FBcprAuxModel


class FrozenPolicy(FBcprAuxModel):
    def __init__(self, run, device='cuda:0'):
        folder = Path(run) / 'checkpoint/model'
        cfg = FBcprAuxModelConfig(**{**json.loads((folder/'config.json').read_text()), 'device':'cuda' if str(device).startswith('cuda') else 'cpu'})
        kwargs = load_build_kwargs(folder)
        BaseModel.__init__(self,kwargs['obs_space'],kwargs['action_dim'],cfg)
        self._actor = cfg.archi.actor.build(kwargs['obs_space'],cfg.archi.z_dim,kwargs['action_dim'])
        self._backward_map = cfg.archi.b.build(kwargs['obs_space'],cfg.archi.z_dim)
        self._obs_normalizer = cfg.obs_normalizer.build(kwargs['obs_space'])
        with safe_open(folder/'model.safetensors',framework='pt',device='cpu') as f:
            state={k:f.get_tensor(k) for k in f.keys() if k.startswith(('_actor.','_backward_map.','_obs_normalizer.'))}
        self.load_state_dict(state,strict=True)
        self.eval().requires_grad_(False).to(device)

    def fingerprint(self):
        sha=hashlib.sha256()
        for key,value in sorted(self.state_dict().items()):
            sha.update(key.encode());sha.update(value.detach().cpu().numpy().tobytes())
        return sha.hexdigest()
