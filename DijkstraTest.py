import unittest
from Dijkstra import dijkstra  # Importiere den Algorithmus aus dijkstra.py
import sys

class TestDijkstraLargeGraphs(unittest.TestCase):
    def setUp(self):
        """Initialisiere Beispielgraphen für alle Tests."""
        # Graph 1: 6 Knoten
        self.graph1 = {
            'A': [('B', 7), ('C', 9), ('F', 14)],
            'B': [('A', 7), ('C', 10), ('D', 15)],
            'C': [('A', 9), ('B', 10), ('D', 11), ('F', 2)],
            'D': [('B', 15), ('C', 11), ('E', 6)],
            'E': [('D', 6), ('F', 9)],
            'F': [('A', 14), ('C', 2), ('E', 9)]
        }

        # Graph 2: 10 Knoten (komplexer)
        self.graph2 = {
            'A': [('B', 3), ('C', 1)],
            'B': [('A', 3), ('C', 7), ('D', 5)],
            'C': [('A', 1), ('B', 7), ('E', 2)],
            'D': [('B', 5), ('E', 7), ('F', 1)],
            'E': [('C', 2), ('D', 7), ('F', 3), ('G', 8)],
            'F': [('D', 1), ('E', 3), ('G', 2)],
            'G': [('E', 8), ('F', 2), ('H', 3)],
            'H': [('G', 3), ('I', 1)],
            'I': [('H', 1), ('J', 6)],
            'J': [('I', 6)]
        }

    def test_shortest_path_in_graph1(self):
        """Teste den kürzesten Pfad von A nach E in Graph 1."""
        dist, path = dijkstra(self.graph1, 'A', 'E')
        self.assertEqual(dist, 20)
        self.assertEqual(path, ['A', 'C', 'F', 'E'])

    def test_no_path_in_disconnected_graph(self):
        """Teste den Fall, dass kein Pfad existiert."""
        graph = {
            'A': [('B', 1)],
            'B': [('A', 1)],
            'C': [('D', 1)],
            'D': [('C', 1)]
        }
        dist, path = dijkstra(graph, 'A', 'D')
        self.assertEqual(dist, float('inf'))
        self.assertEqual(path, [])

    def test_large_graph_with_10_nodes(self):
        """Teste den kürzesten Pfad von A nach J in Graph 2."""
        dist, path = dijkstra(self.graph2, 'A', 'J')
        self.assertEqual(dist, 18)
        self.assertEqual(path, ['A', 'C', 'E', 'F', 'G', 'H', 'I', 'J'])

    def test_all_distances_in_graph1(self):
        """Teste alle kürzesten Distanzen von A in Graph 1."""
        expected_distances = {'A': 0, 'B': 7, 'C': 9, 'D': 20, 'E': 20, 'F': 11}
        distances = dijkstra(self.graph1, 'A')
        self.assertEqual(distances, expected_distances)

    def test_single_node_path(self):
        """Teste den Pfad von einem Knoten zu sich selbst."""
        dist, path = dijkstra(self.graph1, 'A', 'A')
        self.assertEqual(dist, 0)
        self.assertEqual(path, ['A'])

    def test_recursion_depth(self):
        """Teste, ob die Rekursionstiefe für einen großen Graphen korrekt gehandhabt wird."""
        print(f"Aktuelles Rekursionslimit: {sys.getrecursionlimit()}")

        # Erzeuge einen langen linearen Graphen
        linear_graph = {str(i): [(str(i + 1), 1)] for i in range(1000)}
        linear_graph[str(999)] = []  # Letzter Knoten hat keine Nachbarn

        try:
            # Teste den Pfad vom Start- zum Endknoten in einem tiefen rekursiven Aufruf
            dist, path = dijkstra(linear_graph, '0', '999')
            self.assertEqual(dist, 999)
            self.assertEqual(path, [str(i) for i in range(1000)])
        except RecursionError:
            self.fail("RecursionError: Rekursionstiefe überschritten!")

if __name__ == '__main__':
    unittest.main()
