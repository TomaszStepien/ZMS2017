import random
import simpy


# import numpy

# source generates new cars randomly
# and we need 4 of them because 4 directions of arrival are possible
def source_east(env, number, interval, rondo, rondo_quarter=5.00):
    for i in range(number):  # number of cars coming from this direction
        c = car(env, 'Car%02dEast' % i, rondo, rondo_quarter)
        env.process(c)
        # t = random.expovariate(1.0 / interval) # czestotliwosc pojawiania sie aut
        t = 5
        yield env.timeout(t)


def source_west(env, number, interval, rondo, rondo_quarter=5.00):
    for i in range(number):
        c = car(env, 'Car%02dWest' % i, rondo, rondo_quarter)
        env.process(c)
        # t = random.expovariate(1.0 / interval) # czestotliwosc pojawiania sie aut
        t = 5
        yield env.timeout(t)


def source_north(env, number, interval, rondo, rondo_quarter=5.00):
    for i in range(number):
        c = car(env, 'Car%02dNorth' % i, rondo, rondo_quarter)
        env.process(c)
        # t = random.expovariate(1.0 / interval) # czestotliwosc pojawiania sie aut
        t = 5
        yield env.timeout(t)


def source_south(env, number, interval, rondo, rondo_quarter=5.00):
    for i in range(number):
        c = car(env, 'Car%02dSouth' % i, rondo, rondo_quarter)
        env.process(c)
        # t = random.expovariate(1.0 / interval)  # czestotliwosc pojawiania sie aut
        t = 5
        yield env.timeout(t)


def car(env, name, rondo, rondo_quarter):
    """car arrives, is served and leaves"""
    arrive = env.now
    print('%7.4f %s: Here I am' % (arrive, name))

    with rondo.request() as req:
        yield req
        wait = env.now - arrive

        # We got to the rondo
        print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))
        i = random.choice([1, 2, 3, 4])  # for each car a random exit from the roundabout is chosen
        tir = i * rondo_quarter + wait  # random.expovariate(1.0 / time_in_bank)
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

capacity = 20  # How many cars can enter the roundabout simultaneously

# set up the environment
print('RONDO')
random.seed(random_seed)
env = simpy.Environment()

# Start processes and run
rondo = simpy.Resource(env, capacity=capacity)
env.process(source_east(env,
                        number=cars_east,
                        interval=interval_east,
                        rondo=rondo,
                        rondo_quarter=6))
env.process(source_west(env,
                        number=cars_west,
                        interval=interval_west,
                        rondo=rondo,
                        rondo_quarter=6))
env.process(source_north(env,
                         number=cars_north,
                         interval=interval_north,
                         rondo=rondo,
                         rondo_quarter=6))
env.process(source_south(env,
                         number=cars_south,
                         interval=interval_south,
                         rondo=rondo,
                         rondo_quarter=6))
env.run()

env.run()
