import time
import requests
import hashlib
import random

# from traversal import take_treasure, status_inventory, sell_treasure, wise_explorer, movement, name_changer, pray
from mine import proof_of_work, valid_proof
from graphutils import graph
from player import Player
from dreamy import dreamy

player = Player()

print("Hunting for treasure!")
print(f"Current gold: {player.gold}")
# Once we have a name, we no longer collect gold. So I guess this part goes in a while loop. While no name or not 1000 gold, we traverse the map for treasure
while player.gold < 1000 and "User" in player.name:
    while player.encumbrance < player.strength - 1:
        visited = set({player.current_room})

        if player.room_items and any([t for t in player.room_items if "treasure" in t]):
            print("Found treasure! Taking it...")
            player.take_treasure("tiny treasure")
            print(f"Took treasure. Current items: {player.items}")
        else:
            exits = graph.rooms[player.current_room]["exits"]
            unvisited = {direction: room for direction,
                         room in exits.items() if room not in visited}
            if unvisited:
                exits = unvisited

            direction = random.choice([d for d in exits])

            print(f"Moving {direction}...")
            player.movement(direction)
            print(f"Player moved {direction} to room {player.current_room}")

    # Go to random room
    # On the way to random room, we need to examine the room each time we enter a new one. So if new room, call function examine
    # if there are items in the room, then we take those items up until we have 9 items.
    # When we hit 9 items, we should return to the shop from our current room.
    # handle_items()

    # Go back to the shop and sell the item
    # traversal = bfs(player.current_room, 1)
    # move_to_location(traversal)
    # Try to use wise explorer instead of move endpoint
    # for m in traversal:
    # room = player.current_room
    # exits = map.json[room]["exits"]
    # for direction, roomID in exits:
    #     if roomID == m:
    # response = wise_explorer(m[0], API_KEY, m[1])
    # cooldown = response["cooldown"]
    # time.sleep(cooldown)
    # if "errors" in response:
    #     print(response["errors"])

    # Sell the item
    # for item in player.inventory:
    #     sell_treasure(item, API_KEY)

    # While 1000 gold, make way to pirate ry.
while player.gold >= 1000:
    path = graph.bfs(player.current_room, 467)
    move_to_location(path)
    # for m in path:
    # room = player.current_room
    # exits = map.json[room]["exits"]
    # for direction, roomID in exits:
    #     if roomID == m:
    # wise_explorer(m[0], API_KEY, m[1])
    # cooldown = response["cooldown"]
    # time.sleep(cooldown)
    # if "errors" in response:
    #     print(response["errors"])

    # At pirate ry, change name.
    name_changer(name, API_KEY)
    cooldown = response["cooldown"]
    time.sleep(cooldown)

# Go to the shrine, and use pray function
path = graph.bfs(player.current_room, 374)
move_to_location(path)
pray(API_KEY)

path = graph.bfs(374, 461)
move_to_location(path)
pray(API_KEY)


# Move from pirate ry to the well to solve puzzle with ls-8
path = graph.bfs(461, 55)
move_to_location(path)
# Solve the puzzle

# Move from the well to the new location
# Mine at new location
response = requests.get(
    "https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/", headers=header)
last_bl = response.json()["proof"]
new_proof = proof_of_work(last_bl)
data = json.dumps({"proof": new_proof})
response = requests.post(
    "https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/", headers=header, data=data)


def handle_items():
    # Have to change from map.json? YES
    if response["items"]:
        first_response = status_inventory(API_KEY)
        if len(first_response["inventory"]) > 9:
            # change path player.room_id to the shop room_id: 1
            path = graph.bfs(player.room_id, 1)
            move_to_location(path)
            for item in player.inventory:
                response = sell_treasure(item, API_KEY)
                cooldown = response["cooldown"]
                time.sleep(cooldown)
        for item in response["items"]:
            response = take_treasure(item, API_KEY)
            player.add_to_inventory(item)
            cooldown = response["cooldown"]
            time.sleep(cooldown)
            break


def move_to_location(path):
    for m in path:
        wise_explorer(m[0], API_KEY, m[1])
        cooldown = response["cooldown"]
        time.sleep(cooldown)
        if "errors" in response:
            print(response["errors"])