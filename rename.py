# python rename.py [target_dir]
# rename data e.g. 5HT1A-F-90001110 to 5HT1A-F-900011_00010
import os
from os.path import isdir, join
import sys
import glob

def rename_data(path, key):
	for data_path in glob.glob(join(path, '*.*')):
		cut_pos = len(join(path, key))
		idx = data_path[cut_pos:].split('.')[0]
		file_extension = data_path[cut_pos:].split('.')[1]

		# pad index to length 5
		padding_zero_cnt = 5 - len(idx)
		if padding_zero_cnt < 0:
			print('Error in rename_data()')
		else:
			padding_zero = '0' * padding_zero_cnt
			idx = '_' + padding_zero + idx

		os.rename(data_path, join(path, key + idx + '.' + file_extension))

target_dir = sys.argv[1]

if not isdir(target_dir):
	print(target_dir, 'is not directory')
	sys.exit(-1)

files = os.listdir(target_dir)
for file in files:
	if isdir(join(target_dir, file)):
		print('Rename file: ' + file)
		rename_data(join(target_dir, file, 'projection'), file)
