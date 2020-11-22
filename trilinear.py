# implement trilinear interpolation
# python trilinear.py [target directory] [interpolation level]
import numpy as np
from PIL import Image
import torch
import os
from os.path import isdir, join
import glob
import sys
import cv2

def trilinear(input_volume, padding_frame):
	x = torch.from_numpy(input_volume).float()
	x = torch.unsqueeze(x, 0).unsqueeze(0)
	print(x.shape)
	x = torch.nn.functional.interpolate(x, size=(padding_frame, 256, 256), mode='trilinear', align_corners=True)
	x = torch.squeeze(x)
	output_volume = x.numpy()

	return output_volume

target_dir = sys.argv[1]
level = int(sys.argv[2])
gap = 2 ** level
padding_frame_cnt = (179 // gap) * gap + 1

files = os.listdir(target_dir)

output_dir = 'output'
os.mkdir(join(target_dir, output_dir))

for file in files:
# start class loop
	if isdir(join(target_dir, file)):
		os.mkdir(join(target_dir, output_dir, file))

		image_list = []
		for path in sorted(glob.glob(join(target_dir, file, '*.png'))):
		# start frame loop
			image = Image.open(path)
			image_list.append(np.array(image))
		# end frame loop
		image_list = np.array(image_list)

		output_list =  trilinear(image_list, padding_frame_cnt)

		for i in range(output_list.shape[0]):
			zero_padding = 5 - len(str(i))
			output_image = np.round(output_list[i]).astype(np.uint8)
			cv2.imwrite(join(target_dir, output_dir, file, file + '_' + zero_padding * '0' + str(i) + '.png'), output_image)
# end class loop