from agent import agent
from alpha_beta import alphabeta_max_h


class AdverseAgent(agent):
    def __init__(self, x, y, node=None):
        super().__init__(x, y)
        self.node = node

    def act(self, init_graph):
        alphabeta_max_h()
        self.move_request = (self.X, self.Y - 1)
