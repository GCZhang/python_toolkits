#!/usr/bin/env python
import xml.etree.ElementTree as ET
import sys
import os
import re

class IJXMLDefination():
	"""This class parse the I/J defination XML file to obtain the (I,J) point 
	pair. 
	'-' means continuous number and ',' or ' '<blank> means discrete number. Only one of these
	two symbols are allowed in a I/J set label.
	e.g. 3-8 means 3,4,5,6,7,8"""
	def __init__(self):
		self.isetList = []
		self.jsetList = []
		self.ksetList = []		

	def parsexml(self,filename):
		"""filename - xml file name"""
		pointxml = ET.parse(filename)
		root = pointxml.getroot()
		PointSetList = root.findall('pointset')

		if root.get('type')!='TORT' :
			sys.exit('For now, TORT is the only supported file type.')

		print 'Number of IJ point sets:%d.%s'%(len(PointSetList),os.linesep)

		for pset in PointSetList:
			for ijset in pset:
				if ijset.tag == 'iset':
					iset =  ijset.text
					if '-' in iset :
						tempList = map(int,re.split('-',iset))
						try:
							assert(tempList[0] <= tempList[1])
						except AssertionError, e:
							print tempList
							raise e
						self.isetList.append([i for i in xrange(tempList[0],tempList[1]+1)])
					elif ',' in iset :
						self.isetList.append(sorted(map(int,re.split(',',iset))))
					else:
						self.isetList.append(sorted(map(int,iset.split())))
				elif ijset.tag == 'jset':
					jset = ijset.text
					if '-' in jset :
						tempList = map(int,re.split('-',jset))
						try:
							assert(tempList[0] <= tempList[1])
						except AssertionError, e:
							print tempList
							raise e
						self.jsetList.append([j for j in xrange(tempList[0],tempList[1]+1)])
					elif ',' in jset :
						self.jsetList.append(sorted(map(int,re.split(',',jset))))
					else:
						self.jsetList.append(sorted(map(int,jset.split())))
				elif ijset.tag == 'kset':
					kset = ijset.text
					if '-' in kset :
						tempList = map(int,re.split('-',kset))
						try:
							assert(tempList[0] <= tempList[1])
						except AssertionError, e:
							print tempList
							raise e
						self.ksetList.append([j for j in xrange(tempList[0],tempList[1]+1)])
					elif ',' in kset :
						self.ksetList.append(sorted(map(int,re.split(',',kset))))
					else:
						self.ksetList.append(sorted(map(int,kset.split())))		
				else:
					sys.exit('xml format errror (tag) !')

		assert(len(self.isetList)==len(self.jsetList))


	def ouputijpair(self,filename):
		outputfile = file(filename,'w')
		#outputfile.write('Number of IJ point sets:%d.%s'%(len(PointSetList),os.linesep))
		for Index in xrange(len(self.isetList)):
			outputfile.write('-----IJK Pattern of Index %d-----%s'%(Index+1,os.linesep))
			for iNode in self.isetList[Index]:
				for jNode in self.jsetList[Index]:
					for kNode in self.ksetList[Index]:
						outputfile.write("%d,%d,%d %s"%(iNode,jNode,kNode,os.linesep))

if __name__ == '__main__':
	ijdef = IJXMLDefination()

	if len(sys.argv) < 2 :
		sys.exit("ERROR : Lacking XML file name")

	xmlfilename = sys.argv[1]

	ijdef.parsexml(xmlfilename)

	ijdef.ouputijpair('tttt.txt')
	
