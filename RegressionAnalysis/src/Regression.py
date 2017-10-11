import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

def polynomial_regression(x_data, y_data, degree_level, paper, option):

    poly_x_data = [[pow(x, degree) for x in x_data] for degree in range(1, degree_level+1)]
    weights = [tf.Variable(tf.ones([1])) for degree in range(1, degree_level+1)]

    return regression(y_data, poly_x_data, tf.transpose(weights), paper=paper, option=option)

def regression(y_data, x_data, weights, paper, option):

    y_hat = tf.matmul(weights, x_data)

    cost = tf.square(y_hat - y_data)

    regularization = tf.reduce_mean(tf.square(weights) * option["hyper"])

    loss = tf.reduce_mean(cost + regularization)


    optimizer = tf.train.GradientDescentOptimizer(option["learning_rate"])
    train = optimizer.minimize(loss)


    init = tf.global_variables_initializer()
    sess = tf.Session()
    sess.run(init)


    for step in range(option["steps"]):
        sess.run(train) 


    return sess.run(weights)