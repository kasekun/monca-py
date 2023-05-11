import time
from functools import wraps
from typing import Callable, List, Optional

import numpy as np
from scipy.stats import gaussian_kde


class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"


def print_color(message: str, color: str = Color.RESET, *args, **kwargs) -> None:
    print(color + message + Color.RESET, *args, **kwargs)


def gen_kde_xy(data: List[float], resolution: int = 200):
    density = gaussian_kde(
        data, bw_method=0.4
    )  # note this BW will force data to be very smooth
    xs = np.linspace(np.min(data), np.max(data), resolution)
    return xs, density(xs)


def generate_binomial_sample(sample_size: int, conversions: int) -> list[int]:
    data = [1] * conversions + [0] * (sample_size - conversions)
    return data


def timeit(description: Optional[str] = None) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal description
            if description is None:
                description = f"Executing {func.__name__}"
            start_time = time.time()
            print_color(f"\n{description}...", Color.GREEN)
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print_color(
                f"{description} done. Execution time: {elapsed_time:.2f} seconds",
                Color.GREEN,
            )
            return result

        return wrapper

    return decorator
