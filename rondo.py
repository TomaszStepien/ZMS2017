import random
import simpy
# import numpy

# source generates new cars randomly
def source(env, number, interval, rondo, rondo_quarter=5.00):
    for i in range(number):  # liczba samochodow w symulacji
        j = random.choice([0,1,2,3]) # wybor trasy z ktorej samochod przyjezdza
        c = car(env, 'Car%02d%02d' % (i,j), rondo, rondo_quarter, j)
        env.process(c)
        # t = random.expovariate(1.0 / interval) # czestotliwosc pojawiania sie aut
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
        i = random.choice([1, 2, 3, 4]) # dla kazdego samochodu na rondzie wybierany jest losowy zjazd z rona
        tir = i * rondo_quarter + wait  # random.expovariate(1.0 / time_in_bank)
        yield env.timeout(tir)
        print('%7.4f %s: Finished' % (env.now, name))


# Setup and start the simulation
random_seed = 42
new_cars = 5  # Total number of cars
interval_cars = 10.0  # Generate new cars roughly every x seconds

print('RONDO')
random.seed(random_seed)
env = simpy.Environment()

# Start processes and run
rondo = simpy.Resource(env, capacity=2) # ile samochodow moze naraz znajdowac sie na rondzie
env.process(source(env,
                   number=new_cars,
                   interval=interval_cars,
                   rondo=rondo,
                   rondo_quarter=6))
env.run()
