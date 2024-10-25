"""Models of epidemic simulation.
"""

from collections import defaultdict
import random
import numpy as np
import pandas
import simsurveillance as se
from simsurveillance import InfectionStatus as InfStatus


class AgentModel:
    """Abstract agent based model.

    Attributes
    ----------
    persons : dict
        Holds persons of each status. Each key is one of the Infection
        statuses. The corresponding value is the list of persons with
        that status.
    all_persons : list
        Holds all the persons in the simulation, regardless of the
        infection status.
    N : int
        number of agents in the simulation
    params : simsurveillance.ModelParameters
        Storing parameter values
    observers : list of simsurveillance.Observer
        The observation processes that will be called each iteration of the
        simulation.
    steps : list of simsurveillance.ModelStep
        The transmission steps that will be called each iteration of the
        simulation.
    """
    def __init__(self):
        self.persons = {
            infection_status: se.PersonCollection()
            for infection_status in InfStatus
        }
        self.all_persons = se.PersonCollection()
        self.N = 0
        self.params = se.ModelParameters()
        self.observers = []
        self.steps = []

    def add_observers(self, *observers):
        """Add observation processes.

        Parameters
        ----------
        observers : simsurveillance.Observer
            To be added to the model
        """
        for observer in observers:
            self.observers.append(observer)

    def simulate(self, times):
        """Simulate the model and return the output at given times.

        Parameters
        ----------
        times : list
            Time points at which to evaluate outputs.

        Returns
        -------
        pandas.DataFrame
            Time series output of simulation
        """
        raise NotImplementedError


class SIRSAgentModel(AgentModel):
    """Stochastic Agent based model of SIRS.
    """
    def __init__(self, N, seed=1234):
        """Create a new SIRS agent based model.

        Parameters
        ----------
        N : int
            Total number of persons to simulate.
        """
        super().__init__()
        self.transitions = defaultdict(list)
        self.N = N

        for _ in range(N):
            p = se.Person(self)
            self.persons[p.status].add_person(p)
            self.all_persons.add_person(p)

        self.infection_progression_step =\
            se.InfectionProgressionStep(self)
        self.transmission_step = se.TransmissionStep(self)

        self.steps = [
            self.transmission_step,
            self.infection_progression_step,
        ]

        # We employ two random seeds so that consistent simulations can be
        # obtained even if the testing procedure is adjusted.
        np.random.seed(seed)
        random.seed(seed)
        self.simulation_random_state = random.getstate()
        random.seed(seed + 1)
        self.testing_random_state = random.getstate()

    def infect_people(self, persons, time):
        """Move the given people to the I (infected) status.
        """
        for person in persons:
            person.update_status(InfStatus.INFECTED, time)

            # Now they are Infect. Check when they will become recovered.
            next_status_change = random.expovariate(self.params.recovery_rate)
            next_status_change = round(next_status_change)
            self.transitions[time + next_status_change].append(person)

            if random.random() < self.params.proportion_symptomatic:
                person.symptoms = True

    def initialize_infection(self, num_infect, time=0):
        """Start an infection with the given number of infect, randomly
        selected, from amongst the susceptible.

        Parameters
        ----------
        num_infect : int
            Number to infect
        time : int, optional (0)
            Time step. By default, used for initialization, time=0, before
            running the simulation.
        """
        infect = self.persons[InfStatus.SUSCEPTIBLE].random_people(num_infect)
        self.infect_people(infect, time)
        self.transmission_step.num_infected += num_infect

    def simulate(self, times):
        output = defaultdict(list)
        sim_times = range(max(times) + 1)

        for sim_time in sim_times:

            if sim_time in times:
                # Record simulation outputs at this time step
                output['time'].append(sim_time)
                for status in InfStatus:
                    output[status].append(len(self.persons[status]))
                output['transmissions'].append(
                    self.transmission_step.num_infected)

            ##### Observation processes #####
            random.setstate(self.testing_random_state)
            for observer in self.observers:
                observer(sim_time)
            self.testing_random_state = random.getstate()

            ##### Simulation steps #####
            random.setstate(self.simulation_random_state)
            for step in self.steps:
                step(sim_time)
            self.simulation_random_state = random.getstate()

            while len(self.transitions[sim_time]) > 0:
                self.infection_progression_step(sim_time)

        return pandas.DataFrame(output)
