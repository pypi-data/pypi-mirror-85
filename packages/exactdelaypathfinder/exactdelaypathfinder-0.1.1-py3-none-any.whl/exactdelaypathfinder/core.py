class ExactDelayPathfinder:
    def __init__(self):
        self._paths = []
        self._graph = None
        self._result_count = 0
        self._visit_limit = 2

    def search(self, graph, total_delay, start, end, result_count=10):
        '''Obtain paths with total delays equal or close to the user's requirements.'''
        if graph is None:
            raise AttributeError("The graph must not be NoneType")

        if result_count < 0:
            raise AttributeError("The result count must be a non-negative integer.")

        self._paths = []
        self._graph = graph
        self._result_count = result_count

        # This list prevents excessive cycling in the pathfinding process
        visits = {}

        for node in self._graph.nodes:
            visits[str(node)] = 0

        # Assume the starting node is visited at this point
        visits[start] = 1 

        # Find paths that have delays close to the requested delay. The one in front of the list has
        # the closest matching delay of the lot.
        self._search(total_delay, start, end, [], visits)
        
        # Format result to list each path along with their total delays
        result = []

        for path in self._paths:
            result.append({"path":path["path"], "total_delay": total_delay - path["offset"]})

        return result

    def _search(self, delay, curr, target, path, visits):
        if (curr == target and path != []):
            error = abs(delay) # The target was reached
            if not bool(self._paths) or error < self._paths[0]["error"]:
                # The path in front is the one with the lowest error
                self._paths.insert(0, {"path":path.copy(), "error":error, "offset":delay})
                # Ensure that the list is at most ten (10) elements in length
                if len(self._paths) > self._result_count:
                    del self._paths[-1]
            return
        for neighbor in list(self._graph.neighbors(curr)):
            if (visits[str(neighbor)] < self._visit_limit):
                visits[str(neighbor)] += 1
                edge_delay = self._graph.edges[curr, neighbor]['delay']
                path.append((curr, neighbor)) # Found a potential path with this as the starting edge
                self._search(delay - edge_delay, neighbor, target, path, visits)
                del path[-1] # Clean up after an end was reached (target or dead end)
                visits[str(neighbor)] -= 1
