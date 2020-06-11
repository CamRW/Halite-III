import hlt
from hlt import constants
from hlt import game_map
import logging
import queue


def breadthpath(game_map, start, goal):
    max_steps = game_map.calculate_distance(start, goal)

    frontier = queue.Queue()
    frontier.put(start)
    visited = {}
    visited[start] = True

    logging.info("visited = {}".format(visited))

    while not frontier.empty():

        if goal in visited and visited[goal]:
            return visited

        current = frontier.get()
        for node in game_map[current].position.get_surrounding_cardinals():
            if node not in visited:
                frontier.put(node)
                visited[node] = True

    return visited
