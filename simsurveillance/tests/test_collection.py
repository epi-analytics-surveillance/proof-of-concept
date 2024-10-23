"""Test collection.py
"""

import unittest
import simsurveillance


class TestPersonCollection(unittest.TestCase):

    def test_init(self):
        simsurveillance.PersonCollection()

    def test_add_person(self):
        collection = simsurveillance.PersonCollection()

        person = simsurveillance.Person(None)
        collection.add_person(person)

        self.assertIs(person, collection[0])

        # Test adding an existing person
        collection.add_person(person)
        self.assertEqual(len(collection), 1)

    def test_remove_person(self):
        collection = simsurveillance.PersonCollection()

        person = simsurveillance.Person(None)
        collection.add_person(person)
        collection.remove_person(person)
        self.assertEqual(len(collection), 0)

    def test_random_persons(self):
        collection = simsurveillance.PersonCollection()
        person1 = simsurveillance.Person(None)
        person2 = simsurveillance.Person(None)
        person3 = simsurveillance.Person(None)
        collection.add_person(person1)
        collection.add_person(person2)
        collection.add_person(person3)

        for _ in range(100):
            selected_people = collection.random_people(2)
            self.assertEqual(len(selected_people), 2)
            self.assertIsNot(selected_people[0], selected_people[1])
            self.assertIn(selected_people[0], [person1, person2, person3])
            self.assertIn(selected_people[1], [person1, person2, person3])

    def test_iter(self):
        collection = simsurveillance.PersonCollection()
        person1 = simsurveillance.Person(None)
        collection.add_person(person1)

        next_person = next(iter(collection))
        self.assertIs(next_person, person1)

    def test_contains(self):
        collection = simsurveillance.PersonCollection()
        person1 = simsurveillance.Person(None)
        person2 = simsurveillance.Person(None)
        collection.add_person(person1)

        self.assertTrue(person1 in collection)
        self.assertFalse(person2 in collection)

    def test_shuffle(self):
        collection = simsurveillance.PersonCollection()
        person1 = simsurveillance.Person(None)
        person2 = simsurveillance.Person(None)
        person3 = simsurveillance.Person(None)
        collection.add_person(person1)
        collection.add_person(person2)
        collection.add_person(person3)

        person1_not_first = 0
        for _ in range(100):
            collection.shuffle()
            if collection[0] is not person1:
                person1_not_first += 1

        self.assertGreater(person1_not_first, 0)


if __name__ == '__main__':
    unittest.main()
