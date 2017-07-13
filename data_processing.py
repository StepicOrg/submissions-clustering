import os
import pickle as pkl
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from parsers.python import parse
from node_embedder.node2int.python import node_embedding

# TODO: chetverg:
# 1) progranat na pip failax, sobrat statistiky

VENV_PY36_PATH = "venv/lib/python3.6/"


def filter_correct_code(code_gen):
    for code in code_gen:
        try:
            if isinstance(code, str):
                yield parse(code)
        except SyntaxError:
            pass


def pickle(obj, filename=None):
    filename = filename or obj.__class__.__name__
    with open(filename, "wb") as f:
        pkl.dump(obj, f, pkl.HIGHEST_PROTOCOL)


def unpickle(filename):
    with open(filename, "rb") as f:
        obj = pkl.load(f)
    return obj


def trees_to_train_set(trees):
    result = []
    for tree in trees:
        result.extend(tree.flatten(add_children_leaves_nums=True))
    return pd.DataFrame(result, columns=["parent", "children", "children_leaves_nums"])


def make_node_emb_dataset(code_gen, node_coding_dump="data/node_coding.dump",
                          train_set_csv="data/node_embedding_train_set.csv"):
    code_gen = filter_correct_code(code_gen)
    trees, node_coding = node_embedding(code_gen)
    pickle(node_coding, node_coding_dump)
    train_set = trees_to_train_set(trees)
    train_set.to_csv(train_set_csv, index=False)


def main():
    def venv_py_code():
        for dir_path, dir_names, file_names in os.walk(VENV_PY36_PATH):
            for file_name in file_names:
                if file_name.endswith(".py") and not file_name.startswith("_"):
                    yield open(os.path.join(dir_path, file_name)).read()

    # make_node_emb_dataset(venv_py_code())

    def parse_nums(ss):
        return list(map(int, ss.strip("[]").split(", ")))

    print("kek")
    X_train = pd.read_csv("data/node_embedding_train_set.csv",
                          converters={"children": parse_nums, "children_leaves_nums": parse_nums})
    print("mem")
    X_train = X_train.sample(20000)
    children_nums = X_train["children"].map(len).as_matrix()

    # print(dict(zip(*np.unique(children_nums, return_counts=True))))
    sns.distplot(children_nums, kde=False, rug=True)
    plt.show()


if __name__ == '__main__':
    main()
