import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

def polynomial_regression(y_data, x_data, order_level, option):
    # Extend data to enter polynomial variable.
    poly_x_data = [[pow(x, order) for x in x_data] for order in range(0, order_level)]
    weights = [tf.Variable(tf.ones([1])) for order in range(0, order_level)]

    return regression(y_data, poly_x_data, tf.transpose(weights), option=option)

## Regression using tensorflow library
def regression(y_data, x_data, weights, option):
    
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