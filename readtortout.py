#!/usr/bin/env python
import sys
#import os
#import re

import numpy as np

class ReadTort():
    """
    read parameters in TORT output. (This should be done first.)
    read mesh boundaries from tort.inp and put them in xList[], yList[] and zList[].
    read flux output and put them in self.flux[ng][k][i][j].
    """
    def __init__(self):
        self.ng = 0
        self.im = 0
        self.jm = 0
        self.km = 0
        self.k  = 0.0
        self.xList = []
        self.yList = []
        self.zList = []
        self.flux = []
        self.conv = []

    def readpara(self,filename):
        '''
        filename : tort.out 
        '''
        # find im, jm, km
        im_done=jm_done=km_done=ng_done = False
        tortfile = file(filename)
        for line in tortfile:       
            linelist = line.split()
            if len(linelist) == 0: continue
            
            if linelist[0] == "0im" :
                self.im = int(linelist[2])
                im_done = True
            
            if linelist[0] == "jm" : 
                self.jm = int(linelist[2])
                jm_done = True
            
            if linelist[0] == "km" : 
                self.km = int(linelist[2])
                km_done = True

            if linelist[0] == '0igm': 
                self.ng = int(linelist[2])
                ng_done = True

            if im_done and jm_done and  km_done and ng_done: break    

        tortfile.close()
        if self.im == 0 or self.jm == 0 or self.km == 0 or self.ng == 0:
            return 1

    def setpara(self, im, jm, km, igm):
        '''
        setpara(im,jm,km,igm)
        im : mesh numbers in i direction
        jm : mesh numbers in j direction
        km : mesh numbers in k direction
        igm : group numbers
        '''
        self.im = int(im)
        self.jm = int(jm)
        self.km = int(km)
        self.ng = int(igm)

    #===========================================================================
    # read tort file. 
    # get im,jm,km
    # get x/y/z[r/theta/z] fine mesh boundaries from 2** 3** 4**
    def readbound(self, filename):
        """ 
        read im,jm,km and x/y/z mesh boundaries
        filename : tort.inp
        """
        #return to the head of tort inputfile
        tortfile = file(filename)
        tortfile.seek(0)

        x_ok = False
        y_ok = False
        z_ok = False

        while True:
            line = tortfile.readline()
            linelist = line.split() 

            if len(linelist) == 0: continue

            if linelist[0] == "2**":
                print "I am reading 2**"
                if len(linelist) >= 2:
                    self.xList.extend(map(float,linelist[1:]))
                while True:
                    if len(self.xList) == self.im+1:
                        x_ok = True
                        break
                    line = tortfile.readline()
                    linelist = line.split()
                    self.xList.extend(map(float,linelist))

            if linelist[0] == "3**":
                print "I am reading 3**"
                if len(linelist) >= 2:
                    self.yList.extend(map(float,linelist[1:]))
                while True:
                    if len(self.yList) == self.jm+1:
                        y_ok = True
                        break
                    line = tortfile.readline()
                    linelist = line.split()
                    self.yList.extend(map(float,linelist))

            if linelist[0] == "4**":
                print "I am reading 4**"
                if len(linelist) >= 2:
                    self.zList.extend(map(float,linelist[1:]))
                while True:
                    if len(self.zList) == self.km+1:
                        z_ok = True
                        break
                    line = tortfile.readline()
                    linelist = line.split()
                    self.zList.extend(map(float,linelist))

            if x_ok and y_ok and z_ok:
                break

        tortfile.close()
        return 0

    # read xlist,ylist,zlist from output file
    def readbound_from_out(self,filename):
        '''
        filename : tort.out
        '''
        tortfile = file(filename)
        tortfile.seek(0)

        x_ok = False
        y_ok = False
        z_ok = False

        while True:
            line = tortfile.readline()
            
            if 'k bndry' in line: 
                while True:
                    linelist = tortfile.readline().split()
                    if len(linelist) == 0 : continue
                    self.zList.append(float(linelist[1]))
                    if len(self.zList) == self.km+1:
                        z_ok = True
                        break

            if 'j bndry' in line:
                while True:
                    linelist = tortfile.readline().split()
                    if len(linelist) == 0 : continue
                    self.yList.append(float(linelist[1]))
                    if len(self.yList) == self.jm+1:
                        y_ok = True
                        break                   

            if 'i bndry' in line:
                while True:
                    linelist = tortfile.readline().split()
                    if len(linelist) == 0 : continue
                    self.xList.append(float(linelist[1]))
                    if len(self.xList) == self.im+1:
                        x_ok = True
                        break               
            if x_ok and y_ok and z_ok :
                break
        tortfile.close()
    

    # read flux from output file.
    def readflux(self, filename):
        import os.path
        '''
        read flux from output file.
        This function should be called after readpara().
        '''
        tortfile = file(filename)
        tortfile.seek(0)

        g  = 0
        im = 0

        #self.flux = [[[[0.0 for j in xrange(self.jm)]for i in xrange(self.im)] for k in xrange(self.km)] for g in xrange(self.ng)]
        self.flux = np.zeros((self.ng,self.km,self.im,self.jm))
        
        while True:
            line = tortfile.readline()
            linelist = line.split()
            if len(linelist) == 0 : continue
            # jump to flux block
            if linelist[0] == '0scalar':
                for g in xrange(self.ng):
                    # print "I am reading group %d"%(g+1)
                    if g != 0:
                        line = tortfile.readline()
                        linelist = line.split()
                    try:
                        assert(g+1 == int(linelist[-1]))
                    except AssertionError,e:
                        raise e
                    # jump over blank line
                    tortfile.readline()

                    if self.jm != 1:
                        for k in xrange(self.km):
                            if self.km != 1 : tortfile.readline()
                            jblocknum = (self.jm-1)/8 + 1
                            for jblock in xrange(jblocknum):
                                iskip = []
                                tortfile.readline()
                                # calculate j start number and j end number of this j block.
                                # last j block 
                                if jblock == jblocknum-1:
                                    jhead = jblock * 8 + 1
                                    jtail = self.jm
                                else:
                                    jhead = jblock * 8 + 1
                                    jtail = jblock * 8 + 8
                                for i in xrange(self.im):
                                    if i in iskip: continue
                                    line = tortfile.readline()
                                    linelist = line.split()
                                    assert(int(linelist[0]) == i+1)

                                    if 'through' in linelist:
                                        istart = i
                                        iend = int(linelist[2])
                                        iskip = [ii for ii in xrange(istart,iend)]
                                        self.flux[g,k,istart:iend,(jhead-1):(jtail)] = self.flux[g,k,istart-1,(jhead-1):(jtail)]
                                        continue

                                    try:
                                        assert((jtail-jhead+1)==(len(linelist)-1))
                                    except AssertionError,e:
                                        print linelist
                                        raise e
                                        
                                    self.flux[g,k,i,(jhead-1):(jtail)] = map(float,linelist[1:])
                    else: # when km=1, output has different format.
                        kblocknum = (self.km-1)/8 + 1
                        for kblock in xrange(kblocknum):
                            # jump over title.
                            tortfile.readline()
                            if kblock == kblocknum - 1:
                                khead = kblock * 8 + 1
                                ktail = self.km
                            else:
                                khead = kblock * 8 + 1
                                ktail = kblock * 8 + 8
                            for i in xrange(self.im):
                                line = tortfile.readline()
                                linelist = line.split()
                                assert(int(linelist[0]) == i+1)

                                if 'through' in linelist:
                                    istart = i
                                    iend = int(linelist[2])
                                    iskip = [ii for ii in xrange(istart,iend)]
                                    self.flux[g,(khead-1):(ktail),istart:iend,0] = self.flux[g,(khead-1):(ktail),istart-1,0]
                                    continue

                                try:
                                    assert((ktail-khead+1)==(len(linelist)-1))
                                except AssertionError,e:
                                    print linelist
                                    raise e

                                self.flux[g,(khead-1):(ktail),i,0] = map(float,linelist[1:])
                break

            # End of File.
            if tortfile.tell() == os.path.getsize(filename): break

        tortfile.close()

    def readconverge(self, filename, out_itn=1, grp=1):
        '''
        read converge informations. Store iteration errors in self.conv[g,it,errors]
        This function could be called independently.
        -------
        filename : tort output filename
        itn : outer iteration number
        grp : group number
        -------
        '''
        # self.conv = np.array(0.0)

        tortfile = file(filename)
        tortfile.seek(0)

        in_out_itn = False
        in_grp = False
        Done = False

        seek_it = 0
        seek_g = 0

        for line in tortfile:

            linelist = line.split()
            if len(linelist) == 0 : continue

            # seek iteration messages
            if line[0:4] == '0itn':
                seek_it = seek_it + 1
                if seek_it == out_itn:
                    in_out_itn = True
                else:
                    in_out_itn = False

                if seek_it == out_itn +1:
                    Done = True
                continue

            if in_out_itn:
                if linelist[0] == '0grp':
                    seek_g = seek_g + 1
                    if seek_g == grp:
                        in_grp = True
                    else:
                        in_grp = False

                    if seek_g == grp + 1:
                        Done = True
                    continue

            if in_out_itn and in_grp:

                try:
                    assert(int(linelist[0]) == grp)
                    self.conv.append(float(linelist[5]))
                except ValueError,e:
                    Done = True
            
            if Done: break
                
                # try:
                #     assert(int(linelist[0]) == grp)
                # except AssertionError,e:
                #     print linelist
                #     raise e

    def readeigen(self,filename):
        read_k = False
        with open(filename,'r') as f:
            for line in f:
                linelist = line.split()
                if len(linelist) == 0 : continue

                if line[0:4] == '0itn':
                    read_k = True
                    continue

                if read_k:
                    self.k = float(linelist[8])
                    read_k = False
                    continue

                # multi process.
                if linelist[0] == '0region' or linelist[0] == '0scalar' :
                    break

        if self.k == 0.0:
            return 1
        else:
            return 0

