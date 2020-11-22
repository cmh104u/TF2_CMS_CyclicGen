# generate .txt file for training input
# python gen.py [target directory] [output directory] [frame gap]
import os
from os.path import isdir, join
import glob
import sys

def rename_data(path, key):
	for data_path in glob.glob(join(path, '*.tiff')):
		cut_pos = len(join(path, key))
		idx = data_path[cut_pos:].split('.')[0]

		# pad index to length 5
		padding_zero_cnt = 5 - len(idx)
		if padding_zero_cnt < 0:
			print('Error in rename_data()')
		else:
			padding_zero = '0' * padding_zero_cnt
			idx = '_' + padding_zero + idx

		os.rename(data_path, join(path, key + idx + '.tiff'))

target_dir = sys.argv[1]
output_dir = sys.argv[2]
gap = int(sys.argv[3])

if not isdir(output_dir):
	os.mkdir(output_dir)

f1 = open(join(output_dir, 'frame1.txt'), 'w')
f2 = open(join(output_dir, 'frame2.txt'), 'w')
f3 = open(join(output_dir, 'frame3.txt'), 'w')

training_data_path = join(os.getcwd(), target_dir)

files = os.listdir(training_data_path)

print('Begin!')

# for else class in training data
for file in files:
	if isdir(join(training_data_path, file)):
		# rename data e.g. 5HT1A-F-90001110 to 5HT1A-F-900011_00010
		#rename_data(join(training_data_path, file, 'projection'), file)

		#write .txt file
		file_cnt = 179 // gap + 1
		#file_cnt = len(os.listdir(join(training_data_path, file, 'projection')))
		cnt = 0
		idx = 0
		for path in sorted(glob.glob(join(training_data_path, file, '*.png'))):
			idx += 1
			if idx % gap != 1:
				continue
			cnt += 1

			# write path of 1st ~ (file_cnt -2)th frames
			if cnt != file_cnt and cnt != file_cnt - 1:
				f1.write(path + '\n')

			# write path of 2nd ~ (file_cnt -1)th frames
			if cnt != 1 and cnt != file_cnt:
				f2.write(path + '\n')

			# write path of 3nd ~ (file_cnt)th frames
			if cnt != 1 and cnt != 2:
				f3.write(path + '\n')
		print('class %s is completed' % (file))


f1.close()
f2.close()
f3.close()
