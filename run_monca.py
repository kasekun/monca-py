import json
import os
from typing import Dict, List

import click

from monca.monca_client import MoncaResponse, VariantInput
from monca.monca_handler import MoncaBinomial
from utils.utils import Color, print_color, timeit


def write_json_to_file(data: Dict, file_path: str):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


@timeit("running monca")
def run_monca(variants: List[VariantInput], return_posteriors=False) -> MoncaResponse:
    APIKEY = "oKuozV9N7g3z7kZwHsZW41ThBLPFTijTHn9Knpoa"

    monca = MoncaBinomial(APIKEY)
    monca.run_analysis(variants, return_posteriors=return_posteriors)

    return monca.monca_response


@click.command()
@click.option(
    "-c",
    "control",
    nargs=2,
    type=int,
    required=True,
    help="Control variant enrollments and conversions",
)
@click.option(
    "-v",
    "test_variants",
    nargs=2,
    type=int,
    multiple=True,
    required=True,
    help="Test variant enrollments and conversions",
)
@click.option(
    "-o",
    "output_file",
    default="output.json",
    help="Output file path (default: output.json)",
)
def main(control, test_variants, output_file):
    names = "ABCDEFGHIJKLMNOPQRSTUV"
    variants = []

    variants.append(
        VariantInput(
            name=names[0],
            enrollments=control[0],
            conversions=control[1],
            is_control=True,
        )
    )

    for i, test in enumerate(test_variants):
        variants.append(
            VariantInput(
                name=names[i + 1],
                enrollments=test[0],
                conversions=test[1],
                is_control=False,
            )
        )

    result = run_monca(variants)
    write_json_to_file(result.to_dict(), os.path.join('output',output_file))

    print_color(
        f"Bayesian calculation time: {result.execution_details.execution_time_micro_seconds / 1e6} seconds",
        Color.CYAN,
    )
    print_color(
        f"Analysis written to: {output_file}",
        Color.CYAN,
    )


if __name__ == "__main__":
    main()
