import random
import simpy
# import numpy

# source generates new cars randomly
def source(env, number, interval, rondo, rondo_quarter=5.00):
    """Source generates cars randomly"""
    for i in range(number):
        c1 = car(env, 'Car01_%02d' % i, rondo, rondo_quarter)
        c2 = car(env, 'Car02_%02d' % i, rondo, rondo_quarter)
        c3 = car(env, 'Car03_%02d' % i, rondo, rondo_quarter)
        c4 = car(env, 'Car04_%02d' % i, rondo, rondo_quarter)
        env.process(random.choice([c1,c2,c3,c4]))
        # t = random.expovariate(1.0 / interval) # czestotliwosc pojawiania
        t = 2
        yield env.timeout(t)


def car(env, name, rondo, rondo_quarter, road):
    """car arrives, is served and leaves."""
    arrive = env.now
    print('%7.4f %s: Here I am' % (arrive, name))

    with rondo.request() as req:
        yield req
        wait = env.now - arrive

        # We got to the rondo
        print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))
        i = random.choice([1, 2, 3, 4])
        tib = i * rondo_quarter  # random.expovariate(1.0 / time_in_bank)
        yield env.timeout(tib)
        print('%7.4f %s: Finished' % (env.now, name))
        # print(time_in_bank)


# Setup and start the simulation
random_seed = 42
new_cars = 5  # Total number of cars
interval_cars = 10.0  # Generate new cars roughly every x seconds

print('RONDO')
random.seed(random_seed)
env = simpy.Environment()

# Start processes and run
rondo = simpy.Resource(env, capacity=2)
env.process(source(env,
                   number=new_cars,
                   interval=interval_cars,
                   rondo=rondo,
                   rondo_quarter=6))
env.run()
