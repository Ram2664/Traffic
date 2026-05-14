from __future__ import annotations


def clamp(value: float, min_value: float = 0.0, max_value: float = 1.0) -> float:
    return max(min_value, min(value, max_value))


def compute_composite_resilience_index(metrics: dict[str, float], weights: dict[str, float] | None = None) -> float:
    default_weights = {
        'connectivity_retention': 0.25,
        'network_efficiency': 0.25,
        'recovery_speed': 0.2,
        'path_stability': 0.15,
        'survivability': 0.15,
    }
    weights = weights or default_weights

    normalized = {
        'connectivity_retention': clamp(metrics.get('lcc_ratio', 0.0)),
        'network_efficiency': clamp(metrics.get('global_efficiency', 0.0)),
        'recovery_speed': clamp(metrics.get('recovery_efficiency', 0.0)),
        'path_stability': 1.0 - clamp(metrics.get('connectivity_loss', 1.0)),
        'survivability': 1.0 - clamp(metrics.get('failure_ratio', 1.0)),
    }

    total_weight = sum(weights.values()) or 1.0
    score = sum(normalized[k] * weights.get(k, 0.0) for k in normalized) / total_weight
    return clamp(score)
