#!/usr/bin/env python
from tempfile import mkstemp
from shutil import move
import os
def setUniformComposition(file_name, region_name, composition):
	'''
	set region_name in file_name to composition at REGION_ALIAS segment.
	'''
	fh, temp_abs_path = mkstemp()
	with open(temp_abs_path, 'w') as new_file:
		with open(file_name) as old_file:
			for line in old_file:
				if 'REGION_ALIAS' in line and region_name in line:
					line_list = line.split()
					line_list[-1] = composition
					new_file.write("REGION_ALIAS    ")
					new_file.write(region_name+"    ")
					new_file.write(composition)
					new_file.write(os.linesep)
				else:
					new_file.write(line)

	os.close(fh)
	os.remove(file_name)
	os.rename(temp_abs_path, file_name)

def main():
	file_name = [name for name in os.listdir('./') if name.startswith('step')]
	#print file_name
	file_path = [os.getcwd()+'/'+name for name in file_name]
	#print file_path

	for file in file_path:
		setUniformComposition(file, 'REGION1', 'COMP_1')

if __name__ == '__main__':
	main()
