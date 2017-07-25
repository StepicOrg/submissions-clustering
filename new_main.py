from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import calinski_harabaz_score
from sklearn.pipeline import Pipeline

from new_pipe.code_gens import *
from new_pipe.cookers import *
from new_pipe.preprocessor import Preprocessor

from difflib import SequenceMatcher

from models.utils.preprocessing import telegram_send


def make_pipe():
    X = np.array(list(from_csv("data/step-12768-submissions.csv", nrows=1000)))
    pipeline = Pipeline([("pre", Preprocessor(language="python", method="astize")),
                         ("bot", BagOfTrees()),
                         ("idf", TfidfTransformer())])
    vecs = pipeline.fit_transform(X)
    # clu = DBSCAN(min_samples=5, n_jobs=-1)
    clu = MiniBatchKMeans(n_clusters=10)
    # clu = MeanShift(n_jobs=-1)
    labels = clu.fit_predict(vecs)
    # print(labels.max() + sum(labels == -1))
    print(labels)
    X = X[pipeline.named_steps["pre"].correct_ind]
    print(calinski_harabaz_score(vecs.toarray(), labels))


def make_dataset_with_ratio():
    df = pd.read_csv("data/step-12768-submissions.csv")
    correct_code = df[df.status == "correct"]["code"]
    step = -1

    def apply_f(c):
        nonlocal step
        step += 1
        print(step)
        if step % 100 == 0:
            telegram_send("step= {}".format(step))
        if c[1] != "correct":
            return max(map(lambda cc: SequenceMatcher(None, c[0], cc).ratio(), correct_code))
        else:
            return 1.

    df["best_ratio"] = pd.Series(df[["code", "status"]].apply(apply_f, axis=1))
    df.to_csv("data/step-12768-submissions-with-ratio.csv")


if __name__ == '__main__':
    make_dataset_with_ratio()
