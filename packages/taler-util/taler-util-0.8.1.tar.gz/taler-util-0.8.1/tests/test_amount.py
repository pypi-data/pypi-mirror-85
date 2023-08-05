#  This file is part of TALER
#  (C) 2017, 2019 Taler Systems SA
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
#  @author Marcello Stanisci
#  @version 0.0
#  @repository https://git.taler.net/taler-util.git/

from taler.util.amount import (
    Amount,
    SignedAmount,
    AmountFormatError,
    AmountOverflowError,
    MAX_AMOUNT_VALUE,
)
from unittest import TestCase
import json


class TestAmount(TestCase):
    def test_very_big_number(self):
        with self.assertRaises(AmountOverflowError):
            self.Amount = Amount(
                "TESTKUDOS",
                value=99999999999999999999999999999999999999999999,
                fraction=0,
            )

    def test_add_overflow(self):
        a1 = Amount("TESTKUDOS", value=MAX_AMOUNT_VALUE, fraction=0)
        with self.assertRaises(AmountOverflowError):
            a2 = a1 + Amount.parse("TESTKUDOS:1")

    def test_sub_overflow(self):
        a1 = Amount("TESTKUDOS", value=MAX_AMOUNT_VALUE, fraction=0)
        s1 = SignedAmount(False, a1)
        with self.assertRaises(AmountOverflowError):
            s2 = s1 - SignedAmount.parse("TESTKUDOS:1")

    def test_parse_error(self):
        with self.assertRaises(AmountFormatError):
            Amount.parse("TESTKUDOS:0,5")
        with self.assertRaises(AmountFormatError):
            Amount.parse("+TESTKUDOS:0.5")
        with self.assertRaises(AmountFormatError):
            Amount.parse("0.5")
        with self.assertRaises(AmountFormatError):
            Amount.parse(":0.5")
        with self.assertRaises(AmountFormatError):
            Amount.parse("EUR::0.5")
        with self.assertRaises(AmountFormatError):
            Amount.parse("EUR:.5")

    def test_parse_and_cmp(self):
        self.assertTrue(Amount.parse("EUR:0.0") < Amount.parse("EUR:0.5"))

    def test_amount(self):
        self.assertEqual(Amount.parse("TESTKUDOS:0").stringify(3), "TESTKUDOS:0.000")

    def test_signed_amount(self):
        self.assertEqual(
            SignedAmount.parse("TESTKUDOS:1.5").stringify(3), "+TESTKUDOS:1.500"
        )

    def test_zero_crossing(self):
        p1 = SignedAmount.parse("EUR:1")
        p2 = SignedAmount.parse("EUR:2")
        p3 = SignedAmount.parse("EUR:3")
        p5 = SignedAmount.parse("EUR:5")
        p8 = SignedAmount.parse("EUR:8")

        self.assertEqual(p5 + p3, p8)
        self.assertEqual(p5 - p3, p2)
        self.assertEqual(p2 - p3, -p1)

        self.assertEqual((-p2) + p3, p1)
