class Measurement:
    """
    This class is for representing measurements
    in the form of (VAL +- UNC), where the VAL is the mean value
    and UNC is the uncertainty of the given value.

    It supports addition, subtraction, division and multiplication
    between Measurements(or with regular floating-point numbers).
    """
    def __init__(self, val: float, unc: float):
        """
        To instantiate a Measurement, you need:

        :param val: the mean value
        :param unc: the uncertainty
        """
        self.val = val
        self.unc = unc

    def __add__(self, m2):
        # TODO: ADD DOCUMENTATION
        val = self.val + m2.val
        unc = norm(self.unc, m2.unc)
        return Measurement(val, unc)

    def __sub__(self, m2):
        # TODO: ADD DOCUMENTATION
        val = self.val - m2.val
        unc = norm(self.unc, m2.unc)
        return Measurement(val, unc)

    def __mul__(self, m2):
        # TODO: ADD DOCUMENTATION
        if isinstance(m2, Measurement):
            val = self.val * m2.val
            unc = val * norm(self.unc / self.val, m2.unc / m2.val)
            return Measurement(val, unc)
        # Otherwise, it's a scalar
        else:
            return Measurement(self.val * m2, self.unc * m2)

    # Define multiplication as commutative
    __rmul__ = __mul__

    def __truediv__(self, m2):
        # TODO: ADD DOCUMENTATION
        if isinstance(m2, Measurement):
            val = self.val / m2.val
            unc = val * norm(self.unc / self.val, m2.unc / m2.val)
            return Measurement(val, unc)
        else:
            return Measurement(self.val / m2, self.unc / m2)

    def __pow__(self, exp):
        # TODO: ADD DOCUMENTATION
        return Measurement(self.val ** exp, exp * self.val ** (exp - 1) * self.unc)

    def __str__(self):
        # TODO: improve this printing
        # TODO: Figure out how to use localization(E.g. US vs European notation, etc)
        return f"{self.val:.3f} \\pm {self.unc:.3f}"


def norm(*x: float) -> float:
    """Returns the norm of x, i.e. the squareroot of the sum of squares in the tuple x"""
    return (sum([i ** 2 for i in x])) ** 0.5
