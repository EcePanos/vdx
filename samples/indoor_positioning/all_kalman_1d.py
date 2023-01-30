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

    kalman_count = 0
    multilateration_count = 0
    circle_count = 0
    #positions = []
    circles = []
    distances = {}
    for i in range(len(beacons["AC233F826E21"])): 
        for beacon in beacons:
            if beacon not in distances:
                distances[beacon] = []
            distances[beacon].append(beacons[beacon][i]*100)
    kalman_start = time.time()  
    for item in distances:
        distances[item] = kalman.KalmanFilter(distances[item], -75, 25**2, 0.001, 5)[-1]
        kalman_count += 1
    kalman_end = time.time()
    print("Kalman time: " + str(kalman_end-kalman_start))

    for item in distances:
        circles.append(Circle(sensors[item]['X'], sensors[item]['Y'], distances[item]))
        circle_count += 1

    multilateration_start = time.time()
    result, meta = easy_least_squares(circles)  
    create_circle(result, target=True)
    multilateration_count += 1  
    print("Result: {}".format(result))
    multilateration_end = time.time()
    print("Multilateration time: " + str(multilateration_end-multilateration_start))
    circles.append(Point(x_pos, y_pos))
    print("Positioning error: " + str(math.dist([x_pos, y_pos], [result.center.x, result.center.y])))
    print("Kalman count: " + str(kalman_count))
    print("Multilateration count: " + str(multilateration_count))
    print("Circle count: " + str(circle_count))
    #draw(circles)
    
vote("positionsA.csv", 0, 210)
vote("positionsB.csv", 198, 190)
vote("positionsC.csv", 198, 555)
vote("positionsD.csv", 0, 550)