import pandas as pd
from parsers.python import parse
from node_embedder.node2int.python import node_embedding

if __name__ == '__main__':
    dataset = pd.read_csv("data/step-12768-submissions.csv")
    code = dataset["code"][0]
    tree, node_coding = node_embedding(parse(code))
    tree.map(node_coding).pretty_print()
