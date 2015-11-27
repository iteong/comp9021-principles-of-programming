# Written by Eric Martin for COMP9021

from tkinter import *
import tkinter.messagebox
from math import pi, cos, sin
from random import choice, randrange


OFFSET = 10
ROAD_WIDTH = 20
CIRCUIT_OUTER_DIAMETER = 600
CIRCUIT_INNER_DIAMETER = CIRCUIT_OUTER_DIAMETER - ROAD_WIDTH * 2
CIRCUIT_MIDDLE_RADIUS = (CIRCUIT_OUTER_DIAMETER + CIRCUIT_INNER_DIAMETER) // 4
CIRCUIT_CENTER = CIRCUIT_OUTER_DIAMETER // 2 + OFFSET
ROAD_COLOUR = '#FFFAF0'
CENTRE_COLOUR = '#F0FFF0'
MIN_NB_OF_CARS = 30
MAX_NB_OF_CARS = 60
MIN_SPEED = 20                                    # In km/h
MAX_SPEED = 110                                   # In km/h
CIRCUIT_LENGTH = 1000                             # In metres
DELAY = 10                                        # In milliseconds
FACTOR_FOR_DISTANCE_PER_ITERATION = DELAY / 3600  # In metres when multipled by speed in km/h
SAFETY_DISTANCE = 10                              # In metres


