import random
import simpy
import numpy

RANDOM_SEED = 42
NEW_CUSTOMERS = 5 # Total number of customers
INTERVAL_CUSTOMERS = 10.0  # Generate new customers roughly every x seconds

# source generates new cars randomly
def source(env, number, interval, rondo, rondo_quarter=5.00):
    """Source generates cars randomly"""
    for i in range(number):
        c = car(env, 'Car%02d' % i, rondo, rondo_quarter)
        env.process(c)
        # t = random.expovariate(1.0 / interval) # czestotliwosc pojawiania
        t = 5
        yield env.timeout(t)


def car(env, name, rondo, rondo_quarter):
    """car arrives, is served and leaves."""
    arrive = env.now
    print('%7.4f %s: Here I am' % (arrive, name))

    with rondo.request() as req:
        yield req
        wait = env.now - arrive

        # We got to the rondo
        print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))
        i = random.choice([1,2,3,4])
        tib = i*rondo_quarter # random.expovariate(1.0 / time_in_bank)
        yield env.timeout(tib)
        print('%7.4f %s: Finished' % (env.now, name))
        # print(time_in_bank)

# Setup and start the simulation
print('RONDO')
random.seed(RANDOM_SEED)
env = simpy.Environment()

# Start processes and run
rondo = simpy.Resource(env, capacity=1)
env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, rondo, 6))
env.run()
