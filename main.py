from pipe.code_gens import *
from pipe.cookers import *
from pipe.pickler import *
from pipe.pipe_base import *
from pipe.preprocessor import *
from pipe.terminaters import *


def main1():
    # make_node_embedding_train_set()

    def parse_nums(ss):
        return list(map(int, ss.strip("[]").split(", ")))

    X_train = pd.read_csv("data/node_embedding_train_set.csv",
                          converters={"children": parse_nums, "children_leaves_nums": parse_nums})

    pcEmbedding = ParentChildrenEmbedding(epochs=3, N=10000, variables_dump="data/model.ckpt")
    emb = pcEmbedding.fit(X_train)

    pd.DataFrame(emb[1:]) \
        .to_csv("data/node_emb.dump", sep='\t', index=False, header=None)

    node_coding = unpickle("data/node_coding.dump")
    pd.DataFrame(node_coding.sorted_kinds()) \
        .to_csv("data/emb_coding.dump", sep='\t', index=False, header=None)


def do_if_not_exists(path):
    if exists(path):
        node_embedding = unpickle(path)
    else:
        pipe = Pipe(FromCSV("data/step-12768-submissions.csv"))
        pipe.transform(Preprocessor(language="python", method="astize"))
        pipe.transform(ForNodeEmbedding())
        node_embedding = pipe.terminate(Pickle(path))
    print(len(node_embedding.dataset))


def main():
    do_if_not_exists("data/node_embedding.dump")


if __name__ == '__main__':
    main()
