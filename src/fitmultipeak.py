#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File       : fitmultipeak.py
Author     : Rolf Verberg
Description: Test program to fit a multipeak spectrum
"""

# System modules
from argparse import ArgumentParser
import random

# Third party modules
from lmfit.lineshapes import gaussian
from nexusformat.nexus import (
    NXdata,
    NXfield,
)
import numpy as np

# Local modules
from fit import FitProcessor

def ran_uni(set_seed=None):
    """Create a random number distributed in the range `[-0.5, 0.5]`.

    :param set_seed: Initialial seed for the random number generator
        if set.
    :type set_seed: int, optional
    :return: Random number distributed in `[-0.5, 0.5]` if set_seed
        is `None`.
    :rtype: Union[None, float]
    """
    if set_seed is None:
        return random.random()-0.5
    random.seed(set_seed)
    return None

def create_data(
        peak_pars, trend_pars=None, num_peak=3, seed=1, scale=0.05,
        no_noise=False, num=1000):
    """Create the data to fit.

    :param peak_pars: Peak parameters and their stdev.
    :type peak_pars: dict
    :param trend_pars: Treadline parameters, default to no trendline.
    :type trend_pars: dict, optional
    :param num_peak: Number of peaks, defaults to `3`.
    :type num_peak: int, optional
    :param seed: Random generator initial seed, default to `1`.
    :type seed: int
    :param scale: Stdev for y-coordinate noise, defaults to `0.05`.
    :type scale: float, optional
    :param no_noise: No noise is added if set, defaults to `False`.
    :type no_noise: bool, optional
    :param num: Number of data points, defaults to `1000`.
    :type num: int, optional
    :return: The x and y coordinates and the nominal peak center
        positions.
    :rtype: np.ndarray, np.ndarray, list[float]
    """
    # Initialize the Numpy random number generator
    rng = np.random.default_rng(seed=seed)

    # Create the data
    x = np.array(np.linspace(0, 20, num))
    y = (trend_pars['a']*x + trend_pars['b'])*x + trend_pars['c']
    if no_noise:
        for n in range(num_peak):
            y += gaussian(
                x, peak_pars['amp'], (n+1)*peak_pars['cen'], peak_pars['sig'])
    else:
        for n in range(num_peak):
            y += gaussian(
                x,
                peak_pars['amp'] + peak_pars['amp_sig']*ran_uni(),
                (n+1)*peak_pars['cen'] + peak_pars['cen_sig']*ran_uni(),
                peak_pars['sig'] + peak_pars['sig_sig']*ran_uni())
        y += rng.normal(size=x.size, scale=scale)

    return x, y, [(n+1)*peak_pars['cen'] for n in range(num_peak)]

def fit(x, y, centers):
    """Fit a spectrum with a multipeak Gaussian function and optionally
    a quadratic trendline.

    :param x: x-coordinates.
    :type x: np.ndarray
    :param y: y-coordinates.
    :type y: np.ndarray
    :param centers: Nominal peak center positions.
    :type centers: list[float]
    :return: The fit result.
    :rtype: CHAP.utils.fit.Fit
    """
    # Create the fit configuration
    nxdata = NXdata(NXfield(y, 'y'), NXfield(x, 'x'))
    models = [
        {'model': 'quadratic'},
        {'model': 'multipeak', 'centers': centers, 'fit_type': 'uniform',
         'centers_range': 1, 'fwhm_min': 0.1, 'fwhm_max': 0.5}
    ]
    config = {
        'plot': True,
        'print_report': True,
        'models': models,
    }

    # Perform uniform fit
    fit = FitProcessor()
    print(f'Uniform fit result:')
    result = fit.process(nxdata, config)

    # Perform unconstrained fit from uniform result
    config['models'][1]['fit_type'] = 'unconstrained'
    config['models'][1]['fwhm_max'] = 2.0
    print(f'\nUnconstrained fit result:')
    result = fit.process(result, config)

    return result

def main():
    """Main function."""

    parser = ArgumentParser(description='Fit a multipeak spectrum')
    parser.add_argument(
        '--num_peak', default=3, type=int, help='Number of peaks')
    parser.add_argument(
        '--seed', default=1, type=int, help='Seed')
    parser.add_argument(
        '--scale', default=0.05, type=float,
        help='Stdev for y-coordinate noise')
    parser.add_argument(
        '--no_noise', action='store_true', help='No noise flag')
    parser.add_argument(
        '--num', default=1000, type=int, help='Number of points')
    args = parser.parse_args()

    peak_pars = {
        'amp': 2.0, 'amp_sig': 1.0,
        'cen': 5.0, 'cen_sig': 1.0,
        'sig': 0.5, 'sig_sig': 0.2,
    }
    trend_pars = {'a': 0.002, 'b': -0.01, 'c':-0.5}

    # Initialize the random number generator
    ran_uni(set_seed=args.seed)

    # Create the data
    x, y, centers = create_data(
        peak_pars=peak_pars, trend_pars=trend_pars, num_peak=args.num_peak,
        seed=args.seed, scale=args.scale, no_noise=args.no_noise, num=args.num)

    # Perform the fit
    result = fit(x, y, centers)

if __name__ == '__main__':
    main()
