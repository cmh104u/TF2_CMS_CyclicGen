'''
compute PSNR with tensorflow
'''
import tensorflow as tf
 
 
 
def read_img(path):
	return tf.image.decode_image(tf.read_file(path))
 
def psnr(tf_img1, tf_img2):
	return tf.image.psnr(tf_img1, tf_img2, max_val=255)
 
def _main():
	t1 = read_img('t1.jpg')
	t2 = read_img('t2.jpg')
	with tf.Session() as sess:
		sess.run(tf.global_variables_initializer())
		y = sess.run(psnr(t1, t2))
		print(y)
 
 
if __name__ == '__main__':
    _main()