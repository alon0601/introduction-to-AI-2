def heuristic(graph_sta, player):
    number_of_packages_sent = len(list(map(lambda p: p.delivered, player.packages)))
    number_of_packages_picked = len(player.packages) - number_of_packages_sent
    number_of_packages_not_picked = len(list(map(lambda p: not p.picked, graph_sta.graph_state['P'])))
    return 0.25 * number_of_packages_not_picked + 0.5 * number_of_packages_picked + number_of_packages_sent
