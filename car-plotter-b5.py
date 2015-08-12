#0: no car
#1: stopped car
#2: half speed
#3: constant speed car

#Attempts to plot # of cars, average speed
#Attempts to plot # of jams, average speed of jams, 

import random
import numpy as np
import matplotlib.pyplot as plt
import array
import itertools
import bases

#In python: Black = 0; White = 1
#In ECA: Black = 1; white = 0

#neighborhood radius is number of blocks to either side
#For ECA n_rad = 1
n_rad = 3

#number of states for each site
#for ECA, n_rad = 2 [0,1]
n_k = 5

#Because python arrays are reversed need index limit for applying rule
hood_limit = n_k**(2*n_rad+1)-1

#Rule is integer between 1 and 256 for elementary CA
#For CA, integer may be larger
#Convert rule to bitarray of size 8 (for ECA)
#rule is  base n_k
#rulen is base 10
rule = 110112222110112000110112000
rulen = 0
for k in range(len(str(rule))): rulen = rulen + n_k**(hood_limit-k)*int(str(rule)[k])

#Create initial array
CA_size = 201

#random start
#x = np.random.randint(2,size = CA_size)

#random start with x_on% on
x_on = 0.38
xx = np.random.random_sample(size = CA_size)
x = array.array("i",itertools.repeat(0,CA_size))
for k in range(CA_size):
    if xx[k] > 1.-x_on:
        x[k] = 2
        
#seeded start
#x = array.array("i",itertools.repeat(0,CA_size))
#x[CA_size/2] = 1

#Make array "circular" put copy 0th element to end, copy nth element to beginning
#Unnecessary for neighborhood size of 3 --> may need to reinstate for larger neighborhoods
#x_temp = x
#x_temp = np.append(x_temp, x[0])
#x_temp = np.insert(x_temp,0,x[-1])

#Get neighborhood arrangements
nhoods = array.array("i",itertools.repeat(0,CA_size))

stopped = array.array("i",itertools.repeat(1,CA_size))
moving = array.array("i",itertools.repeat(2,CA_size))

steps = 400
num_cars = [np.count_nonzero(x)]
num_moving = [201-np.count_nonzero(np.subtract(x,moving))]
num_stopped = [201-np.count_nonzero(np.subtract(x,stopped))]
jam_dist = array.array("i",itertools.repeat(0,CA_size))

for j in range(steps):
    for i in range(CA_size):
        if i < CA_size-2:
            ii = i+1
#           iii = i+2
        else:
            if i == CA_size-1:
                ii = 0
#               iii = 1
            else:
                ii = i+1
#               iii = 0
        if j == 0:    
           nhoods[i] = x[i-1]*n_k**2+x[i]*n_k**1+x[ii]
        else:
           nhoods[i] = x[j,i-1]*n_k**2+x[j,i]*n_k**1+x[j,ii]
    new_x = array.array("i",itertools.repeat(0,CA_size))

#apply rule
    for i in range(CA_size):
        new_x[i] = int(str(rule)[hood_limit-nhoods[i]])
    if j == 0:
        x = np.append([x],[new_x], axis = 0)
    else:
        x = np.append(x,[new_x], axis = 0)

#calculate statistics
    num_cars = np.append(num_cars,[np.count_nonzero(new_x)],axis = 0)
    num_stopped = np.append(num_stopped,[201-np.count_nonzero(np.subtract(new_x,stopped))],axis = 0)
    num_moving = np.append(num_moving,[201-np.count_nonzero(np.subtract(new_x,moving))],axis = 0)
    #num_jams = np.append(num_jams,,axis = 0)
    #dist_jams = np.append(dist_jams,,axis = 0)

ave_speed = np.true_divide(num_moving,num_cars)    
            
#write output as portable bitmap (PBM)
#first line is "P1 width height" followed by
#height lines of 0's and 1's of length width

# Lets plot
#fig, ax = plt.subplots()
fig = plt.figure(figsize= (12,8)) #makes way for new plot
ax = plt.subplot2grid((4,2),(0,0), rowspan = 4)
bx = plt.subplot2grid((4,2),(0,1))
cx = plt.subplot2grid((4,2),(1,1))
dx = plt.subplot2grid((4,2),(2,1))
ex = plt.subplot2grid((4,2),(3,1))



image = x
ax.imshow(image, cmap=plt.cm.gist_yarg, interpolation='nearest')
ax.set_title('ECA Rule #'+str(rulen))

# Move left and bottom spines outward by 10 points
ax.spines['left'].set_position(('outward', 10))
#ax.spines['bottom'].set_position(('outward', 10))

# Hide the right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
#ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

ax.xaxis.set_major_locator(plt.NullLocator())
ax.set_ylabel('Generation')

# Only show ticks on the left and bottom spines
#ax.yaxis.set_ticks_position('left')
#ax.xaxis.set_ticks_position('bottom')

lab1 = 'Total'
lab2 = 'Stopped'
lab3 = 'Moving'

bx.set_ylabel('# of cars')
bx.set_ylim(0,1.1*num_cars[0])
bx.plot(num_cars, color='black', label=lab1)
bx.plot(num_stopped, color='red', label=lab2)
bx.plot(num_moving, color='green', label=lab3)

cx.set_ylabel('Average speed')
cx.set_ylim(0,1.1)
cx.plot(ave_speed,color = 'blue')

dx.set_ylabel('Number of jams')

ex.set_ylabel('Speed of jams')

ex.set_xlabel('Generation')

plt.show()

print num_cars