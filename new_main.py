from sklearn.pipeline import Pipeline

from new_pipe.code_gens import *
from new_pipe.cookers import *
from new_pipe.preprocessor import Preprocessor

if __name__ == '__main__':
    pipeline = Pipeline([("pre", Preprocessor(language="python", method="tokenize")),
                         ("bow", BagOfWords(ngram_range=(1, 3)))])
    print(pipeline.fit_transform(list(from_csv("data/step-12768-submissions.csv", nrows=100))).shape)
    print(pipeline.named_steps["bow"].vocabulary_)
