#!/bin/env python

import sys
import os

file_BOXES = sys.argv[1]
file_HEX = sys.argv[2]
coords = []

output_file = open(file_HEX, 'w')

HEX_faces = []
HEX_faces.append([1,5,6])
HEX_faces.append([2,3,4])

with open(file_BOXES) as input_file:
	line = input_file.readline()
	line_list = line.split()
	output_file.write(line)
	numVertices = int(line_list[0])
	dimension = int(line_list[1])
	numBlocks = int(line_list[2])

	modulus = (dimension*numVertices)%8
	if (modulus==0):
		line_num = (dimension*numVertices)/8
	else:
		line_num = (dimension*numVertices - modulus)/8 + 1

	for num in range(line_num):
		line = input_file.readline()
		output_file.write(line)

	for block in range(numBlocks):
		line = input_file.readline()
		line_list = line.split()
		NumElementsInBlock = int(line_list[0])
		NumBoundarySurfaces = int(line_list[1])
		NodesPerElement = 6
		unusedInteger = 0
		Order_Interp = int(line_list[4])
		Order_Equat = int(line_list[5])
		if NumElementsInBlock !=2:
			sys.stderr.write("The NumElementsInBlock is not 2!")
			sys.exit(1)
		output_file.write("%10d"%(1))
		output_file.write("%10d"%(NumBoundarySurfaces))
		output_file.write("%10d"%(NodesPerElement))
		output_file.write("%10d"%(unusedInteger))
		output_file.write("%10d"%(Order_Interp))
		output_file.write("%10d"%(Order_Equat))
		output_file.write("%s"%os.linesep)

		# element type and material zone
		line = input_file.readline()
		line_list = line.split()
		RegionName = line_list[1]
		ElementType = "HEXAGON"
		output_file.write("%s%s"%(ElementType.ljust(16),RegionName.ljust(16)))
		output_file.write("%s"%os.linesep)

		# node index
		line = input_file.readline()
		line_list = line.split()
		output_file.write("%10s%10s%10s%10s%10s%10s"%(line_list[0],line_list[1],line_list[5],line_list[6],line_list[2],line_list[3]))
		output_file.write("%s"%os.linesep)
		# reflective boundaries
		if NumBoundarySurfaces != 0:
			output_file.write(input_file.readline())
			line = input_file.readline()
			line_list = line.split()
			for face in range(NumBoundarySurfaces):
				element = int(line_list[2*face])
				BOX_face_idx = int(line_list[2*face+1])
				if element == 1:
					if BOX_face_idx == 1:
						HEX_face_idx = 1
					elif BOX_face_idx == 3:
						HEX_face_idx = 5
					elif BOX_face_idx == 4:
						HEX_face_idx = 6
					else:
						sys.stderr.write("Error!")
						sys.exit(1)
				else:
					HEX_face_idx = HEX_faces[element-1][BOX_face_idx-1]

				output_file.write("%10d%10d"%(1,HEX_face_idx))
			output_file.write("%s"%os.linesep)


