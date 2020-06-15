from graph_class import Vertex


def bfs(graph, first_element):
    queue = []

    for vertex in graph.vertices:
        vertex.state = 0
    first_element.state = 1

    queue_index = -1
    queue.append(first_element)

    while queue_index < len(queue) - 1:
        queue_index += 1
        opened_vertex = queue[queue_index]
        if not isinstance(opened_vertex, Vertex):
            continue

        for edge in opened_vertex.edges:

            if edge.vertices[0] == opened_vertex:
                neighbor = edge.vertices[1]
            else:
                neighbor = edge.vertices[0]

            if neighbor.state == 0:
                neighbor.state = 1
                queue.append(edge)
                queue.append(neighbor)
    return queue
