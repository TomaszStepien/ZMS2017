import random
import simpy
# import numpy

# source generates new cars randomly
def source(env, number, interval, intersection, times):
    for i in range(number):  # liczba samochodow w symulacji
        j = random.choice([0,1,2,3]) # wybor trasy z ktorej samochod przyjezdza
        c = car(env, 'Car%02d%02d' % (i,j), intersection, times)
        env.process(c)
        # t = random.expovariate(1.0 / interval) # czestotliwosc pojawiania sie aut
        t = 5
        yield env.timeout(t)


def car(env, name, intersection, times):
    """car arrives, is served and leaves"""
    arrive = env.now
    cykl = sum(times)
    red_time = max(times[0] - arrive % cykl, 0)  # zakladamy ze zaczyna sie od czerwonego

    print('%7.4f %s: Here I am' % (arrive, name))

    with intersection.request() as req:
        yield req
        light_time = 5
        wait = env.now - arrive + red_time

        # We got to the rondo
        print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))
        tir = 5.00 + wait  # random.expovariate(1.0 / time_in_bank)
        yield env.timeout(tir)
        print('%7.4f %s: Finished' % (env.now, name))


# Setup and start the simulation
times = [20.00,
         60.00]


random_seed = 42
new_cars = 5  # Total number of cars
interval_cars = 10.0  # Generate new cars roughly every x seconds

print('RONDO')
random.seed(random_seed)
env = simpy.Environment()

# Start processes and run
intersection = simpy.Resource(env, capacity=1) # ile samochodow moze naraz znajdowac sie na rondzie
env.process(source(env,
                   number=new_cars,
                   interval=interval_cars,
                   intersection=intersection,
                   times=times))
env.run()

