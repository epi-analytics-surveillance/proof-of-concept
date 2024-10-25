"""Test the classes of the diffeq_model.py
"""

import unittest
import pints
import simsurveillance


class TestSIRSModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_params = [0.1, 0.01, 0.005]
        cls.test_times = [10.1, 10.5, 11, 15, 17, 18.0]
        cls.test_init_cond = [0.99, 0.01, 0.0]

    def test_init(self):
        # test init of the model
        m = simsurveillance.SIRSModel()
        self.assertIsInstance(m, pints.ForwardModel)

    def test_n_parameters(self):
        # test n_parameters
        m = simsurveillance.SIRSModel()
        n_parameters = m.n_parameters()
        self.assertEqual(n_parameters, 3)

    def test_simulate(self):
        # test simulate method

        m = simsurveillance.SIRSModel(init_condition=self.test_init_cond)

        y = m.simulate(self.test_params, self.test_times)
        df = m.output_df.copy()

        self.assertEqual(len(df['time']), len(self.test_times))
        self.assertSetEqual(
            set(df.columns), {'time', 'S', 'I', 'R', 'infections'})

        self.assertEqual(y.shape, (len(self.test_times), 2))

    def test_set_population_size(self):
        # test changing the population size
        m = simsurveillance.SIRSModel(init_condition=self.test_init_cond)
        m.set_init_condition([0.9, 0.1, 0.0])
        m.set_population_size(100)
        m.simulate(self.test_params, self.test_times)
        df1 = m.output_df.copy()

        m.set_population_size(1000)
        m.simulate(self.test_params, self.test_times)
        df2 = m.output_df.copy()

        final_t = len(self.test_times) - 1
        self.assertGreater(df2['S'][final_t], df1['S'][final_t])

        m.set_population_size(1)
        output = m.simulate(self.test_params, self.test_times)
        df3 = m.output_df.copy()
        self.assertAlmostEqual(
            df3['S'][final_t] + df3['I'][final_t] + df3['R'][final_t], 1.0)

        self.assertEqual(output.shape, (len(self.test_times), 2))

    def test_set_init_condition(self):
        # Test setting initial condition

        m = simsurveillance.SIRSModel()

        m.set_init_condition([1.0, 0.0, 0.0])
        m.simulate(self.test_params, self.test_times)
        df1 = m.output_df.copy()

        m.set_init_condition([0.9, 0.1, 0.0])
        m.simulate(self.test_params, self.test_times)
        df2 = m.output_df.copy()

        final_t = len(self.test_times) - 1
        self.assertGreater(df2['R'][final_t], df1['R'][final_t])


if __name__ == '__main__':
    unittest.main()
