class RbtNode:

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.parent = None
        self.left_child = None
        self.right_child = None
        self.is_red = True


'''
key greater go to the right
smaller or equal go to the left
'''


class Rbt:
    def __init__(self):
        self.root = None

    def get(self, key):
        cur_node: RbtNode = self.root

        while cur_node is not None and cur_node.key != key:
            if key > cur_node.key:
                cur_node = cur_node.right_child
            else:
                cur_node = cur_node.left_child

        return cur_node

    def insert(self, key, value):  # regular BST insertion
        new_node = RbtNode(key=key, value=value)

        if self.root is None:
            new_node.is_red = False
            self.root = new_node
            return

        parent = self.root

        while parent is not None:
            if parent.key > new_node.key:
                if parent.right_child is None:
                    break

                parent = parent.right_child
            else:
                if parent.left_child is None:
                    break

                parent = parent.left_child

        new_node.parent = parent

        if parent.key > new_node.key:
            parent.right_child = new_node
        else:
            parent.left_child = new_node

        self.fix(new_node)

    def fix(self, new_node: RbtNode):
        return

    def delete(self, key):
        print('delete')


if __name__ == '__main__':
    print("hi")
