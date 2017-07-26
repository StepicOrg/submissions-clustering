from difflib import SequenceMatcher

from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline

from models.utils.preprocessing import telegram_send
from new_pipe.code_gens import *
from new_pipe.cookers import *
from new_pipe.plot import plot
from new_pipe.preprocessor import Preprocessor


def make_pipe():
    X = pd.read_csv("data/step-12768-submissions.csv", nrows=1000)
    pipeline = Pipeline([("pre", Preprocessor(language="python", method="astize")),
                         ("bot", BagOfTrees(ngram_range=(1, 2))),
                         ("idf", TfidfTransformer())])
    vecs = pipeline.fit_transform(X["code"]).toarray()
    X = X.iloc[pipeline.named_steps["pre"].correct_ind]
    # clu = MiniBatchKMeans(n_clusters=10)
    clu = DBSCAN(eps=0.3, min_samples=3, n_jobs=-1)
    # clu = AffinityPropagation(damping=.95)
    labels = clu.fit_predict(vecs)

    plot(vecs, labels,
         method="pca",
         code=X["code"],
         correct=(X["status"] == "correct").astype(int),
         # scaling="centers",
         # centres=clu.cluster_centers_,
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
    make_pipe()
