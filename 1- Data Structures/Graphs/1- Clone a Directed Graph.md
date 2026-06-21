## Clone a Directed Graph

`Educative`

### Node.py
```python
class Node:
    def __init__(self, data):
        self.data = data
        self.neighbors = []
```

### Directed_Graph.py
```python
from node import *

class DirectedGraph:   
    def __init__(self):
        self.nodes = []
        
    def add_vertex(self, data):
        obj_node = Node(data)
        self.nodes.append(obj_node)
    
    def find_vertex_by_data(self, data):
        for node in self.nodes:
            if node.data == data:
                return node 
        return None

    def count(self):
      return len(self.nodes)
    
    def add_edge(self, start_node, end_node):
        start = self.find_vertex_by_data(start_node)
        end = self.find_vertex_by_data(end_node)

        if start and end:
            start.neighbors.append(end)
        else:
            print("Node not found\n")

    def print_graph(self):
        for node in self.nodes:
            print(str(node.data) + " -> {  ", end="")
            for n in node.neighbors:
                print(str(n.data) + "  ", end="")
            print("}")

    # vertex insert
    def add_vertex_in_nodes(self, node):
        self.nodes.append(node)

    def delete_edge(self, node, neighbor):
      for v in self.nodes:
        if v.data == node:
            for n in v.neighbors:
                if (n.data == neighbor):
                    v.neighbors.remove(n) 
```

### Main.py

```python
from directed_graph import *

def clone_rec(root, graph, nodes_completed):
  # Base case when there is no node
  if not root:
    return None

  # Creating new vertex/node
  pNew = Node(root.data)

  # Using hashmap to keep track of visited nodes
  nodes_completed[root] = pNew

  # Adding new vertex in the graph
  graph.add_vertex_in_nodes(pNew)

  # Iterate over each neighbor of the current vertex/node
  for p in root.neighbors:
    x = nodes_completed.get(p)
    if not x:
      # If node is not visited call recursive function to create vertex/node
      pNew.neighbors.append(clone_rec(p, graph, nodes_completed))
    else:
      # If node is visited just add it to the neighbors of current vertex/node
      pNew.neighbors.append(x)
  return pNew

def clone(graph):
  # Hashmap to keep record of visited nodes
  nodes_completed = {}
  
  # Creating new graph
  clone_graph = DirectedGraph()
  
  # clone_rec function call
  # Passing first node as root node
  
  if not graph.nodes:
    return None
  else:
    clone_rec(graph.nodes[0], clone_graph, nodes_completed)

  # Return deep copied graph
  return clone_graph

def main():
  # Main start from here
  g1 = DirectedGraph()

  print("------------   EXAMPLE # 1    -----------")
  # Adding verteces/nodes
  g1.add_vertex(0)
  g1.add_vertex(1)
  g1.add_vertex(2)
  g1.add_vertex(3)
  g1.add_vertex(4)

  # Adding edges of vertex/node 0
  g1.add_edge(0, 2)
  g1.add_edge(0, 3)
  g1.add_edge(0, 4)

  # Adding edges of vertex/node 1
  g1.add_edge(1, 2)

  # Adding edges of vertex/node 2
  g1.add_edge(2, 0)

  # Adding edges of vertex/node 3
  g1.add_edge(3, 2)

  # Adding edges of vertex/node 4
  g1.add_edge(4, 1)
  g1.add_edge(4, 3)
  g1.add_edge(4, 0)

  # Printing graph

  print("Original graph (before copy): ")
  print(g1)

  g1_copy = clone(g1)
  print("Cloned graph (after copy):")
  print(g1_copy)

  print("\nOriginal graph (after deleting an edge [0->2]):")
  g1.delete_edge(0, 2)
  print(g1)

  print("\nCloned graph (after deleting an edge [0->2] from original the graph): ")
  print(g1_copy)

  g2 = DirectedGraph()

  # Adding verteces/nodes

  print("\n\n------------   EXAMPLE # 2    -----------")
  g2.add_vertex("v1")
  g2.add_vertex("v2")
  g2.add_vertex("v3")
  g2.add_vertex("v4")
  g2.add_vertex("v5")

  g2.add_edge("v1", "v2")
  g2.add_edge("v1", "v3")
  g2.add_edge("v1", "v4")

  g2.add_edge("v2", "v1")
  g2.add_edge("v2", "v3")
  g2.add_edge("v2", "v4")

  g2.add_edge("v3", "v1")
  g2.add_edge("v3", "v2")
  g2.add_edge("v3", "v4")
  g2.add_edge("v3", "v5")

  g2.add_edge("v4", "v1")
  g2.add_edge("v4", "v2")
  g2.add_edge("v4", "v3")
  g2.add_edge("v4", "v5")

  g2.add_edge("v5", "v3")

  print("Original graph (before copy):")
  print(g2)

  g2_copy = clone(g2)
  print("\nCloned graph (after copy):")
  print(g2_copy)


  print("\nOriginal graph (after deleting an edge [v5->v3]):")
  g2.delete_edge("v5", "v3")
  print(g2)

  print("\nCloned graph (after deleting an edge [v5->v3] from original the graph): ")
  print(g2_copy)

if __name__ == '__main__':
  main()
```