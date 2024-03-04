from agent import agent
from maximax import maximax_decision


class FullAgent(agent):
    def __init__(self, x, y, id, node=None):
        super().__init__(x, y)
        self.node = node
        self.id = id

    def act(self, init_graph):
        move = maximax_decision(init_graph, self.id)
        init_graph.move_agent(self.id, move)