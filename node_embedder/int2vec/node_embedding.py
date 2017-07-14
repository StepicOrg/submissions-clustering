import os
import numpy as np
import tensorflow as tf
from ..utils.preprocessing import pad_sequences, split_into_batches

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


# TODO: 1) data download scripts + data processing scripts
# TODO: 3) deal with how we gonna train and retrain our emb model, with changing num_codes / max_children_num
# TODO: 6) max children num?

# goo.gl/aefJaE

class ParentChildrenEmbedding:
    def __init__(self, N_f=32, delta=1, lr=1e-3, momentum=0.9, alpha=0,
                 batch_size=128, epochs=1, codes_num=0, max_children_num=15,
                 variables_dump=None):
        self.N_f = N_f
        self.delta = delta
        self.lr = lr
        self.momentum = momentum
        self.alpha = alpha
        self.batch_size = batch_size
        self.epochs = epochs
        self.codes_num = codes_num
        self.max_children_num = max_children_num
        self.variables_dump = variables_dump

    def generate_input(self, next_batch):
        batch_parent = next_batch["parent"].as_matrix()
        batch_children = pad_sequences(next_batch["children"].as_matrix(),
                                       maxlen=self.max_children_num, padding="post")

        batch_children_num = next_batch["children"].map(len).as_matrix()
        batch_children_leaves_nums = pad_sequences(next_batch["children_leaves_nums"].as_matrix(),
                                                   maxlen=self.max_children_num, padding="post")

        batch_parent_c = batch_parent.copy()
        batch_children_c = batch_children.copy()
        for i in range(len(next_batch)):
            k = np.random.randint(batch_children_num[i] + 1)
            new_code = np.random.randint(1, self.codes_num + 1)
            if k:
                batch_children_c[i, k - 1] = new_code
            else:
                batch_parent_c[i] = new_code

        batch_leaves_coef = batch_children_leaves_nums / np.sum(batch_children_leaves_nums, axis=1)[:, np.newaxis]

        batch_left_coef, batch_right_coef = [], []
        for i in range(len(next_batch)):
            n = batch_children_num[i]
            if n == 1:
                batch_left_coef.append([0.5])
                batch_right_coef.append([0.5])
            else:
                batch_left_coef.append((np.arange(n - 1, -1, -1) / (n - 1)).tolist())
                batch_right_coef.append((np.arange(n) / (n - 1)).tolist())
        batch_left_coef = pad_sequences(batch_left_coef, maxlen=self.max_children_num, padding="post")
        batch_right_coef = pad_sequences(batch_right_coef, maxlen=self.max_children_num, padding="post")

        return batch_parent, batch_children, \
               batch_children_leaves_nums, \
               batch_parent_c, batch_children_c, \
               batch_leaves_coef, batch_left_coef, batch_right_coef

    def fit(self, X):
        self.codes_num = X["children"].map(max).max()
        self.max_children_num = min(self.max_children_num, X["children"].map(len).max())
        X = X[X["children"].map(len) <= self.max_children_num]

        parent = tf.placeholder(tf.float32, [None])
        children = tf.placeholder(tf.float32, [None, self.max_children_num])
        children_leaves_nums = tf.placeholder(tf.float32, [None, self.max_children_num])
        parent_c = tf.placeholder(tf.float32, [None])
        children_c = tf.placeholder(tf.float32, [None, self.max_children_num])
        leaves_coef = tf.placeholder(tf.float32, [None, self.max_children_num])
        left_coef = tf.placeholder(tf.float32, [None, self.max_children_num])
        right_coef = tf.placeholder(tf.float32, [None, self.max_children_num])

        placeholders = parent, children, children_leaves_nums, \
                       parent_c, children_c, leaves_coef, left_coef, right_coef

        theta = {
            "W_l": tf.Variable(tf.random_normal([self.N_f, self.N_f])),
            "W_r": tf.Variable(tf.random_normal([self.N_f, self.N_f])),
            "b": tf.Variable(tf.random_normal([self.N_f])),
            "vec": tf.Variable(tf.random_normal([self.codes_num + 1, self.N_f]))
        }

        batch_size = tf.shape(parent)[0]
        W = tf.reshape(left_coef, [batch_size, self.max_children_num, 1, 1]) \
            * tf.tile(tf.reshape(theta["W_l"], [1, 1, self.N_f, self.N_f]), [batch_size, self.max_children_num, 1, 1])
        W += tf.reshape(right_coef, [batch_size, self.max_children_num, 1, 1]) \
             * tf.tile(tf.reshape(theta["W_r"], [1, 1, self.N_f, self.N_f]), [batch_size, self.max_children_num, 1, 1])
        W += tf.reshape(leaves_coef, [batch_size, self.max_children_num, 1, 1]) * W

        def make_dist_tensor(p, cs):
            dist = W @ tf.expand_dims(tf.gather(theta["vec"], tf.cast(cs, tf.int32)), -1)
            dist = tf.tanh(tf.squeeze(tf.reduce_sum(dist, axis=1)) + tf.expand_dims(theta["b"], 0))
            dist = tf.norm(tf.gather(theta["vec"], tf.cast(p, tf.int32)) - dist, axis=1) ** 2
            return dist

        d = make_dist_tensor(parent, children)
        d_c = make_dist_tensor(parent_c, children_c)
        y = tf.nn.relu(self.delta + d - d_c)

        l2_c = (self.alpha / (2 * (self.N_f ** 2)))
        l2 = l2_c * (tf.norm(theta["W_l"], ord="fro", axis=[0, 1]) ** 2
                     + tf.norm(theta["W_r"], ord="fro", axis=[0, 1]) ** 2)
        cost = 0.5 * tf.reduce_mean(y) + l2

        # optimizer = tf.train.AdamOptimizer(learning_rate=self.lr).minimize(cost)
        optimizer = tf.train.MomentumOptimizer(learning_rate=self.lr, momentum=self.momentum).minimize(cost)
        # optimizer = tf.train.AdadeltaOptimizer().minimize(cost)

        saver = tf.train.Saver()
        with tf.Session() as sess:
            if self.variables_dump and os.path.exists(self.variables_dump + ".index"):
                print("Restoring variables from \"{}\".".format(self.variables_dump))
                saver.restore(sess, self.variables_dump)
            else:
                print("Initialize variables.")
                sess.run(tf.global_variables_initializer())

            N = 10000

            print("Optimization begin.")
            for epoch in range(self.epochs):
                avg_cost = 0
                total_batch = N // self.batch_size
                for batch in split_into_batches(X, self.batch_size, max_elem=N):
                    feed_dict = {a: b for a, b in zip(placeholders, self.generate_input(batch))}
                    _, c = sess.run([optimizer, cost], feed_dict=feed_dict)
                    avg_cost += c / total_batch
                print("epoch= {} cost= {}".format(epoch, avg_cost))
                # saver.save(sess, self.variables_dump)
            print("Optimization finished.")

            """
            if self.variables_dump:
                print("Dump variables to \"{}\".".format(self.variables_dump))
                saver.save(sess, self.variables_dump)
            """

            return theta["vec"].eval()
