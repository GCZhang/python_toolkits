#!/usr/bin/env python

import readtortout as RT
import matplotlib.pyplot as plt
import numpy as np
import sys

filename1 = sys.argv[1]
filename2 = sys.argv[2]

outerNum = int(sys.argv[3])
groupNum = [1,2,3,4]

plt.figure(num=1, figsize=(16, 9))
plt.title('Converge info', size=12)

#==============================================================================
# subplot 1
#==============================================================================
for i in range(len(groupNum)):
	plt.subplot(len(groupNum)/2,2,i+1)

	out1 = RT.ReadTort()
	out2 = RT.ReadTort()

	out1.readconverge(filename1,1,groupNum[i])
	out2.readconverge(filename2,1,groupNum[i])

	xData1 = np.arange(1,len(out1.conv)+1)
	xData2 = np.arange(1,len(out2.conv)+1)

	plt.xlabel('Iteration Number', size=12)
	plt.ylabel('Iteration Error', size=12)

	plt.xlim(0,max(len(out1.conv), len(out2.conv))+1)

	plt.semilogy(xData1, np.abs(out1.conv), color='b', marker='o'\
		, label=filename1)
	plt.semilogy(xData2, np.abs(out2.conv), color='r', marker='*'\
		, label=filename2)

	plt.legend(loc='best',fontsize='12')

	plt.text(0.5,0.85,\
		"Group : %d"%(groupNum[i]),\
		ha='center', va='center', fontsize=12, \
		transform=plt.gca().transAxes)

# plt.tight_layout()

plt.savefig('conv_o%s.png'%(outerNum),fmt='png')
