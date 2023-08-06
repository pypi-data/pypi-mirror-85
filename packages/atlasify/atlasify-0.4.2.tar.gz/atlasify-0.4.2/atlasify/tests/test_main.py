"""
Copyright (C) 2019-2020 Frank Sauerburger

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import unittest

import numpy as np
import matplotlib.pyplot as plt

from atlasify import atlasify

class SurvivalTestCase(unittest.TestCase):
    """
    Test that the method does not crash..
    """
    def setUp(self):
        """
        Call plt.plot().
        """
        x = np.linspace(-3, 3, 200)
        y = np.exp(-x**2)
        
        plt.plot(x, y, label="Something")

    def tearDown(self):
        """
        Clear the figure.
        """
        plt.clf()

    def test_default(self):
        """
        Check that calling atlasify() without arguments does not crash.
        """
        try:
            atlasify()
        except:
            sef.assertFail("Calling atlasify() raised an exception")

    def test_False(self):
        """
        Check that calling atlasify() without badge does not crash.
        """
        try:
            atlasify(False)
        except:
            sef.assertFail("Calling atlasify() raised an exception")

    def test_label(self):
        """
        Check that calling atlasify() with a label does not crash.
        """
        try:
            atlasify("Internal")
        except:
            sef.assertFail("Calling atlasify() raised an exception")

    def test_subtext(self):
        """
        Check that calling atlasify() with a subtext does not crash.
        """
        try:
            atlasify("Internal", "Hello\nWorld\nHow are you")
        except:
            sef.assertFail("Calling atlasify() raised an exception")

    def test_enlarge(self):
        """
        Check that calling atlasify() with different enalrge does not crash.
        """
        try:
            atlasify("Internal", enlarge=2)
        except:
            sef.assertFail("Calling atlasify() raised an exception")
