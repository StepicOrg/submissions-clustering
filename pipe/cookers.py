from .pipe_base import Expander


class ForNodeEmbedding(Expander):
    def expand(self, elem, state):
        return elem.flatten(add_children_leaves_num=True)
