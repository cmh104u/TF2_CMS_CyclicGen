#python tiff2png.py [target directory]
import os
from os.path import isdir, join
import glob
from PIL import Image
import sys

target_dir = sys.argv[1]

destination_dir = sys.argv[1] + '_png'

os.mkdir(destination_dir)

files = os.listdir(target_dir)

print('Begin!')
for file in files:
	if isdir(join(target_dir, file)):
		print(file)
		os.mkdir(join(destination_dir, file))
		for path in glob.glob(join(target_dir, file, 'projection', '*.tiff')):
			im = Image.open(path)
			#print(path)
			#print(destination_dir)
			#print(file)
			#print(path.split('\\')[-1][:-5] + '.png')
			im.save(join(destination_dir, file, path.split('/')[-1][:-5] + '.png'))	#in server path is splited by /
