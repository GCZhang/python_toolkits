#!/usr/bin/env python

# how to align the double y axis (linear and log)?
import numpy as np
import sys
from matplotlib import rcParams
rcParams['font.family'] = 'Times New Roman'
import matplotlib.ticker
import matplotlib.pyplot as plt

input_file = sys.argv[1]

time = []
power= []
error= []

# ---------------read power from output file
with open(input_file, 'r') as f:
    for line in f:
        line_list = line.split()
        if line_list[0] == '[MOCEX_TFSP]' or line_list[0] == '[MOCEX-K]':
            time.append(float(line_list[3]))
            power.append(float(line_list[-1]))

error = [power[i]-power[i-1] for i in range(1,len(power))]

print ("time: ", time)
print ("power: ", power)
print ("error: ", error)
# ---------------plot power-------------------
fig, ax1 = plt.subplots()
#plt.plot(time, power, marker='s', color='#ff557f', label='Power')

# power
ax1.plot(time, power, color='#ff557f', label='Power')
ax1.set_xlabel('Times (s)', color='#ff557f')
ax1.set_ylabel('Relative Integral Power', color='#ff557f')
ax1.tick_params('y', colors='#ff557f')
ax1.ticklabel_format(axis='y', style='plain', useOffset=False)
ax1_yticks = ax1.get_yticks()
print("ax1 yticks: ", ax1.get_yticks())

# error
ax2 = ax1.twinx()
ax2.semilogy(time[1:], map(abs,error), color='k')
ax2.set_ylabel('sucessive difference', color='k')
ax2.tick_params('y', colors='k')
ax2_ylim = ax2.get_ylim()
print("ax2 ylim: ", ax2.get_ylim())
ax2_yticks = np.logspace(np.log10(ax2_ylim[0]), np.log10(ax2_ylim[1]), len(ax1_yticks))
print("ax2_ticks: ", ax2_yticks)
#ax2.set_yticks(ax2_yticks)
#ax2.yaxis.set_major_locator(matplotlib.ticker.FixedLocator(ax2_yticks))
#ax2.ticklabel_format(axis='y', style='sci', scilimits=(0,0))


#fig.legend(loc='best')
plt.grid(b=True, which='major', linestyle='--')

fig.tight_layout()

plt.show()
