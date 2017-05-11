from model_helper import load_feature_sets
import numpy as np
import os
from process_data import create_feature_vector
import sys
import tensorflow as tf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def test(model):
	with tf.Session() as sess:
		test_x, test_y = load_feature_sets(False)
		saver = tf.train.import_meta_graph(model + ".meta")
		saver.restore(sess, model)
		pred = tf.get_collection('vars')[0]
		x = tf.get_collection('vars')[1]
		y = tf.get_collection('vars')[2]
		correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
		accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
		res = accuracy.eval({x: test_x, y: test_y})
		print("Accuracy: ", res, sep='')

def use(model, input_data):
	with tf.Session() as sess:
		saver = tf.train.import_meta_graph(model + ".meta")
		saver.restore(sess, model)
		pred = tf.get_collection('vars')[0]
		x = tf.get_collection('vars')[1]
		#y = tf.get_collection('vars')[2]
		features = np.array(create_feature_vector(input_data))
		# Minor bug: [1,0], argmax: 0
                # Major bug: [0,1], argmax: 1
		result = (sess.run(tf.argmax(pred.eval(feed_dict={x: [features]}), 1)))
		if result[0] == 0:
			print('Minor bug:', input_data)
		elif result[0] == 1:
			print('Major bug:', input_data)

#test(sys.argv[1])
use(sys.argv[1], sys.argv[2])
