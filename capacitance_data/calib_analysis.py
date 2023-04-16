import matplotlib.pyplot as plt
import numpy as np

F = plt.figure(figsize=(15,8))
ax = F.add_subplot(121)
xa = F.add_subplot(122)
labels = ['Soil 1 (N=50)','Soil 2 (N=50)','Veg Soil (N=149)','Bonsai Soil (N=150)']
pf = ['','2','_veg','_bonsai']
for l,p in zip(labels,pf):
    dd = np.loadtxt('dry_data'+p+'.txt')
    wd = np.loadtxt('wet_data'+p+'.txt')
    ax.hist(dd,bins=15,histtype='step',label=l,density=True)
    xa.hist(wd,bins=15,histtype='step',density=True)
ax.legend(loc='upper center',fontsize=15,ncol=2)
plt.savefig('test.png')