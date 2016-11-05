#!/usr/bin/env python
import readtortout as rtort
import math
import numpy as np
import bisect
import sys

from matplotlib import pyplot as plt
#-----------------------------------
# note: ./printPointFLux tort.out scalar_flux

jsnt = rtort.ReadTort()
tort = rtort.ReadTort()

outFile1 = sys.argv[1]
outFile2 = sys.argv[2]

errCode = jsnt.setpara(90,90,90,1)
errCode = tort.setpara(90,90,90,1)
if errCode: sys.exit('Error occured when reading para.')
jsnt.readbound_from_out('jsnt.out')
jsnt.readflux(outFile2)
tort.readbound_from_out('tort.out')
tort.readflux(outFile1)

mvp1A = [
8.29260E+00,
1.87028E+00,
7.13986E-01,
3.84685E-01,
2.53984E-01,
1.37220E-01,
4.65913E-02,
1.58766E-02,
5.47036E-03,
1.85082E-03
]

#---------------------1A----------------------
pointList1A = []
Index1A = []
jsntflux = []
tortflux = []
yList = np.arange(5.0,100.0,10.0)

x = 5.0
z = 5.0

for y in yList:
	pointList1A.append([x,y,z])

print '%10s, :   tort flux   :   jsnt flux'%('index')
for point in pointList1A:
	xIndex = bisect.bisect(jsnt.xList, point[0])
	yIndex = bisect.bisect(jsnt.yList, point[1])
	zIndex = bisect.bisect(jsnt.zList, point[2])

	Index1A.append([xIndex,yIndex,zIndex])
	print xIndex,yIndex,zIndex, ' : ', tort.flux[0,zIndex-1,xIndex-1,yIndex-1], ':', jsnt.flux[0,zIndex-1,xIndex-1,yIndex-1]
	jsntflux.append(jsnt.flux[0,zIndex-1,xIndex-1,yIndex-1])
	tortflux.append(tort.flux[0,zIndex-1,xIndex-1,yIndex-1])

plt.figure(num=1,figsize=(8,6))

plt.title('flux distribution along y of Case ii')
plt.xlabel(r'$y/cm$')
plt.ylabel(r'$flux/cm^{-2}\cdot{s}^{-1}$')

plt.semilogy(yList, mvp1A, marker='*', markersize=8, color='r', label='GMVP')
plt.semilogy(yList, jsntflux, marker='o', markersize=8, color='b', label='JSNTS')
plt.semilogy(yList, tortflux, marker='^', markersize=8, color='y', label='TORT')
plt.semilogy([45,45],[1.0e-3,mvp1A[4]],c='r',linewidth=2, linestyle='--')
plt.annotate(r'$y_0=45cm$',xy=(45,1.0e-3),xytext=(+10,+10),textcoords='offset points',fontsize=12)

plt.legend(loc='best')

plt.savefig('1A.png',fmt='png')
# plt.show()

#---------------------1A----------------------
jsntflux = []
tortflux = []
pointList1B = []
xData = []
yList = np.arange(5.0,100.0,10.0)
mvp1B = [
8.29260E+00,
6.63233E-01,
2.68828E-01,
1.56683E-01,
1.04405E-01,
3.02145E-02,
4.06555E-03,
5.86124E-04,
8.66059E-05,
1.12892E-05
]

for y in yList:
	pointList1B.append(np.array([y,y,y]))
print '%10s, :   tort flux   :   jsnt flux'%('index')
for point in pointList1B:
	xIndex = bisect.bisect(jsnt.xList, point[0])
	yIndex = bisect.bisect(jsnt.yList, point[1])
	zIndex = bisect.bisect(jsnt.zList, point[2])
	xData.append(np.sqrt(np.sum(point**2)))
	print xIndex,yIndex,zIndex, ' : ', tort.flux[0,zIndex-1,xIndex-1,yIndex-1], ':', jsnt.flux[0,zIndex-1,xIndex-1,yIndex-1]
	jsntflux.append(jsnt.flux[0,zIndex-1,xIndex-1,yIndex-1])
	tortflux.append(tort.flux[0,zIndex-1,xIndex-1,yIndex-1])
print xData

plt.figure(num=2,figsize=(8,6))
ax = plt.gca()
plt.subplot(111)
plt.title('flux distribution of Case ii : 1B')
plt.xlabel(r'$l/cm$')
plt.ylabel(r'$flux/cm^{-2}\cdot{s}^{-1}$')
plt.xlim(0.0,np.max(xData)*1.1)
plt.ylim(np.min(mvp1B)*0.5,np.max(mvp1B)*1.5)

ticks = [0.0]
ticks.extend(xData)
# print ticks
ax.set_xticks(ticks)
ax.set_xticklabels(["0",r"$5\sqrt{3}$",r"$15\sqrt{3}$",r"$25\sqrt{3}$",r"$35\sqrt{3}$",r"$45\sqrt{3}$"\
	,r"$55\sqrt{3}$",r"$65\sqrt{3}$",r"$75\sqrt{3}$",r"$85\sqrt{3}$",r"$95\sqrt{3}$"])

plt.semilogy(xData, mvp1B, marker='*', markersize=8, color='r', label='GMVP')
plt.semilogy(xData, jsntflux, marker='o', markersize=8, color='b', label='JSNTS')
plt.semilogy(xData, tortflux, marker='^', markersize=8, color='y', label='TORT')
# plt.semilogy([45,45],[1.0e-3,mvp1A[4]],c='r',linewidth=2, linestyle='--')
# plt.annotate(r'$y_0=45cm$',xy=(45,1.0e-3),xytext=(+10,+10),textcoords='offset points',fontsize=12)

plt.legend(loc='best')
plt.grid(True)

plt.savefig('1B.png',fmt='png')