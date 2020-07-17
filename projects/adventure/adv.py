from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# Create an empty dictionary to save all the visited rooms
visited = {}
# Create an empty list that will save my reverse path, allowing me to back track when neccesary
backPath = []
# Save all possible movement options as keys, with their opposite directions as values
movementOptions = {'n':'s', 's':'n', 'w':'e', 'e':'w'}
# Saves the current room (Room Number) in visited as a key, with each possible exit DIRECTION as values
visited[player.current_room.id] = player.current_room.get_exits()

# While there is still rooms to visit AKA my driver code
while len(visited) < len(room_graph):

    # check if the current room has not been visited and if so
    if player.current_room.id not in visited:
        # Save the current room in visited as a key (or "room" 0 for example) with each possible exit as values for the key ( direcitons like "n,e,s,w")
        visited[player.current_room.id] = player.current_room.get_exits()
        # Save the last direction in backPath as the prev_Room. When we walk East the prev_Room becomes West and is stored in backPath
        prev_Room = backPath[-1]
        print("previousRoom: ", prev_Room)
        print("backtrackPath: ", backPath)
        print("Currently in: ", player.current_room.id)
        # Remove the direction I just came from as a possible exit. So if we start in room 0 and go E, W is removed as a possible exit.
        visited[player.current_room.id].remove(prev_Room)

    # if the room HAS been visited and HAS exits we have not used yet
    # go through one of the exits and check it off
    # so if we're not in room 0 and the room is in visited
    elif len(visited[player.current_room.id]) > 0 and player.current_room.id in visited:
        # Save the last of the current rooms exits as a variable
        # so if we're in room 1 and it has [N,X,S,E] as exits our next_Room variable will become E.
        next_Room = visited[player.current_room.id][-1]
        print("next_Room: ", next_Room)
        print("backPath: ", backPath)
        print("Currently in: ", player.current_room.id)
        # remove the next_Room from the current rooms exits I use pop because it removes the last index which is what I want
        visited[player.current_room.id].pop()
        # add that to the answer aka traversal path. this builds a answer of rooms we HAVE been in like [West, Eeast, Eeast, Eeast, West, West, West, and now we're back at room 0 to explore the WEST branch]
        # this is our answer basically
        traversal_path.append(next_Room)
        # add the reverse movement to backPath list to keep track of where i am going {'n':'s', 's':'n', 'w':'e', 'e':'w'} these are our options
        backPath.append(movementOptions[next_Room])
        # go into the next room so now we went from room 0 in the MIDDLE, to room 1 East and our backtrack should be West. with a next room of East (I'm testing this on the cross map for simplicity)
        player.travel(next_Room)
        print("Walking to:", next_Room)

    # If there are no more exits for the current room this code will execute
    # go back in Backpath order to the prior room
    elif len(visited[player.current_room.id]) == 0:
        # Save the direction i just came from as the previous room pushing whatever this room number was from the end of backpath to previous room variable
        prev_Room = backPath[-1]
        print("prev_Room(last call): ", prev_Room)
        print("backPath: ", backPath)
        print("Currently in: ", player.current_room.id)
        # Remove that direction from the backPath
        backPath.pop()
        # Add that to the answer path
        traversal_path.append(prev_Room)
        # Go back to the previous room
        player.travel(prev_Room)
        print("Walking BACK to:", prev_Room)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
