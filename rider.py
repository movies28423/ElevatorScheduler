from ride import Ride

class Rider:
    def __init__(self, rider_name, time_point, starting_point, end_point):
        self._rider_name = rider_name
        self._ride_list = [Ride(time_point, starting_point, end_point)]

    def get_rider_name(self):
        return self._rider_name   

    def get_rider_list(self):
        return self._ride_list  

    def add_ride(self, time_point, starting_point, end_point):
        self._ride_list.append(Ride(time_point, starting_point, end_point))

    def remove_ride(self):
        if len(self._ride_list) > 1:
            self._ride_list = self._ride_list[1::]
        else:
            self._ride_list = []


