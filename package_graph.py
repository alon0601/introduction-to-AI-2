import copy
from package import package
from edge import edge
import re
from AdverseAgent import AdverseAgent
from human_agent import human_agent


class package_graph():
    def __init__(self, init_file_path, game_type):
        self.first_player = None
        self.second_player = None
        self.graph_state = {}
        self.curr_player = None
        packages = list()
        blocked_edges = list()
        fragile_edges = list()
        agents = {}
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
            elif line[1] == 'A1':
                agents[1] = AdverseAgent(int(all_numbers_in_line[0]), int(all_numbers_in_line[1]), 1)
                # self.curr_player = agents[line[1]]
                # self.first_player = agents[line[1]]
            elif line[1] == 'A2':
                agents[2] = AdverseAgent(int(all_numbers_in_line[0]), int(all_numbers_in_line[1]), 2)
                # self.second_player = agents[line[1]]
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

    def get_moves(self, id):
        successors = []
        possible_moves = ["R", "U", "D", "L"]
        for move in possible_moves:
            new_node = copy.deepcopy(self)
            first_player = self.graph_state['Agents'][id]
            second_player = self.graph_state['Agents'][3-id]
            x_1 = first_player.X
            y_1 = first_player.Y
            x_2 = second_player.X
            y_2 = second_player.Y
            next_move = None
            if move == 'R':
                next_move = edge(x_1 + 1, y_1, x_1, y_1)
                if x_1 + 1 >= new_node.graph_state['X'] or next_move in new_node.graph_state['B']:
                    continue
                if (x_1 + 1 == x_2) and (y_1 == y_2):
                    continue
                new_node.graph_state['Agents'][id].X += 1
            if move == 'L':
                next_move = edge(x_1 - 1, y_1, x_1, y_1)
                if x_1 - 1 < 0 or next_move in new_node.graph_state['B']:
                    continue
                if (x_1 - 1 == x_2) and (y_1 == y_2):
                    continue
                new_node.graph_state['Agents'][id].X -= 1
            if move == 'U':
                next_move = edge(x_1, y_1 + 1, x_1, y_1)
                if y_1 + 1 >= new_node.graph_state['Y'] or next_move in new_node.graph_state['B']:
                    continue
                if (x_1 == x_2) and (y_1 + 1 == y_2):
                    continue
                new_node.graph_state['Agents'][id].Y += 1
            if move == 'D':
                next_move = edge(x_1, y_1 - 1, x_1, y_1)
                if y_1 - 1 < 0 or next_move in new_node.graph_state['B']:
                    continue
                if (x_1 == x_2) and (y_1 - 1 == y_2):
                    continue
                new_node.graph_state['Agents'][id].Y -= 1
            if next_move in new_node.graph_state['F']:
                new_node.graph_state['F'].remove(next_move)
                new_node.graph_state['B'].append(next_move)
            new_node.graph_state['T'] += 1  # important: this is only half a move, consider the time
            new_node.pick_up_package()
            successors.append((new_node, move))
        return successors

    def move_agent(self, id, move):
        # check if agent can move there and move him
        blocked_edges = self.graph_state['B']
        fragile_edges = self.graph_state['F']
        new_x = self.graph_state['Agents'][id].X
        new_y = self.graph_state['Agents'][id].Y
        if move == 'D':
            new_y -= 1
        elif move == 'U':
            new_y += 1
        elif move == 'R':
            new_x += 1
        elif move == 'L':
            new_x -= 1
        else:
            return False
        edge_to_move = edge(self.graph_state['Agents'][id].X, self.graph_state['Agents'][id].Y, new_x, new_y)
        for a_id, agent in self.graph_state['Agents'].items():
            if a_id != id and agent.X == new_x and agent.Y == new_y:
                return False
        if edge_to_move in blocked_edges:
            return False
        self.graph_state['Agents'][id].X = new_x
        self.graph_state['Agents'][id].Y = new_y
        if edge_to_move in fragile_edges:
            print("a fragile edge was traversed")
            fragile_edges.remove(edge_to_move)
            blocked_edges.append(edge_to_move)
        self.pick_up_package()
        return True

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

    def visualize_state(self):
        # Initialize an empty grid with dashes
        grid = [['-' for _ in range(self.graph_state['X'] + 1)] for _ in range(self.graph_state['Y'] + 1)]

        # Add blocked edges to the grid
        for e in self.graph_state['B']:
            for point in e.points:
                x, y = point
                if grid[y][x] == '-':  # Only mark if not already marked by a package or agent
                    grid[y][x] = 'B'

        # Add fragile edges to the grid
        for e in self.graph_state['F']:
            for point in e.points:
                x, y = point
                if grid[y][x] == '-':  # Only mark if not already marked by a package or agent
                    grid[y][x] = 'F'

        # Add packages to the grid
        for package in self.graph_state['P']:
            if not package.picked:
                grid[package.p_y][package.p_x] = 'P'

        # Add agents to the grid
        for age, age_value in self.graph_state['Agents'].items():
            grid[age_value.Y][age_value.X] = age

        grid.reverse()

        # Print the grid
        for row in grid:
            print(' '.join(row))

