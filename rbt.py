class RbtNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.parent: RbtNode = None
        self.left_child: RbtNode = None
        self.right_child: RbtNode = None
        self.is_red = True


def successor_node(node: RbtNode):
    cur_node = node

    while cur_node.left_child is not None:
        cur_node = cur_node.left_child

    return cur_node


def sibling_node(node: RbtNode):
    if node is None or node.parent is None:
        return None
    if node.parent.left_child == node:
        return node.parent.right_child
    else:
        return node.parent.left_child


class Rbt:
    def __init__(self):
        self.root: RbtNode

    def get_node(self, key):
        cur_node: RbtNode = self.root

        while cur_node is not None and cur_node.key != key:
            if cur_node.key < key:
                cur_node = cur_node.right_child
            else:
                cur_node = cur_node.left_child

        return cur_node

    def get(self, key):
        node = self.get_node(key)

        if node is not None:
            return node.value
        else:
            return None

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

        self.fix_red_red(new_node)

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

    def fix_red_red(self, node: RbtNode):
        if node == self.root:
            node.is_red = False
            return

        parent = node.parent
        uncle = sibling_node(parent)
        grandparent = parent.parent

        if parent.is_red:
            if uncle is not None and uncle.is_red:
                parent.is_red = False
                uncle.is_red = False
                grandparent.is_red = True
                self.fix_red_red(grandparent)
            else:
                if parent.parent.left_child == parent:
                    if node.parent.left_child == node:
                        parent.is_red, grandparent.is_red = grandparent.is_red, parent.is_red
                    else:
                        self.rotate_left(parent)
                        node.is_red, grandparent.is_red = grandparent.is_red, node.is_red

                    self.rotate_right(grandparent)
                else:
                    if node.parent.left_child == node:
                        self.rotate_right(parent)
                        node.is_red, grandparent.is_red = grandparent.is_red, node.is_red
                    else:
                        parent.is_red, grandparent.is_red = grandparent.is_red, parent.is_red
                    self.rotate_left(grandparent)

    def delete(self, key):
        node = self.get_node(key)

        if node is not None:
            self.delete_node(node)

    def delete_node(self, node_to_delete: RbtNode):
        substitute_node: RbtNode

        if node_to_delete.left_child is not None and node_to_delete.right_child is not None:
            substitute_node = successor_node(node_to_delete.right_child)
        elif node_to_delete.left_child is not None:
            substitute_node = node_to_delete.left_child
        elif node_to_delete.right_child is not None:
            substitute_node = node_to_delete.right_child
        else:
            substitute_node = None

        both_black = (substitute_node is None or not substitute_node.is_red) and (not node_to_delete.is_red)
        parent = node_to_delete.parent

        if substitute_node is None:
            if node_to_delete == self.root:
                self.root = None
            else:
                if both_black:
                    self.fix_black_black(node_to_delete)

                if parent.left_child == node_to_delete:
                    parent.left_child = None
                else:
                    parent.right_child = None

            del node_to_delete
            return

        if node_to_delete.left_child is None or node_to_delete.right_child is None:
            if node_to_delete == self.root:
                node_to_delete.key = substitute_node.value
                node_to_delete.value = substitute_node.value
                node_to_delete.left_child = node_to_delete.right_child = None
                del substitute_node
            else:
                if node_to_delete.parent.left_child == node_to_delete:
                    node_to_delete.parent.left_child = substitute_node
                else:
                    node_to_delete.parent.right_child = substitute_node
                del node_to_delete

                substitute_node.parent = parent

                if both_black:
                    self.fix_black_black(substitute_node)
                else:
                    substitute_node.is_red = False
            return

        substitute_node.key, substitute_node.value, node_to_delete.key, node_to_delete.value \
            = node_to_delete.key, node_to_delete.value, substitute_node.key, substitute_node.value
        self.delete_node(substitute_node)

    def fix_black_black(self, node: RbtNode):
        if node == self.root:
            return

        sibling = sibling_node(node)
        parent = node.parent

        if sibling is None:
            self.fix_black_black(parent)
        else:
            if sibling.is_red:
                parent.is_red = True
                sibling.is_red = False

                if sibling.parent.left_child == sibling:
                    self.rotate_right(parent)
                else:
                    self.rotate_left(parent)

                self.fix_black_black(node)
            else:
                if (sibling.left_child is not None and sibling.left_child.is_red) \
                            or (sibling.right_child is not None and sibling.right_child.is_red):
                    if sibling.left_child is not None and sibling.left_child.is_red:
                        if sibling.parent.left_child == sibling:
                            sibling.left_child.is_red = sibling.is_red
                            sibling.is_red = parent.is_red
                            self.rotate_right(parent)
                        else:
                            sibling.left_child.is_red = parent.is_red
                            self.rotate_right(sibling)
                            self.rotate_left(parent)
                    else:
                        if sibling.parent.left_child == sibling:
                            sibling.right_child.is_red = parent.is_red
                            self.rotate_left(sibling)
                            self.rotate_right(parent)
                        else:
                            sibling.right_child.is_red = sibling.is_red
                            sibling.is_red = parent.is_red
                            self.rotate_left(parent)
                    parent.is_red = False
                else:
                    sibling.is_red = True
                    if not parent.is_red:
                        self.fix_black_black(parent)
                    else:
                        parent.is_red = False
