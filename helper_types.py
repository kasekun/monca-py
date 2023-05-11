from typing import List

import numpy as np


class PosteriorData:
    def __init__(self, label: str, points: np.ndarray):
        self.label = label
        self.points = points

    @property
    def mean(self):
        return np.mean(self.points)

    def as_dict(self):
        return {"label": self.label, "points": self.points.tolist(), "mean": self.mean}


class MoncaResponse:
    def __init__(self, key: str, variants: List["Variant"]):
        self.key = key
        self.variants = variants

    @classmethod
    def from_dict(cls, data: dict):
        key = data.get("key")
        variants_data = data.get("variants", [])
        variants = [Variant.from_dict(v) for v in variants_data]
        return cls(key=key, variants=variants)


class Variant:
    def __init__(self, key: str, name: str, is_control: bool, statistics: "Statistics"):
        self.key = key
        self.name = name
        self.is_control = is_control
        self.statistics = statistics

    @classmethod
    def from_dict(cls, data: dict):
        key = data.get("key")
        name = data.get("name")
        is_control = data.get("is_control", False)
        statistics_data = data.get("statistics", {})
        statistics = Statistics.from_dict(statistics_data)
        return cls(key=key, name=name, is_control=is_control, statistics=statistics)


class Statistics:
    def __init__(
        self,
        comparison_absolute: "Comparison",
        comparison_relative: "Comparison",
        winning_probability: float,
        enrollments: int,
        conversions: int,
        posterior_data: List[float] = None,
    ):
        self.comparison_absolute = comparison_absolute
        self.comparison_relative = comparison_relative
        self.winning_probability = winning_probability
        self.enrollments = enrollments
        self.conversions = conversions
        self.posterior_data = posterior_data

    @classmethod
    def from_dict(cls, data: dict):
        comparison_absolute_data = data.get("comparison_absolute", {})
        comparison_absolute = Comparison.from_dict(comparison_absolute_data)
        comparison_relative_data = data.get("comparison_relative", {})
        comparison_relative = Comparison.from_dict(comparison_relative_data)
        winning_probability = data.get("winning_probability", 0.0)
        enrollments = data.get("enrollments", 0)
        conversions = data.get("conversions", 0)
        posterior_data = data.get("posterior_data", [])
        return cls(
            comparison_absolute=comparison_absolute,
            comparison_relative=comparison_relative,
            winning_probability=winning_probability,
            enrollments=enrollments,
            conversions=conversions,
            posterior_data=posterior_data,
        )


class Comparison:
    def __init__(
        self, proportional_difference: float, ci_lower: float, ci_upper: float
    ):
        self.proportional_difference = proportional_difference
        self.ci_lower = ci_lower
        self.ci_upper = ci_upper

    @classmethod
    def from_dict(cls, data: dict):
        proportional_difference = data.get("proportional_difference", 0.0)
        ci_lower = data.get("ci_lower", 0.0)
        ci_upper = data.get("ci_upper", 0.0)
        return cls(
            proportional_difference=proportional_difference,
            ci_lower=ci_lower,
            ci_upper=ci_upper,
        )
