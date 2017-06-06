import random
import simpy


# import numpy

# source generates new cars randomly
# and we need 4 of them because 4 directions of arrival are possible
def source_east(env, number, interval, intersection, lights):
    for i in range(number):  # number of cars coming from this direction
        c = car(env, 'Car%02dEast' % i, intersection, lights)
        env.process(c)
        # t = random.expovariate(1.0 / interval) # czestotliwosc pojawiania sie aut
        t = 5
        yield env.timeout(t)


def source_west(env, number, interval, intersection, lights):
    for i in range(number):
        c = car(env, 'Car%02dWest' % i, intersection, lights)
        env.process(c)
        # t = random.expovariate(1.0 / interval) # czestotliwosc pojawiania sie aut
        t = 5
        yield env.timeout(t)


def source_north(env, number, interval, intersection, lights):
    for i in range(number):
        c = car(env, 'Car%02dNorth' % i, intersection, lights)
        env.process(c)
        # t = random.expovariate(1.0 / interval) # czestotliwosc pojawiania sie aut
        t = 5
        yield env.timeout(t)


def source_south(env, number, interval, intersection, lights):
    for i in range(number):
        c = car(env, 'Car%02dSouth' % i, intersection, lights)
        env.process(c)
        # t = random.expovariate(1.0 / interval)  # czestotliwosc pojawiania sie aut
        t = 5
        yield env.timeout(t)

def car(env, name, intersection, lights):
    """car arrives, is served and leaves"""
    arrive = env.now
    cykl = sum(lights)
    red_time = max(lights[0] - arrive % cykl, 0)  # zakladamy ze zaczyna sie od czerwonego

    print('%7.4f %s: Here I am' % (arrive, name))

    with intersection.request() as req:
        yield req
        wait = env.now - arrive + red_time

        # We got to the rondo
        print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))
        tir = 5.00 + wait  # random.expovariate(1.0 / time_in_bank)
        yield env.timeout(tir)
        print('%7.4f %s: Finished' % (env.now, name))


# set parameters
random_seed = 2137

cars_east = 5  # how many cars coming from each direction
cars_west = 5
cars_north = 5
cars_south = 5

interval_east = 10.0  # Generate new cars roughly every x seconds
interval_west = 10.0
interval_north = 10.0
interval_south = 10.0

capacity = 20  # How many cars can enter the intersection simultaneously

lights = [20,40]  # red, green

# set up the environment
print('Intersection with lights')
random.seed(random_seed)
env = simpy.Environment()

# Start processes and run
intersection = simpy.Resource(env, capacity=1)
env.process(source_east(env,
                        number=cars_east,
                        interval=interval_east,
                        intersection=intersection,
                        lights=lights))

env.process(source_west(env,
                        number=cars_west,
                        interval=interval_west,
                        intersection=intersection,
                        lights=lights))

env.process(source_north(env,
                         number=cars_north,
                         interval=interval_north,
                         intersection=intersection,
                        lights=lights))

env.process(source_south(env,
                         number=cars_south,
                         interval=interval_south,
                         intersection=intersection,
                        lights=lights))
env.run()



