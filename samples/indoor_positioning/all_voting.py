import kalman
import service_redis as service
import pandas as pd
from easy_trilateration.model import *  
from easy_trilateration.least_squares import easy_least_squares  
from easy_trilateration.graph import *  
import math
import sys
import time


def vote(file, x, y):
    data = pd.read_csv(file)
    # data = pd.read_csv("positionsD.csv")
    beacons = {}
    for column in data.columns:
        beacons[column] = data[column][:3].tolist()
    #print(beacons)
    # Split beacons into groups of 5
    beacons_1 = [beacons["AC233F826E21"], beacons["AC233F826E2D"], beacons["AC233F826E18"], beacons["AC233F826E17"], beacons["AC233F851F20"]]
    beacons_2 = [beacons["AC233F826E2A"], beacons["AC233F826E25"], beacons["AC233F826E24"], beacons["AC233F826E20"], beacons["AC233F851F2A"]]
    beacons_3 = [beacons["AC233F826E27"], beacons["AC233F826E29"], beacons["AC233F826E26"], beacons["AC233F826E16"], beacons["AC233F851F1D"]]
    beacons_4 = [beacons["AC233F826E19"], beacons["AC233F826E1A"], beacons["AC233F826E1D"], beacons["AC233F826E1B"], beacons["AC233F851F29"]]

    # Apply the Kalman filter to the measurements
    filtered_1 = []
    filtered_2 = []
    filtered_3 = []
    filtered_4 = []
    kalman_count = 0
    kalman_start = time.time()
    for item in beacons_1:
        filtered_1.append(kalman.KalmanFilter(item, -75, 25**2, 0.001, 5)[-1])
        kalman_count += 1
    for item in beacons_2:
        filtered_2.append(kalman.KalmanFilter(item, -75, 25**2, 0.001, 5)[-1])
        kalman_count += 1
    for item in beacons_3:
        filtered_3.append(kalman.KalmanFilter(item, -75, 25**2, 0.001, 5)[-1])
        kalman_count += 1
    for item in beacons_4:
        filtered_4.append(kalman.KalmanFilter(item, -75, 25**2, 0.001, 5)[-1])
        kalman_count += 1
    kalman_end = time.time()
    print("Kalman filter applied to " + str(kalman_count) + " measurements in " + str(kalman_end - kalman_start) + " seconds")
    #print("Kalman filter applied to " + str(kalman_count) + " measurements")


    # Print the results
    #print("Filtered values for each beacon in each group")
    #print("Group 1: " + str(filtered_1))
    #print("Group 2: " + str(filtered_2))
    #print("Group 3: " + str(filtered_3))
    #print("Group 4: " + str(filtered_4))


    # Define the voting algorithm
    service.create_algorithm("simple", "no_history", "average", 0.05, 2, False)

    # Define the candidates
    service.create_candidate("beacon_1")
    service.create_candidate("beacon_2")
    service.create_candidate("beacon_3")
    service.create_candidate("beacon_4")
    service.create_candidate("beacon_5")
    vote_count = 0
    vote_start = time.time()
    # Vote
    output1, history, weights = service.vote_num("simple", 
                                            ["beacon_1", "beacon_2", "beacon_3", "beacon_4", "beacon_5"], 
                                            filtered_1)
    vote_count += 1
    output2, history, weights = service.vote_num("simple",
                                                ["beacon_1", "beacon_2", "beacon_3", "beacon_4", "beacon_5"],
                                                    filtered_2)
    vote_count += 1
    output3, history, weights = service.vote_num("simple",
                                                    ["beacon_1", "beacon_2", "beacon_3", "beacon_4", "beacon_5"],
                                                    filtered_3)
    vote_count += 1
    output4, history, weights = service.vote_num("simple",
                                                    ["beacon_1", "beacon_2", "beacon_3", "beacon_4", "beacon_5"],
                                                    filtered_4)
    vote_count += 1
    vote_end = time.time()
    print("Voting applied to " + str(vote_count) + " measurements in " + str(vote_end - vote_start) + " seconds")
    #print("Voting applied to " + str(vote_count) + " measurements")

    # Print the results
    #print("Voting results, in meters of distance")
    #print("Range 1: " + str(output1))
    #print("Range 2: " + str(output2))
    #print("Range 3: " + str(output3))
    #print("Range 4: " + str(output4))

    # Define the circles
    lsml_start = time.time()
    arr = [Circle(0, 0, output1 * 100),
        Circle(198, 0, output2 * 100),
        Circle(0, 718, output3 * 100),
        Circle(198, 718, output4 * 100)]
    result, meta = easy_least_squares(arr)  
    create_circle(result, target=True)  
    print("Result: {}".format(result))
    # Points: [0,210], [198,190],[198,555],[0,550]
    #arr.append(Point(x, y))
    # Print the distance between the result and the target
    print("Positioning error: " + str(math.dist([x, y], [result.center.x, result.center.y])))
    lsml_end = time.time()
    print("Least squares applied in " + str(lsml_end - lsml_start) + " seconds")
    #draw(arr)
    # plot the circles in arr using matplotlib
    for circle in arr:
        plt.gca().add_patch(plt.Circle((circle.center.x, circle.center.y), circle.radius, fill=False, color='blue'))
        # draw the center of the circle
        plt.plot(circle.center.x, circle.center.y, 'o', color='blue')
    plt.plot(x, y, 'o', color='green')
    plt.axis('scaled')
    plt.xlabel('X position (cm)')
    plt.ylabel('Y position (cm)')
    plt.show()

vote("positionsA.csv", 0, 210)
vote("positionsB.csv", 198, 190)
vote("positionsC.csv", 198, 555)
vote("positionsD.csv", 0, 550)