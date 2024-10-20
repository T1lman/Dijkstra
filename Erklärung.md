
---

## **Beispiel-Graph**

Der folgende Graph ist ein gewichteter, gerichteter Graph mit den Knoten **A, B, C, D, E** und den Kanten mit ihren Gewichten:

```
    A --1--> B --2--> C
    |         \
    4          3
    v           \
    D            E
```

**Graph als Dictionary:**
```python
graph = {
    'A': [('B', 1), ('D', 4)],
    'B': [('C', 2), ('E', 3)],
    'C': [],
    'D': [],
    'E': []
}
```

- Startknoten: **A**  
- Endknoten: **C**

---

## **Erwartetes Ergebnis**
Der kürzeste Pfad von **A** nach **C** ist:  
```
A -> B -> C
```
Die Gesamtdistanz dieses Pfads ist `1 + 2 = 3`.

---

## **Schritt-für-Schritt Ablauf des Algorithmus**

### **Initialisierung**
- **Distanzen**: `{'A': 0}` (Distanz zu sich selbst ist 0)  
- **Vorgänger**: `{}` (noch keine Vorgänger bekannt)  
- **Warteschlange (Heap)**: `[(0, 'A')]` (Start bei A mit Distanz 0)  
- **Besuchte Knoten**: `frozenset()` (noch kein Knoten besucht)

---

### **Rekursiver Ablauf**

#### **1. Rekursion: Verarbeitung von Knoten 'A'**
- **Warteschlange**: `[(0, 'A')]`  
  - Pop aus Heap: `(0, 'A')`
- **Verarbeitung von 'A'**:
  - Nachbarn von 'A': `B (1)` und `D (4)`
  
##### **Update der Nachbarn**
1. **Knoten B**:
   - Neue Distanz: `0 + 1 = 1`
   - Update von Distanzen: `{'A': 0, 'B': 1}`
   - Update von Vorgängern: `{'B': 'A'}`
   - Warteschlange: `[(1, 'B')]`

2. **Knoten D**:
   - Neue Distanz: `0 + 4 = 4`
   - Update von Distanzen: `{'A': 0, 'B': 1, 'D': 4}`
   - Update von Vorgängern: `{'B': 'A', 'D': 'A'}`
   - Warteschlange: `[(1, 'B'), (4, 'D')]`

- **Besuchte Knoten**: `{'A'}`

---

#### **2. Rekursion: Verarbeitung von Knoten 'B'**
- **Warteschlange**: `[(1, 'B'), (4, 'D')]`  
  - Pop aus Heap: `(1, 'B')`
- **Verarbeitung von 'B'**:
  - Nachbarn von 'B': `C (2)` und `E (3)`

##### **Update der Nachbarn**
1. **Knoten C**:
   - Neue Distanz: `1 + 2 = 3`
   - Update von Distanzen: `{'A': 0, 'B': 1, 'D': 4, 'C': 3}`
   - Update von Vorgängern: `{'B': 'A', 'D': 'A', 'C': 'B'}`
   - Warteschlange: `[(3, 'C'), (4, 'D')]`

2. **Knoten E**:
   - Neue Distanz: `1 + 3 = 4`
   - Update von Distanzen: `{'A': 0, 'B': 1, 'D': 4, 'C': 3, 'E': 4}`
   - Update von Vorgängern: `{'B': 'A', 'D': 'A', 'C': 'B', 'E': 'B'}`
   - Warteschlange: `[(3, 'C'), (4, 'D'), (4, 'E')]`

- **Besuchte Knoten**: `{'A', 'B'}`

---

#### **3. Rekursion: Verarbeitung von Knoten 'C'**
- **Warteschlange**: `[(3, 'C'), (4, 'D'), (4, 'E')]`  
  - Pop aus Heap: `(3, 'C')`
- **Verarbeitung von 'C'**:
  - Keine Nachbarn (leere Liste)

- **Besuchte Knoten**: `{'A', 'B', 'C'}`  
- Da wir am Zielknoten **C** angekommen sind, können wir den **kürzesten Pfad** rekonstruieren.

---

### **Pfad-Rückverfolgung**
- Start bei Zielknoten **C**:
  - Vorgänger von `C` ist `B`
  - Vorgänger von `B` ist `A`
- Pfad: `A -> B -> C`

---

### **Endgültiges Ergebnis**
- **Kürzeste Distanz**: 3  
- **Pfad**: `['A', 'B', 'C']`

---

## **Rekursionsbaum Übersicht**

```
Rekursion 1: A -> (B, 1), (D, 4)
  Rekursion 2: B -> (C, 3), (E, 4)
    Rekursion 3: C (Zielknoten erreicht)
```

---

## **Zusammenfassung des Ablaufs**

1. Der Algorithmus startet bei **A** und verarbeitet seine Nachbarn.
2. In jedem Rekursionsschritt wird der Knoten mit der kleinsten bekannten Distanz aus der **Warteschlange** entnommen.
3. Jeder Nachbar wird verarbeitet, und falls ein kürzerer Pfad gefunden wird, werden die **Distanzen** und **Vorgänger** aktualisiert.
4. Der Prozess endet, wenn die Warteschlange leer ist oder das **Ziel erreicht** wurde.
5. Schließlich wird der **Pfad rekursiv zurückverfolgt**, um die Abfolge der Knoten vom Start zum Ziel zu bestimmen.

---

## **Funktionale Aspekte im Ablauf**

- **Rekursive Struktur**: Anstelle von Schleifen wird die Verarbeitung rekursiv durchgeführt.
- **Immutable Datenstrukturen**: Besuchte Knoten und Distanzen werden als neue Instanzen aktualisiert, ohne die alten Werte zu überschreiben.


---

Dieses Beispiel zeigt, wie der **funktionale Dijkstra-Algorithmus** arbeitet und wie er Knoten schrittweise verarbeitet, um den kürzesten Pfad zu finden. Die Verwendung von Rekursion macht die Implementierung besonders elegant und klar.