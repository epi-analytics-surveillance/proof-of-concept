"""Classification of infection status.
"""

from enum import Enum


class InfectionStatus(Enum):
    """The various possible states of a persons infection with the disease.
    """
    SUSCEPTIBLE = 1
    INFECTED = 2
    RECOVERED = 3
