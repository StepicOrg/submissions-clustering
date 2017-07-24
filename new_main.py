from sklearn.pipeline import Pipeline

from new_pipe.code_gens import *
from new_pipe.preprocessor import Preprocessor

if __name__ == '__main__':
    pipeline = Pipeline([("pre", Preprocessor(language="python", method="grammarize"))])
    print(pipeline.fit_transform(list(single_file("new_main.py"))))
    print(pipeline.named_steps["pre"].encoding)
