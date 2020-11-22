import os
from os.path import isdir, join
import glob
import shutil

output_dir = 'output'
testing_dir = 'Fly_Testing_Data'

os.mkdir(output_dir)
files = os.listdir(testing_dir)

f1 = open('first.txt', 'w')
f2 = open('second.txt', 'w')
f3 = open('out.txt', 'w')

for file in files:
	if isdir(join(testing_dir, file)):
		print(file)
		os.mkdir(join(output_dir, file))
		cnt = 0
		for path in sorted(glob.glob(join(testing_dir, file, 'projection', '*.png'))):
			file_name = path.split('/')[-1]
			print(file_name)
			cnt += 1
			if cnt % 2 == 1:
				shutil.copyfile(path, join(output_dir, file, file_name))
				if cnt != 179:
					f1.write(join(output_dir, file, file_name) + '\n')
				if cnt != 1:
					f2.write(join(output_dir, file, file_name) + '\n')
			elif cnt == 180:
				shutil.copyfile(path, join(output_dir, file, file_name))
			else:
				idx = str(cnt - 1)
				padding = 5 - len(idx)
				f3.write(join(output_dir, file, file_name[:-9] + '0'*padding + idx + '.png') + '\n')

f1.close()
f2.close()
f3.close()