#python [target directory] [name]
import glob
from os.path import join
import imageio as io
import sys

target_dir = sys.argv[1]
name = sys.argv[2]

images = []
for filename in sorted(glob.glob(join(target_dir, '*.*'))):
    images.append(io.imread(filename))
io.mimsave(join(target_dir, name + '.gif'), images, duration = 0.1)