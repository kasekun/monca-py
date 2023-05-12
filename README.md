# monca-py
**Bayesian AB testing** in Python using the **Monca Go API**

The Monca Go API allows you to perform rigorous statistical comparison of any number of AB variants versus `control` and versus each-other in a pair-wise manner.
This is a python wrapper around that API.

### Speed
- Monca typically takes less than `0.04 seconds` to analyse > 1 million data points, with the API round-trip taking about `0.3 seconds`.
- Pymc3 will take more than `50 seconds`!

### Web vs Console
- If you don't want to build your own UI around this statistics engine, see [monca.app](https://www.monca.app)
- If you just want to run a quick analysis in a web-ui see [monca.app/analyser](https://www.monca.app/analyser)

## Table of Contents
1. [Getting Started](#getting-started)
   - [Clone the Repository](#1-clone-the-repository)
   - [Set Up the Environment](#2-set-up-the-environment)
2. [Compare monca to pymc3](#compare-monca-to-pymc3)
3. [Using Monca for Bayesian Binomial analysis](#using-monca-for-your-bayesian-binomial-analysis)
4. [Future of `monca-py`](#future-of-monca-py)
5. [JSON Structure](#json-structure)

## Getting Started

### 1. Clone the Repository
```sh
git clone git@github.com:kasekun/monca-py.git
cd monca-py
```

### 2. Set Up the Environment
We recommend using `pipenv` to manage the project's dependencies.
```sh
pipenv --python 3.10.10
pipenv install
```

To automatically activate `pipenv` virtual environment in this directory and it's children, see [Optional Setup](./docs/optional-setup.md)

## Compare monca to pymc3
Run the following command:
```sh
pipenv run python run_compare.py
```

This will output timings to console, and produce a comparison posterior plot at `output/plot.png`

## Using Monca for your Bayesian Binomial analysis

A simple wrapper around the Monca API can be accessed via `run_monca.py`

Suppose you want to compare your `control (-c)` data to two (or more) `variant (-v)` data. You would need the `sample_size` and the `conversion_count` for each of these inputs. Then, you can run the following command:

```sh
# linebreaks added for readability
pipenv run python run_monca.py \
    -c <control sample size>  <control conversion count> \
    -v <variant1 sample size>  <variant1 conversion count> \ 
    -v <variant2 sample size>  <variant2 conversion count> \
    -o <output file name>
```
For example,

```sh
# linebreaks added for readability
pipenv run python run_monca.py \
    -c 11443 1372 \
    -v 12342 1727 \
    -v 11602 1432 \
    -o my_metric.json
```
This will create an output JSON file in `output/my_metric.json`. For details on the structure of this JSON file, refer to [JSON Structure](#json-structure).


## Future of `monca-py`

We plan to formalise this as an SDK in the near future and add automatic API key provisioning.
- For now, there is a single public API key hard-coded into `run_monca.py`.
- The rate limits are a bit aggressive, if you'd like your own key, please [contact us](https://www.monca.app/contact) and we'll be happy to help.

Currently the Monca Go API supports only binomial metrics, we plan to add support for `continuous non-negative` (think revenue and video watch time), and `discrete non-negative metrics` (think number of page visits and cart-volume) as they are needed.

## JSON Structure

This JSON structure represents the results of an Monca bayesian analysis. Here's a brief overview of its structure:

```yaml
key: UUID                               # A unique identifier for the analysis.

pairwise_comparisons:                   # An array comparing each `variant` (including `control`) to all other variants. (e.g., A vs B, B vs A, ... )
  - key: UUID                           # A unique identifier for the comparison.
    name: String                        # The name of the "primary" variant in the comparison.
    is_control: Boolean                 # Indicates whether this variant is the control variant.
    statistics: 
      enrollments: Integer              # The number of enrollments (or "sample size") for this variant.
      conversions: Integer              # The number of conversions for this variant.
      comparison_absolute:              # Contains data about the absolute comparison
        proportional_difference: Float  # The proportional difference in the comparison.
        ci_lower: Float                 # The lower bound of the confidence interval.
        ci_upper: Float                 # The upper bound of the confidence interval.
      comparison_relative:              # Contains data about the relative comparison
        proportional_difference: Float  # The proportional difference in the comparison.
        ci_lower: Float                 # The lower bound of the confidence interval.
        ci_upper: Float                 # The upper bound of the confidence interval.
      winning_probability: Float        # The probability that this variant beats the `compare_to_variant`.
      posterior:                        # Contains data about the posterior.
        data: Null or List              # The likelihood data for the posterior (currently a length of 2000 points).
        percentiles:                    # Contains the percentiles at `5n` intervals  (p05 to p95).
    compared_to_variant:                # Contains information about the variant that this variant is compared to.
      key: UUID                         # A unique identifier for the compared variant.
      name: String                      # The name of the compared variant.

versus_control:                         # Identical structure to `pairwise_comparisons` but filtered to only contain comparisons to `control`

execution_details:                      # Contains details about the execution of the analysis.
  execution_time_micro_seconds: Integer # The time taken for the execution in microseconds.
  execution_size: Integer               # The number of input data-points for this analysis.
