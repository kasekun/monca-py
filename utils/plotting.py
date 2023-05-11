from itertools import zip_longest
from typing import List, Union

from matplotlib import pyplot as plt

from utils.helper_types import PosteriorData
from utils.utils import gen_kde_xy


def plot_posterior_onto_axis(
    axis: plt.Axes, posterior: PosteriorData, color: Union[str, None] = None
):
    x, y = gen_kde_xy(posterior.points)
    axis.plot(x, y, label=posterior.label, color=color)


def generate_posteriors_plot(
    posteriors: List[PosteriorData],
    axis: Union[plt.Axes, None] = None,
    colors: Union[List[str], None] = None,
):
    if not axis:
        _, axis = plt.subplots(1, figsize=(12, 5))

    for pdat, color in zip_longest(posteriors, colors):
        plot_posterior_onto_axis(axis, pdat, color=color)

    axis.get_yaxis().set_visible(False)
    axis.legend()
