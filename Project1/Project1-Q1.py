#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 20:52:20 2020

@author: AppleMoony
"""
import numpy as np
import matplotlib.pyplot as plt

######## a) Plot theta1, theta2, theta3 over n 

#x = sorted(list(set(np.round(10** np.arange(0, 7.2, 0.2)))))
arr = np.round(10** np.arange(0.2, 7.2, 0.2))


theta1=np.empty(len(arr))
theta2=np.empty(len(arr))
theta3=np.empty(len(arr))
ess2=np.empty(len(arr))
ess3=np.empty(len(arr))

for i in range(len(arr)):

    n=int(arr[i])

## alternative 1

    x = np.random.normal(2, 1, n)
    y = np.random.normal(2, 1, n)
    li1=np.sqrt(x**2 + y**2)
    theta1[i]=np.mean(li1)

    
    
## alternative 2

    x = np.random.normal(0, 1, n)
    y = np.random.normal(0, 1, n)
    w2 = np.exp(2*(x+y-2))
    ess2[i] = n/(1+np.var(w2, ddof = 1))
    li2= np.sqrt(x**2+y**2) * w2
    theta2[i]=np.mean(li2)

    
## alternative 3

    x = np.random.normal(0, 4, n)
    y = np.random.normal(0, 4, n)
    w3 = 16 * np.exp( -15./32.*(x**2 + y**2) + 2*(x+y) - 4)
    li3=  w3 * np.sqrt(x**2+y**2)
    ess3[i] = n/(1+np.var(w3, ddof = 1))
    theta3[i]=np.mean(li3)




fig = plt.figure()
plt.title('Theta over n')
plt.xscale('symlog')
plt.plot(arr, theta1)
plt.plot(arr, theta2)
plt.plot(arr, theta3)
plt.legend(['theta1', 'theta2', 'theta3'], loc='upper right')
plt.xlabel('sample size')
plt.ylabel('estimated theta')

plt.show()
fig.savefig('q1_1.png')



######## b) Plot theta1, theta2, theta3 over n 

temp = list(range(1, 10000)) + list(range(10000, 1000000, 10000))

error1 = np.empty(50)


error11 = np.empty(len(temp))
error22 = np.empty(len(arr))
error33 = np.empty(len(arr))

# True theta
theta_t = theta1[-1]


### calculation for error 1
for i in range(len(temp)):
    for j in range(50):
        x1 = np.random.normal(loc = 2, size = temp[i])
        y1 = np.random.normal(loc = 2, size = temp[i])
        error1[j] = abs( np.mean(np.sqrt(x1**2 + y1**2)) - theta_t)
        
    error11[i] = np.mean(error1)


# caculate error 2 and 3
for i in range(len(arr)):
    error2 = np.empty(100)
    error3 = np.empty(100)
    for j in range(100):
           
        x2 = np.random.normal(size = int(arr[i]))
        y2 = np.random.normal(size = int(arr[i]))
        omega2 = np.exp(2*(x2+y2-2))
        error2[j] = abs(np.mean(omega2 * np.sqrt(np.square(x2) + np.square(y2))) - theta_t)
        
        x3 = np.random.normal(loc=0, scale = 4, size = int(arr[i]))
        y3 = np.random.normal(loc=0, scale = 4, size = int(arr[i]))
        omega3 = 16 * np.exp(-15./32.*(x3**2 + y3**2) + 2*(x3+y3) - 4)
        error3[j] = abs( np.mean(omega3 * np.sqrt(x3**2 + y3**2)) - theta_t )   

    error22[i] = np.mean(error2)
    error33[i] = np.mean(error3)

# estimated effective sample sizes for alternative2 and alternative3

ess2_est = np.empty(35)
for i in range(35):
    ess2_est[i] = temp[np.min(np.where(error11 <= error22[i]))]

ess3_est = np.empty(35)
for i in range(35):
    ess3_est[i] = temp[np.min(np.where(error11 <= error33[i]))]
    
#rank2 = np.argsort(ess2_est)
#rank3 = np.argsort(ess3)



##plot 1###
fig = plt.figure()
plt.xscale('symlog')
plt.yscale('symlog')
plt.title('Alternative 2 ess* and ess')
#ess*
plt.plot(arr, ess2_est)
#ess
plt.plot(arr, ess2)
plt.legend(['ess*', 'ess'], loc='upper left')
plt.xlabel('sample size')
plt.ylabel('ess')
fig.savefig('q1_2_1.png')

##plot2##
fig = plt.figure()
plt.xscale('symlog')
plt.yscale('symlog')
plt.title('Alternative 3 ess* and ess')
#ess*
plt.plot(arr, ess3_est)
#ess
plt.plot(arr, ess3)
plt.legend(['ess*', 'ess'], loc='upper left')
plt.xlabel('sample size')
plt.ylabel('ess')
fig.savefig('q1_2_2.png')

####
fig = plt.figure()
rank2 = np.argsort(ess2_est)
plt.plot(ess2_est[rank2], ess2[rank2])
plt.xlabel('ess*')
plt.ylabel('ess')
plt.title('Alternative 2 ess* and ess')
fig.savefig('q1_2_3.png')


## plot3 ##
fig = plt.figure()
rank3 = np.argsort(ess3_est)
plt.plot(ess3_est[rank3], ess3[rank3])
#plt.plot(ess3_est, ess3)
plt.xlabel('ess*')
plt.ylabel('ess')
plt.title('Alternative 3 ess* and ess')
fig.savefig('q1_2_4.png')

