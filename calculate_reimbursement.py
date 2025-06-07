import json
import sys
import math
import random
import heapq
list = []

with open('public_cases.json', 'r') as file:
    data = json.load(file)
for point in data:
    sublist = ((point["input"]["trip_duration_days"], point["input"]["miles_traveled"], point["input"]["total_receipts_amount"]), point["expected_output"])
    list.append(sublist)
random.shuffle(list)
list1 = list[0:200]
list2 = list[200:1000]

maxes = [0,0,0]
for i in list:
    point = i[0]
    for k in range(3):
        if point[k] > maxes[k]:
            maxes[k] = point[k]
def closest_point(point,set):
    smallest = (-1,-1,-1)
    smallest_dist = 100000
    output = -1
    for sup in set:
        s = sup[0]
        d = math.sqrt(((point[0]-s[0])/maxes[0])**2 + ((point[1]-s[1])/maxes[1])**2 + ((point[2]-s[2])/maxes[2])**2)
        if d < smallest_dist:
            smallest = s
            smallest_dist = d
            output = sup[1]
    return output
def k_closest_points(point,set,k,p=2):
    k_list = []
    for i in range(k):
        smallest_dist = -100000
        output = -1
        k_list.append((smallest_dist, output))
        heapq.heapify(k_list)
        for sup in set:
            s = sup[0]
            d = math.sqrt(((point[0]-s[0])/maxes[0])**2 + ((point[1]-s[1])/maxes[1])**2 + ((point[2]-s[2])/maxes[2])**2)
            heapq.heappushpop(k_list,(-1*d,s,sup[1]))
            if d < smallest_dist:
                smallest = s
                smallest_dist = d
                output = sup[1]
        distances = [-i[0] for i in k_list]
        outputs = [i[2] for i in k_list]
        num = 0
        den = 0
        for i in range(len(k_list)):
            if distances[i] == 0:
                return outputs[i]
            num += outputs[i]/(distances[i]**p)
            den += 1/(distances[i]**p)
        return num/den

def calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount):
    return k_closest_points((trip_duration_days,miles_traveled,total_receipts_amount),list,10)
def main():
    trip_duration = float(sys.argv[1])
    miles = float(sys.argv[2])
    receipts = float(sys.argv[3])                        
    result = calculate_reimbursement(trip_duration, miles, receipts)
    print(result)
if __name__ == "__main__":
    main()
