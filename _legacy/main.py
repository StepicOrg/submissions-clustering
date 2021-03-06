from difflib import SequenceMatcher

import numpy as np
from sc._legacy.score import score_ratio
from sc.plot import plot
from sklearn.pipeline import Pipeline

from _legacy.ne import NodeEmbedding
from sc.pipe.steps.seekers import Seeker
from sc.utils.cookers import telegram_send

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
        sc = Pipe(Walk("data/dummyenv/lib/python3.6/", ext=".py"))
        sc.transform(Preprocessor(language="python", method="astize"))
        sc.transform(ForNodeEmbedding())
        node_embedding = sc.terminate(Pickle(path))
    train_vec(node_embedding)
"""


def do_test():
    pipeline = Pipeline([("pre", Preprocessor(language="python", method="astize"))])
    ne = NodeEmbedding(dump_path="data/model.ckpt")
    print(ne.theta.vec)
    X = pipeline.fit_transform(__single_file_gen("main.py"))
    print(ne.transform(X))


def do_score():
    transform = Pipeline([("pre", Preprocessor(language="python", method="tokenize")),
                          ("bot", BagOfWords(ngram_range=(2, 3))),
                          ("idf", TfidfTransformer())])
    cluster = MiniBatchKMeans(n_clusters=20, random_state=322)
    # cluster = DBSCAN(eps=0.25)
    mean_ratio, var_ratio = score_ratio(transform, cluster=cluster,
                                        start_from_center=False, inside_cluster=False,
                                        max_c=500, dist_c=2.,
                                        nrows=10000,
                                        show_dist_plot=True)
    # Фиксируем, что берем первые 10k сэмплов и разбиваем k-means на 20 кластеров, random_state=322:
    # tokenize => bow12 => idf
    # fff mean= 0.03353417738778997, var= 0.002961114989888911, time= 10:06 [300/2./10/30]
    print("mean= {}, var= {}".format(mean_ratio, var_ratio))


def do_plot():
    X = pd.read_csv("data/step-12768-submissions.csv", nrows=1000)
    # X = X[X["status"] == "correct"]
    pipeline1 = Pipeline([("pre", Preprocessor(language="python", method="astize")),
                          ("bot", BagOfTrees(ngram_range=(1, 2))),
                          ("idf", TfidfTransformer())])
    pipeline2 = Pipeline([("pre", Preprocessor(language="python", method="tokenize")),
                          ("bot", BagOfWords(ngram_range=(1, 3))),
                          ("idf", TfidfTransformer())])
    pipeline = pipeline1
    vecs = pipeline.fit_transform(X["code"]).toarray()
    X = X.iloc[pipeline.named_steps["pre"].icorrect]
    clu = MiniBatchKMeans(n_clusters=25, random_state=322)
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


def do_pipe_test():
    X = pd.read_csv("data/step-12768-submissions.csv")
    pipeline = Pipeline([("pre", Preprocessor(language="python", method="astize")),
                         ("fem", ForNodeEmbedding())])
    print(pipeline.fit_transform(X["code"]))


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


from amorph.tokens.patch import get_tokens


def token_metric(src1, src2):
    return SequenceMatcher(None, get_tokens(src1), get_tokens(src2)).ratio()


def do_token_ratio():
    df = pd.read_csv("data/step-12768-submissions.csv")
    pipeline = Pipeline([("pre", Preprocessor(language="python", method="astize"))])
    pipeline.fit_transform(df.code.values)

    old_df = df
    lc = pipeline.named_steps["pre"].icorrect
    df = df.iloc[pipeline.named_steps["pre"].icorrect]

    df["code"] = list(map(get_tokens, df.code))
    c_code = df[df.status == "correct"]["code"]

    best_ratio, best_ind = [], []
    for ind, tkns, status in zip(df.index, df.code, df.status):
        if ind % 100 == 0:
            print(ind)
            telegram_send("step= {}".format(ind))

        if status == "correct":
            _best_ratio = 1.
            _best_ind = ind
        else:
            _best_ratio = -1
            _best_ind = None
            for c_ind, c_tkns in zip(c_code.index, c_code):
                mtr = SequenceMatcher(None, tkns, c_tkns).ratio()
                if mtr > _best_ratio:
                    _best_ratio = mtr
                    _best_ind = c_ind

        best_ratio.append(_best_ratio)
        best_ind.append(_best_ind)

    old_df["best_ratio"] = .0
    old_df["best_ind"] = 0
    old_df.loc[lc, "best_ratio"] = best_ratio
    old_df.loc[lc, "best_ind"] = best_ind
    old_df.to_csv("data/step-12768-submissions-tokens-ratio.csv")


def do_test_ss():
    method = Method.from_str("python", "diff")
    ss = SubmissionsSimilarity(method=method)
    df = pd.read_csv("data/step-12768-submissions.csv", nrows=1000)
    ss.fit(r for _, r in df.iterrows())
    # print(ss.submissions)


def do_test_seeker():
    s = Seeker.from_str("nn")
    s.set_params(insider_cluster=True, start_from_center=True, only_centroids=True)
    s.fit(np.array([[1, 2, 3], [1, 2, 5.1]]))
    print(s.neighbors(np.array([[1, 2, 4]])))


if __name__ == '__main__':
    do_test_seeker()
    # do_test_ss()
    # do_token_ratio()
    # do_test()
    # do_score()
    # do_plot()
    # do_pipe_test()

# ________-------__________-------__________-------__________-------__________-------__________-------__________-------


from timeit import timeit

from sc import sc_from_spec
from sc.scorers import scorer_from_spec
from sc.utils import pickler
from sc.utils import read_subs


def score():
    sc = sc_from_spec("python", "diff")
    sc.fit(*read_subs.from_sl3("data/subs.sl3", nrows=1000))

    scorer = scorer_from_spec("python", "diff")
    sc.score_with(scorer)


def time():
    print(timeit(lambda: read_subs.from_sl3("data/subs.sl3"), number=3))
    print(timeit(lambda: read_subs.from_csv("data/step-12768-submissions.csv"), number=3))


def main():
    sc = sc_from_spec("python", "diff")
    codes, statuses = read_subs.from_sl3("data/subs.sl3", nrows=10000)
    sc.fit(codes, statuses)
    print("BEGIN")
    print(timeit(lambda: pickler.pickle(sc, "data/sc.dump"), number=1))

    del sc
    sc = pickler.unpickle("data/sc.dump")
    print(len(sc.neighbors([codes[0]])[0]))

    # plotter = plotter_from_spec("plotly")
    # sc.plot_with(plotter, title="Test plot", path="plots/temp_plot.html")


if __name__ == '__main__':
    # score()
    # time()
    main()
