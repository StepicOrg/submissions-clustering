import os
import numpy as np
import tensorflow as tf
from ..utils.preprocessing import pad_sequences

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


# TODO: 1) data download scripts + data processing scripts
# TODO: 2) rewrite py_func with separate placeholder (to be able to serialize meta graph)
# TODO: 3) deal with how we gonna train and retrain our emb model, with changing num_codes
# TODO: 4) batch learning
# TODO: 5) регуляризация

# https://goo.gl/QoqruK

class ParentChildrenEmbedding:
    def __init__(self):
        pass

    def fit(self, X, training_epochs=10):
        N_f = 32
        delta = 1
        learning_rate = 0.001
        batch_size = 128

        codes_num = X["children"].map(max).max()
        max_children_num = X["children"].map(len).max()

        parent = tf.placeholder(tf.float32, [None])
        children = tf.placeholder(tf.float32, [None, max_children_num])
        children_num = tf.placeholder(tf.float32, [None])
        children_leaves_nums = tf.placeholder(tf.float32, [None, max_children_num])
        parent_c = tf.placeholder(tf.float32, [None])
        children_c = tf.placeholder(tf.float32, [None, max_children_num])
        leaves_coef = tf.placeholder(tf.float32, [None, max_children_num])
        left_coef = tf.placeholder(tf.float32, [None, max_children_num])
        right_coef = tf.placeholder(tf.float32, [None, max_children_num])

        tetta = {
            "W_l": tf.Variable(tf.random_normal([N_f, N_f])),
            "W_r": tf.Variable(tf.random_normal([N_f, N_f])),
            "b": tf.Variable(tf.random_normal([N_f])),
            "vec": tf.Variable(tf.random_normal([codes_num + 1, N_f]))
        }

        k = tf.shape(parent)[0]
        W = tf.reshape(left_coef, [k, max_children_num, 1, 1]) \
            * tf.tile(tf.reshape(tetta["W_l"], [1, 1, N_f, N_f]), [k, max_children_num, 1, 1])
        W += tf.reshape(right_coef, [k, max_children_num, 1, 1]) \
             * tf.tile(tf.reshape(tetta["W_r"], [1, 1, N_f, N_f]), [k, max_children_num, 1, 1])
        W += tf.reshape(leaves_coef, [k, max_children_num, 1, 1]) * W

        def make_d_tensor(p, cs):
            d = W @ tf.expand_dims(tf.gather(tetta["vec"], tf.cast(cs, tf.int32)), -1)
            d = tf.tanh(tf.squeeze(tf.reduce_sum(d, axis=1)) + tf.expand_dims(tetta["b"], 0))
            d = tf.norm(tf.gather(tetta["vec"], tf.cast(p, tf.int32)) - d, axis=1)
            return d

        d = make_d_tensor(parent, children)
        d_c = make_d_tensor(parent_c, children_c)
        y = tf.nn.relu(delta + d - d_c)
        
        def generate_input(batch):
            batch_parent = batch["parent"].as_matrix()
            batch_children = pad_sequences(batch["children"].as_matrix(),
                                           maxlen=max_children_num, padding="post")

            batch_children_num = batch["children"].map(len).as_matrix()
            batch_children_leaves_nums = pad_sequences(batch["children_leaves_nums"].as_matrix(),
                                                       maxlen=max_children_num, padding="post")

            batch_parent_c = batch_parent.copy()
            batch_children_c = batch_children.copy()
            for i in range(len(batch)):
                k = np.random.randint(batch_children_num[i] + 1)
                new_code = np.random.randint(1, codes_num + 1)
                if k:
                    batch_children_c[i, k - 1] = new_code
                else:
                    batch_parent_c[i] = new_code

            batch_leaves_coef = batch_children_leaves_nums / np.sum(batch_children_leaves_nums, axis=1)[:, np.newaxis]

            batch_left_coef, batch_right_coef = [], []
            for i in range(len(batch)):
                n = batch_children_num[i]
                if n == 1:
                    batch_left_coef.append([0.5])
                    batch_right_coef.append([0.5])
                else:
                    batch_left_coef.append((np.arange(n - 1, -1, -1) / (n - 1)).tolist())
                    batch_right_coef.append((np.arange(n) / (n - 1)).tolist())
            batch_left_coef = pad_sequences(batch_left_coef, maxlen=max_children_num, padding="post")
            batch_right_coef = pad_sequences(batch_right_coef, maxlen=max_children_num, padding="post")

            return batch_parent, batch_children, \
                   batch_children_num, batch_children_leaves_nums, \
                   batch_parent_c, batch_children_c, \
                   batch_leaves_coef, batch_left_coef, batch_right_coef

        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())

            placeholders = parent, children, children_num, children_leaves_nums, \
                           parent_c, children_c, leaves_coef, left_coef, right_coef

            batch = X.sample(batch_size)

            feed_dict = {a: b for a, b in zip(placeholders, generate_input(batch))}

            print(sess.run(y, feed_dict=feed_dict))

        """
        self.num_codes = max(self.num_codes, X["children"].map(max).max() + 1)

        shape_type = tf.int32
        code_type = tf.int32
        feature_type = tf.float32

        p = tf.placeholder(dtype=code_type, shape=[1])
        cs = tf.placeholder(dtype=code_type, shape=[None])
        ls = tf.placeholder(dtype=shape_type, shape=[None])

        def negative_sample(sample_p, sample_cs):
            n = sample_cs.shape[0]
            k = np.random.randint(n + 1)
            if k:
                sample_cs = sample_cs.copy()
                sample_cs[k - 1] = np.random.randint(self.num_codes)
            else:
                sample_p = sample_p.copy()
                sample_p[0] = np.random.randint(self.num_codes)
            return sample_p, sample_cs

        p_c, cs_c = tf.py_func(negative_sample, [p, cs], [code_type, code_type])

        W_l = tf.Variable(tf.random_normal([self.N_f, self.N_f], dtype=feature_type), name="W_l")
        W_r = tf.Variable(tf.random_normal([self.N_f, self.N_f], dtype=feature_type), name="W_r")
        b = tf.Variable(tf.random_normal([self.N_f], dtype=feature_type), name="b")
        vec = tf.Variable(tf.random_normal([self.num_codes, self.N_f], dtype=feature_type), name="vec")

        n = tf.shape(cs, out_type=shape_type)[0]

        l_i = tf.divide(tf.cast(ls, dtype=feature_type), tf.cast(tf.reduce_sum(ls), dtype=feature_type))

        left_c = tf.cond(tf.equal(n, 1),
                         lambda: tf.constant([0.5], dtype=feature_type),
                         lambda: tf.divide(tf.cast(tf.range(n - 1, -1, -1), dtype=feature_type),
                                           tf.cast(n - 1, dtype=feature_type)))

        right_c = tf.cond(tf.equal(n, 1),
                          lambda: tf.constant([0.5], dtype=feature_type),
                          lambda: tf.divide(tf.cast(tf.range(n), dtype=feature_type),
                                            tf.cast(n - 1, dtype=feature_type)))

        W_i = tf.reshape(left_c, [n, 1, 1]) * tf.tile(tf.expand_dims(W_l, 0), [n, 1, 1]) \
              + tf.reshape(right_c, [n, 1, 1]) * tf.tile(tf.expand_dims(W_r, 0), [n, 1, 1])
        W_i = tf.reshape(l_i, [n, 1, 1]) * W_i

        approx_vec_p = tf.tanh(W_i @ tf.expand_dims(tf.gather(vec, cs), -1) + b)
        d = tf.norm(tf.gather(vec, p) - approx_vec_p)

        approx_vec_p_c = tf.tanh(W_i @ tf.expand_dims(tf.gather(vec, cs_c), -1) + b)
        d_c = tf.norm(tf.gather(vec, p_c) - approx_vec_p_c)

        y = tf.nn.relu(self.delta + d - d_c)

        cost = tf.reduce_mean(y)
        # optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(cost)
        optimizer = tf.train.MomentumOptimizer(learning_rate=0.001, momentum=0.1).minimize(cost)

        init_op = tf.global_variables_initializer()

        with tf.Session() as sess:
            sess.run(init_op)

            N = 100000

            print("Optimization begin!")
            for epoch in range(training_epochs):
                avg_cost = 0
                for i in range(N):
                    sample_p, sample_cs, sample_ls = X.loc[1500]
                    sample_p = [sample_p]

                    _, c = sess.run([optimizer, cost],
                                    feed_dict={p: sample_p, cs: sample_cs, ls: sample_ls})

                    avg_cost += c
                print("epoch= {} cost= {}".format(epoch, avg_cost))
            print("Optimization finished!")

            # TODO: accuracy?

            VEC = vec.eval()
        return VEC
        """
