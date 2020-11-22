# generate the test input and output list according to interpolation level
# python gen_test_v2.py [target directory] [checkpoints name] [interpolation level] [end frame]
import os
from os.path import isdir, join
import glob
import shutil
import sys
#import time

testing_dir = sys.argv[1]
cp_name = sys.argv[2]
level = int(sys.argv[3])
files = os.listdir(testing_dir)
index_len = 3
file_extension_len = 4

#date = time.strftime("%y%m%d", time.localtime())
output_dir = testing_dir + '_Output_' + str(level) + '_cp_' + cp_name
os.mkdir(output_dir)

first_level = True
end_frame = int(sys.argv[4])

for l in range(1, level + 1):
# start level loop
	print('level ' + str(l))
	f1 = open(join(output_dir, 'first_%d.txt' % (l)), 'w')
	f2 = open(join(output_dir, 'second_%d.txt' % (l)), 'w')
	f3 = open(join(output_dir, 'out_%d.txt' % (l)), 'w')

	gap = 2 ** (level - l)
	print("gap = %d" % (gap))
	if end_frame % (gap * 2) == 0:
		final_input_frame = end_frame - gap * 2 + 1
	else:
		final_input_frame = end_frame - (end_frame % (gap * 2)) + 1
	end_frame = final_input_frame
	print("final_input_frame = %d" % (final_input_frame))
	print("end_frame = %d" % (end_frame))
	for file in files:
	# start class loop
		if isdir(join(testing_dir, file)):
			if first_level:
				os.mkdir(join(output_dir, file))
			cnt = 0
			for path in sorted(glob.glob(join(testing_dir, file, '*.png'))):
			# start frame loop
				print(path)
				file_name = os.path.basename(path)

				cnt += 1
				if cnt > final_input_frame:
					# unchanged frames
						if first_level:
							shutil.copyfile(path, join(output_dir, file, file_name))
				elif cnt % gap == 1 or l == level:
					if cnt % (gap*2) == 1:
					# input frames
						if first_level:
							shutil.copyfile(path, join(output_dir, file, file_name))
						if cnt != final_input_frame:
							f1.write(join(output_dir, file, file_name) + '\n')
						if cnt != 1:
							f2.write(join(output_dir, file, file_name) + '\n')
					else:
					# output frames
						idx = str(cnt - 1)
						padding = index_len - len(idx)
						f3.write(join(output_dir, file, file_name[:-index_len-file_extension_len] + '0'*padding + idx + '.png') + '\n')
			# end frame loop
	# end class loop
	f1.close()
	f2.close()
	f3.close()

	first_level = False
#end level loop