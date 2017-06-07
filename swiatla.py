import random
import simpy
import pandas as pd


# import numpy

# source generates new cars randomly
# and we need 4 of them because 4 directions of arrival are possible
def source(env, number, interval, intersection, lights, times, origin):
    for i in range(number):  # number of cars coming from this direction
        c = car(env, 'Car%02d%s' % (i, origin), intersection, lights, times)
        env.process(c)
        # t = random.expovariate(1.0 / interval) # czestotliwosc pojawiania sie aut
        t = 5
        yield env.timeout(t)
        times['origin'].append(origin)

def car(env, name, intersection, lights, times):
    """car arrives, is served and leaves"""
    arrive = env.now
    times['arrival_time'].append(arrive)
    cykl = sum(lights)
    red_time = max(lights[0] - arrive % cykl, 0)  # zakladamy ze zaczyna sie od czerwonego
    print('%7.4f %s: Here I am' % (arrive, name))

    with intersection.request() as req:
        yield req
        wait = env.now - arrive + red_time

        # We got to the intersection
        yield env.timeout(wait)
        times['waiting_time'].append(wait)
        print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))
        tir = 5.00  # random.expovariate(1.0 / time_in_bank)
        yield env.timeout(tir)
        times['total_time'].append(wait + tir)
        print('%7.4f %s: Finished' % (env.now, name))


# set parameters
random_seed = 2137

# for each origin there are: name, number of cars and interval
origins = (('east', 5, 10),
           ('west', 5, 10),
           ('north', 5, 10),
           ('south', 5, 10))

capacity = 5  # How many cars can enter the intersection simultaneously

lights1 = (20, 40)  # red, green
lights2 = (20, 40)  # green, red

# set up the environment
print('Intersection with lights')
random.seed(random_seed)
env = simpy.Environment()
times = {'waiting_time': [],
         'total_time': [],
         'arrival_time': [],
         'origin': []}

# Start processes and run
intersection = simpy.Resource(env, capacity=capacity)
for e in origins:
    env.process(source(env,
                       number=e[1],
                       interval=e[2],
                       intersection=intersection,
                       lights=lights1,
                       times=times,
                       origin=e[0]))

env.run()

times = pd.DataFrame(times)

print(times)
