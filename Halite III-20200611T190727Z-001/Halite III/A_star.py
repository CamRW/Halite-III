import hlt
from hlt import constants
from hlt import game_map
import logging
import queue


def a_star_navigate(game_map, start, goal, heuristic=None):
    if heuristic is None:
        def heuristic(game_map, a, b):
            return game_map.calculate_distance(a, b)

    frontier = queue.PriorityQueue()
    frontier.put(start)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0.0
    #logging.info("cost_so_far[start] = {}".format(cost_so_far[start]))

    while not frontier.empty():
        current = frontier.get()
        cur_pos = current
        logging.info("current = {}".format(current))
        #logging.info("current type = {}".format(type(current)))

        if isinstance(current, hlt.positionals.Position) and current == goal:
            break

        elif isinstance(current, tuple):
            cur_pos = current[1]
            if current[1] == goal:
                break

        if not isinstance(cur_pos, hlt.positionals.Position):
            break
        #
        # if isinstance(hlt.positionals.Position, type(current)):
        #
        #     logging.info("current = {} is type Position".format(current))
        #
        #     return frontier
        #     # Return path
        # elif isinstance(tuple, type(current)):
        #     logging.info("current tuple = {} {}".format(current[0], current[1]))
        #
        #     return frontier
        #
        # if current == None:
        #     return frontier

        for next_space in game_map[cur_pos].position.get_surrounding_cardinals():
            new_cost = cost_so_far[cur_pos] + .1*game_map[next_space].halite_amount
            #logging.info("cost_so_far[current] = {}".format(cost_so_far[current]))
            #logging.info("cost_so_far = {} and next_space = {}".format(cost_so_far, next_space))
            if next_space not in cost_so_far or new_cost < cost_so_far[next_space]:
                cost_so_far[next_space] = new_cost
                #logging.info("cost_so_far[next_space] = {}".format(cost_so_far[next_space]))

                priority = new_cost + heuristic(game_map, next_space, goal)
                logging.info("Priority = {}".format(priority))
                frontier.put(priority, next_space)
                came_from[next_space] = current

                logging.info("Next space = {} cost so far = {}".format(next_space, cost_so_far))

    return came_from, cost_so_far

# def reconstruct_path(came_from, start, goal):
#     current = goal
#     path = []
#     while current != start:
#         path.append(current)
#         logging.info("came_from in reconstruct path = {}".format(came_from))
#         current = came_from[current]
#     path.append(start) # optional
#     path.reverse() # optional
#     return path