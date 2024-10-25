"""Test the observation processes from observation.py
"""

import unittest
import simsurveillance


class TestDiseaseTest(unittest.TestCase):

    def test_init(self):
        test = simsurveillance.DiseaseTest(0.8, 0.99)

        self.assertEqual(test.sensitivity, 0.8)
        self.assertEqual(test.specificity, 0.99)

    @unittest.mock.patch('simsurveillance.Person')
    def test_call(self, mock_person):
        # Test a perfect test with a truly positive person
        mock_person.status = simsurveillance.InfectionStatus.INFECTED
        test = simsurveillance.DiseaseTest()
        result = test(mock_person)
        self.assertTrue(result)

        # Test a perfect test with a truly negative person
        mock_person.status = simsurveillance.InfectionStatus.SUSCEPTIBLE
        test = simsurveillance.DiseaseTest()
        result = test(mock_person)
        self.assertFalse(result)

        # Test imperfect tests
        mock_person.status = simsurveillance.InfectionStatus.INFECTED
        test = simsurveillance.DiseaseTest(0.75, 1.0)
        positive_tests = 0
        for _ in range(10000):
            if test(mock_person):
                positive_tests += 1
        self.assertGreater(positive_tests, 7000)
        self.assertLess(positive_tests, 8000)

        mock_person.status = simsurveillance.InfectionStatus.SUSCEPTIBLE
        test = simsurveillance.DiseaseTest(1.0, 0.85)
        positive_tests = 0
        for _ in range(10000):
            if test(mock_person):
                positive_tests += 1
        self.assertGreater(positive_tests, 1000)
        self.assertLess(positive_tests, 2000)


class TestObserver(unittest.TestCase):

    @unittest.mock.patch('simsurveillance.AgentModel')
    def test_init(self, model):
        observer = simsurveillance.Observer(model)
        self.assertIs(observer.model, model)

    @unittest.mock.patch('simsurveillance.AgentModel')
    def test_call(self, model):
        observer = simsurveillance.Observer(model)
        with self.assertRaises(NotImplementedError):
            observer(2)


class TestSymptomaticTesting(unittest.TestCase):

    @unittest.mock.patch('simsurveillance.DiseaseTest')
    @unittest.mock.patch('simsurveillance.AgentModel')
    def test_init(self, model, test):
        symptomatic_testing = simsurveillance.SymptomaticTesting(model, test)
        self.assertEqual(symptomatic_testing.times, [])
        self.assertEqual(symptomatic_testing.cases, [])

    def test_call(self):
        test = simsurveillance.DiseaseTest()
        model = simsurveillance.SIRSAgentModel(10)

        model.all_persons[0].update_status(
            simsurveillance.InfectionStatus.INFECTED, 2)
        model.all_persons[0].symptoms = True

        symptomatic_testing = simsurveillance.SymptomaticTesting(model, test)
        symptomatic_testing(3)
        symptomatic_testing(4)

        self.assertEqual(symptomatic_testing.times, [3, 4])
        self.assertEqual(symptomatic_testing.cases, [1, 0])


class TestPrevalenceSurvey(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_days = [4, 5]
        cls.num_tests = [1, 2]

    @unittest.mock.patch('simsurveillance.DiseaseTest')
    @unittest.mock.patch('simsurveillance.AgentModel')
    def test_init(self, model, test):
        survey = simsurveillance.PrevalenceSurvey(
            model, test, self.test_days, self.num_tests)
        self.assertEqual(survey.times, [])
        self.assertEqual(survey.num_tested, [])
        self.assertEqual(survey.num_positive, [])

    def test_call(self):
        test = simsurveillance.DiseaseTest()
        model = simsurveillance.SIRSAgentModel(10)

        model.all_persons[0].update_status(
            simsurveillance.InfectionStatus.INFECTED, 2)

        survey = simsurveillance.PrevalenceSurvey(
            model, test, self.test_days, self.num_tests)

        survey(3)
        self.assertEqual(survey.times, [])
        self.assertEqual(survey.num_tested, [])
        self.assertEqual(survey.num_positive, [])

        survey(4)
        self.assertEqual(survey.times, [4])
        self.assertEqual(survey.num_tested, [1])

        survey(5)
        self.assertEqual(survey.times, [4, 5])
        self.assertEqual(survey.num_tested, [1, 2])

        found_positive = False
        for _ in range(1000):
            survey(5)
            if survey.num_positive[-1] > 0:
                found_positive = True
        self.assertTrue(found_positive)

    def test_uncertainty(self):
        test = simsurveillance.DiseaseTest()
        model = simsurveillance.SIRSAgentModel(10)
        survey = simsurveillance.PrevalenceSurvey(
            model, test, self.test_days, self.num_tests)

        survey(4)
        survey(5)

        posterior = survey.uncertainty()
        self.assertTrue(0 < posterior[0].median() < 1)
        self.assertTrue(0 < posterior[1].median() < 1)


if __name__ == '__main__':
    unittest.main()
