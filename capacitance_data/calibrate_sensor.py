import glob
import matplotlib.pyplot as plt
import numpy as np

dd1 = np.loadtxt('dry_data.txt')
dd2 = np.loadtxt('dry_data2.txt')
wd1 = np.loadtxt('wet_data.txt')
wd2 = np.loadtxt('wet_data2.txt')

F = plt.figure()
ax = F.add_subplot(111)
ax.hist(dd1,bins=12,histtype='step')
ax.hist(dd2,bins=12,histtype='step')
ax.hist(wd1,bins=12,histtype='step')
ax.hist(wd2,bins=12,histtype='step')
plt.show()