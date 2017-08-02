from collections import namedtuple

import matplotlib.pyplot as plt
import tensorflow as tf
from bunch import Bunch
from sklearn.base import BaseEstimator, TransformerMixin
from tqdm import tqdm

from ..pipe.pickler import *

from .utils.preprocessing import *

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

Input = namedtuple("Input", ["parent", "children", "children_leaves_nums",
                             "parent_c", "children_c",
                             "leaves_coefs", "left_coefs", "right_coefs"])
Theta = namedtuple("Theta", ["W_l", "W_r", "b", "vec"])
Output = namedtuple("Output", ["cost", "optimizer", "saver"])
Graph = namedtuple("Graph", ["input", "theta", "output"])


# TODO: 1) data download scripts + data processing scripts
# TODO: 3) deal with how we gonna train and retrain our emb model, with changing num_codes / max_children_num

class ParentChildrenEmbedding(BaseEstimator, TransformerMixin):
    def __init__(self, N_f=32, delta=1, alpha=1e-1,
                 optimizer="momentum", lr=1e-2, momentum=0.9,
                 batch_size=64, epochs=10, children_num_c=15,
                 N=None, dump_path=None, draw_cost_plot=False):
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
        self.draw_cost_plot = draw_cost_plot

        self.codes_num = None
        self.children_num = None
        self.theta = None
        self.graph = None

        if self.dump_path:
            consts_dump = self.dump_path + ".consts"
            if file_exists(consts_dump):
                self.codes_num, self.children_num = unpickle(consts_dump)
            if (self.codes_num, self.children_num) != (None, None):
                self.graph = self.build_graph()
                saver = self.graph.output.saver
                with tf.Session() as sess:
                    if file_exists(self.dump_path + ".index"):
                        saver.restore(sess, self.dump_path)
                    else:
                        sess.run(tf.global_variables_initializer())

        if self.dump_path:
            consts_dump = self.dump_path + ".consts"
            if file_exists(consts_dump):
                self.codes_num, self.children_num = unpickle(consts_dump) if file_exists(consts_dump) else None, None

            if file_exists(consts_dump):
                self.codes_num, self.children_num = unpickle(self.dump_path + ".consts") if file_exists(consts_dump)
        else:
            self.codes_num, self.children_num, self.theta = None, None, None

        self.codes_num, self.children_num = unpickle(self.dump_path + ".consts") if self.dump_path else 0, 0

        # _, theta, _ = self.build_graph()

        with tf.Session() as sess:
            saver = tf.train.Saver()
            saver = saver.restore(sess, self.dump_path)
            print(tf.all_variables())
            # print(theta.b.eval())

        self.theta = None

    def pre_fit(self, X):
        self.codes_num = max(self.codes_num or 0, max(X["parent"].max(), X["children"].map(max).max()))
        self.children_num = min(self.children_num_c, max(self.children_num or 0, X["children"].map(len).max()))
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
        return X

    def generate_input(self, batch):
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

    def build_graph(self):
        ph = Input(
            parent=tf.placeholder(tf.float32, [None]),
            children=tf.placeholder(tf.float32, [None, self.children_num_c]),
            children_leaves_nums=tf.placeholder(tf.float32, [None, self.children_num_c]),
            parent_c=tf.placeholder(tf.float32, [None]),
            children_c=tf.placeholder(tf.float32, [None, self.children_num_c]),
            leaves_coefs=tf.placeholder(tf.float32, [None, self.children_num_c]),
            left_coefs=tf.placeholder(tf.float32, [None, self.children_num_c]),
            right_coefs=tf.placeholder(tf.float32, [None, self.children_num_c])
        )

        tt = Theta(
            W_l=tf.Variable(tf.random_normal([self.N_f, self.N_f])),
            W_r=tf.Variable(tf.random_normal([self.N_f, self.N_f])),
            b=tf.Variable(tf.random_normal([self.N_f])),
            vec=tf.Variable(tf.random_normal([self.codes_num + 1, self.N_f]))
        )

        batch_size = tf.shape(ph.parent)[0]
        W = tf.reshape(ph.left_coefs, [batch_size, self.children_num_c, 1, 1]) \
            * tf.tile(tf.reshape(tt.W_l, [1, 1, self.N_f, self.N_f]), [batch_size, self.children_num_c, 1, 1])
        W += tf.reshape(ph.right_coefs, [batch_size, self.children_num_c, 1, 1]) \
             * tf.tile(tf.reshape(tt.W_r, [1, 1, self.N_f, self.N_f]), [batch_size, self.children_num_c, 1, 1])
        W = tf.reshape(ph.leaves_coefs, [batch_size, self.children_num_c, 1, 1]) * W

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

        return ph, tt, ct

    def choose_optimizer(self):
        if self.optimizer == "momentum":
            optimizer = tf.train.MomentumOptimizer(learning_rate=self.lr, momentum=self.momentum)
        elif self.optimizer == "adam":
            optimizer = tf.train.AdamOptimizer(learning_rate=self.lr)
        elif self.optimizer == "adadelta":
            optimizer = tf.train.AdadeltaOptimizer(learning_rate=self.lr)
        else:
            raise ValueError("No such optimizer supported yet")
        return optimizer

    def fit(self, X, y=None):

        X = self.pre_fit(X)

        placeholders, theta, cost = self.build_graph()

        optimizer = self.choose_optimizer().minimize(cost)

        saver = tf.train.Saver()

        with tf.Session() as sess:
            if self.dump_path and os.path.exists(self.dump_path + ".index"):
                print("Restoring variables from \"{}\".".format(self.dump_path))
                saver.restore(sess, self.dump_path)
            else:
                print("Initialize variables.")
                sess.run(tf.global_variables_initializer())

            print("Optimization begin.")
            N = self.N or len(X)
            cost_line = []
            for epoch in range(1, self.epochs + 1):
                avg_cost = 0
                total_batch = N // self.batch_size
                for batch in tqdm(split_into_batches(X, self.batch_size, max_len=N),
                                  total=total_batch, dynamic_ncols=True):
                    feed_dict = {a: b for a, b in zip(placeholders, self.generate_input(batch))}
                    _, c = sess.run([optimizer, cost], feed_dict=feed_dict)
                    avg_cost += c / total_batch
                cost_line.append(avg_cost)
                print("epoch= {} cost= {}".format(epoch, avg_cost))
                if self.dump_path and epoch == self.epochs:
                    if epoch == self.epochs:
                        print("Dump variables to \"{}\".".format(self.dump_path))
                    saver.save(sess, self.dump_path)
            print("Optimization finished.")

            if self.draw_cost_plot:
                plt.plot(cost_line)
                plt.savefig("data/node_emb_error_plot.png")
                plt.show()

            return theta.vec.eval()
