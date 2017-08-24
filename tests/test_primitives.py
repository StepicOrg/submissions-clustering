from subsclu.primitives import DefaultIntBijection, Tree


def test_dib():
    dib = DefaultIntBijection(zero_value="ZERO")
    assert dib["ZERO"] == 0, "check zero value"
    assert dib.rev[0] == "ZERO", "rev check zero value"
    assert len(dib) == 1, "dib has only zero value"
    assert dib["NEW"] == 1, "inc and get new mapping"
    assert dib.rev[1] == "NEW", "back check"
    assert list(dib) == [(0, "ZERO"), (1, "NEW")], "check yieding mappings"
    assert dib is not dib.rev, "check reversing"


def test_tree():
    tree = Tree(0, [Tree(1), Tree(2), Tree(3)])
    assert tree.value == 0, "simple check"
    assert tree.children == [Tree(1), Tree(2), Tree(3)], "simple children"
    assert tree.leaves_num == 3, "check leaves num"
    assert tree.map(lambda x: x + 10).value == 10, "mapping"
    assert tree.depth == tree.height == 2, "depth and height"
    assert tree.subtree(1) == (0,), "subtree of height 1"
    assert tree.subtree(2) == (0, (1,), (2,), (3,)), "subtree of height 2"
