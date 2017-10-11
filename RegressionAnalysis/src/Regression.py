import numpy as np


num_points = 50
degree = 6
hyper = 0
learning_rate = 0.001

import matplotlib.pyplot as plt
import tensorflow as tf

def regression(argx_data, argy_data, degree_hat, paper, option):
    #x init
    x_data = [[0 for col in range(num_points)] for row in range(degree_hat)]
    for i in range(num_points):
        x = argx_data[i]
    
        for j in range(degree_hat):
            x_data[j][i] = pow(x,j+1)

    #y init
    y_data = argy_data

    #w init
    weights = []
    for i in range(degree_hat):
        weights.append(tf.Variable(tf.ones([1])))
    weights = tf.transpose(weights)



        


    y_hat = tf.matmul(weights, x_data[0:degree_hat])

    cost = tf.square(y_hat - y_data)

    regularization = tf.reduce_mean(tf.square(weights) * option["hyper"])

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



    paper.plot(draw_x_data[0], np.transpose(draw_y_data))
    print(sess.run(weights))




