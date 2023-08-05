import unittest
import numpy as np
from taurex.data.planet import Planet, Earth
from taurex.constants import G, RJUP, MJUP


class PlanetTest(unittest.TestCase):

    def setUp(self):

        self.jup = Planet()
        self.earth = Earth()

    def test_properties(self):
        self.assertEqual(self.jup.mass, 1)

        self.assertEqual(self.jup.fullMass, MJUP)
        self.assertEqual(self.jup.fullRadius, RJUP)
        self.assertAlmostEqual(self.jup.gravity, 25.916, places=2)

        # self.assertAlmostEqual(self.earth.gravity,9.819,places=2)

    def test_fitparams(self):
        earth_params = self.earth.fitting_parameters()

        self.assertIn('planet_radius', earth_params)
        self.assertIn('planet_mass', earth_params)
