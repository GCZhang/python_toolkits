#!/usr/bin/env python

import sys
import os
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


import readtortout as read
import IJXMLDefination as ijxml

if len(sys.argv) < 3:
    sys.exit("Arguments Error!")

tort = read.ReadTort()
filename = sys.argv[1]
errorcode = tort.readpara(filename)
if errorcode : sys.exit("Error occured when reading im,jm,km,ng")
tort.readflux(filename)

jsnt = read.ReadTort()
filename_jsnt = sys.argv[2]
errorcode = jsnt.readpara(filename_jsnt)
if errorcode : sys.exit("Error occured when reading im,jm,km,ng")
jsnt.readflux(filename_jsnt)

try:
    open('ijset.xml','r')
except IOError, e:
    sys.exit('Error occured when opening ijset.xml!')
inputxml = ijxml.IJXMLDefination()
inputxml.parsexml('ijset.xml')

if len(sys.argv) == 4 and sys.argv[3] == '-d':
    Debug = True
else:
    Debug = False

if Debug:
    debugfile = file("compare_debug.txt",'w')
    debugfile.write("im = %d, jm = %d, km = %d ng = %d %s"%(tort.im,tort.jm,tort.km,tort.ng,os.linesep))

for g in xrange(tort.ng):
    if Debug: debugfile.write("-group %d-%s"%(g+1,os.linesep))
    for k in xrange(tort.km):
        if Debug: debugfile.write("--k %d--%s"%(k+1,os.linesep))
        #a = ["j=" for i in xrange(10)]
        #b = [j for j in xrange(10)]
        #jo = map(plus,a,b)
        #print >> debugfile,jo
        error = []
        maxerror = 0.0
        ii = 0
        jj = 0
        for index in xrange(len(inputxml.isetList)):
            for iNode in inputxml.isetList[index]:
                for jNode in inputxml.jsetList[index]:
                    a = tort.flux[g][k][iNode-1][jNode-1]
                    b = jsnt.flux[g][k][iNode-1][jNode-1]
                    Err = (b-a)/a
                    error.append(abs(Err))
                    if maxerror < abs(Err):
                        maxerror = abs(Err)
                        ii = iNode
                        jj = jNode
                    if Debug: debugfile.write("%s(i=%3d j=%3d) : %12.5e | %s %12.5e | %12.5e %s"\
                        %(sys.argv[1],iNode,jNode,a,sys.argv[2],b,Err,os.linesep))

        maxerror1=max(error)
    if Debug:
        debugfile.write('max error : %e occured at [%3d, %3d, %3d, %3d]%s'\
        %(maxerror,g+1,k+1,ii,jj,os.linesep))
    else:
        print 'max error : %e occured at [%3d, %3d, %3d, %3d]'\
        %(maxerror,g+1,k+1,ii,jj)
        print ' '*35,'[  g,   k,   i,   j]'
        

# =======================================================================
# plot
#fig = plt.figure(1)
#
## ax = fig.add_subplot(111,projection='3d')
#
#ax = Axes3D(fig)
#
#X = np.arange(1,len(jsnt.flux[0,0,:,0])+1)
#Y = np.arange(1,len(jsnt.flux[0,0,0,:])+1)
#X,Y = np.meshgrid(X,Y)
#
#Z = np.transpose(jsnt.flux[0,0,:,:])
#
#ax.plot_surface(X,Y,Z,rstride=1,cstride=1,cmap='hot')
#
## semilogy does not work for 3D!
## ax.semilogy(X,Y,np.log10(Z),rstride=1,cstride=1,cmap='hot')
#
#plt.show()
