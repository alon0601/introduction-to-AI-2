from typing import Tuple, List

from alpha_beta import alphabeta_max_h, alphabeta_min_h
from heuristics import heuristic
from edge import edge
from package_graph import package_graph


class Agent:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.packages_delivered = 0

    def deliver_package(self):
        self.packages_delivered += 1


class Environment:
    def __init__(self, graph: package_graph, game_type: str):
        self.graph = graph
        self.game_type = game_type
        self.agents = {agent_id: Agent(agent_id) for agent_id in graph.graph_state['Agents']}

    def terminal_condition(self) -> bool:
        # Define terminal condition based on your game logic
        pass

    def apply_action_to_graph(self, action: Tuple[str, Tuple[int, int]], agent_id: str) -> None:
        # Apply the action to the graph
        # Move the agent to the new position
        x, y = action[1].graph_state['Agents'][agent_id].X, action[1].graph_state['Agents'][agent_id].Y
        self.graph.graph_state['Agents'][agent_id].X = x
        self.graph.graph_state['Agents'][agent_id].Y = y
        # Check if any package is picked up or delivered
        self.graph.pick_up_package()
        self.graph.curr_player = self.graph.graph_state['Agents'][list(filter(lambda x: x is not agent_id, list(self.graph.graph_state['Agents'].keys())))[0]]

    def simulate_game(self, depth: int = 0, max_terns=10) -> None:
        """
        Simulate the game based on the specified game type.
        """
        # Main simulation loop
        while not self.terminal_condition() and max_terns > 0:
            # Get actions for each agent
            for agent_id in self.graph.graph_state['Agents']:
                if self.game_type == 'adversarial':
                    action = self.adversarial_agent(agent_id)
                elif self.game_type == 'semi-cooperative':
                    action = self.semi_cooperative_agent(agent_id, depth)
                elif self.game_type == 'fully-cooperative':
                    action = self.fully_cooperative_agent(agent_id, depth)
                else:
                    raise ValueError("Invalid game type")
                # Apply action to the graph
                self.apply_action_to_graph(action, agent_id)
                # Update agent's package delivery count
                if action[0] == 'traverse':
                    self.agents[agent_id].deliver_package()
                # Display world status
                print(self.graph)

                # Check if terminal condition is reached
                if self.terminal_condition():
                    break
            max_terns -= 1

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


if __name__ == "__main__":
    # Initialize the package graph
    init_file_path = "test"  # Provide the path to your initialization file
    graph = package_graph(init_file_path)

    # Specify the game type (adversarial, semi-cooperative, fully-cooperative)
    game_type = "adversarial"  # Change this to the desired game type

    # Create the environment
    env = Environment(graph, game_type)

    # Simulate the game
    env.simulate_game()
