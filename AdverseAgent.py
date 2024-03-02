from agent import agent


class AdverseAgent(agent):
    def __init__(self, x, y):
        super().__init__(x, y)

    def act(self, init_graph):
        self.move_request = (self.X, self.Y - 1)
