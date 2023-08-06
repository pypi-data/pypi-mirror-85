import tensorflow as tf
import numpy as np
import os

def get_all_files(file_path, total_classes, is_random=True):
    image_list = []
    label_list = []
    no_of_images = 0

    for class_label in range(total_classes):
        class_path = file_path + '/' + str(class_label)
        for item in os.listdir(class_path):
            item_path = class_path + '/' + item

            if os.path.isfile(item_path):
                image_list.append(item_path)
                no_of_images = no_of_images + 1

            else:
                raise ValueError('The path to the test image file is incorrect')

            label_list.append(class_label)

    image_list = np.asarray(image_list)
    label_list = np.asarray(label_list)

    if is_random:
        rnd_index = np.arange(len(image_list))
        np.random.shuffle(rnd_index)
        image_list = image_list[rnd_index]
        label_list = label_list[rnd_index]
        train_list = [image_list, label_list]

    return train_list, no_of_images

def get_batch(train_list, image_height, image_width, batch_size, no_of_images, is_random=True):
    tf.compat.v1.disable_eager_execution()
    print("Reading image files from the directory..")
    # input queue contains the queued data produced by slice_input_producer
    intput_queue = tf.compat.v1.train.slice_input_producer(train_list, shuffle=False)

    image_train = tf.io.read_file(intput_queue[0])
    image_train = tf.io.decode_jpeg(image_train, channels=3)
    image_train = tf.image.resize(image_train, [image_height, image_width])
    image_train = tf.cast(image_train, tf.float32) / 255.
    label_train = intput_queue[1]
    print("Reading image files completed.")
    # shuffle the batch if required
    if is_random:
        image_train_batch, label_train_batch = tf.compat.v1.train.shuffle_batch([image_train, label_train],
                                                                                batch_size=batch_size,
                                                                                capacity=100,
                                                                                min_after_dequeue=4,
                                                                                num_threads=2)
    else:
        image_train_batch, label_train_batch = tf.compat.v1.train.batch([image_train, label_train],
                                                                        batch_size=1,
                                                                        capacity=no_of_images,
                                                                        num_threads=1)
    return image_train_batch, label_train_batch


if __name__ == '__main__':

    image_dir = 'data\\test'
    train_list = get_all_files(image_dir, True)
    image_train_batch, label_train_batch = get_batch(train_list, 256, 1, 200, False)
