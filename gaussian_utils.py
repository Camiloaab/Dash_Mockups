"""Utilities to compute the parameters of a Gaussian distribution from harvest data."""
import numpy as np
import scipy.integrate as integrate


def std_gaussian(x):
    """Compute the standard Gaussian distribution evaluated in x."""
    factor = 1 / np.sqrt(2 * np.pi)
    exponent = -((x) ** 2) / 2
    return factor * np.exp(exponent)


def gaussian(mu, sigma, area, x):
    """Compute the Gaussian distribution with given parameters evaluated in x."""
    factor = area / (sigma * np.sqrt(2 * np.pi))
    exponent = -((x - mu) ** 2) / (2 * sigma**2)
    return factor * np.exp(exponent)


def get_mu(total_area:float, sigma:float, upper_limit:float, accumulated_area:float)->float:
    r"""Compute the mean of the Gaussian distribution.

    This is done solving the equation
    $$accumulated_area = \int_{-\infty}^{upper_limit}gaussian(mu, sigma, total_area)$$
    for mu, which is the mean of the distribution.
    The equation is solved numerically using a grid search
    over possible values of mu.
    """
    DAY_RANGE = np.linspace(-13, 13, 27)
    DECI_DAY_RANGE = np.linspace(-0.5, 0.5, 11)

    errors = []
    mus = []
    for day in DAY_RANGE:
        mu = upper_limit + day
        integral = integrate.quad(lambda x: gaussian(mu, sigma, total_area, x), -np.inf, upper_limit)[0]
        error = np.abs(integral - accumulated_area)
        errors.append(error)
        mus.append(mu)
    mu_day = mus[np.argmin(errors)]

    errors = []
    mus = []
    for frac in DECI_DAY_RANGE:
        mu = mu_day + frac
        integral = integrate.quad(lambda x: gaussian(mu, sigma, total_area, x), -np.inf, upper_limit)[0]
        error = np.abs(integral - accumulated_area)
        errors.append(error)
        mus.append(mu)
    final_mu = mus[np.argmin(errors)]

    return final_mu