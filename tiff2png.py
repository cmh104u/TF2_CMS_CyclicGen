#python tiff2png.py [target directory]
import os
from os.path import isdir, join
import glob
import sys
import cv2

target_dir = sys.argv[1]

destination_dir = sys.argv[1] + '_png'

os.mkdir(destination_dir)

files = os.listdir(target_dir)

for file in files:
	if isdir(join(target_dir, file)):
		print(file)
		os.mkdir(join(destination_dir, file))
		for path in glob.glob(join(target_dir, file, '*.tiff')):
			name, _ = os.path.splitext(os.path.basename(path))
			img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
			cv2.imwrite(join(destination_dir, file, name + '.png'), img)