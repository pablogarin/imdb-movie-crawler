from collections import deque


class Node(object):
    def __init__(self, char):
        self.char = char
        self.children = dict()
        self.is_word = False
        self.keys = set()


class Trie(object):
    def __init__(self):
        self.root = Node('*')

    def add(self, word, node=None):
        parent = node or self.root
        if len(word) == 0:
            if node is not None:
                node.is_word = True
                return node
            return None
        char = word[0]
        if char not in parent.children:
            parent.children[char] = Node(char)
        return self.add(word[1:], parent.children[char])

    def search(self, word, node=None):
        parent = node or self.root
        if len(word) == 0:
            return node.is_word, node
        char = word[0]
        if char not in parent.children:
            return False, None
        return self.search(word[1:], parent.children[char])

    def autocomplete_word(self, word, node):
        possible_matches = []
        stack = deque()
        if node.is_word:
            possible_matches.append((word, node))
        for char in node.children:
            stack.append((word, node.children[char]))
        while len(stack) > 0:
            partial_word, curr_node = stack.pop()
            curr_partial_word = partial_word+curr_node.char
            if curr_node.is_word:
                possible_matches.append((curr_partial_word, curr_node))
            for c in curr_node.children:
                stack.append((curr_partial_word, curr_node.children[c]))
        return possible_matches
