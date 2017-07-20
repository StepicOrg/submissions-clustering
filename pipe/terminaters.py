import pandas as pd
from bunch import Bunch
from tqdm import tqdm

from .pickler import pickle
from .pipe_base import Terminater


class ToList(Terminater):
    def terminate(self, gen, state):
        return list(gen)


class Pickle(Terminater):
    def __init__(self, path):
        self.path = path

    def terminate(self, gen, state):
        store = Bunch(state)
        store.dataset = pd.DataFrame.from_records(gen)
        pickle(store, self.path)
        return store
