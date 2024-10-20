import tkinter as tk
from tkinter import ttk, messagebox
from Dijkstra import dijkstra  # Importiere den Algorithmus
import networkx as nx
import matplotlib.pyplot as plt

# Beispielgraph für die GUI
graph = {
    'A': [('B', 7), ('C', 9), ('F', 14)],
    'B': [('A', 7), ('C', 10), ('D', 15)],
    'C': [('A', 9), ('B', 10), ('D', 11), ('F', 2)],
    'D': [('B', 15), ('C', 11), ('E', 6)],
    'E': [('D', 6), ('F', 9)],
    'F': [('A', 14), ('C', 2), ('E', 9)]
}

nodes = list(graph.keys())  # Liste der Knoten für Dropdowns

def get_proportional_layout(G):
    """Erstellt ein Layout, bei dem die Kanten proportional zu ihren Gewichten dargestellt werden."""
    pos = nx.spring_layout(G, weight='weight', iterations=100)

    # Skalieren der Positionen zur besseren Darstellung
    for key, (x, y) in pos.items():
        pos[key] = (x * 10, y * 10)  # Skaliere die Koordinaten
    return pos

def clear_figure():
    """Löscht die aktuelle Matplotlib-Figur."""
    plt.clf()  # Löscht die aktuelle Figur
    plt.close()  # Schließt das Fenster, falls es offen ist

def draw_graph(path):
    """Visualisiere den Graphen und markiere den Pfad proportional zu den Kantenlängen."""
    clear_figure()  # Stelle sicher, dass die alte Figur gelöscht wird

    G = nx.Graph()

    # Füge alle Kanten und Gewichte zum Graphen hinzu
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors:
            G.add_edge(node, neighbor, weight=weight)

    pos = get_proportional_layout(G)  # Hole das skalierte Layout

    # Zeichne den gesamten Graphen
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)})

    # Markiere die Kanten des kürzesten Pfades in Rot
    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=2.5)

    # Zeige den Graphen an
    plt.show()

def calculate_path():
    """Berechne den kürzesten Pfad und visualisiere ihn."""
    start = start_node.get()
    end = end_node.get()

    if start == end:
        messagebox.showinfo("Pfad", f"Start und Ziel sind identisch: {start}")
        return

    dist, path = dijkstra(graph, start, end)

    if dist == float('inf'):
        messagebox.showwarning("Kein Pfad", f"Es gibt keinen Pfad von {start} nach {end}.")
    else:
        result_label.config(text=f"Kürzester Pfad: {' -> '.join(path)}\nDistanz: {dist}")
        draw_graph(path)  # Visualisiere den Graphen mit dem Pfad

def clear_result():
    """Lösche das Ergebnislabel."""
    result_label.config(text="")
    clear_figure()  # Lösche die Figur bei Bedarf

# GUI-Hauptfenster erstellen
root = tk.Tk()
root.title("Dijkstra Algorithmus - Kürzester Pfad Finder")

# Layout-Frame
frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Dropdowns für Start- und Zielknoten
ttk.Label(frame, text="Startknoten:").grid(row=0, column=0, padx=5, pady=5)
start_node = ttk.Combobox(frame, values=nodes, state="readonly")
start_node.grid(row=0, column=1, padx=5, pady=5)
start_node.current(0)

ttk.Label(frame, text="Zielknoten:").grid(row=1, column=0, padx=5, pady=5)
end_node = ttk.Combobox(frame, values=nodes, state="readonly")
end_node.grid(row=1, column=1, padx=5, pady=5)
end_node.current(1)

# Button zum Berechnen des Pfades
calc_button = ttk.Button(frame, text="Berechne Pfad", command=calculate_path)
calc_button.grid(row=2, column=0, columnspan=2, pady=10)

# Button zum Löschen des Ergebnisses
clear_button = ttk.Button(frame, text="Löschen", command=clear_result)
clear_button.grid(row=3, column=0, columnspan=2, pady=5)

# Ergebnislabel
result_label = ttk.Label(frame, text="", relief="sunken", anchor="center")
result_label.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

# Fenstergröße anpassen und anzeigen
root.mainloop()
