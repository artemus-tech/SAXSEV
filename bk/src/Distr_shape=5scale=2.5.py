import matplotlib.pyplot as plt
import scipy.special as sps
import numpy as np
shape, scale = 6., 2.5  # mean=4, std=2*sqrt(2)
s = np.random.gamma(shape, scale, 1000)
M = np.loadtxt("c:\VFDF.txt")
X,Y = M[:,0],M[:,4]
plt.plot(X, Y, linewidth=2, color='b')
#count, bins, ignored = plt.hist(s, 50, density=True)
y = X**(shape-1)*(np.exp(-X/scale) / (sps.gamma(shape)*scale**shape))
plt.plot(X, y*13, linewidth=2, color='r')
plt.show()

