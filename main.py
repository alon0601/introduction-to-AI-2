from typing import Tuple, List

from alpha_beta import alphabeta_max_h
from heuristics import heuristic
from edge import edge
from maximax import maximax_decision
from package_graph import package_graph
from SemiCoop import max_h_coop

if __name__ == "__main__":
    # Initialize the package graph
    init_file_path = "test"  # Provide the path to your initialization file
    # game_type = "adversarial"  # Change this to the desired game type
    # game_type = "fully-cooperative"
    game_type = "semi cooperative"
    if game_type == "fully-cooperative":
        strategy = maximax_decision
    elif game_type == "adversarial":
        strategy = alphabeta_max_h
    elif game_type == "semi cooperative":
        strategy = max_h_coop
    graph = package_graph(init_file_path, strategy)

    max_delivery_time = max([p.d_time for p in graph.graph_state['P']])
    num_of_packages = len(graph.graph_state['P'])

    while graph.graph_state['P'] and graph.graph_state['T'] < max_delivery_time+1:
        for agent in graph.graph_state['Agents'].values():
            agent.act(graph)
        graph.graph_state['T'] += 1
        print("graph state after ", graph.graph_state['T'])
        graph.visualize_state()
    if graph.packages_left() == 0:
        print("all packages delivered.")
    else:
        print(f"{graph.packages_left()} packages were not delivered")

    # Specify the game type (adversarial, semi-cooperative, fully-cooperative)

