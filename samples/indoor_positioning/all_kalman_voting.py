import kalman
import service_redis as service
import pandas as pd
from easy_trilateration.model import *  
from easy_trilateration.least_squares import easy_least_squares  
from easy_trilateration.graph import *  
import math
import sys
from easy_trilateration.model import *  
from easy_trilateration.least_squares import easy_least_squares  
from easy_trilateration.graph import *  
import math
import numpy as np
import matplotlib.pyplot as plt
import json
import time


def kalman_filter(x, P, z, R, A, H, Q):
    # Prediction step
    x = np.dot(A, x)
    P = np.dot(A, np.dot(P, A.T)) + Q

    # Correction step
    y = z - np.dot(H, x)
    S = np.dot(H, np.dot(P, H.T)) + R
    K = np.dot(P, np.dot(H.T, np.linalg.inv(S)))
    x = x + np.dot(K, y)
    P = P - np.dot(K, np.dot(H, P))

    return x, P


def vote(input_file, x_pos, y_pos):
    with open("sensors.json") as f:
        sensors = json.load(f)
    file = input_file
    data = pd.read_csv(file)
    # data = pd.read_csv("positionsD.csv")
    beacons = {}
    for column in data.columns:
        beacons[column] = data[column][:3].tolist()

    beacons_1 = [beacons["AC233F826E21"], beacons["AC233F826E2D"], beacons["AC233F826E18"], beacons["AC233F826E17"], beacons["AC233F851F20"]]
    beacons_2 = [beacons["AC233F826E2A"], beacons["AC233F826E25"], beacons["AC233F826E24"], beacons["AC233F826E20"], beacons["AC233F851F2A"]]
    beacons_3 = [beacons["AC233F826E27"], beacons["AC233F826E29"], beacons["AC233F826E26"], beacons["AC233F826E16"], beacons["AC233F851F1D"]]
    beacons_4 = [beacons["AC233F826E19"], beacons["AC233F826E1A"], beacons["AC233F826E1D"], beacons["AC233F826E1B"], beacons["AC233F851F29"]]


    positions = []
    vote_count = 0
    lsml_count = 0
    vote_total_time = 0
    lsml_total_time = 0
    
    for i in range(3):
        circles = []
        distances = {}
        vote_start = time.time()
        sum1 = 0
        for item in beacons_1:
            sum1 += item[i]
        distances["AC233F826E21"] = sum1/5
        vote_count += 1
        sum2 = 0
        for item in beacons_2:
            sum2 += item[i]
        distances["AC233F826E2A"] = sum2/5
        vote_count += 1
        sum3 = 0
        for item in beacons_3:
            sum3 += item[i]
        distances["AC233F826E27"] = sum3/5
        vote_count += 1
        sum4 = 0
        for item in beacons_4:
            sum4 += item[i]
        distances["AC233F826E19"] = sum4/5
        vote_count += 1
        vote_end = time.time()
        vote_total_time += vote_end - vote_start
        for item in distances:
            circles.append(Circle(sensors[item]["X"], sensors[item]["Y"], distances[item]*100))
        print("number of circles: " + str(len(circles)))
        lsml_start = time.time()
        result, meta = easy_least_squares(circles)  
        create_circle(result, target=True)  
        #print("Result: {}".format(result))
        #circles.append(Point(138,688))
        #print("Positioning error: " + str(math.dist([138, 688], [result.center.x, result.center.y])))
        #draw(circles)
        positions.append([result.center.x, result.center.y])
        lsml_end = time.time()
        lsml_total_time += lsml_end - lsml_start
        lsml_count += 1
    
    print("vote total time: " + str(vote_total_time))
    print("lsml total time: " + str(lsml_total_time))
    print("vote count: " + str(vote_count))
    print("lsml count: " + str(lsml_count))


    # Initialize the Kalman filter
    x = np.array([0, 0, 0, 0])  # Initial state (position and velocity in x and y)
    P = np.eye(4)  # Initial state covariance
    R = np.eye(2)  # Measurement noise covariance
    Q = np.eye(4)  # Process noise covariance
    A = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]])  # Transition matrix
    H = np.array([[1, 0, 0, 0], [0, 1, 0, 0]])  # Measurement function

    # Arrays to store the filtered and unfiltered position data
    x_filtered = []
    y_filtered = []
    x_raw = []
    y_raw = []
    kalman_start = time.time()
    for z in positions:
        x, P = kalman_filter(x, P, z, R, A, H, Q)
        x_filtered.append(x[0])  # Store the filtered x position
        y_filtered.append(x[1])  # Store the filtered y position
        x_raw.append(z[0])  # Store the raw x position
        y_raw.append(z[1])  # Store the raw y position

    kalman_end = time.time()
    print("kalman time: " + str(kalman_end - kalman_start))
    print("Final position: (%.2f, %.2f)" % (x[0], x[1]))
    print("Positioning error: " + str(math.dist([x_pos, y_pos], [x[0], x[1]])))

    plt.plot(x_filtered, y_filtered, label='Filtered')
    plt.plot(x_raw, y_raw, label='Raw')
    plt.xlabel('X position (cm)')
    plt.ylabel('Y position (cm)')
    plt.legend()
    plt.show()
    
vote("positionsA.csv", 0, 210)
vote("positionsB.csv", 198, 190)
vote("positionsC.csv", 198, 555)
vote("positionsD.csv", 0, 550)