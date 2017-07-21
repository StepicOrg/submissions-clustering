from .pipe_base import Expander, Mapper, LinPoint


class ForNodeEmbedding(Expander):
    def expand(self, elem, state):
        return elem.flatten(add_children_leaves_num=True)


@LinPoint
class BagOfWords(Mapper):
    def map(self, elem, state):
        pass
