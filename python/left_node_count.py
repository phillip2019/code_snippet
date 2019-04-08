#!/usr/bin/python
# -*- coding: utf-8 -*-

class Node(object):
    def __init__(self, value):
        self.left = None
        self.value = value
        self.right = None

class Tree(object):

    def __init__(self, *args, **kwargs):
        self.root = None
        return super().__init__(*args, **kwargs)
    
    def add_left(self, p, value):
        if not self.root:
            p = Node(value)
            self.root = p
            return p
        n = Node(value)
        p.left = n
        return n
    
    def add_right(self, p, value):
        if not self.root:
            p = Node(value)
            self.root = p
            return p
        n = Node(value)
        p.right = n
        return n
    
    def print_tree(self, p, _elements):
        if not p:
            return
        self.print_tree(p.left, _elements)
        self.print_tree(p.right, _elements)
        _elements.append(p.value)
    
    def left_sum(self, p, left=False):
        if not p:
            return 0
        if not p.left and not p.right and left:
            return p.value
        return self.left_sum(p.left, left=True) + self.left_sum(p.right)

class Solution:
    def sumOfLeftLeaves(self, root: TreeNode) -> int:
        if not root:
          return 0
        # left is not None, but left has no children 
        if root.left is not None and root.left.left is None and root.left.right is None:
            left = root.left.val
        else:
            left = self.sumOfLeftLeaves(root.left)
        right = self.sumOfLeftLeaves(root.right)
        return left + right


if __name__ == "__main__":
    t = Tree()
    r = t.add_left(None, 3)
    # t.add_left(r, 9)
    s = t.add_right(r, 20)
    # t.add_left(s, 15)
    # t.add_right(s, 7)
    els = []
    t.print_tree(t.root, els)
    print(els)

    print(t.left_sum(t.root, left=True))