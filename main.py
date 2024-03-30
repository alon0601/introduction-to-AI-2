from typing import Tuple, List

from alpha_beta import alphabeta_max_h
from maximax import maximax_decision
from package_graph import package_graph
from SemiCoop import max_h_coop


if __name__ == "__main__":
    max_turns = 10
    # Initialize the package graph
    init_file_path = "test"  # Provide the path to your initialization file
    print("Maximax decision")
    strategy = maximax_decision

    graph = package_graph(init_file_path, strategy)

    max_delivery_time = max([p.d_time for p in graph.graph_state['P']])
    num_of_packages = len(graph.graph_state['P'])

    while graph.graph_state['P'] and graph.graph_state['T'] < max_delivery_time + 1 and max_turns > 0:
        for agent in graph.graph_state['Agents'].values():
            agent.act(graph)
        graph.graph_state['T'] += 1
        max_turns -= 1
        print("graph state after ", graph.graph_state['T'])
        graph.visualize_state()
    if graph.packages_left() == 0:
        print("all packages delivered.")
    else:
        print(f"{graph.packages_left()} packages were not delivered")
    print("########################")
    print("Aplpha beta decision")
    strategy = alphabeta_max_h
    graph = package_graph(init_file_path, strategy)

    max_delivery_time = max([p.d_time for p in graph.graph_state['P']])
    num_of_packages = len(graph.graph_state['P'])
    max_turns = 10
    while graph.graph_state['P'] and graph.graph_state['T'] < max_delivery_time + 1 and max_turns > 0:
        for agent in graph.graph_state['Agents'].values():
            agent.act(graph)
        graph.graph_state['T'] += 1
        max_turns -= 1
        print("graph state after ", graph.graph_state['T'])
        graph.visualize_state()
    if graph.packages_left() == 0:
        print("all packages delivered.")
    else:
        print(f"{graph.packages_left()} packages were not delivered")

    # Specify the game type (adversarial, semi-cooperative, fully-cooperative)
    print("########################")
    print("Coop decision")
    strategy = max_h_coop
    graph = package_graph(init_file_path, strategy)
    max_turns = 10
    max_delivery_time = max([p.d_time for p in graph.graph_state['P']])
    num_of_packages = len(graph.graph_state['P'])

    while graph.graph_state['P'] and graph.graph_state['T'] < max_delivery_time + 1 and max_turns > 0:
        for agent in graph.graph_state['Agents'].values():
            agent.act(graph)
        graph.graph_state['T'] += 1
        max_turns -= 1
        print("graph state after ", graph.graph_state['T'])
        graph.visualize_state()
    if graph.packages_left() == 0:
        print("all packages delivered.")
    else:
        print(f"{graph.packages_left()} packages were not delivered")
