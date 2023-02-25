import numpy as np
import matplotlib.pyplot as plt

dat43 = []
dat29 = []
with open("pump_data.dat",'r') as fin:
    for line in fin.readlines():
        td = line.split(',')
        if "#" in line: continue
        if td[0] != '':
            dat43.append(float(td[0]))
        dat29.append(float(td[1]))


F = plt.figure(figsize=(15,5))
ax = F.add_subplot(111)
ax.violinplot([dat29,dat43],positions=[29,43])
ax.set_xlabel('Hose Length')
ax.set_ylabel('mL pumped in 1.5s')
plt.savefig('pump_test.png')
