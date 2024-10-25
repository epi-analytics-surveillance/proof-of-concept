"""Data structure for holding persons.
"""

import random


class PersonCollection:
    """A collection of persons.

    It supports adding people, removing people, and randomly sampling people
    faster than just a list, by simultaneously saving the index of each
    person in a dictionary.

    See https://stackoverflow.com/questions/15993447/python-data-structure-for-efficient-add-remove-and-random-choice  # noqa
    for discussion.
    """
    def __init__(self):
        """Initialize an empty collection.
        """
        self.persons = []
        self.persons_map = dict()

    def add_person(self, person):
        """Add a person to this collection.

        Parameters
        ----------
        person : simsurveillance.Person
            Person to be added
        """
        if person not in self.persons_map:
            self.persons.append(person)
            self.persons_map[person] = len(self.persons) - 1

    def remove_person(self, person):
        """Remove a person from this collection.

        Parameters
        ----------
        person : simsurveillance.Person
            Person to be removed
        """
        map_location = self.persons_map.pop(person)
        last_person = self.persons.pop()

        # If the person requested to be removed happened to be the last, no
        # further action is necessay. Otherwise, now slot in the last person
        # wherever the person was removed.
        if map_location == len(self.persons):
            return
        self.persons[map_location] = last_person
        self.persons_map[last_person] = map_location

    def random_people(self, num):
        """Select people, at random, without replacement from the collection.

        Parameters
        ----------
        num : int
            Number to randomly sample

        Returns
        -------
        list
            List of people who happened to be chosen
        """
        return random.sample(self.persons, num)

    def shuffle(self):
        """Randomize the order of persons in this collection.
        """
        new_persons = []
        new_persons_map = dict()

        random.shuffle(self.persons)
        for person in self.persons:
            new_persons.append(person)
            new_persons_map[person] = len(new_persons) - 1

        self.persons = new_persons
        self.persons_map = new_persons_map

    def __iter__(self):
        return iter(self.persons)

    def __len__(self):
        return len(self.persons)

    def __contains__(self, person):
        return person in self.persons_map

    def __getitem__(self, i):
        return self.persons[i]
