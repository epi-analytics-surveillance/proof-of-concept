"""Steps in an agent based model.

These classes are used to represent the different mechanisms in
the agent based model, simulated at each given time step.
"""

import random
import numpy as np
from simsurveillance import InfectionStatus


class ModelStep:
    """One step in an agent based model.

    Attributes
    ----------
    model : simsurveillance.AgentModel
        Model to which this step is attached.
    """
    def __init__(self, model):
        self.model = model

    def __call__(self, time):
        """Run this step at the indicated time point.

        Parameters
        ----------
        time : int
            Time step
        """
        raise NotImplementedError


class InfectionProgressionStep(ModelStep):
    """Transition persons from I to R, or from R to S.
    """

    def __call__(self, time):
        for person in self.model.transitions[time]:

            self.model.transitions[time].remove(person)

            if person.status is InfectionStatus.INFECTED:
                self._recover_people([person], time)

            elif person.status is InfectionStatus.RECOVERED:
                person.update_status(InfectionStatus.SUSCEPTIBLE, time)

    def _recover_people(self, persons, time):
        """Move the given people to the R (recovered) status.
        """
        for person in persons:

            person.update_status(InfectionStatus.RECOVERED, time)

            person.symptoms = False

            # Now they are Recovered.
            # Check when they will become susceptible again (waning).
            next_status_change = \
                random.expovariate(self.model.params.waning_rate)

            next_status_change = round(next_status_change)

            self.model.transitions[time + next_status_change].append(person)


class TransmissionStep(ModelStep):
    """Infects persons from S to I, based on transmission from other
    infectious.
    """
    def __init__(self, model):
        super().__init__(model)
        self.num_infected = 0

    def _transmission_rate(self, num_susceptible):
        r = self.model.params.transmission_rate * num_susceptible \
            / self.model.N
        return r

    def _compute_number_to_infect(self, initial_rate):
        return np.random.poisson(initial_rate)

    def __call__(self, time):
        num_infected_this_time_step = \
            len(self.model.persons[InfectionStatus.INFECTED])

        num_susceptible_this_time_step = \
            len(self.model.persons[InfectionStatus.SUSCEPTIBLE])

        # Counter for total number infected this time step. Can be
        # accessed to keep track of incidence.
        self.num_infected = 0

        for _ in range(num_infected_this_time_step):
            rate_to_infect = \
                self._transmission_rate(num_susceptible_this_time_step)

            if rate_to_infect <= 0:
                continue

            num_to_infect = self._compute_number_to_infect(rate_to_infect)

            # Do not attempt to infect more than susceptibles that are
            # available.
            if num_to_infect > num_susceptible_this_time_step:
                num_to_infect = num_susceptible_this_time_step

            persons_to_infect = \
                self.model.persons[InfectionStatus.SUSCEPTIBLE]\
                    .random_people(num_to_infect)

            self.model.infect_people(persons_to_infect, time)

            self.num_infected += num_to_infect
            num_susceptible_this_time_step -= num_to_infect
