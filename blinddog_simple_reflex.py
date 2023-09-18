# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 11:38:46 2020

@author: mhabayeb
@author: Vincent Ngan (Student ID: 301328893)

"""
import collections
from collections.abc import Callable
import numbers


class Thing:
    """This represents any physical object that can appear in an Environment.
    You subclass Thing to get the things you want. Each thing can have a
    .__name__  slot (used for output only)."""

    def __repr__(self):
        return '<{}>'.format(getattr(self, '__name__', self.__class__.__name__))

    def is_alive(self):
        """Things that are 'alive' should return true."""
        return hasattr(self, 'alive') and self.alive

    def show_state(self):
        """Display the agent's internal state. Subclasses should override."""
        print("I don't know how to show_state.")


class Agent(Thing):
    """An Agent is a subclass of Thing with one required slot,
    .program, which should hold a function that takes one argument, the
    percept, and returns an action. (What counts as a percept or action
    will depend on the specific environment in which the agent exists.)
    Note that 'program' is a slot, not a method. If it were a method,
    then the program could 'cheat' and look at aspects of the agent.
    It's not supposed to do that: the program can only look at the
    percepts. An agent program that needs a model of the world (and of
    the agent itself) will have to build and maintain its own model.
    There is an optional slot, .performance, which is a number giving
    the performance measure of the agent in its environment."""

    def __init__(self, program=None):
        self.alive = True
        self.bump = False
        self.holding = []
        self.performance = 0
        if program is None or not isinstance(program, collections.abc.Callable):
            print("Can't find a valid program for {}, falling back to default.".format(self.__class__.__name__))

            def program(percept):
                return eval(input('Percept={}; action? '.format(percept)))

        self.program = program

    def can_grab(self, thing):
        """Return True if this agent can grab this thing.
        Override for appropriate subclasses of Agent and Thing."""
        return False


class Environment:
    """Abstract class representing an Environment. 'Real' Environment classes
    inherit from this. Your Environment will typically need to implement:
        percept:           Define the percept that an agent sees.
        execute_action:    Define the effects of executing an action.
                           Also update the agent.performance slot.
    The environment keeps a list of .things and .agents (which is a subset
    of .things). Each agent has a .performance slot, initialized to 0.
    Each thing has a .location slot, even though some environments may not
    need this."""

    def __init__(self):
        self.things = []
        self.agents = []

    def thing_classes(self):
        return []  # List of classes that can go into environment

    def percept(self, agent):
        """Return the percept that the agent sees at this point. (Implement this.)"""
        raise NotImplementedError

    def execute_action(self, agent, action):
        """Change the world to reflect this action. (Implement this.)"""
        raise NotImplementedError

    def default_location(self, thing):
        """Default location to place a new thing with unspecified location."""
        return None

    def exogenous_change(self):
        """If there is spontaneous change in the world, override this."""
        pass

    def is_done(self):
        """By default, we're done when we can't find a live agent."""
        return not any(agent.is_alive() for agent in self.agents)

    def step(self):
        """Run the environment for one time step. If the
        actions and exogenous changes are independent, this method will
        do. If there are interactions between them, you'll need to
        override this method."""
        if not self.is_done():
            actions = []
            for agent in self.agents:
                if agent.alive:
                    actions.append(agent.program(self.percept(agent)))
                else:
                    actions.append("")
            for (agent, action) in zip(self.agents, actions):
                self.execute_action(agent, action)
            self.exogenous_change()

    def run(self, steps=1000):
        """Run the Environment for given number of time steps."""
        for step in range(steps):
            if self.is_done():
                return
            self.step()

    def list_things_at(self, location, tclass=Thing):
        """Return all things exactly at a given location."""
        if isinstance(location, numbers.Number):
            return [thing for thing in self.things
                    if thing.location == location and isinstance(thing, tclass)]
        return [thing for thing in self.things
                if all(x == y for x, y in zip(thing.location, location)) and isinstance(thing, tclass)]

    def some_things_at(self, location, tclass=Thing):
        """Return true if at least one of the things at location
        is an instance of class tclass (or a subclass)."""
        return self.list_things_at(location, tclass) != []

    def add_thing(self, thing, location=None):
        """Add a thing to the environment, setting its location. For
        convenience, if thing is an agent program we make a new agent
        for it. (Shouldn't need to override this.)"""
        if not isinstance(thing, Thing):
            thing = Agent(thing)
        if thing in self.things:
            print("Can't add the same thing twice")
        else:
            thing.location = location if location is not None else self.default_location(thing)
            self.things.append(thing)
            if isinstance(thing, Agent):
                thing.performance = 0
                self.agents.append(thing)

    def delete_thing(self, thing):
        """Remove a thing from the environment."""
        try:
            self.things.remove(thing)
        except ValueError as e:
            print(e)
            print("  in Environment delete_thing")
            print("  Thing to be removed: {} at {}".format(thing, thing.location))
            print("  from list: {}".format([(thing, thing.location) for thing in self.things]))
        if thing in self.agents:
            self.agents.remove(thing)
            ############

class Food(Thing):
    pass


class Water(Thing):
    pass


class Tree(Thing):
    pass


#
# 2 - Add a new thing to the environment called Person
#
class Person(Thing):
    def __init__(self, name=None):
        if name is not None:
            self.__name__ = name


