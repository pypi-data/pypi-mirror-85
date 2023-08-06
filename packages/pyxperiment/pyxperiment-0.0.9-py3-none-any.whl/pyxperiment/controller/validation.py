"""
    pyxperiment_controller/validation.py:
    Validators check the conformity to given constraints

    This file is part of the PyXperiment project.

    Copyright (c) 2019 PyXperiment Developers

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
"""

from abc import ABCMeta, abstractmethod
from decimal import Decimal

class Validator(metaclass=ABCMeta):
    """
    Used to check the compliance of an element to certain criteria
    """

    @abstractmethod
    def check_value(self, value):
        """
        Validate a single element
        """

    def check_values(self, values):
        """
        Validate the compliance of all values to constraints
        """
        return [self.check_value(x) for x in values]

class EmptyValidator(Validator):
    """
    Validates all elements
    """

    @staticmethod
    def check_value(value):
        del value
        return True

    @staticmethod
    def check_values(values):
        return [True for x in values]

class SimpleRangeValidator(Validator):
    """
    Validates the presence of a decimal value within given decimal range
    """

    def __init__(self, lower, upper, quant=None):
        self._lower = Decimal(lower)
        self._upper = Decimal(upper)
        self._quant = Decimal(quant) if quant is not None else None

    def check_value(self, value):
        """Validate the compliance of a single value to constraints"""
        value = Decimal(value)
        return (
            value >= self._lower and value <= self._upper and
            (self._quant is None or divmod(value, self._quant)[1] > 0)
        )
