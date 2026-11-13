"""与仿真器解耦的球面局部 CEM；目标函数越大越好。"""
from dataclasses import dataclass, asdict
import numpy as np


def project(z, radius):
    z = np.asarray(z, dtype=np.float64)
    norm = np.linalg.norm(z, axis=-1, keepdims=True)
    if np.any(norm < 1e-12) or not np.isfinite(z).all():
        raise ValueError('z must be finite and nonzero')
    return z * (radius / norm)


@dataclass(frozen=True)
class CEMConfig:
    population: int = 128
    elites: int = 16
    iterations: int = 20
    sigma: float = .18
    min_sigma: float = .025
    smoothing: float = .7
    max_angle: float = .55
    seed: int = 20261113


def constrain(z, anchor, max_angle):
    """限制相对 z0 的球面夹角，防止局部搜索退化成另一项技能。"""
    radius = np.linalg.norm(anchor)
    u = anchor / radius
    z = project(z, radius)
    cos = np.clip(z @ u / radius, -1, 1)
    angle = np.arccos(cos)
    tangent = z / radius - cos[:, None] * u
    tangent /= np.maximum(np.linalg.norm(tangent, axis=-1, keepdims=True), 1e-12)
    clipped = np.minimum(angle, max_angle)
    return radius * (np.cos(clipped)[:, None] * u + np.sin(clipped)[:, None] * tangent)


def optimize(anchor, evaluate, config=CEMConfig(), callback=None):
    """evaluate 接收 [population, latent_dim]，返回独立评估的标量分数。保留 z0。"""
    if config.population < 3 or not 1 <= config.elites < config.population or config.iterations < 1:
        raise ValueError('invalid CEM budget')
    if not 0 < config.max_angle < np.pi or config.sigma <= 0:
        raise ValueError('invalid search scale')
    anchor = np.asarray(anchor, dtype=np.float64).reshape(-1)
    radius = np.linalg.norm(anchor)
    rng = np.random.default_rng(config.seed)
    mean, std = anchor.copy(), np.full(anchor.shape, config.sigma)
    best, best_score, history = anchor.copy(), -np.inf, []
    for iteration in range(config.iterations):
        candidates = constrain(mean + rng.normal(size=(config.population, anchor.size)) * std, anchor, config.max_angle)
        candidates[0], candidates[1] = anchor, best
        candidates[2] = constrain(mean[None], anchor, config.max_angle)[0]
        scores = np.asarray(evaluate(candidates.astype(np.float32)), dtype=np.float64)
        if scores.shape != (config.population,) or not np.isfinite(scores).all():
            raise ValueError('objective must return one finite score per candidate')
        elite_ids = np.argsort(scores)[-config.elites:]
        winner = int(np.argmax(scores))
        if scores[winner] > best_score:
            best, best_score = candidates[winner].copy(), float(scores[winner])
        elites = candidates[elite_ids]
        mean = project((1-config.smoothing)*mean + config.smoothing*elites.mean(0), radius)
        std = np.maximum(config.min_sigma, (1-config.smoothing)*std + config.smoothing*elites.std(0))
        row = dict(iteration=iteration+1, best_score=best_score, anchor_score=float(scores[0]),
                   median_score=float(np.median(scores)), elite_score=float(scores[elite_ids].mean()),
                   best_angle_rad=float(np.arccos(np.clip(best @ anchor / radius**2, -1, 1))), sigma_mean=float(std.mean()))
        history.append(row)
        if callback:
            callback(best.astype(np.float32), history)
    return best.astype(np.float32), history
