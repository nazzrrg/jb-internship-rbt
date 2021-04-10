class RbtNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.parent: RbtNode = None
        self.left_child: RbtNode = None
        self.right_child: RbtNode = None
        self.is_red = True


class Rbt:
    def __init__(self):
        self.root: RbtNode = None

    def get(self, key):
        cur_node: RbtNode = self.root

        while cur_node is not None and cur_node.key != key:
            if cur_node.key < key:
                cur_node = cur_node.right_child
            else:
                cur_node = cur_node.left_child

        return cur_node.value

    def insert(self, key, value):
        new_node = RbtNode(key=key, value=value)

        if self.root is None:
            new_node.is_red = False
            self.root = new_node
            return

        parent = self.root

        while parent is not None:
            if parent.key == key:
                parent.value = value
                return
            elif parent.key < new_node.key:
                if parent.right_child is None:
                    break

                parent = parent.right_child
            else:
                if parent.left_child is None:
                    break

                parent = parent.left_child

        new_node.parent = parent

        if parent.key < new_node.key:
            parent.right_child = new_node
        else:
            parent.left_child = new_node

        self.fix(new_node)

    def rotate_right(self, node: RbtNode):
        left_child = node.left_child

        node.left_child = left_child.right_child
        if node.left_child is not None:
            node.left_child.parent = node

        left_child.parent = node.parent
        if left_child.parent is None:
            self.root = left_child
        elif node.parent.left_child == node:
            node.parent.left_child = left_child
        else:
            node.parent.right_child = left_child

        left_child.right_child = node
        node.parent = left_child

    def rotate_left(self, node: RbtNode):
        right_child = node.right_child

        node.right_child = right_child.left_child
        if node.right_child is not None:
            node.right_child.parent = node

        right_child.parent = node.parent
        if right_child.parent is None:
            self.root = right_child
        elif node.parent.left_child == node:
            node.parent.left_child = right_child
        else:
            node.parent.right_child = right_child

        right_child.left_child = node
        node.parent = right_child

    def fix(self, cur_node: RbtNode):
        while cur_node != self.root and cur_node.parent.is_red and cur_node.is_red:
            parent = cur_node.parent
            grandparent = parent.parent

            if parent == grandparent.left_child:

                uncle = grandparent.right_child

                if uncle is not None and uncle.is_red:
                    grandparent.is_red = True
                    parent.is_red = False
                    uncle.is_red = False
                    cur_node = grandparent
                else:
                    if cur_node == parent.right_child:
                        self.rotate_left(parent)
                        cur_node = parent
                        parent = cur_node.parent

                    self.rotate_right(grandparent)
                    parent.is_red, grandparent.is_red = grandparent.is_red, parent.is_red
                    cur_node = parent
            else:
                uncle = grandparent.left_child

                if uncle is not None and uncle.is_red:
                    grandparent.is_red = True
                    parent.is_red = False
                    uncle.is_red = False
                    cur_node = grandparent
                else:
                    if cur_node == parent.left_child:
                        self.rotate_right(parent)
                        cur_node = parent
                        parent = cur_node.parent

                    self.rotate_left(grandparent)
                    parent.is_red, grandparent.is_red = grandparent.is_red, parent.is_red
                    cur_node = parent

        self.root.is_red = False

    def delete(self, key):
        raise Exception("Deletion not implemented")  # todo implement
