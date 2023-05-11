import json
import uuid
from typing import Dict, List, Optional

import requests


class PosteriorPercentiles:
    def __init__(
        self,
        p05: float,
        p10: float,
        p15: float,
        p20: float,
        p25: float,
        p30: float,
        p35: float,
        p40: float,
        p45: float,
        p50: float,
        p55: float,
        p60: float,
        p65: float,
        p70: float,
        p75: float,
        p80: float,
        p85: float,
        p90: float,
        p95: float,
    ):
        self.p05 = p05
        self.p10 = p10
        self.p15 = p15
        self.p20 = p20
        self.p25 = p25
        self.p30 = p30
        self.p35 = p35
        self.p40 = p40
        self.p45 = p45
        self.p50 = p50
        self.p55 = p55
        self.p60 = p60
        self.p65 = p65
        self.p70 = p70
        self.p75 = p75
        self.p80 = p80
        self.p85 = p85
        self.p90 = p90
        self.p95 = p95

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**data)


class Posterior:
    def __init__(self, data: Optional[List[float]], percentiles: PosteriorPercentiles):
        self.data = data
        self.percentiles = percentiles

    def to_dict(self):
        return {"data": self.data, "percentiles": self.percentiles.to_dict()}

    @classmethod
    def from_dict(cls, data: Dict):
        percentiles = PosteriorPercentiles.from_dict(data.pop("percentiles"))
        return cls(percentiles=percentiles, data=data.get("data"))


class Comparison:
    def __init__(
        self, proportional_difference: float, ci_lower: float, ci_upper: float
    ):
        self.proportional_difference = proportional_difference
        self.ci_lower = ci_lower
        self.ci_upper = ci_upper

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**data)


class Statistics:
    def __init__(
        self,
        enrollments: int,
        conversions: int,
        comparison_absolute: Optional[Comparison],
        comparison_relative: Optional[Comparison],
        winning_probability: Optional[float],
        posterior: Optional[Posterior],
    ):
        self.enrollments = enrollments
        self.conversions = conversions
        self.comparison_absolute = comparison_absolute
        self.comparison_relative = comparison_relative
        self.winning_probability = winning_probability
        self.posterior = posterior

    def to_dict(self):
        return {
            "enrollments": self.enrollments,
            "conversions": self.conversions,
            "comparison_absolute": self.comparison_absolute.to_dict(),
            "comparison_relative": self.comparison_absolute.to_dict(),
            "winning_probability": self.winning_probability,
            "posterior": self.posterior.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict):
        comparison_absolute_data = data.pop("comparison_absolute", None)
        comparison_absolute = (
            Comparison.from_dict(comparison_absolute_data)
            if comparison_absolute_data
            else None
        )

        comparison_relative_data = data.pop("comparison_relative", None)
        comparison_relative = (
            Comparison.from_dict(comparison_relative_data)
            if comparison_relative_data
            else None
        )

        posterior_data = data.pop("posterior", None)
        posterior = Posterior.from_dict(posterior_data) if posterior_data else None

        return cls(
            comparison_absolute=comparison_absolute,
            comparison_relative=comparison_relative,
            posterior=posterior,
            **data,
        )


class VariantMetaData:
    def __init__(self, key: str, name: str):
        self.key = key
        self.name = name

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**data)


class ABVariant:
    def __init__(
        self,
        key: str,
        name: str,
        is_control: bool,
        statistics: Statistics,
        compared_to_variant: VariantMetaData,
    ):
        self.key = key
        self.name = name
        self.is_control = is_control
        self.statistics = statistics
        self.compared_to_variant = compared_to_variant

    def to_dict(self):
        return {
            "key": self.key,
            "name": self.name,
            "is_control": self.is_control,
            "statistics": self.statistics.to_dict(),
            "compared_to_variant": self.compared_to_variant.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict):
        statistics = Statistics.from_dict(data.pop("statistics"))
        compared_to_variant = VariantMetaData.from_dict(data.pop("compared_to_variant"))
        return cls(
            statistics=statistics, compared_to_variant=compared_to_variant, **data
        )


class ExecutionDetails:
    def __init__(self, execution_time_micro_seconds: int, execution_size: int):
        self.execution_time_micro_seconds = execution_time_micro_seconds
        self.execution_size = execution_size

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**data)


class MoncaResponse:
    def __init__(
        self,
        key: str,
        pairwise_comparisons: List[ABVariant],
        versus_control: List[ABVariant],
        execution_details: ExecutionDetails,
    ):
        self.key = key
        self.pairwise_comparisons = pairwise_comparisons
        self.versus_control = versus_control
        self.execution_details = execution_details

    def to_dict(self):
        return {
            "key": self.key,
            "pairwise_comparisons": [pc.to_dict() for pc in self.pairwise_comparisons],
            "versus_control": [vc.to_dict() for vc in self.versus_control],
            "execution_details": self.execution_details.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict):
        pairwise_comparisons = [
            ABVariant.from_dict(pc) for pc in data.get("pairwise_comparisons", [])
        ]
        versus_control = [
            ABVariant.from_dict(vc) for vc in data.get("versus_control", [])
        ]
        execution_details = ExecutionDetails.from_dict(
            data.get("execution_details", {})
        )

        return cls(
            key=data.get("key", ""),
            pairwise_comparisons=pairwise_comparisons,
            versus_control=versus_control,
            execution_details=execution_details,
        )


class VariantInput:
    def __init__(self, name: str, is_control: bool, enrollments: int, conversions: int):
        self.variant_key = str(uuid.uuid4())
        self.name = name
        self.is_control = is_control
        self.enrollments = enrollments
        self.conversions = conversions

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**data)


class MoncaRequest:
    def __init__(
        self, variants: List[VariantInput], return_posteriors: Optional[bool] = None
    ):
        self.variants = variants
        self.return_posteriors = return_posteriors

    def to_dict(self):
        return {
            "variants": [v.to_dict() for v in self.variants],
            "return_posteriors": self.return_posteriors,
        }


class BaseService:
    def __init__(self, api_key: Optional[str] = None):
        self.session = requests.Session()
        self.api_key = api_key

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        self._api_key = value
        self.session.headers.update({"x-api-key": self._api_key})


class MoncaClient(BaseService):
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
        self.endpoint = "https://3jdfftiiz0.execute-api.ap-southeast-2.amazonaws.com/prod/monca-bayes-ab"

    def perform_ab_test(self, ab_test_request: MoncaRequest) -> MoncaResponse:
        try:
            response = self.session.post(
                self.endpoint, data=json.dumps(ab_test_request.to_dict())
            )
            response.raise_for_status()

            data = response.json()

            pairwise_comparisons = [
                ABVariant.from_dict(variant)
                for variant in data.get("pairwise_comparisons", [])
            ]
            versus_control = [
                ABVariant.from_dict(variant)
                for variant in data.get("versus_control", [])
            ]
            execution_details = ExecutionDetails.from_dict(
                data.get("execution_details", {})
            )

            ab_test_response = MoncaResponse(
                key=str(uuid.uuid4()),
                pairwise_comparisons=pairwise_comparisons,
                versus_control=versus_control,
                execution_details=execution_details,
            )

            return ab_test_response

        except requests.HTTPError as http_err:
            raise Exception(
                f"HTTP error occurred: {http_err}, {response.text}"
            ) from http_err
        except Exception as err:
            raise Exception(f"Other error occurred: {err}") from err
