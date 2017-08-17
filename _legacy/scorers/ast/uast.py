import ast
import copy
import json
import uuid
from typing import List, Dict, Union, Type, Any

from .constants import NODE_DESC
from .exceptions import InvalidArgumentException

__all__ = []

ASTNode = Union[ast.AST, List[ast.AST], None]
ASTNodeType = Union[Type[ast.AST], Type[List[ast.AST]], Type[None]]
NodeProps = Dict[str, Any]
NoneType = type(None)
NodePkType = str


class Node(object):
    def __init__(self, element: ASTNode, parent: Union['Node', None] = None):
        self._pk = NodePkType(uuid.uuid4())
        self._ast_type = type(element)
        self._parent = parent
        self._props = {}
        self._children = []

        if self.ast_type == NoneType:
            return

        elif self.ast_type == list:
            self.children = [Node(child, self) for child in element]

        elif self.ast_type in NODE_DESC:
            for prop in NODE_DESC[self.ast_type]['props']:
                self.props[prop] = getattr(element, prop)

            for name in NODE_DESC[self.ast_type]['children']:
                child = getattr(element, name)
                self.children.append(Node(child, self))

        else:
            raise InvalidArgumentException('{} is not a valid AST node'.format(self.ast_type.__name__))

    def detach_child(self, child: 'Node'):
        pos = child.children_pos
        self.children = self.children[:pos] + self.children[pos + 1:]
        child.parent = None

    def attach_child(self, child: 'Node', pos: int):
        self.children = self.children[:pos] + [child] + self.children[pos:]
        child.parent = self

    def update(self, new_type: ASTNodeType, new_props: NodeProps):
        self.ast_type = new_type
        self.props = copy.deepcopy(new_props)

    def find(self, pk: NodePkType) -> Union['Node', None]:
        if self.pk == pk:
            return self

        for child in self.children:
            result = child.find(pk)
            if result is not None:
                return result

        return None

    def to_dict(self) -> dict:
        return {
            'pk': self.pk,
            'ast_type': self.ast_type.__name__,
            'props': self.props,
            'children': [child.to_dict() for child in self.children]
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @property
    def children_pos(self) -> int:
        for idx, child in enumerate(self.parent.children):
            if child.pk == self.pk:
                return idx

    @property
    def is_leaf(self) -> bool:
        return len(self.children) == 0

    @property
    def pk(self) -> NodePkType:
        return self._pk

    @property
    def ast_type(self) -> ASTNodeType:
        return self._ast_type

    @ast_type.setter
    def ast_type(self, new_type: ASTNodeType):
        self._ast_type = new_type

    @property
    def props(self):
        return self._props

    @props.setter
    def props(self, new_props: NodeProps):
        self._props = new_props

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, new_parent: Union['Node', None]):
        self._parent = new_parent

    @property
    def children(self) -> List['Node']:
        return self._children

    @children.setter
    def children(self, new_children: List['Node']):
        self._children = new_children

    @property
    def nodes_num(self):
        return 1 + (sum(child.nodes_num for child in self.children) if not self.is_leaf else 0)
