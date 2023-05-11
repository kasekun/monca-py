import logging
from typing import List

from matplotlib import pyplot as plt

from helper_types import PosteriorData
from monca_bayes import get_posterior_data_ab, get_summary_data_ab
from monca_client import VariantInput
from monca_handler import MoncaBinomial
from plotting import generate_posteriors_plot
from pymc3_bayes import Pymc3Test
from utils import Color, print_color, timeit

logger = logging.getLogger("pymc3")
logger.propagate = False


import json
from typing import Dict


def pretty_print_json(data: Dict):
    print(json.dumps(data, indent=4))


@timeit("running monca")
def get_monca_posteriors(
    variant_a: VariantInput, variant_b: VariantInput
) -> List[PosteriorData]:
    APIKEY = "oKuozV9N7g3z7kZwHsZW41ThBLPFTijTHn9Knpoa"

    monca = MoncaBinomial(APIKEY)
    monca.run_analysis([variant_a, variant_b], return_posteriors=True)

    pretty_print_json(get_summary_data_ab(monca.monca_response))
    print_color(
        f"Bayesian calculation time: {monca.monca_response.execution_details.execution_time_micro_seconds / 1e6} seconds",
        Color.CYAN,
    )
    posteriors = get_posterior_data_ab(monca.monca_response)
    posteriors[0].label = "PA_Monca"
    posteriors[1].label = "PB_Monca"
    posteriors[2].label = "PDIFF_Monca"  # B - A (i.e., how much better is B?)
    return posteriors


@timeit("running pymc3")
def get_pymc3_posteriors(
    variant_a: VariantInput, variant_b: VariantInput
) -> List[PosteriorData]:
    pymc3_test = Pymc3Test(variant_a, variant_b)
    pretty_print_json(pymc3_test.get_summary_data())
    posteriors = pymc3_test.get_posterior_data()

    posteriors[0].label = "PA_PYMC3"
    posteriors[1].label = "PB_PYMC3"
    posteriors[2].label = "PDIFF_PYMC3"  # B - A (i.e., how much better is B?)
    return posteriors


if __name__ == "__main__":
    variant_a = VariantInput("A", is_control=True, enrollments=68130, conversions=2725)
    variant_b = VariantInput("B", is_control=False, enrollments=55901, conversions=2683)

    monca_results = get_monca_posteriors(variant_a, variant_b)
    pymc3_posteriors = get_pymc3_posteriors(variant_a, variant_b)

    posteriors = [
        monca_results[0],
        monca_results[1],
        pymc3_posteriors[0],
        pymc3_posteriors[1],
    ]
    colors = ["#2480DB", "#24DBDA", "#DB7F24", "#DB2425"]

    posteriors_diffs = [monca_results[2], pymc3_posteriors[2]]

    fig, [ax0, ax1] = plt.subplots(2, 1, figsize=(12, 9))

    generate_posteriors_plot(posteriors, colors=colors, axis=ax0)
    generate_posteriors_plot(posteriors_diffs, colors=["#2480DB", "#DB7F24"], axis=ax1)
    plt.tight_layout()
    fig.savefig("output/plot.png")
    print_color("saved posterior plot to output/plot.png", Color.CYAN)