class Park(Environment):
    def percept(self, agent):
        """return a list of things that are in our agent's location"""
        things = self.list_things_at(agent.location)
        return things

    def execute_action(self, agent, action):
        """changes the state of the environment based on what the agent does."""
        if action == "move down":
            print('{} at location: {} decided to move down to location: {}'
                  .format(str(agent)[1:-1], agent.location, agent.location + 1))
            agent.movedown()

        elif action == "eat":
            items = self.list_things_at(agent.location, tclass=Food)
            if len(items) != 0:
                if agent.eat(items[0]):  # Have the dog eat the first item
                    print('{} ate {} at location: {} and then moved down to location: {}'
                          .format(str(agent)[1:-1], str(items[0])[1:-1], agent.location, agent.location + 1))
                    self.delete_thing(items[0])  # Delete it from the Park after.
            agent.movedown()

        elif action == "drink":
            items = self.list_things_at(agent.location, tclass=Water)
            if len(items) != 0:
                if agent.drink(items[0]):  # Have the dog drink the first item
                    print('{} drank {} at location: {} and then moved down to location: {}'
                          .format(str(agent)[1:-1], str(items[0])[1:-1], agent.location, agent.location + 1))
                    self.delete_thing(items[0])  # Delete it from the Park after.
            agent.movedown()

        #
        # 4a - Add a condition to handle the action "bark".
        # When the agent (BlindDog) encounters a thing which is of
        # type Person, it calls the bark() method to check
        # if the bark() supports this action. If yes, the program
        # goes on to move the person up one location, and move
        # the agent down one location.
        #
        elif action == "bark":
            items = self.list_things_at(agent.location, tclass=Person)
            if len(items) != 0:
                person = items[0]
                if agent.bark(person):  # Have the dog bark at the first person
                    print('{} barked at {} at location: {}'
                          .format(str(agent)[1:-1], str(person)[1:-1], agent.location))
                    # Delete person from the Park after:
                    self.delete_thing(person)
                    # Add the person back to Park at (agent.location - 1):
                    self.add_thing(person, agent.location - 1)
                    print('{} was scared by {} and moved to location: {}'
                          .format(str(person)[1:-1], str(agent)[1:-1], agent.location - 1))
                    print('{} moved down to location: {}'
                          .format(str(agent)[1:-1], agent.location + 1))
            agent.movedown()

    def is_done(self):
        """By default, we're done when we can't find a live agent,
        but to prevent killing our cute dog, we will stop before itself - when there is no more food or water"""
        no_edibles = not any(isinstance(thing, Food) or isinstance(thing, Water) for thing in self.things)
        dead_agents = not any(agent.is_alive() for agent in self.agents)
        done = dead_agents or no_edibles
        return done
    #########
    # So we defined everything now we can run a program#


class BlindDog(Agent):
    location = 1

    def movedown(self):
        self.location += 1

    def eat(self, thing):
        """returns True upon success or False otherwise"""
        if isinstance(thing, Food):
            return True
        return False

    def drink(self, thing):
        """ returns True upon success or False otherwise"""
        if isinstance(thing, Water):
            return True
        return False

    #
    # 4b - Add a new method called bark() for BindDog to represent
    # the bark behavior of BlindDog.
    #
    def bark(self, thing):
        """
        This method models the 'bark' behavior of BlindDog.
        It returns True if the input parameter thing is an instance
        of Person; otherwise it returns False.
        """
        if isinstance(thing, Person):
            return True
        return False
    ##########


def program(percepts):
    """Returns an action based on the dog's percepts"""
    for p in percepts:
        if isinstance(p, Food):
            return 'eat'
        elif isinstance(p, Water):
            return 'drink'
        #
        # 4c - Add a percept that a Person can be barked at by the BlindDog
        #
        elif isinstance(p, Person):
            return 'bark'
    return 'move down'


# Now it's time to implement a program module for our dog.
# A program controls how the dog acts upon its environment.
# Our program will be very simple, and is shown in the table below.
#
# Percept:	Feel Food	Feel Water	Feel Nothing
# Action:	   eat      	drink	move down
#####
def main():
    park = Park()
    dog = BlindDog(program)
    dogfood = Food()
    water = Water()

    park.add_thing(dog, 1)
    park.add_thing(dogfood, 5)
    park.add_thing(water, 7)

    #
    # 1 - Add a new food item called chicken to the park a location 9
    #
    chicken = Food()
    park.add_thing(chicken, 9)

    #
    # 3 - Create two instances of Person and add them to the park at location 3 and 12 respectively
    #
    person1 = Person("Vincent")
    person2 = Person("Ngan")
    park.add_thing(person1, 3)
    park.add_thing(person2, 12)

    #
    # 5 - Run the park for 18 steps
    #
    park.run(18)

    print("Park is done: {}".format(park.is_done()))

    no_edibles = not any(
        isinstance(thing, Food) or isinstance(thing, Water)
        for thing in park.things
    )
    no_agents_alive = not any(
        agent.is_alive() for agent in park.agents
    )
    if no_edibles:
        print("{} starved at location: {}".format(str(dog)[1:-1], dog.location))
    if no_agents_alive:
        print("{} died at location: {}".format(str(dog)[1:-1], dog.location))


if __name__ == "__main__":
    main()
