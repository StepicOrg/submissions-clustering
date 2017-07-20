from models.node_embedding import *
from pipe.cookers import *
from pipe.initers import *
from pipe.pickler import *
from pipe.pipe_base import *
from pipe.preprocessor import *
from pipe.terminaters import *


def train_vec(node_embedding):
    pc_embedding = ParentChildrenEmbedding(epochs=15, N=5000000, variables_dump="data/model.ckpt")
    node_vec = pc_embedding.fit(node_embedding.dataset)
    pd.DataFrame(node_vec).to_csv("data/node_vec.dump", sep='\t', index=False, header=None)
    node_list = list(item[1] for item in node_embedding.encoding)
    pd.DataFrame(node_list).to_csv("data/node_list.dump", sep='\t', index=False, header=None)


def do_if_not_exists(path):
    if exists(path):
        node_embedding = unpickle(path)
    else:
        pipe = Pipe(Walk("data/dummyenv/lib/python3.6/", ext=".py"))
        pipe.transform(Preprocessor(language="python", method="astize"))
        pipe.transform(ForNodeEmbedding())
        node_embedding = pipe.terminate(Pickle(path))
    train_vec(node_embedding)


def main():
    do_if_not_exists("data/node_embedding.dump")


if __name__ == '__main__':
    main()
