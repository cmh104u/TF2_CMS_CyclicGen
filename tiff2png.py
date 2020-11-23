#python tiff2png.py [target directory] [split token]
import os
from os.path import isdir, join
import glob
from PIL import Image
import sys

target_dir = sys.argv[1]
split_token = sys.argv[2]

idx_len = 5

IsPadding = False
if split_token != None:
	IsPadding = True

destination_dir = sys.argv[1] + '_png'

os.mkdir(destination_dir)

files = os.listdir(target_dir)

print('Begin!')
for file in files:
	if isdir(join(target_dir, file)):
		print(file)
		os.mkdir(join(destination_dir, file))
		for path in glob.glob(join(target_dir, file, '*.tiff')):
			name, _ = os.path.splitext(os.path.basename(path))
			name_split = name.split(split_token)
			name = split_token.join(name_split[:-1])
			print(name)
			idx = name_split[-1]
			print(idx)
			padding_cnt = idx_len - len(idx)
			im = Image.open(path)
			im.save(join(destination_dir, file, name + '_' + (padding_cnt * '0') + idx + '.png'))	#in server path is splited by /
