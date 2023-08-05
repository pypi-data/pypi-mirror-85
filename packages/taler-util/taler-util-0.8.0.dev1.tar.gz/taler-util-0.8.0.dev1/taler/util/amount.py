# This file is part of GNU Taler
# (C) 2017-2020 Taler Systems SA
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later
# version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301  USA
#
# @author Marcello Stanisci
# @version 0.1
# @repository https://git.taler.net/taler-util.git/

from dataclasses import dataclass
from functools import total_ordering
import re


class CurrencyMismatchError(Exception):
    """
    Exception class to raise when an operation between two
    amounts of different currency is being attempted.
    """

    def __init__(self, curr1, curr2) -> None:
        super(CurrencyMismatchError, self).__init__(
            f"mismatched currency: {curr1} vs {curr2}"
        )


class AmountOverflowError(Exception):
    pass


class AmountFormatError(Exception):
    pass


MAX_AMOUNT_VALUE = 2 ** 52

FRACTIONAL_LENGTH = 8

FRACTIONAL_BASE = 1e8


@total_ordering
class Amount:
    def __init__(self, currency, value, fraction):
        if fraction >= FRACTIONAL_BASE:
            raise AmountOverflowError("amount fraction too big")
        if value > MAX_AMOUNT_VALUE:
            raise AmountOverflowError("amount value too big")
        self._currency = currency
        self._value = value
        self._fraction = fraction

    @property
    def currency(self):
        return self._currency

    @property
    def value(self):
        return self._value

    @property
    def fraction(self):
        return self._fraction

    def __repr__(self):
        return f"Amount(currency={self.currency!r}, value={self.value!r}, fraction={self.fraction!r})"

    def __str__(self):
        return self.stringify()

    @classmethod
    def parse(cls, amount_str):
        exp = r"^\s*([-_*A-Za-z0-9]+):([0-9]+)\.?([0-9]+)?\s*$"
        parsed = re.search(exp, amount_str)
        if not parsed:
            raise AmountFormatError(f"invalid amount: {amount_str}")

        tail = "." + (parsed.group(3) or "0")

        if len(tail) > FRACTIONAL_LENGTH + 1:
            raise AmountOverflow()
        value = int(parsed.group(2))
        fraction = round(FRACTIONAL_BASE * float(tail))
        currency = parsed.group(1)
        return Amount(currency, value, fraction)

    def __add__(self, other):
        if self.currency != other.currency:
            raise CurrencyMismatchError(self.currency, other.currency)
        v = int(
            self.value
            + other.value
            + (self.fraction + other.fraction) // FRACTIONAL_BASE
        )
        if v >= MAX_AMOUNT_VALUE:
            raise AmountOverflowError()
        f = int((self.fraction + other.fraction) % FRACTIONAL_BASE)
        return Amount(self.currency, v, f)

    def __sub__(self, other):
        if self.currency != other.currency:
            raise CurrencyMismatchError(self.currency, other.currency)
        v = self.value
        f = self.fraction
        if self.fraction < other.fraction:
            v -= 1
            f += FRACTIONAL_BASE
        f -= other.fraction
        if v < other.value:
            raise AmountOverflowError()
        v -= other.value
        return Amount(self.currency, v, f)

    def stringify(self, ndigits=0, pretty=False) -> str:
        s = str(self.value)
        if self.fraction != 0:
            s += "."
            frac = self.fraction
            while frac > 0 or (ndigits is not None and ndigits > 0):
                s += str(int(frac / (FRACTIONAL_BASE / 10)))
                frac = (frac * 10) % FRACTIONAL_BASE
                if ndigits > 0:
                    ndigits -= 1
        elif ndigits != 0:
            s += "." + ("0" * ndigits)
        if not pretty:
            return f"{self.currency}:{s}"
        return f"{s} {self.currency}"

    def cmp(self, am2) -> int:
        if self.currency != am2.currency:
            raise CurrencyMismatchError(self.currency, am2.currency)
        if self.value == am2.value:
            if self.fraction < am2.fraction:
                return -1
            if self.fraction > am2.fraction:
                return 1
            return 0
        if self.value < am2.value:
            return -1
        return 1

    def is_zero(self):
        return self.fraction == 0 and self.value == 0

    def __eq__(self, other):
        return self.cmp(other) == 0

    def __lt__(self, other):
        return self.cmp(other) == -1

    def as_signed(self):
        """
        Return the (positive) SignedAmount corresponding to
        this amount.
        """
        return SignedAmount(True, self)


@total_ordering
class SignedAmount:
    """
    Amount with a sign.
    """

    def __init__(self, is_positive, amount):
        self._is_positive = is_positive
        self._amount = amount

    @property
    def is_positive(self):
        return self._is_positive

    @property
    def amount(self):
        return self._amount

    def __eq__(self, other):
        if self.is_zero() and other.is_zero():
            return True
        if self.is_positive == other.is_positive:
            return self.amount == other.amount
        return False

    def __lt__(self, other):
        if self.is_positive:
            if other.is_positive:
                return self.amount < other.amount
            else:
                return False
        else:
            if other.is_positive:
                return True
            else:
                return self.amount > other.amount

    def stringify(self, ndigits=0, pretty=False) -> str:
        if self.is_positive:
            sgn = "+"
        else:
            sgn = "-"
        return sgn + self.amount.stringify(ndigits, pretty)

    @classmethod
    def parse(cls, amount_str):
        c0 = amount_str[0:1]
        if c0 == "+":
            return SignedAmount(True, Amount.parse(amount_str[1:]))
        if c0 == "-":
            return SignedAmount(False, Amount.parse(amount_str[1:]))
        return SignedAmount(True, Amount.parse(amount_str))

    def __neg__(self):
        return SignedAmount(not self.is_positive, self.amount)

    def __add__(self, other):
        if self.is_positive == other.is_positive:
            return SignedAmount(self.is_positive, self.amount + other.amount)
        if self.is_positive:
            if self.amount >= other.amount:
                return SignedAmount(True, self.amount - other.amount)
            else:
                return SignedAmount(False, other.amount - self.amount)
        else:
            if other.amount >= self.amount:
                return SignedAmount(True, other.amount - self.amount)
            else:
                return SignedAmount(False, self.amount - other.amount)

    def is_zero(self):
        return self.amount.is_zero()

    def __sub__(self, other):
        return self + (-other)

    def __repr__(self):
        return f"SignedAmount(is_positive={self.is_positive!r}, amount={self.amount!r})"

    def __str__(self):
        return self.stringify()
