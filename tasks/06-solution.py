""" Day 6

    - object can orbit only one object
    - COM orbits nothing

"""

from copy import deepcopy
import common

TEST_INPUT = ["COM)B",
              "B)C",
              "C)D",
              "D)E",
              "E)F",
              "B)G",
              "G)H",
              "D)I",
              "E)J",
              "J)K",
              "K)L"]

TEST2_INPUT = ["COM)B",
               "B)C",
               "C)D",
               "D)E",
               "E)F",
               "B)G",
               "G)H",
               "D)I",
               "E)J",
               "J)K",
               "K)L",
               "K)YOU",
               "I)SAN"]
               
PUZZ_INPUT = common.listify_input_file("06-input.txt")

class Node(object):
    
    def __init__(self, data):
        self.data = data
        self.children = []

    def __repr__(self):
        return "<Node " + self.data + " children: " + str(len(self.children)) + ">"


def make_paths(pairs):

    nodes = {}
    children = set()

    for pair in pairs:
        parent, child = pair.split(")")
        if parent not in nodes:
            nodes[parent] = Node(parent)
        if child not in nodes:
            nodes[child] = Node(child)
        nodes[parent].children.append(nodes[child])
        children.add(child)

    return nodes, children


def get_root(parents, children):
    """ The root should always be 'COM' """

    for parent in parents:
        if parent not in children:
            return parent
    
    return "error"


# preorder printing:
def print_preorder(root):
    if root:
        print(root)
        for child in root.children:
            print_preorder(child)


# find all paths from root
def get_all_paths(nodes, root):
    """Generate the maximal cycle-free paths in graph starting at v (root).
    Graph must be a mapping from vertices to collections of neighbouring vertices.

    Modified from https://codereview.stackexchange.com/a/56423

    >>> nodes, children = make_paths(TEST_INPUT)
    >>> root = get_root(nodes, children)
    >>> sorted(get_all_paths(nodes, root))
    [['COM', 'B', 'C', 'D', 'E', 'F'],
     ['COM', 'B', 'C', 'D', 'E', 'J', 'K', 'L'],
     ['COM', 'B', 'C', 'D', 'I'],
     ['COM', 'B', 'G', 'H']]

    """

    path = [root]                  # path traversed so far
    seen = {root}                  # set of nodes in path
    def traverse():
        dead_end = True
        for child in nodes[path[-1]].children:
            if child.data not in seen:
                dead_end = False
                seen.add(child.data)
                path.append(child.data)
                yield from traverse()
                path.pop()
                seen.remove(child.data)
        if dead_end:
            yield list(path)
    yield from traverse()


def get_all_hops(nodes, root):
    """Generates all paths from root to each node.

    Arguments:
        nodes {dict} -- Nodes in graph; keys: data, vals: node
        root {string} -- String of node.data, must be valid key in nodes

    >>> nodes, children = make_paths(TEST_INPUT)
    >>> root = get_root(nodes, children)
    >>> sorted(get_all_hops(nodes, root))
    [['COM'],
     ['COM', 'B'],
     ['COM', 'B', 'C'],
     ['COM', 'B', 'C', 'D'],
     ['COM', 'B', 'C', 'D', 'E'],
     ['COM', 'B', 'C', 'D', 'E', 'F'],
     ['COM', 'B', 'C', 'D', 'E', 'J'],
     ['COM', 'B', 'C', 'D', 'E', 'J', 'K'],
     ['COM', 'B', 'C', 'D', 'E', 'J', 'K', 'L'],
     ['COM', 'B', 'C', 'D', 'I'],
     ['COM', 'B', 'G'],
     ['COM', 'B', 'G', 'H']]

    """

    path = [root]                  # path traversed so far
    def traverse():
        for child in nodes[path[-1]].children:
            path.append(child.data)
            yield from traverse()
            path.pop()
        yield list(path)
    yield from traverse()


def count_hops(paths):
    """Count total hops in all paths from root to each node.

    Arguments:
        paths {list} -- List of paths, where each path is a list of nodes

    Returns:
        int -- number of total hops
    """
    return sum(map(len, paths)) - len(paths)






##########
if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)

    # Test input
    nodes, children = make_paths(TEST_INPUT)
    root = get_root(nodes, children)
    paths = sorted(get_all_hops(nodes, root))
    hops = count_hops(paths)
    print("Test (expected 42):", hops)

    # Part 1
    nodes, children = make_paths(PUZZ_INPUT)
    root = get_root(nodes, children)
    paths = sorted(get_all_hops(nodes, root))
    hops = count_hops(paths)
    print("Part 1:", hops)

    # Part 2
    paths = sorted(get_all_paths(nodes, root))
    for path in paths:
        if path[-1] == 'YOU':
            you = path
        elif path[-1] == 'SAN':
            san = path

    # by looking, common node is 'BX1'
    for i, code in enumerate(you):
        if code == 'BX1':
            you_i = i
    for i, code in enumerate(san):
        if code == 'BX1':
            san_i = i

    you_to_san = (len(you) - 2 - you_i) + (len(san) - 2 - san_i)
    print("Part 2:", you_to_san)
