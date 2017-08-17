import ast
import os
import subprocess

import requests

from .uast import Node
from ..base import BaseScorer

__all__ = ["ASTScorer"]


class ASTScorer(BaseScorer):
    _CMD_PREFIX = "java -jar"
    _API_ENDPOINT = "http://localhost:4567/api/diff"

    def _make_process(self):
        cmd = "{} {}".format(self._CMD_PREFIX, self.patch_server_jar_path)
        fnull = open(os.devnull, "w")
        return subprocess.Popen(cmd, stdout=fnull, stderr=subprocess.STDOUT, shell=True)

    def __init__(self, patch_server_jar_path):
        self.patch_server_jar_path = patch_server_jar_path

        self._process = self._make_process()

    def __del__(self):
        self._process.terminate()

    def _code_to_node(self, code):
        return Node(ast.parse(code))

    def score(self, src, dst):
        src_node, dst_node = self._code_to_node(src), self._code_to_node(dst)
        result = requests.post(self._API_ENDPOINT, {
            "src": src_node.to_json(),
            "dst": dst_node.to_json()
        })
        return float(len(list(result.json())))
