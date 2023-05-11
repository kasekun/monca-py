from typing import Dict, List

import numpy as np
import pymc3 as pm

from monca.monca_client import VariantInput
from utils.helper_types import PosteriorData
from utils.utils import generate_binomial_sample


class Pymc3Test:
    def __init__(
        self, variant_a: VariantInput, variant_b: VariantInput, alpha: float = 0.05
    ):
        self.variant_a = variant_a
        self.variant_b = variant_b
        self.alpha = alpha
        self._trace = None

    @property
    def trace(self):
        if self._trace is None:
            observations_a = generate_binomial_sample(
                self.variant_a.enrollments, self.variant_a.conversions
            )
            observations_b = generate_binomial_sample(
                self.variant_b.enrollments, self.variant_b.conversions
            )
            with pm.Model():
                # Priors
                p_a = pm.Beta("p_a", alpha=1, beta=1)
                p_b = pm.Beta("p_b", alpha=1, beta=1)

                # Likelihoods
                pm.Bernoulli("lik_a", p=p_a, observed=observations_a)
                pm.Bernoulli("lik_b", p=p_b, observed=observations_b)

                self._trace = pm.sample(2000, return_inferencedata=False)
        return self._trace

    def get_summary_data(self) -> Dict[str, float]:
        p_a_samples, p_b_samples = self.trace["p_a"], self.trace["p_b"]
        diff = (p_b_samples - p_a_samples) / p_a_samples
        ci = np.percentile(diff, [(self.alpha / 2) * 100, (1 - self.alpha / 2) * 100])

        return {
            "percent_difference": np.mean(diff) * 100,
            "ci_lower": ci[0] * 100,
            "ci_upper": ci[1] * 100,
            "prob_b_better": np.mean(p_b_samples > p_a_samples),
            "prob_a_better": np.mean(p_a_samples > p_b_samples),
        }

    def get_posterior_data(self) -> List[PosteriorData]:
        return [
            PosteriorData("variant_a", self.trace["p_a"].tolist()),
            PosteriorData("variant_b", self.trace["p_b"].tolist()),
            PosteriorData(
                "b_vs_a_diff", (self.trace["p_a"] - self.trace["p_b"]).tolist()
            ),
        ]

    def __str__(self):
        return f"<BayesTest for variants {self.variant_a} and {self.variant_b}>"
