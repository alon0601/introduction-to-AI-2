class Node(object):
    def __init__(self, value, state, parent=None):
        self.children = []
        self.value = value
        self.parent = parent
        self.state = state
