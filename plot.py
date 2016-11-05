#!/usr/bin/env python

import readtortout as RT
import matplotlib.pyplot as plt
import numpy as np
import sys

out1 = RT.ReadTort()
out2 = RT.ReadTort()

filename1 = sys.argv[1]
filename2 = sys.argv[2]

outerNum = int(sys.argv[3])
Group1    = int(sys.argv[4])

out1.readconverge(filename1,outerNum,Group1)
out2.readconverge(filename2,outerNum,Group1)

xData1 = np.arange(1,len(out1.conv)+1)
xData2 = np.arange(1,len(out2.conv)+1)

plt.figure(num=1, figsize=(12.8, 7.2))


#==============================================================================
# subplot 1
#==============================================================================
# plt.subplot(211)

plt.title('Converge info', size=12)
plt.xlabel('Iteration Number', size=12)
plt.ylabel('Iteration Error', size=12)

plt.semilogy(xData1, np.abs(out1.conv), color='b', marker='o'\
	, label=filename1)
plt.semilogy(xData2, np.abs(out2.conv), color='r', marker='*'\
	, label=filename2)

plt.legend(loc='best')

plt.text(0.5,0.85,\
	"Outer Number : %d\nGroup Number : %d"%(outerNum,Group1),\
	ha='center', va='center', fontsize=12, \
	transform=plt.gca().transAxes)

#==============================================================================
# subplot 1
#==============================================================================
# out12 = RT.ReadTort()
# out22= RT.ReadTort()
# 
# out12.readconverge(filename1,outerNum,2)
# out22.readconverge(filename2,outerNum,2)
# 
# xData12 = np.arange(1,len(out12.conv)+1)
# xData22 = np.arange(1,len(out22.conv)+1)
# 
# plt.subplot(212)
# plt.xlabel('Iteration Number', size=12)
# plt.ylabel('Iteration Error', size=12)
# 
# plt.semilogy(xData12, np.abs(out12.conv), color='b', \
# 	label=filename1)
# plt.semilogy(xData22, np.abs(out22.conv), color='r', \
# 	label=filename2)
# 
# plt.legend(loc='best')
# 
# plt.text(0.5,0.85,\
# 	"Outer Number : %d\nGroup Number : %d"%(outerNum,2),\
# 	ha='center', va='center', fontsize=12, \
# 	transform=plt.gca().transAxes)

#============================================================================== 
plt.savefig('conv_o%sg%s.png'%(outerNum, Group1),fmt='png')
