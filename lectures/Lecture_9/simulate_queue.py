# Illustrates the use of the queue ADT in modeling a real queue.
# Prompts the user to input:
# - the average time, lambda, between two successive arrivals
#   of customers joining the queue, in minutes;
# - the average time, mu, needed to serve a customer when
#   her turn comes, in minutes;
# - how long the simulation should be run, in hours.
# It is assumed that the interarrival time between successive
# customers is modeled by an exponentially distributed random variables with
# an expected value of lambdaand the service time for a given customer are
# and mu, respectively.
# The first two inputs allow one to theoretically estimate:
# - the average number of customers in the queue including those being served;
# - the average number of customers in the queue waiting to be served;
# - the average waiting time for a customer, excluding service time;
# - the average waiting and service time for a customer.
# These estimates are computed and displayed.
#
# Then a simulation is run, with at every second, the following happening.
# - Some customers possibly join the queue, their total number
#   being randomly generated following a Poisson distribution
#   with an expected value of lambda, based on the relationship
#   the latter has with the exponential distribution with the
#   same expected value.
# - The requested service time of the customers who have just
#   joined the queue, if any, is randomly generated following
#   an exponential distribution with an expected value of mu,
#   and rounded to an integral number of seconds.
# - If somebody is being served but the remainig service time
#   is 0, then that customer leaves the queue.
# - Whether the previous case applies or nobody is being served,
#   if the queue is not empty then the customer at the front of
#   the queue starts being served. Her requested service time
#   could be 0 in which case she would immediately quit the
#   queue and the process would repeat with the next customer,
#   if any; otherwise what remains of the service time for this
#   customer is decreased by 1.
# - Running sums of how long a customer had to wait before she
#   could start being served, of how long it took a customer
#   to wait and be fully served, and of how long the queue is
#   after the customers who have just been served have left,
#   including or not the customer now being served, if any, are
#   kept. At the end of the simulation, these sums are divided
#   by the number of seconds during which the simulation has
#   been run to yield the empirical values of the entities that
#   have previously been theoretically estimated.
#   The total number of customers who have joined the queue
#   is also displayed.
#
# Written by Eric Martin for COMP9021


from random import random
from math import log
from array_queue import *


SIXTY = 60


class Customer:
    def __init__(self, arrival_time = 0, service_time = 0):
        self.arrival_time = arrival_time
        self.service_time = service_time


class QueueSimulation:
    def __init__(self):
        self.average_time_between_two_arrivals = float(input('Enter the average time, in minutes, between two arrivals: '))
        self.average_service_time = float(input('Enter the average time, in minutes, needed to serve a customer: '))
        
    def display_time(self, time):
        nonzero_time = False
        if time >= SIXTY * SIXTY:
            hours = time // (SIXTY * SIXTY)
            print(' {:} '.format(hours), end = '')
            if hours > 1:
                print('hours', end = '')
            else:
                print('hour', end = '')
            time %= SIXTY * SIXTY
            nonzero_time = True
        if time >= SIXTY:
            minutes = time // SIXTY
            print(' {:} '.format(minutes), end = '')
            if minutes > 1:
                print('minutes', end = '')
            else:
                print('minute', end = '')
            time %= SIXTY;
            nonzero_time = True
        if time:
            print(' {:} '.format(time), end = '')
            if time > 1:
                print('seconds', end = '')
            else:
                print('second', end = '')
            nonzero_time = True
        return nonzero_time

    def compute_and_display_estimates(self):
        traffic_intensity = self.average_service_time / self.average_time_between_two_arrivals
        print('Estimated average number of customers in queue including those being served: {:}'.format(
               round(traffic_intensity / (1 - traffic_intensity))))
        print('Estimated average number of customers in queue waiting to be served: {:}'.format(
               round(traffic_intensity * traffic_intensity / (1 - traffic_intensity))))
        print('Estimated average waiting time, excluding serving time: ', end = '')
        if self.display_time(round(1 / (1 / self.average_service_time - 1 / self.average_time_between_two_arrivals) * SIXTY)):
              print()
        else:
            printf('instantaneous')
        print()

    def run_simulation(self):
        simulation_time = int(input('For how long, in hours, do you want to run to simulation? '))
        simulation_limit = simulation_time * SIXTY * SIXTY
        self.average_time_between_two_arrivals *= SIXTY
        self.average_service_time *= SIXTY

        queue = ArrayQueue()
        nb_of_customers = 0
        cumulative_queue_length = 0
        cumulative_waiting_length = 0
        # A service time of -1 indicates that nobody is being served, which can only happen
        # if the queue is empty, possibly following the departure of the last served customer.
        service_time = -1
        cumulative_waiting_time = 0
        cumulative_waiting_and_serving_time = 0
        for simulation_tick in range(simulation_limit):
            # Doing it the hard way...
            # If random() randomly generates a real in [0, 1] then -exp . log(random()) simulates the
            # cumulative distribution of an exponentially distributed random variable with an
            # expected value of exp.
            # To simulate a Poisson distribution with an expected value of exp, it suffices to
            # keep a running sum of the values generated by the previous expression until that
            # sum becomes greater than 1; the number of terms in that sum can then be interpreted
            # as a value randomly generated from that distribution.
            r = 0
            while True:
                r += -self.average_time_between_two_arrivals * log(random())
                if r > 1:
                    break
                nb_of_customers += 1
                customer = Customer()
                customer.arrival_time = simulation_tick
                customer.service_time = int(-self.average_service_time * log(random()))
                queue.enqueue(customer)
            # A new customer can now start being served.
            if service_time == -1 and not queue.is_empty():
                service_time = queue.peek_at_the_front().service_time
                cumulative_waiting_time += simulation_tick - queue.peek_at_the_front().arrival_time
            # If the customer at the front has been served, then she should now quit the queue
            # and all customers that follow her and that need no time to be served should follow
            # her (these guys have been queuing for a while just to find out that they
            # do not have an indispensible piece of information when they are about to be
            # served; surely, they are pretty upset when they quit the queue).
            while service_time == 0:
                cumulative_waiting_and_serving_time += simulation_tick - queue.peek_at_the_front().arrival_time
                queue.dequeue()
                if not queue.is_empty():
                    service_time = queue.peek_at_the_front().service_time
                    cumulative_waiting_time += simulation_tick - queue.peek_at_the_front().arrival_time
                else:
                    service_time = -1
            cumulative_queue_length += len(queue)
            if not queue.is_empty():
                service_time -= 1
                cumulative_waiting_length += len(queue) - 1
        if nb_of_customers:
            print('Number of customers who have joinded the queue: {:}'.format(round(nb_of_customers)))
            print('Average number of customers in queue including those being served: {:}'.format(
                   round(cumulative_queue_length / simulation_limit)))
            print('Average number of customers in queue waiting to be served: {:}'.format(
                   round(cumulative_waiting_length / simulation_limit)))
            print('Average waiting time, excluding serving time:', end = '')
            if self.display_time(round(cumulative_waiting_time / nb_of_customers)):
                print()
            else:
                print(' instantaneous')
            print('Average waiting and serving time: ', end = '')
            if self.display_time(round(cumulative_waiting_and_serving_time / nb_of_customers)):
                print()
            else:
                print(' instantaneous')
        else:
            print('No one has joined the queue; a very quiet day...')

if __name__ == '__main__':
    simulation = QueueSimulation()
    simulation.compute_and_display_estimates()
    simulation.run_simulation()
              
              