#------------------------------------------------------------------------------
if __name__ == '__main__':
    import IJXMLDefination as ijxml

    def plus(a,b):
        return str(a)+str(b)

    tort = ReadTort()
    filename = sys.argv[1]
    errorcode = tort.readpara(filename)
    if errorcode : sys.exit("Error occured when reading im,jm,km,ng")
    tort.readflux(filename)

    tortme = ReadTort()
    filename_me = sys.argv[2]
    errorcode = tortme.readpara(filename_me)
    if errorcode : sys.exit("Error occured when reading im,jm,km,ng")
    tortme.readflux(filename_me)

    inputxml = ijxml.IJXMLDefination()
    inputxml.parsexml('ijset.xml')

    debugfile = file("debug.txt",'w')
    debugfile.write("im = %d, jm = %d, km = %d ng = %d %s"%(tort.im,tort.jm,tort.km,tort.ng,os.linesep))
    for g in xrange(tort.ng):
        debugfile.write("-group %d-%s"%(g+1,os.linesep))
        for k in xrange(tort.km):
            debugfile.write("--k %d--%s"%(k+1,os.linesep))
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
                        b = tortme.flux[g][k][iNode-1][jNode-1]
                        error.append(abs((a-b)/b))
                        if maxerror < abs((a-b)/b) :
                            maxerror = abs((a-b)/b)
                            ii = iNode
                            jj = jNode
                        debugfile.write("%s(i=%3d j=%3d) : %12.5e | %s %12.5e | %12.5e %s"\
                            %(sys.argv[1],iNode,jNode,a,sys.argv[2],b,(a-b)/b,os.linesep))

            maxerror1=max(error)
            debugfile.write('max error : %e occured at [%3d, %3d, %3d, %3d]%s'\
                %(maxerror,g+1,k+1,ii,jj,os.linesep))
        

        
