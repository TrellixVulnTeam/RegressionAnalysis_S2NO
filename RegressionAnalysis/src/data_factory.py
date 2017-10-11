import numpy as np

def factory():
    num_points = 50
    degree = 6
    hyper = 1000
    learning_rate = 0.001

    x_data = [[0 for col in range(num_points)] for row in range(degree)]
    y_data = []
    prev_W = [0.5,0.5,1,1,1,0]

    for i in range(num_points):
        x = np.random.normal(0, 1.0)
         
        for j in range(degree):
            x_data[j][i] = pow(x,j+1)

    y_data = np.dot(prev_W, x_data)


    return x_data[0],y_data