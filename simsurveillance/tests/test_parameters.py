"""Test parameters.py
"""

import unittest
import simsurveillance


class TestModelParameters(unittest.TestCase):

    def test_init(self):
        simsurveillance.ModelParameters()

    def test_set_parameters(self):
        p = simsurveillance.ModelParameters()
        p.set_parameters({'a': 1})
        self.assertEqual(p.a, 1)

    def test_default_parameters(self):
        p = simsurveillance.ModelParameters()
        self.assertEqual(p.transmission_rate, 1.0)
        p.set_parameters({'transmission_rate': 1.5})
        self.assertEqual(p.transmission_rate, 1.5)

    def test_remove_parameters(self):
        p = simsurveillance.ModelParameters()
        p.set_parameters({'a': 1})
        p.remove_parameter('a')
        with self.assertRaises(AttributeError):
            p.a


if __name__ == '__main__':
    unittest.main()
