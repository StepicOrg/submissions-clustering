from difflib import SequenceMatcher

from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline

from models.utils.preprocessing import telegram_send
from pipe.code_gens import *
from pipe.cookers import *
from pipe.plot import plot
from pipe.preprocessor import Preprocessor
from pipe.score import score_ratio

"""
def train_vec(node_embedding):
    pc_embedding = ParentChildrenEmbedding(epochs=10, N=10000000, variables_dump="data/model.ckpt")
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
"""


def do_score():
    transform = Pipeline([("pre", Preprocessor(language="python", method="astize")),
                          ("bot", BagOfTrees(ngram_range=(1, 2))),
                          ("idf", TfidfTransformer())])
    cluster = MiniBatchKMeans(n_clusters=10)
    mratio = score_ratio(transform,
                         cluster=cluster,
                         method="cluster",
                         nrows=100)
    print(mratio)


def do_plot():
    X = pd.read_csv("data/step-12768-submissions.csv", nrows=1000)
    # X = X[X["status"] == "correct"]
    pipeline = Pipeline([("pre", Preprocessor(language="python", method="astize")),
                         ("bot", BagOfTrees(ngram_range=(1, 2))),
                         ("idf", TfidfTransformer())])
    vecs = pipeline.fit_transform(X["code"]).toarray()
    X = X.iloc[pipeline.named_steps["pre"].icorrect]
    clu = MiniBatchKMeans(n_clusters=10)
    # clu = DBSCAN(eps=0.25, min_samples=2, n_jobs=-1)
    # clu = AffinityPropagation(damping=.95)
    labels = clu.fit_predict(vecs)

    plot(vecs, labels,
         method="tsne",
         code=X["code"],
         correct=(X["status"] == "correct").astype(int),
         scaling="centers",
         centres=clu.cluster_centers_,
         title="Submissions of step №12768 clustering")

    """
    # X = np.array(list(from_csv("data/step-12768-submissions.csv", nrows=1000)))
    # clu = DBSCAN(min_samples=5, n_jobs=-1)
    clu = MiniBatchKMeans(n_clusters=10)
    # clu = MeanShift(n_jobs=-1)
    labels = clu.fit_predict(vecs)
    # print(labels.max() + sum(labels == -1))
    print(labels)
    X = X[pipeline.named_steps["pre"].correct_ind]
    print(calinski_harabaz_score(vecs.toarray(), labels))
    """


def make_dataset_with_ratio():
    df = pd.read_csv("data/step-12768-submissions.csv")
    correct_code = df[df.status == "correct"]["code"]
    step = -1

    def apply_f(c):
        nonlocal step
        step += 1
        if step % 100 == 0:
            telegram_send("step= {}".format(step))
        if c[1] != "correct":
            return max(map(lambda cc: SequenceMatcher(None, str(c[0]), cc).ratio(), correct_code))
        else:
            return 1.

    df["best_ratio"] = pd.Series(df[["code", "status"]].apply(apply_f, axis=1))
    df.to_csv("data/step-12768-submissions-with-ratio.csv")


if __name__ == '__main__':
    do_score()
    # do_plot()
