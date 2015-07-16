from Elevator_Scheduler import Elevator_Scheduler

'''

Generates the Data for a given Elevator Schedule
Interface for interacting with the Scheduler

'''
class Elevator_Times:
    def __init__(self, rider_file):
        self._elevator_scheduler = Elevator_Scheduler(rider_file)
        self._iterations = 0
        self.run_elevator_scheduler()
    
    ''' 
    function implements the programs strategy to determine how fast the elevator schedule can be completed
    '''
    def run_elevator_scheduler(self):
        while len(self._elevator_scheduler.get_completed_rides()) < self._elevator_scheduler.get_total_riders():
            while len([x for x in self._elevator_scheduler.get_cabs() if x.get_next_time() <= self._elevator_scheduler.get_time()]):

                first_cab = min(self._elevator_scheduler.get_cabs(), key=lambda p: (p.get_next_time()))
                last_time = first_cab.get_next_time()
                removed_riders = [x for x in first_cab.get_current_riders() if x[1].get_rider_list() != [] and  x[1].get_rider_list()[0].get_end_point() == first_cab.get_current_floor()]
                first_cab.set_current_riders([x for x in first_cab.get_current_riders() if x[1].get_rider_list() != [] and x[1].get_rider_list()[0].get_end_point() != first_cab.get_current_floor()])
                self._elevator_scheduler.let_riders_off(removed_riders)

                riders_to_add = self._elevator_scheduler.let_riders_on(first_cab)

                for rider in riders_to_add:
                    self._elevator_scheduler.get_rider_queue()[rider[1].get_rider_list()[0].get_starting_point()].put((rider[1].get_rider_list()[0].get_time_point(), rider[1]))

                if self._elevator_scheduler.change_direction(first_cab):
                    first_cab.change_direction()

                first_cab.move_car()
                first_cab.update_next_time() 
                
            self._elevator_scheduler.update_time()
            self._iterations += 1

    def get_completed_rides(self):
        return self._elevator_scheduler.get_completed_rides()

    def get_time(self):
        return self._elevator_scheduler.get_time()
