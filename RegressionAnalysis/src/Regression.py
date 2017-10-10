import numpy as np


num_points = 50
degree = 6
hyper = 0
learning_rate = 0.001


def factory():
    x_data = [[0 for col in range(num_points)] for row in range(degree)]
    y_data = []
    prev_W = [0.5,0.5,1,1,1,0]

    for i in range(num_points):
        x = np.random.normal(0, 1.0)
         
        for j in range(degree):
            x_data[j][i] = pow(x,j+1)

    y_data = np.dot(prev_W, x_data)

    return x_data[0], y_data

#######################


import matplotlib.pyplot as plt
import tensorflow as tf

def regression(argx_data, argy_data):
    y_data = argy_data

    degree_level = 10

    plt.plot(argx_data, argy_data, 'ro')
    
    for degree_hat in range(1, degree_level):
        #x init
        x_data = [[0 for col in range(num_points)] for row in range(degree_hat)]
        for i in range(num_points):
            x = argx_data[i]
    
            for j in range(degree_hat):
                x_data[j][i] = pow(x,j+1)

        #w init
        weights = []
        for i in range(degree_hat):
            weights.append(tf.Variable(tf.ones([1])))
        weights = tf.transpose(weights)



        


        y_hat = tf.matmul(weights, x_data[0:degree_hat])

        cost = tf.square(y_hat - y_data)

        regularization = tf.reduce_mean(tf.square(weights) * hyper)

        loss = tf.reduce_mean(cost + regularization)


        optimizer = tf.train.GradientDescentOptimizer(learning_rate)
        train = optimizer.minimize(loss)


        init = tf.global_variables_initializer()
        sess = tf.Session()
        sess.run(init)


        for step in range(500):
            sess.run(train) 







        
        # draw

        draw_x_data = [[0 for col in range(100)] for row in range(degree_hat)]
        draw_x_data[0] = np.linspace(-10,10,100)


        for i in range(100):
            for j in range(degree_hat-1):
                draw_x_data[j+1][i] = pow(draw_x_data[0][i],j+2)

        draw_y_data = np.dot(sess.run(weights),draw_x_data)



        plt.plot(draw_x_data[0], np.transpose(draw_y_data))
        print(sess.run(weights))

    plt.xlim(-2,2)
    plt.ylim(-30, 120)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()


argx_data, argy_data = factory()
regression(argx_data, argy_data)