import itertools
import math
import networkx as nx

class GCodeParser:
    def __init__(self, gcode_filename):
        self.gcode_filename = gcode_filename
        self.z_commands = set()
        self.travel_height = None
        self.travel_points = []
        self.unique_travel_points = []

    def extract_unique_z_commands(self):
        with open(self.gcode_filename, 'r') as file:
            for line in file:
                line = line.strip()  # Remove any leading/trailing whitespace
                if line.startswith('Z') or ' Z' in line:
                    self._process_z_command(line)
                elif line.startswith('G00') or ' G00' in line:
                    self._process_g00_command(line)
        
        sorted_z_commands = sorted(self.z_commands)
        if sorted_z_commands:
            self.travel_height = max(sorted_z_commands)
        
        self.unique_travel_points = list(set(self.travel_points))
        return sorted_z_commands

    def _process_z_command(self, line):
        words = line.split()
        for word in words:
            if word.startswith('Z'):
                try:
                    z_value = float(word[1:])
                    self.z_commands.add(z_value)
                except ValueError:
                    pass  # Ignore if there's an issue with the value

    def _process_g00_command(self, line):
        x_value, y_value = None, None
        words = line.split()
        for word in words:
            if word.startswith('X'):
                try:
                    x_value = float(word[1:])
                except ValueError:
                    pass
            elif word.startswith('Y'):
                try:
                    y_value = float(word[1:])
                except ValueError:
                    pass
        
        if x_value is not None and y_value is not None:
            self.travel_points.append((x_value, y_value))

class PathOptimizer:
    def __init__(self, travel_points):
        self.travel_points = travel_points
        self.shortest_path = []

    def find_shortest_path(self):
        if not self.travel_points:
            return []

        G = nx.Graph()
        # Add nodes to the graph
        for idx, point in enumerate(self.travel_points):
            G.add_node(idx, pos=point)
        
        # Add edges with distances as weights
        for i, point1 in enumerate(self.travel_points):
            for j, point2 in enumerate(self.travel_points):
                if i != j:
                    distance = self.calculate_distance(point1, point2)
                    G.add_edge(i, j, weight=distance)
        
        # Find the shortest path using NetworkX's shortest_path function
        tsp_path = nx.approximation.traveling_salesman_problem(G, weight='weight')
        self.shortest_path = [self.travel_points[node] for node in tsp_path]
        return self.shortest_path

    def calculate_distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Example usage
gcode_filename = 'single-pass-test.ngc'  # Change this to your G-code file path
gcode_parser = GCodeParser(gcode_filename)
unique_z_commands = gcode_parser.extract_unique_z_commands()
print(f"unique Z heights: {unique_z_commands}")
print(f"Travel Height: {gcode_parser.travel_height}")
print(f"Travel Points: {gcode_parser.travel_points}")
print(f"Unique Travel Points: {gcode_parser.unique_travel_points}")
print(f"Total Travel Points: {len(gcode_parser.travel_points)}")

# Optimize travel path
path_optimizer = PathOptimizer(gcode_parser.travel_points)
shortest_path = path_optimizer.find_shortest_path()
print(f"Shortest Path: {shortest_path}")
