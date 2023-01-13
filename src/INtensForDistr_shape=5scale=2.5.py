import matplotlib.pyplot as plt
import scipy.special as sps
import numpy as np
M = np.loadtxt("c:\_volume_vrija_.txt")
X,Y = M[:,0],M[:,4]
plt.plot(X, Y, linewidth=2, color='b')
#count, bins, ignored = plt.hist(s, 50, density=True)
plt.show()

