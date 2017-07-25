from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.cluster import AffinityPropagation, KMeans, SpectralClustering, DBSCAN, MiniBatchKMeans, MeanShift
from sklearn.metrics import calinski_harabaz_score, silhouette_score
from sklearn.mixture import BayesianGaussianMixture

from new_pipe.code_gens import *
from new_pipe.cookers import *
from new_pipe.preprocessor import Preprocessor

if __name__ == '__main__':
    X = np.array(list(from_csv("data/step-12768-submissions.csv", nrows=1000)))
    pipeline = Pipeline([("pre", Preprocessor(language="python", method="tokenize")),
                         ("bot", BagOfWords()),
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
