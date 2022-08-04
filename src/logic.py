import random
import math
from typing import List, Dict

from grid import grid, gridCell, flood_fill
from grid import flood_fill

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
    print(data['board']['snakes'])
    my_snake = data["you"]      # A dictionary describing your snake's position on the board
    my_head = my_snake["head"]  # A dictionary of coordinates like {"x": 0, "y": 0}
    my_body = my_snake["body"]  # A list of coordinate dictionaries like [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    my_health = my_snake['health']
    my_tail = my_body[-1]

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
       

    Grid = grid(board['height'], data)
    gridAs2DArray = Grid.serialize()
    print(gridAs2DArray)
  
    movesWithMostSpace = flood_fill(Grid.getGrid(),my_head)
    if 'root' in movesWithMostSpace.keys(): del movesWithMostSpace['root']
    movesWithMostSpace = sorted(movesWithMostSpace.items(), key=lambda x:x[1],reverse=True)
    print(movesWithMostSpace)


    # TODO: Step 4 - Find food.
    # Use information in `data` to seek out and find food.

    # I think it shouldnt rule out moves that arent in favour of food,
    # Will add remaining moves at the end so they are still a option and instead of
    # randomly picking the move will pick based on the one that
    # has the most possible moves after.
    food = data['board']['food']
    if  30 < my_health <= 100 and smaller_snakes(data['board']['snakes'], my_snake['length']-3):
      agressive_moves = beAggressive(data['board']['snakes'], my_snake)
      agressive_moves = list(set(possible_moves).intersection(agressive_moves)) 
      for remainingMove in set(possible_moves).difference(agressive_moves):
        agressive_moves.append(remainingMove)     
      if len(agressive_moves) > 0:
        possible_moves = agressive_moves
        print(f"being agressive : {agressive_moves}")
    elif my_health < 30 and food:
      food_moves = moves_to(my_head, nearest_food(food, my_head))
      food_moves = list(set(possible_moves).intersection(food_moves)) 
      for remainingMove in set(possible_moves).difference(food_moves):
        food_moves.append(remainingMove)     
      if len(food_moves) > 0:
        possible_moves = food_moves
        print(f"getting food : {food_moves}")
    # Maybe if a snake head of a smaller snake is within a certain distance from our head, start hunting it, if otherwise good on health
    # if no food, or good on health, chase tail
    else:
      tail_moves = moves_to(my_head, my_tail)
      tail_moves = list(set(possible_moves).intersection(tail_moves))
      for remainingMove in set(possible_moves).difference(tail_moves):
        tail_moves.append(remainingMove)
      if len(tail_moves) > 0:
        possible_moves = tail_moves
        print(f"chasing tail : {tail_moves}")
    

    if my_health < 10:
      for move in possible_moves:
        if movesWithMostSpace > 0:
          return move
    
    
    #We want to avoid certain cells around snakes that are longer than us
    cellsToAvoid = []
    for snake in data['board']['snakes']:
      if snake['length'] < my_snake['length'] + 2:
        continue

      allPossibleMoves=headLocationAfterMove(snake['head'])
      for move in allPossibleMoves:
        cellsToAvoid.append((allPossibleMoves[move]['x'], allPossibleMoves[move]['y']))
    print("cellsToAvoid: ", cellsToAvoid)
    
    # movesWithMostSpace is a sorted list of tuples with each move and how much space it has
    # ideally instead of a random move we want to take the move that will put us in the most space


    #if we can avoid certain cells we should
    move = random.choice(possible_moves)
    for possibleMove, space in movesWithMostSpace:
      if possibleMove in possible_moves:
        possibleLocation = headLocationAfterMove(my_head)
        if possibleLocation[possibleMove] not in cellsToAvoid:
          print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves} avoiding")
          return possibleMove
        else:
          print(f"avoided move {possibleMove} because of danger in cell {possibleLocation[possibleMove]}")

  #will run only if there are no possible moves when avoiding
    for possibleMove, space in movesWithMostSpace:
      if possibleMove in possible_moves:
        print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves} in cells to avoid")
        return possibleMove
    
    # TODO: Explore new strategies for picking a move that are better than random

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} random picked from all valid options in {possible_moves}")
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
    # could potentially return min distance as well if we want to hunt snakes based on a distance heuristic
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

def beAggressive(all_snakes, me): # maybe you could use something like this
  # closest snake (snake = food lol)
  snake = nearest_food(smaller_snakes(all_snakes, me['length']-3), me['head'])
  #flood_fill will return the most likely moves in order
  moves = iter(flood_fill(Grid.getGrid(), snake['head']))
  mostLikelyMove = next(moves)
  #next(iter()) will give the first one in the dict (the best move)
  nextHeadLocation = headLocationAfterMove(snake['head'])
  # check that most likely move is not its neck (just in case) -- unless that's already covered in grid
  if nextHeadLocation[mostLikelyMove] not in snake['body']:
    return moves_to(me['head'], nextHeadLocation[mostLikelyMove])
  else:
    # take next most likely move
    return moves_to(me['head'], nextHeadLocation[next(moves)])

def headLocationAfterMove(enemy_head):
  return {
      'up':{'x':enemy_head['x'], 'y':enemy_head['y'] + 1 }, 
      'down':{'x':enemy_head['x'], 'y':enemy_head['y'] - 1 }, 
      'left':{'x':enemy_head['x'] - 1, 'y':enemy_head['y'] }, 
      'right':{'x':enemy_head['x'] + 1, 'y':enemy_head['y'] }
                       }

# all snakes includes us, but we should be removed with length check
def smaller_snakes(all_snakes, my_length):
  smaller = []
  for snake in all_snakes:
    if snake['length'] < my_length:
      smaller.append(snake)
  return smaller

# chase a snake's tail - could be useful in some circumstances
def chase_snake(all_snakes, me):
  pass