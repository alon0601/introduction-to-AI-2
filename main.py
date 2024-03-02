from typing import Tuple, List

from alpha_beta import alphabeta_max_h, alphabeta_min_h
from heuristics import heuristic
from edge import edge
from package_graph import package_graph


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

