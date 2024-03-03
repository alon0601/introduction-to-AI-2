def heuristic(graph_sta, player_id):
    packages = graph_sta.graph_state['Agents'][player_id].packages
    number_of_packages_delivered = len(list(filter(lambda p: p.delivered, packages)))
    number_of_packages_picked = len(packages) - number_of_packages_delivered
    number_of_packages_not_picked = len(list(filter(lambda p: not p.picked, graph_sta.graph_state['P'])))
    return 0.25 * number_of_packages_not_picked + 0.5 * number_of_packages_picked + number_of_packages_delivered
