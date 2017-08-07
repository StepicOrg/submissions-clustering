from collections import namedtuple

import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
from sklearn.base import BaseEstimator, TransformerMixin
from tqdm import tqdm

from .pickler import *
from .utils.preprocessing import *

Input = namedtuple("Input", ["parent", "children", "children_leaves_nums",
                             "parent_c", "children_c",
                             "leaves_coefs", "left_coefs", "right_coefs"])
Theta = namedtuple("Theta", ["W_l", "W_r", "b", "vec"])
Output = namedtuple("Output", ["optimizer", "cost"])
Graph = namedtuple("Graph", ["input", "theta", "output"])


class NodeEmbedding(BaseEstimator, TransformerMixin):
    def __init__(self, N_f=32, delta=1, alpha=1e-1,
                 optimizer="momentum", lr=1e-2, momentum=0.9,
                 batch_size=64, epochs=10, children_num_c=15,
                 N=None, dump_path=None, cost_plot_path=None,
                 method="node2vec"):
        self.N_f = N_f
        self.delta = delta
        self.alpha = alpha
        self.optimizer = optimizer
        self.lr = lr
        self.momentum = momentum
        self.batch_size = batch_size
        self.epochs = epochs
        self.children_num_c = children_num_c
        self.N = N
        self.dump_path = dump_path
        self.cost_plot_path = cost_plot_path
        self.method = method

        self.codes_num = None
        self.children_num = None
        self.theta = None

        self._graph = None
        self._read_dump()

    def _read_dump(self):
        if self.dump_path:
            consts_dump = self.dump_path + ".consts"
            if file_exists(consts_dump):
                self.codes_num, self.children_num = unpickle(consts_dump)
            if (self.codes_num, self.children_num) != (None, None):
                self._build_graph()
                self._train()

    def _pre_fit(self, X):
        new_codes_num = max(self.codes_num or 0, max(X["parent"].max(), X["children"].map(max).max()))
        new_children_num = min(self.children_num_c, max(self.children_num or 0, X["children"].map(len).max()))
        shape_changes = (self.codes_num != new_codes_num) or (self.children_num != new_children_num)
        self.codes_num = new_codes_num
        self.children_num = new_children_num
        X = X[X["children"].map(len) <= self.children_num].copy()
        X["children_num"] = X["children"].map(len)
        X["children"] = list(pad_sequences(X["children"].as_matrix(), max_len=self.children_num))
        children_leaves_nums = pad_sequences(X["children_leaves_nums"].as_matrix(), max_len=self.children_num)
        X["children_leaves_nums"] = list(children_leaves_nums)
        X["leaves_coefs"] = list((children_leaves_nums / np.sum(children_leaves_nums, axis=1)[:, np.newaxis]))
        left_coefs, right_coefs = [], []
        for i, n in enumerate(X["children_num"]):
            if n == 1:
                left_coefs.append([0.5])
                right_coefs.append([0.5])
            else:
                left_coefs.append((np.arange(n - 1, -1, -1) / (n - 1)).tolist())
                right_coefs.append((np.arange(n) / (n - 1)).tolist())
        X["left_coefs"] = list(pad_sequences(left_coefs, max_len=self.children_num))
        X["right_coefs"] = list(pad_sequences(right_coefs, max_len=self.children_num))
        return X, shape_changes

    def _generate_input(self, batch):
        cols = {column: np.squeeze(np.vstack(batch[column].as_matrix())).astype(float) for column in batch.columns}
        parent_c = cols["parent"].copy()
        children_c = cols["children"].copy()
        for i, n in enumerate(cols.pop("children_num")):
            k = np.random.randint(n + 1)
            new_code = np.random.randint(1, self.codes_num + 1)
            if k:
                children_c[i, k - 1] = new_code
            else:
                parent_c[i] = new_code
        cols["parent_c"] = parent_c
        cols["children_c"] = children_c
        return Input(**cols)

    def _build_graph(self):
        ph = Input(
            parent=tf.placeholder(tf.float32, [None]),
            children=tf.placeholder(tf.float32, [None, self.children_num]),
            children_leaves_nums=tf.placeholder(tf.float32, [None, self.children_num]),
            parent_c=tf.placeholder(tf.float32, [None]),
            children_c=tf.placeholder(tf.float32, [None, self.children_num]),
            leaves_coefs=tf.placeholder(tf.float32, [None, self.children_num]),
            left_coefs=tf.placeholder(tf.float32, [None, self.children_num]),
            right_coefs=tf.placeholder(tf.float32, [None, self.children_num])
        )

        tt = Theta(
            W_l=tf.Variable(tf.random_normal([self.N_f, self.N_f])),
            W_r=tf.Variable(tf.random_normal([self.N_f, self.N_f])),
            b=tf.Variable(tf.random_normal([self.N_f])),
            vec=tf.Variable(tf.random_normal([self.codes_num + 1, self.N_f]))
        )

        batch_size = tf.shape(ph.parent)[0]
        W = tf.reshape(ph.left_coefs, [batch_size, self.children_num, 1, 1]) \
            * tf.tile(tf.reshape(tt.W_l, [1, 1, self.N_f, self.N_f]), [batch_size, self.children_num, 1, 1])
        W += tf.reshape(ph.right_coefs, [batch_size, self.children_num, 1, 1]) \
             * tf.tile(tf.reshape(tt.W_r, [1, 1, self.N_f, self.N_f]), [batch_size, self.children_num, 1, 1])
        W = tf.reshape(ph.leaves_coefs, [batch_size, self.children_num, 1, 1]) * W

        def make_dist_tensor(p, cs):
            dist = W @ tf.expand_dims(tf.gather(tt.vec, tf.cast(cs, tf.int32)), -1)
            dist = tf.tanh(tf.squeeze(tf.reduce_sum(dist, axis=1)) + tf.expand_dims(tt.b, 0))
            dist = tf.norm(tf.gather(tt.vec, tf.cast(p, tf.int32)) - dist, axis=1) ** 2
            return dist

        d = make_dist_tensor(ph.parent, ph.children)
        d_c = make_dist_tensor(ph.parent_c, ph.children_c)
        y = tf.nn.relu(self.delta + d - d_c)

        l2_coef = tf.constant(self.alpha / (2 * (self.N_f ** 2)))
        W_l_norm = tf.norm(tt.W_l, ord="fro", axis=[0, 1]) ** 2
        W_r_norm = tf.norm(tt.W_r, ord="fro", axis=[0, 1]) ** 2
        l2_reg = l2_coef * (W_l_norm + W_r_norm)
        cost_wo_reg = 0.5 * tf.reduce_mean(y)
        ct = cost_wo_reg + l2_reg
        opt = self._choose_optimizer().minimize(ct)

        op = Output(
            optimizer=opt,
            cost=ct
        )

        self._graph = Graph(
            input=ph,
            theta=tt,
            output=op
        )

    def _choose_optimizer(self):
        if self.optimizer == "momentum":
            optimizer = tf.train.MomentumOptimizer(learning_rate=self.lr, momentum=self.momentum)
        elif self.optimizer == "adam":
            optimizer = tf.train.AdamOptimizer(learning_rate=self.lr)
        elif self.optimizer == "adadelta":
            optimizer = tf.train.AdadeltaOptimizer(learning_rate=self.lr)
        else:
            raise ValueError("No such optimizer supported yet")
        return optimizer

    def _train(self, X=None):
        placeholders, theta, cost = self._graph
        with tf.Session() as sess:
            saver = tf.train.Saver()
            if file_exists(self.dump_path + ".index"):
                saver.restore(sess, self.dump_path)
            else:
                sess.run(tf.global_variables_initializer())

            if X is not None:
                print("Optimization begin.")
                N = self.N or len(X)
                cost_line = []
                for epoch in range(1, self.epochs + 1):
                    avg_cost = 0
                    total_batch = N // self.batch_size
                    for batch in tqdm(split_into_batches(X, self.batch_size, max_len=N),
                                      total=total_batch, dynamic_ncols=True):
                        feed_dict = {a: b for a, b in zip(placeholders, self._generate_input(batch))}
                        _, c = sess.run([optimizer, cost], feed_dict=feed_dict)
                        avg_cost += c / total_batch
                    cost_line.append(avg_cost)
                    print("epoch= {} cost= {}".format(epoch, avg_cost))
                    if self.dump_path and epoch == self.epochs:
                        if epoch == self.epochs:
                            print("Dump variables to \"{}\".".format(self.dump_path))
                        saver.save(sess, self.dump_path)
                print("Optimization finished.")
                if self.cost_plot_path:
                    plt.plot(cost_line)
                    plt.savefig(cost_plot_path)
                    plt.show()

            self.theta = Theta(*map(lambda x: x.eval(), self._graph.theta))

    def fit(self, X, y=None):
        X = pd.DataFrame.from_records(chain.from_iterable(x.flatten(add_children_leaves_nums=True) for x in X))
        X, shape_changes = self._pre_fit(X)
        if self._graph is None or shape_changes:
            self._build_graph()
        self._train(X)
        return self

    def _node2vec(self, X):
        return list(x.map(self.theta.vec) for x in X)

    def transform(self, X):
        if self.method == "node2vec":
            return self._node2vec(X)
        else:
            raise ValueError("No such method supported yet")
