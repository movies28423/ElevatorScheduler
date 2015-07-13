import math

class Car:
    def __init__(self, car_name, capacity, fps, starting_point):
        self._car_name = car_name
        self._fps = fps
        self._current_floor = starting_point
        self._capacity = capacity
        self._current_riders = []
        self._latency = 0
        self._next_time = math.ceil(1/self._fps)
        self._last_direction = 1
        self._last_time = 0.0

    def get_car_name(self):
        return self._car_name   

    def get_fps(self):
        return self._fps

    def get_current_floor(self):
        return self._current_floor

    def get_capacity(self):
        return self._capacity

    def get_current_riders(self):
        return self._current_riders

    def set_current_riders(self, riders_in_car):
        self._current_riders = riders_in_car

    def get_latency(self):
        return self._latency

    def set_latency(self, updated_latency):
        self._latency = updated_latency

    def get_next_time(self):
        return self._next_time

    def update_next_time(self):
        self._last_time = self._next_time
        self._next_time += math.ceil(self._latency + (1/self._fps))

    def get_last_direction(self):
        return self._last_direction 

    def change_direction(self):
        self._last_direction *= -1
    
    def move_car(self):
        self._current_floor += self._last_direction

    def get_last_time(self):
        return self._last_time
