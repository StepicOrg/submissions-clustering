import os
import numpy as np
import tensorflow as tf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


# TODO: 1) data download scripts + data processing scripts
# TODO: 2) rewrite py_func with separate placeholder (to be able to serialize meta graph)
# TODO: 3) deal with how we gonna train and retrain our emb model, with changing num_codes

# http://projector.tensorflow.org/?config=https://gist.githubusercontent.com/StasBel/13ab2047adc15ff85a98412680f111f5/raw/9b888779a5a67f867db121e6475eaecb055c908f/projector_config.json

class ParentChildrenEmbedding:
    def __init__(self, N_f=30, delta=1, learning_rate=0.001):
        self.N_f = N_f
        self.delta = delta
        self.learning_rate = learning_rate
        self.num_codes = 0

    def fit(self, X, training_epochs=10):
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
