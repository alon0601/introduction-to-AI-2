from agent import agent
from alpha_beta import alphabeta_max_h


class AdverseAgent(agent):
    def __init__(self, x, y, id, node=None):
        super().__init__(x, y)
        self.node = node
        self.id = id

    def act(self, init_graph):
        self.move_request = (self.X, self.Y)
        _, move = alphabeta_max_h(init_graph, self.id)
        if move == "U":
            self.move_request = (self.X, self.Y + 1)
        elif move == "D":
            self.move_request = (self.X, self.Y - 1)
        elif move == "R":
            self.move_request = (self.X + 1, self.Y)
        elif move == "L":
            self.move_request = (self.X - 1, self.Y - 1)