class TrafficJams(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Traffic jams')
        self.circuit = Circuit()
        self.traffic = Traffic(self.circuit.road)
        self.control_board = ControlBoard(self.traffic)
        self.control_board.pack()
        self.circuit.pack()


class ControlBoard(Frame):
    def __init__(self, traffic):
        Frame.__init__(self, bd = 10, padx = 20, pady = 20)
        self.traffic = traffic
        self.nb_of_cars_scale = Scale(self, length = 200, orient = HORIZONTAL, label ='́Number of cars:',
              from_ = MIN_NB_OF_CARS, to = MAX_NB_OF_CARS, tickinterval = 10, command = self.set_nb_of_cars)
        self.nb_of_cars_scale.pack(side = LEFT, padx = 50)
        self.simulation_button = Button(self, text = 'Start', command = self.simulate)
        self.simulation_button.pack(side = LEFT, padx = 50)
        Scale(self, length = 150, orient = HORIZONTAL, label ='́Acceleration:',
              from_ = 0.01, to = 0.1, tickinterval = 0.03, resolution = 0.01, command = self.set_acceleration).pack(side = LEFT, padx = 50)
        Scale(self, length = 150, orient = HORIZONTAL, label ='Deceleration:',
              from_ = 1, to = 10, tickinterval = 3, command = self.set_deceleration).pack()
        self.simulating = False

    def set_nb_of_cars(self, nb_of_cars):
        self.traffic.nb_of_cars = int(nb_of_cars)
        self.traffic.generate_and_draw_cars()       

    def set_acceleration(self, acceleration):
        self.traffic.acceleration = float(acceleration)

    def set_deceleration(self, deceleration):
        self.traffic.deceleration = int(deceleration)

    def simulate(self):
        if self.simulating == False:
            self.simulating = True
            self.nb_of_cars_scale.config(state = DISABLED)
            self.simulation_button.config(text = 'Stop')
            self.keep_simulating()
        else:
            self.simulating = False
            self.nb_of_cars_scale.config(state = NORMAL)
            self.simulation_button.config(text = 'Start')

    def keep_simulating(self):
        if self.simulating:
            self.traffic.simulate()
            self.after(DELAY, self.keep_simulating)

   
class Circuit(Frame):
    def __init__(self):
        Frame.__init__(self, bd = 10, padx = 20, pady = 20)
        self.road = Canvas(self, width = CIRCUIT_OUTER_DIAMETER + 2 * OFFSET, height = CIRCUIT_OUTER_DIAMETER + 2 * OFFSET)
        self.road.create_oval(OFFSET, OFFSET, CIRCUIT_OUTER_DIAMETER + OFFSET, CIRCUIT_OUTER_DIAMETER + OFFSET, fill = ROAD_COLOUR)
        self.road.create_oval(ROAD_WIDTH + OFFSET, ROAD_WIDTH + OFFSET, CIRCUIT_INNER_DIAMETER + ROAD_WIDTH + OFFSET,
                              CIRCUIT_INNER_DIAMETER + ROAD_WIDTH + OFFSET, fill = CENTRE_COLOUR)
        self.road.pack()


class Car:
    def __init__(self, position, speed, colour):
        self.position = position
        self.speed = speed
        self.colour = colour
        self.car_at_the_front = None
        self.car_at_the_back = None
        self.drawn_car = None
        

class Traffic:
    def __init__(self, road, nb_of_cars = MIN_NB_OF_CARS, acceleration = 0.01, deceleration = 1):
        self.road = road
        self.nb_of_cars = None
        self.previous_nb_of_cars = None
        self.acceleration = acceleration
        self.deceleration = deceleration
        self.cars = None

    def generate_and_draw_cars(self):
        if self.previous_nb_of_cars:
            for i in range(self.previous_nb_of_cars):
                self.road.delete(self.cars.drawn_car)
                self.cars = self.cars.car_at_the_front
        self.previous_nb_of_cars = self.nb_of_cars
        positions = []
        free_positions = list(range(CIRCUIT_LENGTH))
        for i in range(self.nb_of_cars):
            position = choice(free_positions)
            for gap in range(-SAFETY_DISTANCE, SAFETY_DISTANCE + 1):
                pos = (position + gap) % CIRCUIT_LENGTH
                if pos in free_positions:
                    free_positions.remove(pos)
            positions.append(position)
        positions.sort()
        self.cars = Car(positions[0], speed = randrange(MIN_SPEED, MAX_SPEED + 1), colour = self.random_color())
        current_car = self.cars
        for i in range(1, self.nb_of_cars):
            car = Car(positions[i], speed = randrange(MIN_SPEED, MAX_SPEED + 1), colour = self.random_color())
            current_car.car_at_the_front = car
            car.car_at_the_back = current_car
            current_car = car
        current_car.car_at_the_front = self.cars
        self.cars.car_at_the_back = current_car
        self.draw_cars()

    def random_color(self):
        r = hex(randrange(256))[2:]
        if len(r) == 1:
            r = '0' + r
        g = hex(randrange(256))[2:]
        if len(g) == 1:
            g = '0' + g
        b = hex(randrange(256))[2:]
        if len(b) == 1:
            b = '0' + b
        return '#' + r + g + b

    def draw_cars(self):
        for i in range(self.nb_of_cars):
            self.road.delete(self.cars.drawn_car)
            x = CIRCUIT_CENTER + cos(self.cars.position * 2 * pi / CIRCUIT_LENGTH) * CIRCUIT_MIDDLE_RADIUS
            y = CIRCUIT_CENTER + sin(self.cars.position * 2 * pi / CIRCUIT_LENGTH) * CIRCUIT_MIDDLE_RADIUS
            self.cars.drawn_car = self.road.create_oval(x - 4, y - 4, x + 4, y + 4, fill = self.cars.colour)
            self.cars = self.cars.car_at_the_front
                       
    def simulate(self):
        for i in range(self.nb_of_cars):
            distance = (self.cars.car_at_the_front.position - self.cars.position) % CIRCUIT_LENGTH - SAFETY_DISTANCE
            max_speed = min(self.cars.speed + self.acceleration, MAX_SPEED)
            max_distance = max_speed * FACTOR_FOR_DISTANCE_PER_ITERATION
            if max_distance < distance:
                self.cars.speed = max_speed
            else:
                self.cars.speed = max(self.cars.car_at_the_front.speed - self.deceleration, 0)
            self.cars.position = (self.cars.position + self.cars.speed * FACTOR_FOR_DISTANCE_PER_ITERATION) % CIRCUIT_LENGTH            
            self.cars = self.cars.car_at_the_back
        self.draw_cars()
       

if __name__ == '__main__':
    TrafficJams().mainloop()
