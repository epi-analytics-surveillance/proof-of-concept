"""Test the infection_status
"""

import unittest
import simsurveillance


class TestInfectionStatus(unittest.TestCase):

    def test_infection_statuses(self):
        all_statuses = list(simsurveillance.InfectionStatus)

        # Check there is at least one status
        self.assertGreater(len(all_statuses), 0)

        # Check that the statuses have names
        status_names = [status.name for status in all_statuses]
        [self.assertGreater(len(name), 0) for name in status_names]


if __name__ == '__main__':
    unittest.main()
