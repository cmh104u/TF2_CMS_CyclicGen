# generate the test input according to interpolation level
# python downsampling.py [target directory] [output directory] [interpolation level]
import os
from os.path import isdir, join
import glob
import shutil
import sys

testing_dir = sys.argv[1]
output_dir = sys.argv[2]
level = int(sys.argv[3])

if not isdir(output_dir):
	os.mkdir(output_dir)
files = os.listdir(testing_dir)

gap = 2 ** level

for file in files:
# start class loop
	if isdir(join(testing_dir, file)):
		os.mkdir(join(output_dir, file))
		cnt = 0
		for path in sorted(glob.glob(join(testing_dir, file, '*.png'))):
		# start frame loop
			cnt += 1
			file_name = path.split('/')[-1]

			if cnt % gap == 1:
				shutil.copyfile(path, join(output_dir, file, file_name))
		# end frame loop
# end class loop
