"""Train a voxel flow model on ucf101 dataset."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import os
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
from datetime import datetime
from model_origin_bicubic import Voxel_flow_model
import scipy as sp
import cv2
from vgg16_update import Vgg16
from os.path import join, isdir, splitext

config = tf.ConfigProto()
config.gpu_options.allow_growth = True

FLAGS = tf.app.flags.FLAGS

# Define necessary FLAGS
tf.app.flags.DEFINE_string('pretrained_model_checkpoint_path', None,
                           """If specified, restore this pretrained model """
                           """before beginning any training.""")
tf.app.flags.DEFINE_integer('batch_size', 1, 'The number of samples in each batch.')
tf.app.flags.DEFINE_string('first', '',
                           """first image """)
tf.app.flags.DEFINE_string('second', '',
                           """second image """)
tf.app.flags.DEFINE_string('out', '',
                           """output image """)

output_dir = 'Dataset_pix2pix'
if not isdir(output_dir):
    os.mkdir(output_dir)


def imread(filename):
    """Read image from file.
    Args:
    filename: .
    Returns:
    im_array: .
    """
    im = sp.misc.imread(filename, mode='L')
    im = im.reshape(im.shape + (1,))
    return im / 255 - 0.5


def test(first, second, third):

    data_frame1 = np.expand_dims(imread(first), 0)
    data_frame3 = np.expand_dims(imread(third), 0)

    H = data_frame1.shape[1]
    W = data_frame1.shape[2]

    adatptive_H = int(np.ceil(H / 32.0) * 32.0)
    adatptive_W = int(np.ceil(W / 32.0) * 32.0)

    pad_up = int(np.ceil((adatptive_H - H) / 2.0))
    pad_bot = int(np.floor((adatptive_H - H) / 2.0))
    pad_left = int(np.ceil((adatptive_W - W) / 2.0))
    pad_right = int(np.floor((adatptive_W - W) / 2.0))

    print(str(H) + ', ' + str(W))
    print(str(adatptive_H) + ', ' + str(adatptive_W))

    """Perform test on a trained model."""
    with tf.Graph().as_default():
        # Create input and target placeholder.
        input_placeholder = tf.placeholder(tf.float32, shape=(None, H, W, 2))

        input_pad = tf.pad(input_placeholder, [[0, 0], [pad_up, pad_bot], [pad_left, pad_right], [0, 0]], 'SYMMETRIC')

        edge_vgg_1 = Vgg16(input_pad[:, :, :, :1], reuse=None)
        edge_vgg_3 = Vgg16(input_pad[:, :, :, 1:2], reuse=True)

        edge_1 = tf.nn.sigmoid(edge_vgg_1.fuse)
        edge_3 = tf.nn.sigmoid(edge_vgg_3.fuse)

        edge_1 = tf.reshape(edge_1, [-1, input_pad.get_shape().as_list()[1], input_pad.get_shape().as_list()[2], 1])
        edge_3 = tf.reshape(edge_3, [-1, input_pad.get_shape().as_list()[1], input_pad.get_shape().as_list()[2], 1])

        with tf.variable_scope("Cycle_DVF"):
            # Prepare model.
            model = Voxel_flow_model(is_train=False)
            prediction = model.inference(tf.concat([input_pad, edge_1, edge_3], 3))[0]

        # Create a saver and load.
        sess = tf.Session()

        # Restore checkpoint from file.
        if FLAGS.pretrained_model_checkpoint_path:
            restorer = tf.train.Saver()
            restorer.restore(sess, FLAGS.pretrained_model_checkpoint_path)
            print('%s: Pre-trained model restored from %s' %
                  (datetime.now(), FLAGS.pretrained_model_checkpoint_path))

        feed_dict = {input_placeholder: np.concatenate((data_frame1, data_frame3), 3)}
        # Run single step update.
        prediction_np = sess.run(prediction, feed_dict=feed_dict)

        output = prediction_np[-1, pad_up:adatptive_H - pad_bot, pad_left:adatptive_W - pad_right, :]
        output = np.round(((output +0.5) * 255.0 )).astype(np.uint8)
        #output = np.dstack((output[:, :, 2], output[:, :, 1], output[:, :, 0]))

        # Output combine image
        first_im = sp.misc.imread(first, mode='L')
        first_im = first_im.reshape(first_im.shape + (1,))

        third_im = sp.misc.imread(third, mode='L')
        third_im = third_im.reshape(third_im.shape + (1,))

        second_im = sp.misc.imread(second, mode='L')
        second_im = second_im.reshape(second_im.shape + (1,))

        combine = np.concatenate([first_im, output, third_im, second_im], axis=1)

        class_name = second.split('/')[-2]
        file_name = second.split('/')[-1]
        print(class_name, file_name)
        output_path = os.path.join(output_dir, class_name)
        if not isdir(output_path):
            os.mkdir(output_path)

        output_path = os.path.join(output_path, file_name)
        cv2.imwrite(output_path, combine)

if __name__ == '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    df1 = open('Training_Data_List/frame1.txt','r')
    df2 = open('Training_Data_List/frame2.txt','r')
    df3 = open('Training_Data_List/frame3.txt','r')
    cnt = 0
    for i,j,k in zip(df1,df2,df3):
        print(cnt,'th image')
        #if cnt < 4000:
            #exit()
        cnt += 1
        first = i[0:-1]
        second = j[0:-1]
        third = k[0:-1]
        
        test(first, second, third)
        