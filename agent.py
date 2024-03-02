from heuristics import heuristic
class agent():
    def __init__(self, x, y, strategy, node=None):
        self.X = x
        self.Y = y
        self.Score = 0
        self.strategy = strategy
        self.packages = list()
        self.node = node

    def act(self, init_graph):
        return self.strategy(init_graph, heuristic)

    def __repr__(self):
        return "x :" + str(self.X) + ", y :" + str(self.Y) + ", score :" + str(self.Score) + "\n" + str(self.packages)

    def __eq__(self, other):
        return (
                self.X == other.X
                and self.Y == other.Y
                and self.packages == other.packages
        )
