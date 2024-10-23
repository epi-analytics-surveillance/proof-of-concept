"""Classes for person in a model.
"""

from simsurveillance import InfectionStatus


class Person:
    """Individual person in the model.

    Attributes
    ----------
    status : simsurveillance.InfectionStatus
        Current infection status
    model : simsurveillance.Model
        Model to which this person is attached
    symptoms : bool
        Whether or not they have symptoms
    transition_history : dict
        Keys are simulation time steps, and values are which status they
        switched too at that time. Their initial status is indicated as
        time -1.
    """
    def __init__(self, model):
        self.status = InfectionStatus.SUSCEPTIBLE
        self.model = model
        self.symptoms = False
        self.transition_history = {-1: InfectionStatus.SUSCEPTIBLE}

    def update_status(self, new_status, time):
        """Change my infection status.

        Parameters
        ----------
        new_status : simsurvey.InfectionStatus
            New status to switch to
        """
        self.model.persons[self.status].remove_person(self)
        self.model.persons[new_status].add_person(self)
        self.status = new_status
        self.transition_history[time] = new_status
