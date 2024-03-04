from agent import agent
from alpha_beta import alphabeta_max_h


class AdverseAgent(agent):
    def __init__(self, x, y, id, node=None):
        super().__init__(x, y)
        self.node = node
        self.id = id

    def act(self, init_graph):
        move = alphabeta_max_h(init_graph, self.id)
        init_graph.move_agent(self.id, move)