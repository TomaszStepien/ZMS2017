import random
import simpy
import pandas as pd


# source generates new cars randomly
def source(env, number, interval, rondo, times, origin, rondo_quarter=5.00):
    for i in range(number):  # number of cars coming from this direction
        c = car(env, 'Car%02d%s' % (i, origin), rondo, times, rondo_quarter, origin)
        env.process(c)
        t = random.expovariate(1.0 / interval) # frequency of car creation
        yield env.timeout(t)


def car(env, name, rondo, times, rondo_quarter, origin):
    # car arrives, is served and leaves
    arrive = env.now
    # print('%7.4f %s: Here I am' % (arrive, name))

    with rondo.request() as req:
        yield req
        wait = env.now - arrive

        # We got to the rondo
        yield env.timeout(wait)
        # print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))
        i = random.choice([1, 2, 3, 4])  # for each car a random exit from the roundabout is chosen
        tir = i * rondo_quarter
        yield env.timeout(tir)
        # print('%7.4f %s: Finished' % (env.now, name))

    # dictionary with results is updated
    times['total_time'].append(wait + tir)
    times['waiting_time'].append(wait)
    times['arrival_time'].append(arrive)
    times['origin'].append(origin)


# set parameters
# for each origin there are: name, number of cars and interval
origins = (('east', 100, 5),
           ('west', 100, 5),
           ('north', 100, 5),
           ('south', 100, 5))

times = {'waiting_time': [],
         'total_time': [],
         'arrival_time': [],
         'origin': []}

size = 1000  # the circumference of the roundabout - the bigger it is the more cars can enter
#  but also the longer it takes to travel through it
capacity = size // 3  # How many cars can enter the roundabout simultaneously
rondo_quarter = size // 4  # how many seconds does it take to drive through 1/4 of roundabout

# set up the environment
print('RONDO')
env = simpy.Environment()

# Start processes and run
rondo = simpy.Resource(env, capacity=capacity)

for e in origins:
    env.process(source(env,
                       number=e[1],
                       interval=e[2],
                       rondo=rondo,
                       rondo_quarter=rondo_quarter,
                       times=times,
                       origin=e[0]))

env.run()

times = pd.DataFrame(times)

print(times)
