import tensorflow as tf
import os
import numpy as np
import sys


# class TFRecordExtractor:
#     def __init__(self, tfrecord_file, new_image_shape, batch_size):
#         self.tfrecord_file = tfrecord_file #os.path.abspath(tfrecord_file)
#         self.input_height = new_image_shape[0]
#         self.input_width = new_image_shape[1]
#         self.input_channels = new_image_shape[2]
#         self.batch_size = batch_size
#
#     def extract_image(self, total_data_points):
#         tf.compat.v1.disable_eager_execution()
#         filenameQ = tf.compat.v1.train.string_input_producer(self.tfrecord_file, num_epochs=None)
#         recordReader = tf.compat.v1.TFRecordReader()
#         key, fullExample = recordReader.read(filenameQ)
#         features = tf.io.parse_single_example(
#             fullExample,
#             features={
#                 'image/height': tf.io.FixedLenFeature([], tf.int64),
#                 'image/width': tf.io.FixedLenFeature([], tf.int64),
#                 # 'image/colorspace': tf.io.FixedLenFeature([], dtype=tf.string, default_value=''),
#                 'image/channels': tf.io.FixedLenFeature([], tf.int64),
#                 'image/class/label': tf.io.FixedLenFeature([], tf.int64),
#                 # 'image/class/text': tf.io.FixedLenFeature([], dtype=tf.string, default_value=''),
#                 # 'image/format': tf.io.FixedLenFeature([], dtype=tf.string, default_value=''),
#                 'image/filename': tf.io.FixedLenFeature([], dtype=tf.string, default_value=''),
#                 'image/encoded': tf.io.FixedLenFeature([], dtype=tf.string, default_value='')
#             })
#         # parsed_batch = dict(zip(features.keys(),
#         #                         tf.compat.v1.train.batch(features.values(), batch_size=self.batch_size)))
#
#         label = features['image/class/label']
#         image_buffer = features['image/encoded']
#
#         with tf.name_scope('decode_jpeg'):
#             image = tf.image.decode_jpeg(image_buffer, channels=self.input_channels)
#             image = tf.image.convert_image_dtype(image, dtype=tf.uint8)
#
#         image = tf.image.resize(image, [self.input_height, self.input_width])
#         image = tf.cast(image, tf.float32) / 255.
#         label = tf.stack(tf.one_hot(label - 1, 2))
#         img_shape = tf.stack([features['image/height'], features['image/width'], features['image/channels']])
#         filename = features['image/filename']
#         # imageBatch, labelBatch = tf.compat.v1.train.shuffle_batch([image, label],
#         #                                                           batch_size=8,
#         #                                                           capacity=50,
#         #                                                           min_after_dequeue=10,
#         #                                                            enqueue_many=True)
#
#         return image, label, img_shape, filename
#
#     # def _extract_fn(self, tfrecord):
#     #     # Extract features using the keys set during creation
#     #     features = {
#     #         'image/height': tf.io.FixedLenFeature([], tf.int64),
#     #         'image/width': tf.io.FixedLenFeature([], tf.int64),
#     #         #'image/colorspace': tf.io.FixedLenFeature([], dtype=tf.string, default_value=''),
#     #         'image/channels': tf.io.FixedLenFeature([], tf.int64),
#     #         'image/class/label': tf.io.FixedLenFeature([], tf.int64),
#     #         #'image/class/text': tf.io.FixedLenFeature([], dtype=tf.string, default_value=''),
#     #         #'image/format': tf.io.FixedLenFeature([], dtype=tf.string, default_value=''),
#     #         'image/filename': tf.io.FixedLenFeature([], dtype=tf.string, default_value=''),
#     #         'image/encoded': tf.io.FixedLenFeature([], dtype=tf.string, default_value='')
#     #     }
#     #
#     #     # Extract the data record
#     #     sample = tf.io.parse_single_example(tfrecord, features)
#     #
#     #     image = tf.io.decode_image(sample['image/encoded'])
#     #     img_shape = tf.stack([sample['image/height'], sample['image/width'], sample['image/channels']])
#     #     label = sample['image/class/label']
#     #     filename = sample['image/filename']
#     #
#     #     return image, label, filename, img_shape
#     #
#     #
#     # def extract_image(self, total_data_points):
#     #
#     #     # Pipeline of dataset and iterator
#     #     with tf.compat.v1.Session() as sess:
#     #         dataset = tf.data.TFRecordDataset([self.tfrecord_file])
#     #         dataset = dataset.map(self._extract_fn)
#     #         iterator = tf.compat.v1.data.make_one_shot_iterator(dataset)
#     #         next_image_data = iterator.get_next()
#     #         list_image_data = []
#     #         list_labels = []
#     #         list_filename = []
#     #         list_image_shape = []
#     #
#     #
#     #         for n in range(total_data_points):
#     #             # Keep extracting data till TFRecord is exhausted
#     #             image_data, labels, filename, img_shape = sess.run(next_image_data)
#     #             #image_data_tensor = tf.convert_to_tensor(image_data[0], dtype=tf.uint8)
#     #             #data_tensor = tf.concat([data_tensor, image_data_tensor], 2)
#     #             list_image_data.append(image_data)
#     #             list_labels.append(labels)
#     #             list_filename.append(filename)
#     #             list_image_shape.append(img_shape)
#     #
#     #         return list_image_data, list_labels, list_filename, list_image_shape


