# python rename.py [target_dir] [padding length]
# rename data e.g. 5HT1A-F-900011_10 to 5HT1A-F-900011_00010
import os
from os.path import isdir, join
import sys
import glob

target_dir = sys.argv[1]
padding_len = int(sys.argv[2])

if not isdir(target_dir):
	print(target_dir, 'is not directory')
	sys.exit(-1)

for old_path in glob.glob(join(target_dir, '*' ,'*.*')):
	file_name, file_extension = os.path.splitext(os.path.basename(old_path))

	idx = file_name.split('_')[-1]
	padding_idx = idx.zfill(padding_len)

	class_name = '_'.join(file_name.split('_')[:-1])

	new_file_name = class_name + '_' + padding_idx + file_extension
	new_path = join(os.path.dirname(old_path), new_file_name)

	os.rename(old_path, new_path)
