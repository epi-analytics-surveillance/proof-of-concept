"""Test the classes of the agent_model.py
"""

import unittest
import unittest.mock

import simsurveillance


class TestAgentModel(unittest.TestCase):

    def test_init(self):
        simsurveillance.AgentModel()

    def test_simulate(self):
        m = simsurveillance.AgentModel()
        with self.assertRaises(NotImplementedError):
            m.simulate([1, 2, 3])

    def test_add_observers(self):
        m = simsurveillance.AgentModel()
        obs1 = simsurveillance.Observer(m)
        obs2 = simsurveillance.Observer(m)
        m.add_observers(obs1, obs2)

        self.assertIn(obs1, m.observers)
        self.assertIn(obs2, m.observers)


class TestSIRSAgentModel(unittest.TestCase):

    def test_init(self):
        m = simsurveillance.SIRSAgentModel(10)

        self.assertEqual(
            10, len(m.persons[simsurveillance.InfectionStatus.SUSCEPTIBLE]))

        self.assertEqual(10, m.N)

    def test_initialize_infection(self):
        m = simsurveillance.SIRSAgentModel(10)
        m.params.set_parameters({'recovery_rate': 1})
        m.initialize_infection(5)

        self.assertEqual(
            5, len(m.persons[simsurveillance.InfectionStatus.INFECTED]))

    @unittest.mock.patch('simsurveillance.Observer')
    @unittest.mock.patch('simsurveillance.InfectionProgressionStep')
    @unittest.mock.patch('simsurveillance.TransmissionStep')
    def test_simulate(self,
                      mock_transmission_step,
                      mock_infection_step,
                      mock_observer):

        m = simsurveillance.SIRSAgentModel(10)
        m.add_observers(mock_observer)

        df = m.simulate([1, 2, 3])
        self.assertEqual(len(df), 3)

        self.assertTrue(mock_transmission_step.called)
        self.assertTrue(mock_infection_step.called)
        self.assertTrue(mock_observer.called)


if __name__ == '__main__':
    unittest.main()
