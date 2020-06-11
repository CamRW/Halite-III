#!/usr/bin/env python3
# Python 3.6

# Import the Halite SDK, which will let you interact with the game.
import hlt

# This library contains constant values.
from hlt import constants

# This library contains direction metadata to better interface with the game.
from hlt.positionals import Direction

# This library allows you to generate random numbers.
import random

# Logging allows you to save messages for yourself. This is required because the regular STDOUT
#   (print statements) are reserved for the engine-bot communication.
import logging

import A_star

import BreadthPath
""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()
# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("MouseMooseBot")

# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#   Here, you log here your id, which you can always fetch from the game object by using my_id.
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

""" <<<Game Loop>>> """

while True:
    # This loop handles each turn of the game. The game object changes every turn, and you refresh that state by
    #   running update_frame().
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map

    logging.info("Shipyard at {}".format(me.shipyard))



    # A command queue holds all the commands you will run this turn. You build this list up and submit it at the
    #   end of the turn.
    command_queue = []

    ship_status = {}

    sur_tiles = []
    sur_halite = []
    sur_halite_sorted = []
    sur_halite_sorted_sm = []

    for ship in me.get_ships():

        sur_tiles = ship.position.get_surrounding_cardinals()
        sur_halite.append((ship.position, game_map[ship.position].halite_amount))

        opt_tile = ship.position

        breadth_map = BreadthPath.breadthpath(game_map, ship.position, me.shipyard.position)

        logging.info("BreadthMap = {}".format(breadth_map))

        # came_from, cost_so_far = A_star.a_star_navigate(game_map, ship.position, me.shipyard.position)
        # logging.info(" Path for A_star = {} cost so far = {}".format(came_from, cost_so_far))
        logging.info("Current ship spot = {}".format(ship.position))

        # final_path = A_star.reconstruct_path(came_from, ship.position, me.shipyard.position)
        #
        # logging.info("Final path = {}".format(final_path))

        if (ship.is_full or ship.halite_amount > constants.MAX_HALITE / 4 - 15) and not game_map[me.shipyard].is_occupied:
            move = game_map.naive_navigate(ship, me.shipyard.position)
            command_queue.append(ship.move(move))
            continue

        # Choose the halite tile with the most halite out of the 4 cardinal direction tiles and the current tile

        for tile in sur_tiles:

            #logging.info("Saving {} position with {} halite into sur_halite".format(tile, game_map[tile].halite_amount))
            sur_halite.append((tile, game_map[tile].halite_amount))

        sur_halite_sorted = sorted(sur_halite, key=lambda x: x[1], reverse=True)
        sur_halite_sorted_sm = sorted(sur_halite, key=lambda x: x[1])

        #for tile, halite in sur_halite_sorted:
        #    logging.info("From sur_halite_sorted: tile, halite = {}, {}".format(tile, halite))

        if ship.position == sur_halite_sorted[0][0]:
            # Stay
            #logging.info("Ship {} is already at optimized position {}".format(ship.id, game_map[opt_tile]))
            command_queue.append(ship.stay_still())
            sur_halite = []
            sur_halite_sorted = []
            continue
        if ship.position == sur_halite_sorted[1][0] and ((.25*sur_halite_sorted[0][1] - .1*sur_halite_sorted[0][1]) > .25*sur_halite_sorted[1][1]):
            # Move to new [0][0]
            move = game_map.naive_navigate(ship, sur_halite_sorted[0][0])
            command_queue.append(ship.move(move))
            sur_halite = []
            sur_halite_sorted = []
            continue
        elif ship.position == sur_halite_sorted[1][0] and ((.25*sur_halite_sorted[0][1] - .1*sur_halite_sorted[0][1]) < .25*sur_halite_sorted[1][1]):
            #Stay
           # logging.info("Ship {} is already at optimized position {}".format(ship.id, game_map[opt_tile]))
            command_queue.append(ship.stay_still())
            sur_halite = []
            sur_halite_sorted = []
            continue
        else:
            #Move to [0][0]
            move = game_map.naive_navigate(ship, sur_halite_sorted[0][0])
            command_queue.append(ship.move(move))
            sur_halite = []
            sur_halite_sorted = []
            continue

    # If the game is in the first 200 turns and you have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though - the ships will collide.
    if game.turn_number <= 100 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)

