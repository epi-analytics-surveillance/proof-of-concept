"""Processes to simulate collecting epidemiological data during a simulation.
"""

import random
import scipy.stats
from simsurveillance import InfectionStatus as InfStatus


class DiseaseTest:
    """Imperfect binary testing process for a disease.

    Attributes
    ----------
    sensitivity : float
        Probability of testing positive, when applied to a truly positive
    specificity : float
        Probability of testing negative, when applied to a truly negative
    positive_statuses : list of simsurveillance.InfectionStatus
        Which states count as truly positive for this test.
    cost : float
        Positive number representing the surveillance effort of this test.
    """
    def __init__(self, sensitivity=1.0, specificity=1.0):
        self.sensitivity = sensitivity
        self.specificity = specificity

        self.positive_states = [InfStatus.INFECTED]

        self.cost = 1.0

    def __call__(self, person):
        """Obtain the test result of testing a person.

        Parameters
        ----------
        person : simsurveillance.Person
            Person to be tested.
        """
        if person.status in self.positive_states:
            if random.random() < self.sensitivity:
                return True
            else:
                return False

        else:
            if random.random() < self.specificity:
                return False
            else:
                return True


class Observer:
    """Observation process of an epidemic.

    An observer is called at each simulation time step of the agent based
    model. It can extract exact information or simulate some testing process
    applied to a randomly or deterministically selected subset of the
    population.
    """

    def __init__(self, model):
        """
        Parameters
        ----------
        model : simsurveillance.AgentModel
            Agent based model
        """
        self.model = model

    def __call__(self, time):
        raise NotImplementedError


class SymptomaticTesting(Observer):
    """Symptomatic cases are tested.

    All symptomatic persons, who became infected the previous time step,
    are given a given disease test.

    Attributes
    ----------
    times : list
        The time points where any testing was conducted
    cases : list
        The number of positive cases recorded at that time point
    """
    def __init__(self, model, test, start_time=0):
        """
        test : simsurveillance.DiseaseTest
            The binary test which will be used to test each symptomatic.
        start_time : int, optional (0)
            What time point to start the testing.
        """
        super().__init__(model)

        self.test = test

        self.times = []
        self.cases = []

        self.start_time = start_time

    def __call__(self, time):

        if time < self.start_time:
            return

        cases = 0

        for person in self.model.persons[InfStatus.INFECTED]:
            if person.symptoms:

                if time - 1 in person.transition_history and \
                     person.transition_history[time-1] is InfStatus.INFECTED:

                    result = self.test(person)

                    if result:
                        cases += 1

        self.times.append(time)
        self.cases.append(cases)


class PrevalenceSurvey(Observer):
    """Random survey of the full population to see whether or not they are
    infected.

    Attributes
    ----------
    times : list
        The time points where any testing was conducted
    num_tested : list
        The number of tests which were run
    num_positive : list
        The number of those tests which were positive
    """
    def __init__(self, model, test, test_days, num_tests):
        """
        Parameters
        ----------
        test : simsurveillance.DiseaseTest
            The binary test which will be used to test each symptomatic.
        test_days : list of int
            Which simulation time steps at which to test
        num_tests : list of int
            Number of population to test at each test time step
        """
        super().__init__(model)

        self.test = test

        self.test_days = test_days
        self.num_tests = num_tests

        self.times = []
        self.num_tested = []
        self.num_positive = []

    def __call__(self, time):
        if time in self.test_days:
            idx = self.test_days.index(time)
            num_to_test_today = self.num_tests[idx]

            to_be_tested = \
                self.model.all_persons.random_people(num_to_test_today)

            num_positive = 0
            for p in to_be_tested:
                result = self.test(p)
                if result:
                    num_positive += 1

            self.times.append(time)
            self.num_tested.append(num_to_test_today)
            self.num_positive.append(num_positive)

    def uncertainty(self):
        """Compute posterior estimates of prevalence.

        This method uses previously collected testing data to estimate the
        time varying posterior distribution of prevalence.

        Returns
        -------
        list of scipy.stats.beta
            Posterior estimate of prevalence at each time in self.times
        """
        beta_dists = []

        for _, positive, tested in zip(self.times,
                                       self.num_positive,
                                       self.num_tested):

            posterior = scipy.stats.beta(1 + positive, 1 + tested - positive)
            beta_dists.append(posterior)

        return beta_dists
