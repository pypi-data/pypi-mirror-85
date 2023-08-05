from typing import List

from . import measurement as m


def read(filename: str, headerline=False, col=0, totalcol=1) -> List[float]:
    """
    Reads the data from the file.

    :param filename: the relative/absolute path of the file in your system
    :param headerline: whether or not there is a header in your file
    :param col: TODO: ADD DOCUMENTATION
    :param totalcol: TODO: ADD DOCUMENTATION
    :return: returns the data as a list of floating-point numbers
    """
    # Reads the data from the file.
    # The file MUST have only the raw data
    with open(filename, 'r') as f:
        s = f.read()
        if headerline:
            s = s.split('\n', 1)[1]
        # For European/Brazilian number notation
        s = s.replace(",", ".")
        data = [float(val) for i, val in enumerate(s.split()) if i % totalcol == col]
    return data


def sigma_m(data: List[float], unc: float = 0):
    """
    Calculates the standard deviation of the mean.

    Rationale: just calculating the standard deviation of the
    data isn't enough, we must also account for the estimated
    uncertainty 'unc' of the experiment.

    :param data: the data of the experiment, as a list of floats
    :param unc: the estimated uncertainty of the experiment
    :return: the standard deviation of the mean
    """
    # Data must be number array, for use with unc, or
    length = len(data)
    av = sum(data) / length
    # deviation for the distribution
    dist_sigma = (sum([(x - av) ** 2 for x in data]) / (length - 1)) ** 0.5
    # compounding measurement uncertainty with distribution uncertainty
    total_sigma = m.norm(dist_sigma, unc)
    return total_sigma / length ** 0.5


def create(filename: str, headerline=False, col=0, totalcol=1, unc: float = 0):
    # TODO: ADD DOCUMENTATION
    data = read(filename, headerline, col, totalcol)
    return m.Measurement(sum(data) / len(data), sigma_m(data, unc))
