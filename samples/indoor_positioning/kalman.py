#values = [-74, -76, -76, -73, -74, -78, -78, -77, -78, -79]

# Tunable parameters
v0 = -75
uncertainty = 25**2
q= 0.001
r= 5

def KalmanFilter(values, v0, uncertainty, q, r):
    prediction = []
    prediction.append(v0)
    p = uncertainty + q

    for v in values:
        z = v
        k = p / (p + r)
        x = prediction[-1] + k * (z - prediction[-1])
        p = (1 - k) * p + q
        prediction.append(x)

    # remove first value
    prediction.pop(0)
    return prediction
