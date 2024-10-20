from typing import Dict, List, Tuple, Optional, FrozenSet
from heapq import heappop, heappush  # Min-Heap-Funktionen
from functools import reduce  # Ermöglicht Reduktion einer Liste zu einem Akkumulator
import sys

# Typdefinition für einen gewichteten Graphen: 
# Jeder Knoten verweist auf eine Liste von (Nachbar, Gewicht)-Tupeln
Graph = Dict[str, List[Tuple[str, int]]]

def dijkstra(graph: Graph, start: str, end: Optional[str] = None) -> Tuple[int, List[str]]:
    """
    Funktionaler Dijkstra-Algorithmus zur Berechnung des kürzesten Pfads.
    
    Args:
        graph: Der gewichtete Graph als Dictionary.
        start: Startknoten.
        end: Zielknoten (optional). Wenn `None`, werden alle Distanzen berechnet.
    
    Returns:
        Eine Tupel: (kürzeste Distanz, Pfad als Liste von Knoten).
    """
    
    # Rekursionslimit erhöhen, da große Graphen tiefe Rekursionen erfordern können
    sys.setrecursionlimit(10_000)  

    # Rekursive Funktion für die Hauptlogik des Dijkstra-Algorithmus
    def dijkstra_rec(
        queue: List[Tuple[int, str]],  # Min-Heap-Warteschlange: [(Distanz, Knoten)]
        visited: FrozenSet[str],  # Bereits besuchte Knoten (immutable set)
        distances: Dict[str, int],  # Kürzeste bekannte Distanzen zu jedem Knoten
        predecessors: Dict[str, Optional[str]]  # Vorgänger jedes Knotens für Pfadrückverfolgung
    ) -> Tuple[Dict[str, int], Dict[str, Optional[str]]]:
        """
        Rekursive Funktion, die den Dijkstra-Algorithmus ausführt.
        """
        # Abbruchbedingung: Wenn die Warteschlange leer ist, sind wir fertig
        if not queue:
            return distances, predecessors

        # Knoten mit der kleinsten Distanz aus der Warteschlange holen
        current_dist, current_node = heappop(queue)

        # Wenn der Knoten bereits besucht wurde, überspringen wir ihn
        if current_node in visited:
            return dijkstra_rec(queue, visited, distances, predecessors)

        # Markiere den aktuellen Knoten als besucht (Immutable Set wird erweitert)
        new_visited = visited | frozenset([current_node])

        # Verarbeite alle Nachbarn des aktuellen Knotens
        def update_neighbor(
            acc: Tuple[List[Tuple[int, str]], Dict[str, int], Dict[str, Optional[str]]],
            neighbor: Tuple[str, int]
        ) -> Tuple[List[Tuple[int, str]], Dict[str, int], Dict[str, Optional[str]]]:
            """
            Hilfsfunktion, die für jeden Nachbarn prüft, ob wir einen kürzeren Pfad gefunden haben.
            
            Args:
                acc: Akkumulierte Daten (Queue, Distanzen, Vorgänger).
                neighbor: Ein Nachbar-Knoten und das Gewicht der Kante.
            
            Returns:
                Aktualisierte (Queue, Distanzen, Vorgänger).
            """
            q, dist, preds = acc  # Entpacke Akkumulator
            neighbor_node, weight = neighbor  # Entpacke Nachbar-Daten
            new_dist = current_dist + weight  # Neue potentielle Distanz

            # Wenn der neue Pfad kürzer ist, aktualisieren wir die Distanz und den Vorgänger
            if new_dist < dist.get(neighbor_node, float('inf')):
                # Erstelle neue, immutable Dictionaries mit den aktualisierten Werten
                new_distances = {**dist, neighbor_node: new_dist}
                new_predecessors = {**preds, neighbor_node: current_node}
                
                # Füge den Nachbarn zur Warteschlange hinzu
                new_queue = q + [(new_dist, neighbor_node)]
                heappush(new_queue, (new_dist, neighbor_node))  # Min-Heap bleibt konsistent

                return new_queue, new_distances, new_predecessors

            # Wenn der Pfad nicht kürzer ist, bleibt der Akkumulator unverändert
            return acc

        # Verarbeite alle Nachbarn des aktuellen Knotens mit `reduce`
        new_queue, new_distances, new_predecessors = reduce(
            update_neighbor,  # Funktion, die auf jeden Nachbarn angewendet wird
            graph.get(current_node, []),  # Liste der Nachbarn
            (queue, distances, predecessors)  # Startwert für den Akkumulator
        )

        # Rekursiver Aufruf mit aktualisierten Daten
        return dijkstra_rec(new_queue, new_visited, new_distances, new_predecessors)

    # Initiale Zustände
    initial_queue = [(0, start)]  # Startknoten mit Distanz 0 in die Warteschlange
    initial_distances = {start: 0}  # Distanz zum Startknoten ist 0
    initial_predecessors = {}  # Vorgänger ist zunächst leer
    visited = frozenset()  # Keine Knoten wurden zu Beginn besucht

    # Starte die rekursive Verarbeitung
    distances, predecessors = dijkstra_rec(
        initial_queue, visited, initial_distances, initial_predecessors
    )

    # Wenn kein Zielknoten spezifiziert ist, gib alle Distanzen zurück
    if end is None:
        return distances

    # Falls der Zielknoten unerreichbar ist, gib Unendlich und einen leeren Pfad zurück
    if distances.get(end, float('inf')) == float('inf'):
        return float('inf'), []

    # Rekursive Funktion zur Pfadrückverfolgung vom Ziel zum Start
    def backtrack_path(node: str, acc: List[str]) -> List[str]:
        """
        Rekonstruiert den Pfad rekursiv vom Ziel zum Start.
        
        Args:
            node: Der aktuelle Knoten im Pfad.
            acc: Akkumulierte Liste des Pfads.
        
        Returns:
            Vollständiger Pfad als Liste.
        """
        if node is None:  # Wenn wir am Startknoten angekommen sind
            return acc
        # Rekursiver Aufruf mit dem Vorgänger des aktuellen Knotens
        return backtrack_path(predecessors.get(node), [node] + acc)

    # Starte die Pfadrückverfolgung vom Endknoten aus
    path = backtrack_path(end, [])

    # Gib die kürzeste Distanz und den Pfad zurück
    return distances[end], path
