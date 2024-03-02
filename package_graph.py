import copy
from game_agent import agent
from package import package
from edge import edge
import alpha_beta
import re


class package_graph():
    def __init__(self, init_file_path):
        self.first_player = None
        self.second_player = None
        self.graph_state = {}
        self.curr_player = None
        packages = list()
        blocked_edges = list()
        fragile_edges = list()
        agents = {}
        strategy = alpha_beta.alphabeta_max_h
        init_file = open(init_file_path, mode='r', encoding='utf-8-sig')
        init_file_lines = init_file.readlines()
        for line in init_file_lines:
            all_numbers_in_line = re.findall(r'-?\b\d+\b', line)
            if line[1] == 'X':
                self.graph_state['X'] = int(all_numbers_in_line[0])
            elif line[1] == 'Y':
                self.graph_state['Y'] = int(all_numbers_in_line[0])
            elif line[1] == 'P':
                packages.append(
                    package(int(all_numbers_in_line[0]), int(all_numbers_in_line[1]), int(all_numbers_in_line[2]),
                            int(all_numbers_in_line[3]), int(all_numbers_in_line[4]), int(all_numbers_in_line[5])))
            elif line[1] == 'B':
                blocked_edges.append(
                    edge(int(all_numbers_in_line[0]), int(all_numbers_in_line[1]), int(all_numbers_in_line[2]),
                         int(all_numbers_in_line[3])))
            elif line[1] == 'F':
                fragile_edges.append(
                    edge(int(all_numbers_in_line[0]), int(all_numbers_in_line[1]), int(all_numbers_in_line[2]),
                         int(all_numbers_in_line[3])))
            elif line[1] == 'H':
                agents[line[1]] = human_agent(int(all_numbers_in_line[0]), int(all_numbers_in_line[1]))
            elif line[1] == 'A':
                agents[line[1]] = agent(int(all_numbers_in_line[0]), int(all_numbers_in_line[1]), strategy)
                self.curr_player = agents[line[1]]
                self.first_player = agents[line[1]]
            elif line[1] == 'C':
                agents[line[1]] = agent(int(all_numbers_in_line[0]), int(all_numbers_in_line[1]), strategy)
                self.second_player = agents[line[1]]
        self.graph_state['P'] = packages
        self.graph_state['B'] = blocked_edges
        self.graph_state['F'] = fragile_edges
        self.graph_state['Agents'] = agents
        self.graph_state['T'] = 0

    # I moved pick_up_package to here to use it in the search tree
    def pick_up_package(self):
        packages = self.graph_state['P']
        packages_that_delivered = set()
        for age, age_value in self.graph_state['Agents'].items():
            for package in packages:
                if not package.picked and age_value.X == package.p_x and age_value.Y == package.p_y and self.graph_state['T'] >= package.p_time:
                    package.picked = True
                    age_value.packages.append(package)
                elif package.picked and package in age_value.packages and age_value.X == package.d_x and age_value.Y == package.d_y and self.graph_state['T'] <= package.d_time:
                    packages_that_delivered.add(package)
                    age_value.Score += 1
                    package.delivered = True

        self.graph_state['P'] = [package for package in packages if package not in packages_that_delivered]

    def get_moves(self, node):
        successors = []
        possible_moves = ["R", "U", "D", "L"]
        for move in possible_moves:
            new_node = copy.deepcopy(node)
            current_x = self.curr_player.X
            current_y = self.curr_player.Y
            next_move = None
            if move == 'R':
                next_move = edge(current_x + 1, current_y, current_x, current_y)
                if current_x + 1 >= new_node.graph_state['X'] or next_move in new_node.graph_state['B']:
                    continue
                if (self.curr_player == self.first_player and self.second_player.X == current_x + 1 and self.second_player.Y == self.curr_player.Y) or (self.curr_player == self.second_player and self.first_player.X == current_x + 1 and self.first_player.Y == self.curr_player.Y) :
                    continue
                new_node.curr_player.X += 1
            if move == 'L':
                next_move = edge(current_x - 1, current_y, current_x, current_y)
                if current_x - 1 < 0 or next_move in new_node.graph_state['B']:
                    continue
                if (self.curr_player == self.first_player and self.second_player.X == current_x - 1 and self.second_player.Y == self.curr_player.Y) or (self.curr_player == self.second_player and self.first_player.X == current_x - 1 and self.first_player.Y == self.curr_player.Y) :
                    continue
                new_node.curr_player.X -= 1
            if move == 'U':
                next_move = edge(current_x, current_y + 1, current_x, current_y)
                if current_y + 1 >= new_node.graph_state['Y'] or next_move in new_node.graph_state['B']:
                    continue
                if (self.curr_player == self.first_player and self.second_player.Y == current_y - 1 and self.second_player.X == self.curr_player.X) or (
                        self.curr_player == self.second_player and self.first_player.Y == current_y - 1 and self.first_player.X == self.curr_player.X):
                    continue
                new_node.curr_player.Y += 1
            if move == 'D':
                next_move = edge(current_x, current_y - 1, current_x, current_y)
                if current_y - 1 < 0 or next_move in new_node.graph_state['B']:
                    continue
                if (self.curr_player == self.first_player and self.second_player.Y == current_y + 1 and self.second_player.X == self.curr_player.X) or (
                        self.curr_player == self.second_player and self.first_player.Y == current_y + 1 and self.first_player.X == self.curr_player.X):
                    continue
                new_node.curr_player.Y -= 1
            if next_move in new_node.graph_state['F']:
                new_node.graph_state['F'].remove(next_move)
                new_node.graph_state['B'].append(next_move)
            new_node.prev = node
            new_node.graph_state['T'] += 1
            new_node.pick_up_package()
            successors.append(new_node)
        return successors

    def __repr__(self):
        graph_string = ""
        for key, value in self.graph_state.items():
            graph_string += key + ": " + str(value) + "\n"
        return graph_string

    def __eq__(self, other):
        return (
                self.graph_state['P'] == other.graph_state['P']
                and self.graph_state['B'] == other.graph_state['B']
                and self.graph_state['F'] == other.graph_state['F']
                and self.graph_state['Agents'] == other.graph_state['Agents']
        )

    def get_score(self):
        """
        :return: the current score of the game.
        value = 1000 points is just an arbitrary high number, you can change its value.
        This value is large enough so that the heuristic value will be between 1000 and -1000.
        """
        return self.curr_player.Score

    def is_terminal(self):
        return len(self.get_moves(self)) == 0

    def is_game_finished(self):
        return len(self.graph_state['P']) == 0

    def get_first_player(self):
        return self.first_player

    def get_second_player(self):
        return self.second_player
