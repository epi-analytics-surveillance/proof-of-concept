"""Differential equation models of epidemic simulation.
"""

import numpy as np
import pandas
import pints
import scipy.integrate


class SIRSModel(pints.ForwardModel):
    """SIRS Differential equation model.
    """
    def __init__(self, init_condition=[1.0, 0.0, 0.0], N=None):
        """
        Parameters
        ----------
        init_condition : list, optional ([1.0, 0.0, 0.0])
            initial conditions of S, I, and R stored in a list. If not
            provided, defaults to [1.0, 0.0, 0.0].
        N : int, optional (None)
            Population size. If equal to None or 1, just simulate
            proportions in each compartment.
        """
        super().__init__()

        self.set_init_condition(init_condition)
        self.set_population_size(N or 1)

    def set_population_size(self, N):
        """Set population size.

        A population size of None is interpreted as just reporting
        proportions in each compartment.
        """
        self._N = N

    def set_init_condition(self, init_condition):
        """Set initial condition.

        Parameters
        ----------
        init_condition : list
            initial conditions of S, I, and R stored in a list
        """
        self._init_condition = init_condition

    def n_parameters(self):
        return 3

    def simulate(self, parameters, times):
        transmission_rate, recovery_rate, waning_rate = parameters

        def rhs(t, y):
            S, I, R, _ = y
            dSdt = -transmission_rate * S * I + waning_rate * R
            dIdt = transmission_rate * S * I - recovery_rate * I
            dRdt = recovery_rate * I - waning_rate * R
            dinfectionsdt = transmission_rate * S * I
            return [dSdt, dIdt, dRdt, dinfectionsdt]

        t_span = (min(times), max(times))

        y0 = self._init_condition + [0.0]

        simulation = scipy.integrate.solve_ivp(
            rhs,
            t_span,
            y0,
            method='RK45',
            t_eval=times,
            rtol=1e-6,
            atol=1e-6
        )

        output = simulation.y.T * self._N

        df = pandas.DataFrame(
            {'time': times,
             'S': output[:, 0],
             'I': output[:, 1],
             'R': output[:, 2],
             'infections': output[:, 3],
             }
        )
        self.output_df = df

        multi_output = np.asarray([
            np.asarray(df['I'] / self._N),
            np.asarray([0] + list(np.diff(df['infections'])))
        ]).T

        return multi_output
