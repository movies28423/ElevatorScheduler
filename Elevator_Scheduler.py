import math
import Queue
import car
import rider

class Elevator_Scheduler:
    def __init__(self, rider_file):
        self._rider_queue = {}
        self._total_cabs = 0
        self._cabs = []
        self._total_riders = 0
        self.make_rider_queue(rider_file)
        self._time = max(self._cabs, key=lambda p: (p.get_latency())).get_latency()
        self._completed_rides = []

    def get_rider_queue(self):
        return self._rider_queue

    def get_cabs(self):
        return self._cabs

    def get_total_riders(self):
        return self._total_riders

    def get_max_floor(self):
        return self._max_floor

    def get_min_floor(self):
        return self._min_floor

    def get_time(self):
        return self._time

    def update_time(self):
        self._time += math.ceil(max(self._cabs, key=lambda p: (p.get_latency() + (1/p.get_fps()))).get_latency() + max(self._cabs, key=lambda p: (p.get_latency() + (1/p.get_fps()))).get_fps())

    def get_completed_rides(self):
        return self._completed_rides

    def make_rider_queue(self, riders_text):

        self._total_cabs = int(riders_text.readline())

        i = 0
        while i < self._total_cabs:
            new_cab_line = riders_text.readline()
            new_cab_list = new_cab_line.strip('\n').split(' ')
            self._cabs.append(Car(new_cab_list[0], int(new_cab_list[1]), float('0' + new_cab_list[2]), int(new_cab_list[3])))
            i+=1

        self._total_riders = int(riders_text.readline())

        rider_list = {}
        count = 0
        for line in riders_text:
            r_info = line.strip('\n').split(' ')
            r_name = r_info[0] 
            r_time = int(r_info[1])
            r_start = int(r_info[2])
            r_end = int(r_info[3])
            if len(rider_list.keys()) > 0 and r_name in rider_list.keys():
                rider_list[r_name].add_ride(r_time, r_start, r_end)
                if r_start not in self._rider_queue.keys():
                    self._rider_queue.update({r_start:Queue.PriorityQueue()})
            else:
                rider = Rider(r_name, r_time, r_start, r_end)
                rider_list.update({rider.get_rider_name():rider})
                if r_start in self._rider_queue.keys():
                    self._rider_queue[rider.get_rider_list()[0].get_starting_point()].put((rider.get_rider_list()[0].get_time_point(),rider))
                else:
                    new_floor = Queue.PriorityQueue()
                    new_floor.put((rider.get_rider_list()[0].get_time_point(),rider))
                    self._rider_queue.update({rider.get_rider_list()[0].get_starting_point():new_floor})

    def let_riders_off(self, removed_riders):
        completed_rides = []
        for rider_to_remove in removed_riders:
            self._completed_rides.append(rider_to_remove[1].get_rider_list()[0])
            rider_to_remove[1].remove_ride()
            if len(rider_to_remove[1].get_rider_list()) > 0:
                self._rider_queue[rider_to_remove[1].get_rider_list()[0].get_starting_point()].put((rider_to_remove[1].get_rider_list()[0].get_time_point(), rider_to_remove[1]))

    def let_riders_on(self, current_cab):
        riders_to_add = []
        while len(current_cab.get_current_riders()) < current_cab.get_capacity():
            if not self._rider_queue[current_cab.get_current_floor()].empty():
                next_rider = self._rider_queue[current_cab.get_current_floor()].get()    
                if next_rider != None:
                    if next_rider[1].get_rider_list()[0].get_end_point() == current_cab.get_current_floor():
                        self.let_riders_off([next_rider])
                    elif next_rider[1].get_rider_list()[0].get_time_point() <= int(current_cab.get_next_time()):
                        first_cab.get_current_riders().append(next_rider)                    
                    else:
                        riders_to_add.append(next_rider)
                        break
                else:
                    break
            else:
                break
        return riders_to_add

    def change_direction(self, current_cab):
        next_floor_exists = current_cab.get_current_floor() + current_cab.get_last_direction() in self._rider_queue.keys()
        riders_to_drop_off_in_dir = len([ x for x in current_cab.get_current_riders() if x[1].get_rider_list()[0].get_end_point() * current_cab.get_last_direction() > current_cab.get_current_floor() * current_cab.get_last_direction()]) > 0 
        riders_to_pick_up_in_dir = len([x for x in self._rider_queue.keys() if not self._rider_queue[x].empty() and x * current_cab.get_last_direction() > current_cab.get_current_floor() * current_cab.get_last_direction()]) > 0

        continue_in_current_dir = next_floor_exists and (riders_to_drop_off_in_dir or riders_to_pick_up_in_dir)

        other_dir_floor_exists = current_cab.get_current_floor() - current_cab.get_last_direction() in self._rider_queue.keys()
        riders_to_drop_off_in_other_dir = len([ x for x in current_cab.get_current_riders() if x[1].get_rider_list()[0].get_end_point() * current_cab.get_last_direction() < current_cab.get_current_floor() * current_cab.get_last_direction()]) > 0 
        riders_to_pick_up_in_other_dir = len([x for x in self._rider_queue.keys() if not self._rider_queue[x].empty() and x * current_cab.get_last_direction() < current_cab.get_current_floor() * current_cab.get_last_direction()]) > 0

        riders_in_other_dir = riders_to_drop_off_in_other_dir or riders_to_pick_up_in_other_dir

        return ((not continue_in_current_dir) and other_dir_floor_exists and riders_in_other_dir) or not next_floor_exists
