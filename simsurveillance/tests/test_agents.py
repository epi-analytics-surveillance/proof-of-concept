"""Test the person
"""

import unittest
import simsurveillance


class TestPerson(unittest.TestCase):

    @unittest.mock.patch('simsurveillance.AgentModel')
    def test_init(self, mock_agent_model):
        p = simsurveillance.Person(mock_agent_model)
        self.assertIs(p.status, simsurveillance.InfectionStatus.SUSCEPTIBLE)
        self.assertIs(p.model, mock_agent_model)

    @unittest.mock.patch('simsurveillance.AgentModel')
    def test_update_status(self, mock_agent_model):
        p = simsurveillance.Person(mock_agent_model)
        p.update_status(simsurveillance.InfectionStatus.RECOVERED, 5)
        self.assertIs(p.status, simsurveillance.InfectionStatus.RECOVERED)

        self.assertEqual(p.transition_history[5],
                         simsurveillance.InfectionStatus.RECOVERED)


if __name__ == '__main__':
    unittest.main()
