from typing import Dict, List
from warnings import warn

from helper_types import PosteriorData
from monca_client import MoncaResponse


def get_summary_data_ab(monca_response: MoncaResponse) -> Dict[str, float]:
    if len(monca_response.versus_control) > 1:
        warn(f"Unexpected number of comparisons: {len(monca_response.versus_control)}")
    statistics = monca_response.versus_control[0].statistics
    stats_rel = statistics.comparison_relative
    prob_b_better = statistics.winning_probability

    return {
        "percent_difference": stats_rel.proportional_difference * 100,
        "ci_lower": stats_rel.ci_lower * 100,
        "ci_upper": stats_rel.ci_upper * 100,
        "prob_b_better": prob_b_better,
        "prob_a_better": 1 - prob_b_better,
    }


def get_posterior_data_ab(monca_response: MoncaResponse) -> List[PosteriorData]:
    if len(monca_response.versus_control) > 1:
        warn(f"Unexpected number of comparisons: {len(monca_response.versus_control)}")

    key_control = monca_response.versus_control[0].compared_to_variant.key
    key_variant = monca_response.versus_control[0].key

    pairwise_comparisons = {
        comp.key: comp.statistics for comp in monca_response.pairwise_comparisons
    }
    statistics_a = pairwise_comparisons.get(key_control)
    statistics_b = pairwise_comparisons.get(key_variant)

    if statistics_a is None or statistics_b is None:
        raise ValueError("Could not find pairwise comparisons for A and B")

    # TODO: catch posterior data not there
    posterior_difference_b_vs_a = [
        a - b for a, b in zip(statistics_a.posterior.data, statistics_b.posterior.data)
    ]

    return [
        PosteriorData("variant_a", statistics_a.posterior.data),
        PosteriorData("variant_b", statistics_b.posterior.data),
        PosteriorData("b_vs_a_diff", posterior_difference_b_vs_a),
    ]
