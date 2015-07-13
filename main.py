import Elevator_Scheduler

rider_file = open(r'rider_list.txt','r')
elevator_scheduler = Elevator_Scheduler(rider_file)

i = 0
while len(elevator_scheduler.get_completed_rides()) < elevator_scheduler.get_total_riders():
    while len([x for x in elevator_scheduler.get_cabs() if x.get_next_time() <= elevator_scheduler.get_time()]):

        first_cab = min(elevator_scheduler.get_cabs(), key=lambda p: (p.get_next_time()))
        last_time = first_cab.get_next_time()
        removed_riders = [x for x in first_cab.get_current_riders() if x[1].get_rider_list() != [] and  x[1].get_rider_list()[0].get_end_point() == first_cab.get_current_floor()]
        first_cab.set_current_riders([x for x in first_cab.get_current_riders() if x[1].get_rider_list() != [] and x[1].get_rider_list()[0].get_end_point() != first_cab.get_current_floor()])
        elevator_scheduler.let_riders_off(removed_riders)

        riders_to_add = elevator_scheduler.let_riders_on(first_cab)

        for rider in riders_to_add:
            elevator_scheduler.get_rider_queue()[rider[1].get_rider_list()[0].get_starting_point()].put((rider[1].get_rider_list()[0].get_time_point(), rider[1]))

        if elevator_scheduler.change_direction(first_cab):
            first_cab.change_direction()

        first_cab.move_car()
        first_cab.update_next_time() 
                
    elevator_scheduler.update_time()
    i+=1 

print(max(elevator_scheduler.get_cabs(), key=lambda p: p.get_last_time()).get_last_time())
print(i)
