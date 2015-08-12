import random
import numpy as np
import matplotlib.pyplot as plt
import array
import itertools
import bases

#plt.plot([1,2,3,4])
#plt.ylabel('some numbers')
#plt.show()

# evenly sampled time at 200ms intervals
#t = np.arange(0., 5., 0.2)

# red dashes, blue squares and green triangles
#plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
#plt.show()

#In python: Black = 0; White = 1
#In ECA: Black = 1; white = 0

#neighborhood radius is number of blocks to either side
#For ECA n_rad = 1
n_rad = 1

#number of states for each site
#for ECA, n_rad = 2 [0,1]
n_k = 3

#Because python arrays are reversed need index limit for applying rule
hood_limit = n_k**(2*n_rad+1)-1

#Rule is integer between 1 and 256 for elementary CA
#For CA, integer may be larger
#Convert rule to bitarray of size 8 (for ECA)
rule = 110112222110112000110112000
rulen = 0
for k in range(len(str(rule))): rulen = rulen + n_k**(hood_limit-k)*int(str(rule)[k])

#rulen = 0b11100011111000001110001111100000
#rulen = 3823231968

#ruleb = bin(rulen)
#rule = ruleb[2:]

#Insert leading zero if necessary
#while len(rule) < n_k**(2*n_rad+1): rule = '0'+rule

#Create initial array
CA_size = 201

#random start
#x = np.random.randint(2,size = CA_size)

#random start with x_on% on
x_on = 0.30
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

steps = 400

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

#write output as portable bitmap (PBM)
#first line is "P1 width height" followed by
#height lines of 0's and 1's of length width

# Lets plot
fig, ax = plt.subplots()

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
plt.ylabel('Generation')

# Only show ticks on the left and bottom spines
#ax.yaxis.set_ticks_position('left')
#ax.xaxis.set_ticks_position('bottom')

plt.show()