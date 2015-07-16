from Elevator_Times import Elevator_Times

rider_file = open(r'rider_list.txt','r')
elevator_times = Elevator_Times(rider_file)

print(elevator_times.get_completed_rides())
print(elevator_times.get_time())
