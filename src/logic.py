import random
import math
from typing import List, Dict

from cell import gridCell
from grid import grid

"""
This file can be a nice home for your Battlesnake's logic and helper functions.

We have started this for you, and included some logic to remove your Battlesnake's 'neck'
from the list of possible moves!
"""

def get_info() -> dict:
    """
    This controls your Battlesnake appearance and author permissions.
    For customization options, see https://docs.battlesnake.com/references/personalization

    TIP: If you open your Battlesnake URL in browser you should see this data.
    """
    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Personalize
        "head": "default",  # TODO: Personalize
        "tail": "default",  # TODO: Personalize
    }


def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    my_snake = data["you"]      # A dictionary describing your snake's position on the board
    my_head = my_snake["head"]  # A dictionary of coordinates like {"x": 0, "y": 0}
    my_body = my_snake["body"]  # A list of coordinate dictionaries like [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    my_health = my_snake['health']

    # Uncomment the lines below to see what this data looks like in your output!
    # print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    # print(f"All board data this turn: {data}")
    # print(f"My Battlesnake this turn is: {my_snake}")
    # print(f"My Battlesnakes head this turn is: {my_head}")
    # print(f"My Battlesnakes body this turn is: {my_body}")

  
    
  
    possible_moves = ["up", "down", "left", "right"]

    # Step 0: Don't allow your Battlesnake to move back on it's own neck.
    possible_moves = _avoid_my_neck(my_body, possible_moves)

    # TODO: Step 1 - Don't hit walls.
    # Use information from `data` and `my_head` to not move beyond the game board.
    board = data['board']
    board_height = board['height']
    board_width = board['width']

    Grid = grid(board['height'], data)
    Grid.serialize()

    if (my_head['x'] + 1 >= board_width):
      possible_moves.remove('right')
    if (my_head['x'] - 1 < 0):
      possible_moves.remove('left')
    if (my_head['y'] + 1 >= board_height):
      possible_moves.remove('up')
    if (my_head['y'] - 1 < 0):
      possible_moves.remove('down')

    # TODO: Step 2 - Don't hit yourself.
    # Use information from `my_body` to avoid moves that would collide with yourself.

    def dont_collide(block, possible_moves=possible_moves, my_head=my_head):
      if (my_head['x'] + 1 == block['x'] 
          and my_head['y'] == block['y'] 
          and 'right' in possible_moves
         ):
          possible_moves.remove('right')
      if (my_head['x'] - 1 == block['x'] 
          and my_head['y'] == block['y'] 
          and 'left' in possible_moves
         ):
          possible_moves.remove('left')
      if (my_head['x'] == block['x'] 
          and my_head['y'] + 1 == block['y'] 
          and 'up' in possible_moves
         ):
          possible_moves.remove('up')
      if (my_head['x'] == block['x'] 
          and my_head['y'] - 1 == block['y'] 
          and 'down' in possible_moves
         ):
          possible_moves.remove('down')

  
    for block in my_body: 
      dont_collide(block)
    
    # TODO: Step 3 - Don't collide with others.
    # Use information from `data` to prevent your Battlesnake from colliding with others.

    for snake in data['board']['snakes']:
      for block in snake['body']:
        dont_collide(block)
      dont_collide(snake['head'])
       

    # TODO: Step 4 - Find food.
    # Use information in `data` to seek out and find food.
    food = data['board']['food']
    if my_health < 100 and food:
      food_moves = moves_to(my_head, nearest_food(food, my_head))
      if len(food_moves) > 0:
        possible_moves = list(set(possible_moves).intersection(food_moves))
    
      # Choose a random direction from the remaining possible_moves to move in, and then return that move
    move = random.choice(possible_moves)
    # TODO: Explore new strategies for picking a move that are better than random

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move


def _avoid_my_neck(my_body: dict, possible_moves: List[str]) -> List[str]:
    """
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
    """
    my_head = my_body[0]  # The first body coordinate is always the head
    my_neck = my_body[1]  # The segment of body right after the head is the 'neck'

    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        possible_moves.remove("up")

    return possible_moves

# returns the coordinates of the food nearest to head
def nearest_food(food_list, head):
  dist = []
  for food in food_list:
    dist.append(math.sqrt(((food['x'] - head['x']) ** 2) + ((food['y'] - head['y']) ** 2)))
  return food_list[dist.index(min(dist))]

def moves_to(start, end):
  possible_moves = []
  if end['x'] > start['x']:
    possible_moves.append('right')
  elif end['x'] < start['x']:
    possible_moves.append('left')
  if end['y'] > start['y']:
    possible_moves.append('up')
  elif end['y'] < start['y']:
    possible_moves.append('down')
  return possible_moves