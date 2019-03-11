import numpy as np
import random
import matplotlib
import matplotlib.pyplot as plt

a = random.random()
print(a)

# 定义一个数组
Y = np.zeros(100)


super_sum = 0
n = 100000
for j in range(1,n):
    sum = 0
    for i in range(1,10):
        sum += random.random()*10
    int_sum = round(sum)
    Y[int_sum] += 1
    super_sum += int_sum

ex = super_sum/n
#print(Y)
X = range(0,100)

plt.scatter(X,Y)
plt.show()