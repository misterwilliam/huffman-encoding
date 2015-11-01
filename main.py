# Python 3

import heapq


class Node:

    def __init__(self,
                 left=None,    # Character
                 right=None):  # Character
        if left:
            self.left = left
        if right:
            self.right = right

    def __str__(self):
        left = str(self.left.node) if self.left.node else self.left.symbol
        right = str(self.right.node) if self.right.node else self.right.symbol
        return "(" + left + ", " + right + ")"


class Character:

    def __init__(self, symbol, score, node):
        self.symbol = symbol
        self.score = score
        self.node = node


def makeTree(characters):
    heap = [(character.score, character) for character in characters]
    heapq.heapify(heap)
    if len(characters) == 0:
        raise Exception

    return makeTreeHelper(heap)


def makeTreeHelper(heap):
    # |heap| List<(number, Character)>
    if len(heap) == 1:
        return Node(left=heapq.heappop(heap)[1])
    elif len(heap) == 2:
        return Node(heapq.heappop(heap)[1], heapq.heappop(heap)[1])
    else:
        metaCharacter = makeMetaCharacter(heapq.heappop(heap)[1], heapq.heappop(heap)[1])
        heapq.heappush(heap, (metaCharacter.score, metaCharacter))
        return makeTreeHelper(heap)


def makeMetaCharacter(left,    # Character
                      right):  # Character
    return Character(left.symbol + right.symbol,
                     left.score + right.score,
                     Node(left=left, right=right))


data = [
    ('a', 0.32),
    ('b', 0.25),
    ('c', 0.20),
    ('d', 0.18),
    ('e', 0.05)
]

characters = [Character(symbol, score, None) for symbol, score in data]

tree = makeTree(characters)
print(tree)
