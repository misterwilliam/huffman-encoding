# Python 3

import heapq

from typing import Any, List, Tuple


class Node:

    def __init__(self, left: "Node"=None, right: "Node"=None, data: Any=None):
        self.left = left if left else None
        self.right = right if right else None
        self.data = data if data else None

    def hasChildren(self):
        return self.left is not None or self.right is not None

    def __str__(self):
        if self.hasChildren():
            left = str(self.left)
            right = str(self.right)
            return "(" + left + ", " + right + ")"
        else:
            return str(self.data)


class Character:

    def __init__(self, symbol, score):
        self.symbol = symbol
        self.score = score

    def __str__(self):
        return self.symbol

    @staticmethod
    def MakeMetaCharacter(left: "Character", right: "Character"):
        return Character(left.symbol + right.symbol, left.score + right.score)


def MakeTree(characters: List[Character]):
    heap = [
        (character.score, character, Node(data=character)) for character in characters
    ]
    heapq.heapify(heap)
    if len(characters) == 0:
        raise Exception
    return _makeTreeHelper(heap)


def _makeTreeHelper(heap: List[Tuple[float, Character, Node]]):
    if len(heap) == 1:
        return Node(left=heapq.heappop(heap)[2])
    elif len(heap) == 2:
        return Node(heapq.heappop(heap)[2], heapq.heappop(heap)[2])
    else:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        metaCharacter = Character.MakeMetaCharacter(left[1], right[1])
        heapq.heappush(heap,
                       (metaCharacter.score,
                        metaCharacter,
                        Node(left=left[2], right=right[2], data=metaCharacter)))
        return _makeTreeHelper(heap)


def Encode(message: str, tree: Node):
    return "".join(EncodeCharFancy(char, tree) for char in message)


def EncodeChar(char, tree) -> str:
    encoding = []
    if char in tree.left.data.symbol:
        encoding.append("0")
        left = tree.left
        if left.hasChildren():
            encoding.append(EncodeChar(char, left))
    else:
        encoding.append("1")
        right = tree.right
        if right.hasChildren():
            encoding.append(EncodeChar(char, right))
    return "".join(encoding)


def EncodeCharFancy(char, tree) -> str:
    # Equivalent to EncodeChar, but this does it by using a generic TreeTraverse function
    # call
    def onNode(tree, char):
        if not tree.hasChildren():
            return "stop"
        return "left" if char in tree.left.data.symbol else "right"
    path = TreeTraverse(tree, char, onNode)
    encoding = []
    for direction in path:
        encoding.append("0" if direction == "left" else "1")
    return "".join(encoding)


def TreeTraverse(tree, context, onNode) -> List[str]:
    direction = onNode(tree, context)
    if direction == "stop":
        return []
    elif direction == "left":
        return ["left"] + TreeTraverse(tree.left, context, onNode)
    else:
        return ["right"] + TreeTraverse(tree.right, context, onNode)


def Decode(message: str, tree: Node) -> str:
    def onNode(tree, context):
        if not tree.hasChildren():
            context["decoding"].append(tree.data.symbol)
            return "stop"
        char = context["message"].pop(0)
        if char == "0":
            return "left"
        else:
            return "right"
    decoding = []
    message = [c for c in message]
    while message:
        TreeTraverse(tree, {"decoding": decoding, "message": message}, onNode)
    return "".join(decoding)


data = [
    ('a', 0.32),
    ('b', 0.25),
    ('c', 0.20),
    ('d', 0.18),
    ('e', 0.05)
]

characters = [Character(symbol, score) for symbol, score in data]

tree = MakeTree(characters)
print("Tree:", tree)
print("Tree correct?", str(tree) == "((c, (e, d)), (b, a))")

message = "abcde"
print("Message:", message)
encoding = Encode(message, tree)
print("Encoding:", encoding)
print("Encoding correct?", encoding == "111000011010")
decoding = Decode(encoding, tree)
print("Decoding:", decoding)
print("Decoding correct?", decoding == message)
