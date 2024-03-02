from typing import Tuple, List

from alpha_beta import alphabeta_max_h, alphabeta_min_h
from heuristics import heuristic
from edge import edge
from package_graph import package_graph

def deliver_package(self):
    self.packages_delivered += 1


def adversarial_agent(self, agent_id: str):
    """
    Adversarial agent that aims to maximize (p1 - p2).
    """
    if agent_id == 'A':
        return alphabeta_max_h(self.graph, heuristic)
    else:
        return alphabeta_min_h(self.graph, heuristic)

def semi_cooperative_agent(self, agent_id: str, depth: int) -> Tuple[str, Tuple[int, int]]:
    """
    Semi-cooperative agent that maximizes its own score, breaking ties cooperatively.
    """
    # Check if cutoff
    if self.is_cutoff(depth):
        return self.heuristic_evaluation()
    actions = self.get_actions(agent_id)
    max_p1 = max(actions, key=lambda x: x[1][0])[1][0]
    max_actions_p1 = [action for action in actions if action[1][0] == max_p1]
    return max(max_actions_p1, key=lambda x: x[1][1])

def fully_cooperative_agent(self, agent_id: str, depth: int) -> Tuple[str, Tuple[int, int]]:
    """
    Fully cooperative agent that aims to maximize the sum of individual scores.
    """
    # Check if cutoff
    if self.is_cutoff(depth):
        return self.heuristic_evaluation()
    actions = self.get_actions(agent_id)
    return max(actions, key=lambda x:x[1][0]  + x[1][1])

def is_cutoff(self, depth: int) -> bool:
    """
    Check if the cutoff condition is met based on the depth of the search.
    """
    max_depth = 5  # Maximum depth allowed for the search
    return depth >= max_depth

def get_actions(self, agent_id: str) -> List[Tuple[str, Tuple[int, int]]]:
    """
    Get possible actions for the agent.
    """
    actions = []
    x, y = self.graph.graph_state['Agents'][agent_id].X, self.graph.graph_state['Agents'][agent_id].Y
    neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    for nx, ny in neighbors:
        if 0 <= nx < self.graph.graph_state['X'] and 0 <= ny < self.graph.graph_state['Y'] and edge(x, y, nx, ny) not in self.graph.graph_state['B'] and not any(agent.X == nx and agent.Y == ny for agent in list(self.graph.graph_state['Agents'].values())):
            actions.append(('traverse', (nx, ny)))
    actions.append(('no-op', (x, y), self.graph))  # Adding no-op as a fallback action
    return actions


def move_agents():
    #  move all agents according to their move requests while checking for collisions
    #  turn fragile to broken
    blocked_edges = graph.graph_state['B']
    fragile_edges = graph.graph_state['F']
    does_move_succeeded = False
    for age, age_value in graph.graph_state['Agents'].items():
        if not age_value.move_request:
            continue
        other_agents = {key: value for key, value in graph.graph_state['Agents'].items() if key != age}
        others_locations = list(map(lambda ag: (ag.X, ag.Y), other_agents.values()))
        other_moves = list(map(lambda ag: ag.move_request, other_agents.values()))
        print(age_value.move_request)
        edge_to_move = edge(age_value.X, age_value.Y, age_value.move_request[0], age_value.move_request[1])
        if age_value.move_request not in others_locations or age_value.move_request not in other_moves:
            if not edge_to_move in blocked_edges:
                does_move_succeeded = True
        elif age_value.move_request in others_locations:
            agents_to_move = filter(lambda ag: (ag.X, ag.Y) == age_value.move_request, other_agents.values())
            for agent_to_move in agents_to_move:
                if agent_to_move.move_request != () and not edge_to_move in blocked_edges:
                    does_move_succeeded = True
        if does_move_succeeded:
            age_value.X = age_value.move_request[0]
            age_value.Y = age_value.move_request[1]
            age_value.move_request = ()
            if edge_to_move in fragile_edges:
                print("a fragile edge was traversed")
                fragile_edges.remove(edge_to_move)
                blocked_edges.append(edge_to_move)
        graph.pick_up_package()


if __name__ == "__main__":
    # Initialize the package graph
    init_file_path = "test"  # Provide the path to your initialization file
    game_type = "adversarial"  # Change this to the desired game type
    graph = package_graph(init_file_path, game_type)

    max_delivery_time = max([p.d_time for p in graph.graph_state['P']])
    while graph.graph_state['P'] and graph.graph_state['T'] < max_delivery_time+1:
        for agent in graph.graph_state['Agents'].values():
            agent.act(graph)
        move_agents()
        graph.graph_state['T'] += 1
        graph.visualize_state()

    # Specify the game type (adversarial, semi-cooperative, fully-cooperative)

