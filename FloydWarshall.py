import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def draw_graph(graph, shortest_paths):
    # Create a new directed graph
    result_graph = nx.DiGraph()

    # Add nodes to the graph with labels
    for node in graph:
        result_graph.add_node(node, label=node_labels[node])

    # Add edges to the graph with weights
    for source in graph:
        for target, weight in graph[source]:
            result_graph.add_edge(source, target, weight=weight)

    # Define the layout for the graph
    pos = nx.spring_layout(result_graph)

    # Create a new Tkinter window
    window = tk.Tk()
    window.title("Shortest Paths")

    # Create a new matplotlib figure and axis
    figure = plt.Figure(figsize=(6, 6), dpi=100)
    axis = figure.add_subplot(111)

    # Draw the graph nodes
    nx.draw_networkx_nodes(result_graph, pos, ax=axis, node_color="lightblue", node_size=500)

    # Draw the graph edges
    nx.draw_networkx_edges(result_graph, pos, ax=axis, arrows=True)

    # Draw the node labels
    nx.draw_networkx_labels(result_graph, pos, labels=node_labels, font_size=10, font_weight="bold", ax=axis)

    # Draw the edge weights
    edge_labels = {(source, target): weight for source, target, weight in result_graph.edges.data('weight')}
    nx.draw_networkx_edge_labels(result_graph, pos, edge_labels=edge_labels, font_size=8, ax=axis)

    # Display the graph in the Tkinter window
    canvas = FigureCanvasTkAgg(figure, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Display the shortest paths
    shortest_paths_text = "Shortest Paths:\n"
    for source in shortest_paths:
        for target in shortest_paths[source]:
            if shortest_paths[source][target] != np.inf:
                shortest_paths_text += "From {} to {}: {}\n".format(node_labels[source], node_labels[target], shortest_paths[source][target])

    # Create a new Tkinter label to display the shortest paths
    shortest_paths_label = tk.Label(window, text=shortest_paths_text)
    shortest_paths_label.pack()

    # Run the Tkinter event loop
    window.mainloop()

# Define an empty graph
graph = {}

# Get the number of nodes and edges from the user
num_nodes = int(input("Enter the number of nodes: "))
num_edges = int(input("Enter the number of edges: "))

# Add nodes to the graph
node_labels = {}
for i in range(num_nodes):
    label = input("Enter the label for node {}: ".format(i+1))
    graph[i+1] = []
    node_labels[i+1] = label

# Add edges to the graph
for i in range(num_edges):
    source = int(input("Enter the source node for edge {}: ".format(i+1)))
    target = int(input("Enter the target node for edge {}: ".format(i+1)))
    weight = float(input("Enter the weight for edge {}: ".format(i+1)))
    graph[source].append((target, weight))

# Run floyd algorithm to find shortest paths
n = len(graph)
all_pairs_shortest_paths = np.inf * np.ones((n, n))
for source in graph:
    all_pairs_shortest_paths[source-1, source-1] = 0
    for target, weight in graph[source]:
        all_pairs_shortest_paths[source-1, target-1] = weight

for k in range(n):
    for i in range(n):
        for j in range(n):
            if all_pairs_shortest_paths[i, j] > all_pairs_shortest_paths[i, k] + all_pairs_shortest_paths[k, j]:
                all_pairs_shortest_paths[i, j] = all_pairs_shortest_paths[i, k] + all_pairs_shortest_paths[k, j]

# Create a dictionary to store the shortest paths
shortest_paths = {}
for source in graph:
    shortest_paths[source] = {}
    for target in graph:
        shortest_paths[source][target] = all_pairs_shortest_paths[source-1, target-1]

# Display the graph and shortest paths
draw_graph(graph, shortest_paths)
