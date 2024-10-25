"""Test the agent based simulation steps.
"""

from collections import defaultdict
import unittest
import simsurveillance


class TestModelStep(unittest.TestCase):

    @unittest.mock.patch('simsurveillance.AgentModel')
    def test_init(self, mock_agent_model):
        step = simsurveillance.ModelStep(mock_agent_model)
        self.assertIs(step.model, mock_agent_model)

    @unittest.mock.patch('simsurveillance.AgentModel')
    def test_call(self, mock_agent_model):
        step = simsurveillance.ModelStep(mock_agent_model)
        with self.assertRaises(NotImplementedError):
            step(2)


class TestInfectionProgressionStep(unittest.TestCase):

    @unittest.mock.patch('simsurveillance.AgentModel')
    def test_init(self, mock_agent_model):
        step = simsurveillance.InfectionProgressionStep(mock_agent_model)
        self.assertIs(step.model, mock_agent_model)

    @unittest.mock.patch('simsurveillance.AgentModel')
    def test_call(self, mock_agent_model):
        # Test waning someone
        person = simsurveillance.Person(mock_agent_model)
        person.status = simsurveillance.InfectionStatus.RECOVERED

        mock_agent_model.transitions = {5: [person]}

        step = simsurveillance.InfectionProgressionStep(mock_agent_model)
        step(5)

        self.assertIs(
            person.status, simsurveillance.InfectionStatus.SUSCEPTIBLE)

        # Test recovering person
        mock_agent_model.params.waning_rate = 1e-10
        person = simsurveillance.Person(mock_agent_model)
        person.status = simsurveillance.InfectionStatus.INFECTED

        mock_agent_model.transitions = defaultdict(list)
        mock_agent_model.transitions[5] = [person]

        step = simsurveillance.InfectionProgressionStep(mock_agent_model)
        step(5)

        self.assertIs(person.status, simsurveillance.InfectionStatus.RECOVERED)


class TestTransmissionStep(unittest.TestCase):

    @unittest.mock.patch('simsurveillance.AgentModel')
    def test_init(self, mock_agent_model):
        step = simsurveillance.TransmissionStep(mock_agent_model)
        self.assertIs(step.model, mock_agent_model)

    @unittest.mock.patch('numpy.random.poisson')
    def test_call(self, mock_random_pois):

        # A value to ensure that we will always expect to cause infections
        mock_random_pois.side_effect = lambda x: 100

        # Test infecting both others
        model = simsurveillance.SIRSAgentModel(3)
        params = {'transmission_rate': 0.5,
                  'recovery_rate': 0.05,
                  'waning_rate': 0.005}
        model.params.set_parameters(params)
        model.initialize_infection(1)
        person1 = model.persons[simsurveillance.InfectionStatus.SUSCEPTIBLE][0]
        person2 = model.persons[simsurveillance.InfectionStatus.SUSCEPTIBLE][1]

        step = simsurveillance.TransmissionStep(model)
        step(1)

        self.assertIs(person1.status, simsurveillance.InfectionStatus.INFECTED)
        self.assertIs(person2.status, simsurveillance.InfectionStatus.INFECTED)

        # Test having no one to infect
        model = simsurveillance.SIRSAgentModel(3)
        params = {'transmission_rate': 0.5,
                  'recovery_rate': 0.05,
                  'waning_rate': 0.005}
        model.params.set_parameters(params)
        model.initialize_infection(2)
        person1 = model.persons[simsurveillance.InfectionStatus.SUSCEPTIBLE][0]

        step = simsurveillance.TransmissionStep(model)
        step(1)
        self.assertIs(person1.status, simsurveillance.InfectionStatus.INFECTED)

        # Test computing more to infect than available
        with unittest.mock.patch(
            'simsurveillance.TransmissionStep._transmission_rate') \
                as mock_rate:

            mock_rate.side_effect = lambda x: 1
            mock_random_pois.side_effect = lambda x: 100

            model = simsurveillance.SIRSAgentModel(3)
            params = {'transmission_rate': 0.5,
                      'recovery_rate': 0.05,
                      'waning_rate': 0.005}
            model.params.set_parameters(params)
            model.initialize_infection(2)
            person1 = \
                model.persons[simsurveillance.InfectionStatus.SUSCEPTIBLE][0]

            step = simsurveillance.TransmissionStep(model)
            step(1)


if __name__ == '__main__':
    unittest.main()
