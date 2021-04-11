import pytest
import random

from rbt import *

bh = 0
bh_log = set()


def bh_test_dfs(node: RbtNode):
    global bh_log
    global bh

    if node is None:
        bh_log.add(bh)
        return

    if not node.is_red:
        bh += 1
        bh_test_dfs(node.left_child)
        bh_test_dfs(node.right_child)
        bh -= 1
    else:
        bh_test_dfs(node.left_child)
        bh_test_dfs(node.right_child)


@pytest.fixture
def data():
    tree = Rbt()
    test_dict = dict()
    for i in range(1, int(1e5)):
        key = random.randint(0, int(1e9))
        value = random.randint(0, int(1e8))
        test_dict[key] = value
        tree.insert(key, value)

    for i in range(1, int(1e3)):
        key = random.choice(list(test_dict.keys()))
        test_dict.pop(key)
        tree.delete(key)

    return tree, test_dict


@pytest.fixture
def sample_tree() -> Rbt:
    tree = Rbt()
    tree.insert(6, 6)
    tree.insert(8, 8)
    tree.insert(9, 9)
    tree.insert(7, 7)
    tree.insert(4, 4)
    tree.insert(5, 5)
    tree.insert(2, 2)
    tree.insert(3, 3)
    tree.insert(1, 1)

    return tree


def test_rbt_consistent_black_height(data):
    global bh_log, bh
    bh_log = set()
    bh = 0

    tree = data[0]
    bh_test_dfs(tree.root)
    print(bh_log)
    assert len(bh_log) == 1


def test_rbg_root_is_black(data):
    tree = data[0]

    assert not tree.root.is_red


def test_reds_children_are_consistently_black(data):
    def dfs(node: RbtNode):
        if node is None:
            return

        if node.is_red:
            assert node.right_child is None or not node.right_child.is_red
            assert node.left_child is None or not node.left_child.is_red

        dfs(node.left_child)
        dfs(node.right_child)

    tree = data[0]

    dfs(tree.root)


def test_random_insert_then_get(data):
    tree = data[0]
    dictionary = data[1]

    for key in dictionary.keys():
        assert dictionary[key] == tree.get(key)


def test_insert_root():
    tree = Rbt()
    tree.insert(2, 2)

    key = tree.root.key
    value = tree.root.value
    assert key == 2 and value == 2


def test_insert_to_the_left():
    tree = Rbt()
    tree.insert(2, 2)
    tree.insert(1, 1)

    key = tree.root.left_child.key
    value = tree.root.left_child.value
    assert key == 1 and value == 1


def test_insert_to_the_right():
    tree = Rbt()
    tree.insert(2, 2)
    tree.insert(3, 3)

    key = tree.root.right_child.key
    value = tree.root.right_child.value
    assert key == 3 and value == 3


def test_insert_value_with_existing_key_substitute():
    tree = Rbt()
    tree.insert(2, 2)
    tree.insert(2, 3)

    key = tree.root.key
    value = tree.root.value
    assert key == 2 and value == 3


def test_rotate_right(sample_tree):
    tree = sample_tree

    tree.rotate_right(tree.root)

    key = tree.root.key
    assert key == 4
    key = tree.root.left_child.key
    assert key == 2
    key = tree.root.left_child.left_child.key
    assert key == 1
    key = tree.root.left_child.right_child.key
    assert key == 3
    key = tree.root.right_child.key
    assert key == 6
    key = tree.root.right_child.left_child.key
    assert key == 5
    key = tree.root.right_child.right_child.key
    assert key == 8
    key = tree.root.right_child.right_child.left_child.key
    assert key == 7
    key = tree.root.right_child.right_child.right_child.key
    assert key == 9


def test_rotate_left():
    tree = Rbt()
    tree.insert(4, 4)
    tree.insert(2, 2)
    tree.insert(1, 1)
    tree.insert(3, 3)
    tree.insert(6, 6)
    tree.insert(5, 5)
    tree.insert(8, 8)
    tree.insert(7, 7)
    tree.insert(9, 9)

    tree.rotate_left(tree.root)

    key = tree.root.key
    assert key == 6
    key = tree.root.left_child.key
    assert key == 4
    key = tree.root.left_child.left_child.key
    assert key == 2
    key = tree.root.left_child.left_child.left_child.key
    assert key == 1
    key = tree.root.left_child.left_child.right_child.key
    assert key == 3
    key = tree.root.left_child.right_child.key
    assert key == 5
    key = tree.root.right_child.key
    assert key == 8
    key = tree.root.right_child.left_child.key
    assert key == 7
    key = tree.root.right_child.right_child.key
    assert key == 9


def test_successor_node(sample_tree):
    tree = sample_tree

    assert successor_node(tree.root.right_child).key == 7


def test_sibling(sample_tree):
    tree = sample_tree
    assert sibling_node(tree.root.left_child.left_child).key == 5
    assert sibling_node(tree.root.left_child.right_child).key == 2
