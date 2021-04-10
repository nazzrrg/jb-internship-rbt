import random

from rbt import Rbt


def test_random_insert_then_get():
    tree = Rbt()
    test_dict = dict()
    for i in range(1, int(1e5)):
        key = random.randint(0, int(1e9))
        value = random.randint(0, int(1e8))
        test_dict[key] = value
        tree.insert(key, value)

    for key in test_dict.keys():
        assert test_dict[key] == tree.get(key)


def test_insert_root():
    tree = Rbt()
    tree.insert(2, 2)

    key = tree.root.key
    value = tree.root.value
    assert key == 2 and value == 2


def test_insert_left_of_root():
    tree = Rbt()
    tree.insert(2, 2)
    tree.insert(1, 1)

    key = tree.root.left_child.key
    value = tree.root.left_child.value
    assert key == 1 and value == 1


def test_insert_right_of_root():
    tree = Rbt()
    tree.insert(2, 2)
    tree.insert(3, 3)

    key = tree.root.right_child.key
    value = tree.root.right_child.value
    assert key == 3 and value == 3


def test_insert_substitute_existing():
    tree = Rbt()
    tree.insert(2, 2)
    tree.insert(2, 3)

    key = tree.root.key
    value = tree.root.value
    assert key == 2 and value == 3


def test_rotate_right():
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


def test_fix():
    assert True  # todo implement
