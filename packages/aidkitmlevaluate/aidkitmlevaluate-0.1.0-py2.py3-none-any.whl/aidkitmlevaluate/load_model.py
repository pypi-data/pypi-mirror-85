import tensorflow as tf



class Model(object):
    def __init__(self, model_filepath, input_data, labels, input_node, output_nodes, total_test_data_points, new_image_shape,
                 batch_size, sess):

        # init all parameteres
        self.model_filepath = model_filepath
        self.input_height = new_image_shape[0]
        self.input_width = new_image_shape[1]
        self.input_channels = new_image_shape[2]
        self.input_shape = new_image_shape
        self.input_data = input_data
        self.labels = labels
        self.input_node = input_node
        self.output_nodes = output_nodes
        self.total_data_points = total_test_data_points
        self.batch_size = batch_size
        self.sess = sess

    def infer(self):
        print('Loading model...')
        predicted_out = []
        labels = []

        with tf.io.gfile.GFile(self.model_filepath, 'rb') as f:
            graph_def = tf.compat.v1.GraphDef()
            graph_def.ParseFromString(f.read())
            self.sess.graph.as_default()

            # Create a placeholder for the input data and map it to the input node in the graph
            input_train = tf.compat.v1.placeholder(tf.float32,
                                         [self.batch_size, self.input_width, self.input_height, self.input_channels],
                                         name="input_train")
            tf.import_graph_def(graph_def, input_map={self.input_node : input_train})

            # Get layer names
            names = [op.name for op in self.sess.graph.get_operations()]
            if len(names) == 0:
                raise ValueError('loading model failed.')
            print("Model loaded.")

            self.sess.run([tf.compat.v1.global_variables_initializer(), tf.compat.v1.local_variables_initializer()])
            coord = tf.train.Coordinator()
            threads = tf.compat.v1.train.start_queue_runners(sess=self.sess, coord=coord)
            input_tensor = self.sess.graph.get_tensor_by_name(self.input_node + ":0")
            output_tensor = [self.sess.graph.get_tensor_by_name(name + ":0") for name in self.output_nodes]
            print("Initializing inference..")

            while True:
                try:
                    data_arr, labels_arr = self.sess.run([self.input_data, self.labels])
                    predicted_out.append(self.sess.run(output_tensor, feed_dict={input_train: data_arr}))
                    labels.append(labels_arr)

                except tf.errors.OutOfRangeError:
                    print('Inference completed')
                    break
                finally:
                    coord.request_stop()

            coord.join(threads=threads)
            self.sess.close()
            return predicted_out, labels






