import numpy as np


num_points = 50
degree = 6
hyper = 1000
learning_rate = 0.001

x_data = [[0 for col in range(num_points)] for row in range(degree)]
y_data = []
prev_W = [0.5,0.5,1,1,1,0]

for i in range(num_points):
    prev_x = np.random.normal(0, 1.0)
         
    for j in range(degree):
        x_data[j][i] = pow(prev_x,j+1)

y_data = np.dot(prev_W, x_data)


#######################


import matplotlib.pyplot as plt
import tensorflow as tf



for degree_hat in range(1, degree):
    weights = []
    for i in range(degree_hat):
        weights.append(tf.Variable(tf.ones([1])))
    weights = tf.transpose(weights)

    y_hat = tf.matmul(weights, x_data[0:degree_hat])



    cost = tf.square(y_hat - y_data)

    regularization = tf.reduce_mean(tf.square(weights)*hyper)


    loss = tf.reduce_mean(cost+regularization) #+ lamda * tf.reduce_sum(tf.square(ws))





    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
    train = optimizer.minimize(loss)


    init = tf.global_variables_initializer()
    sess = tf.Session()
    sess.run(init)




    for step in range(500):
        sess.run(train) 
    # 산포도 그리기


    plt.plot(x_data[0], y_data, 'ro')
    # 직선 그리기

    draw_x_data = [[0 for col in range(100)] for row in range(degree_hat)]
    draw_x_data[0] = np.linspace(-10,10,100)


    for i in range(100):
        for j in range(degree_hat-1):
            draw_x_data[j+1][i] = pow(draw_x_data[0][i],j+2)

    draw_y_data = np.dot(sess.run(weights),draw_x_data)



    plt.plot(draw_x_data[0], np.transpose(draw_y_data))
    print(sess.run(weights))


# x, y 축 레이블링을 하고 각 축의 최대, 최소값 범위를 지정합니다.

plt.xlim(-2,2)
plt.ylim(-30, 120)
plt.xlabel('x')
plt.ylabel('y')
plt.show()