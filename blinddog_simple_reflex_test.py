import unittest

from blinddog_simple_reflex import *


class MyTestCase(unittest.TestCase):

    def test_that_Person_can_be_instantiated_with_a_name(self):
        person = Person("Justin Trudeau")
        self.assertEqual("Justin Trudeau", person.__name__)
        self.assertEqual("Justin Trudeau", "{}".format(person)[1:-1])

    def test_that_BlindDog_barks_at_Person(self):
        dog = BlindDog()
        self.assertTrue(dog.bark(Person()))

    def test_that_BlindDog_does_not_bark_at_things_other_than_Person(self):
        dog = BlindDog()
        self.assertFalse(dog.bark(Water()))
        self.assertFalse(dog.bark(Food()))
        self.assertTrue(dog.bark(Person()))

    def test_that_BlindDog_eats_food_if_there_is_food_at_its_current_location(self):
        park = Park()
        dog = BlindDog(program)
        food = Food()

        # place dog at location 1
        park.add_thing(dog, 1)
        self.assertTrue(dog in park.list_things_at(1))

        # place food also at location 1
        park.add_thing(food, 1)
        self.assertTrue(food in park.list_things_at(1))

        # run the program
        park.run(10)

        # after the run, the food should disappear from the park
        self.assertFalse(food in park.things)

    def test_that_BlindDog_drinks_water_if_there_is_water_at_its_current_location(self):
        park = Park()
        dog = BlindDog(program)
        water = Water()

        # place dog at location 1
        park.add_thing(dog, 1)
        self.assertTrue(dog in park.list_things_at(1))

        # place water also at location 2
        park.add_thing(water, 1)
        self.assertTrue(water in park.list_things_at(1))

        # run the program
        park.run(10)

        # after the run, the water should disappear from the park
        self.assertFalse(water in park.things)


    def test_that_BlindDog_moves_to_next_location_after_it_drinks_water_or_eats_a_food_item(self):
        park = Park()
        dog = BlindDog(program)
        water = Water()
        food = Food()

        # place dog at location 1
        park.add_thing(dog, 1)
        self.assertTrue(dog in park.list_things_at(1))

        # place water at location 2
        park.add_thing(water, 2)
        self.assertTrue(water in park.list_things_at(2))

        # place food at location 3
        park.add_thing(food, 3)
        self.assertTrue(food in park.list_things_at(3))

        # run the program
        park.run(10)

        # the dog must now be at location 4
        self.assertEqual(4, dog.location)

        # both water and food no longer exist in the park
        self.assertFalse(water in park.things)
        self.assertFalse(food in park.things)

    def test_that_as_long_as_there_is_food_in_the_park_the_BlindDog_will_continue_move_down_one_location(self):
        park = Park()
        dog = BlindDog(program)
        food = Food()

        # place food at location 1
        park.add_thing(food, 1)
        self.assertTrue(food in park.list_things_at(1))

        # place dog at location 2, so it will never find the food
        park.add_thing(dog, 2)
        self.assertTrue(dog in park.list_things_at(2))

        # run a maximum of 10 steps
        park.run(10)

        # the dog must now be at location 12 after 10 steps
        self.assertEqual(12, dog.location)

        # the food is still there at location 1
        self.assertTrue(food in park.list_things_at(1))

    def test_that_BlindDog_does_not_eat_a_Person(self):
        park = Park()
        dog = BlindDog(program)
        person = Person("Justin Trudeau")
        food = Food()

        park.add_thing(dog, 1)
        park.add_thing(person, 2)
        park.add_thing(food, 3)

        park.run(10)

        # the person is still in the park
        self.assertTrue(person in park.things)

    def test_that_when_a_Person_meets_a_dog_he_will_move_up_one_location(self):
        park = Park()
        dog = BlindDog(program)
        person = Person("Justin Trudeau")
        food = Food()

        park.add_thing(dog, 1)
        park.add_thing(person, 2)
        park.add_thing(food, 3)

        park.run(10)

        # the person is still in the park
        self.assertTrue(person in park.things)
        # and is not at location 1
        self.assertTrue(person in park.list_things_at(1))


if __name__ == '__main__':
    unittest.main()
