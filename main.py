import pickle as pkl
import pandas as pd
from parsers.python import parse
from node_embedder.node2int.python import node_embedding
from node_embedder.int2vec.node_embedding import ParentChildrenEmbedding


def parse_correct_py_programs(codes):
    py_asts = []
    for code in codes:
        try:
            if isinstance(code, str):
                py_asts.append(parse(code))
        except SyntaxError:
            pass
    return py_asts


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


def make_node_embedding_train_set():
    dataset = pd.read_csv("data/step-12768-submissions.csv")
    py_asts = parse_correct_py_programs(dataset["code"].values)
    trees, node_coding = node_embedding(py_asts)
    pickle(node_coding, "data/node_coding.dump")
    train_set = trees_to_train_set(trees)
    train_set.to_csv("data/node_embedding_train_set.csv", index=False)


def main():
    # make_node_embedding_train_set()

    def parse_nums(ss):
        return list(map(int, ss.strip("[]").split(", ")))

    X_train = pd.read_csv("data/node_embedding_train_set.csv",
                          converters={"children": parse_nums, "children_leaves_nums": parse_nums})

    pcEmbedding = ParentChildrenEmbedding(variables_dump="data/model.ckpt")
    emb = pcEmbedding.fit(X_train)

    pd.DataFrame(emb[1:]).to_csv("data/node_emb.dump", sep='\t', index=False, header=None)

    node_coding = unpickle("data/node_coding.dump")
    pd.DataFrame(node_coding.sorted_kinds()) \
        .to_csv("data/emb_coding.dump", sep='\t', index=False, header=None)


if __name__ == '__main__':
    main()
