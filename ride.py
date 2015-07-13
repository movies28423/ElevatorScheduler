class Ride:
    def __init__(self, time_point, starting_point, end_point):
        self._time_point = time_point
        self._starting_point = starting_point
        self._end_point = end_point

    def get_time_point(self):
        return self._time_point

    def get_starting_point(self):
        return self._starting_point

    def get_end_point(self):
        return self._end_point
