# from yaml import serialize
from cell import gridCell
from queue import Queue
# writing this to test a flood fill implementation 
class grid():
  def __init__(self, gridSize, data):
    board = data['board']
    self.grid = []
    for i in range(gridSize):
      row = []
      for j in range(gridSize):
        row.append(gridCell())
      self.grid.append(row)

    for food in board['food']:
      #print(type(self.grid[food['y']][food['x']].isFood))
      self.grid[food['y']][food['x']].isFood = True

    for snake in board['snakes']:
      for part in snake['body']:
        cell = self.grid[part['y']][part['x']]
        cell.isOtherSnakeBody = True
        cell.isObstacle = True
      head = snake['head']
      self.grid[head['y']][head['x']].isOtherSnakeHead = True
      self.grid[head['y']][head['x']].isObstacle = True

    for part in data['you']['body']:
      self.grid[part['y']][part['x']].isSelf = True
      self.grid[part['y']][part['x']].isObstacle = True

    myHead = data['you']['head']
    self.grid[myHead['y']][myHead['x']].isHead = True

  def getGrid(self):
    return self.grid

  def serialize(self):
    serializedArray = []
    for row in self.grid:
      serializedArray.append([str(x) for x in row])
    return serializedArray

def flood_fill(grid, head):
    n = len(grid)
    m = len(grid[0])
    i, j = head['y'], head['x']
    old_color = grid[i][j]
    if old_color == '#':
       return

    queue = Queue()
    queue.put((i, j, 'root', None))
    used = []
    moves = {'right':0, 'left':0, 'up':0, 'down':0, 'root':0}
    while not queue.empty():
        queueInput = queue.get()
        i, j = queueInput[0], queueInput[1]
        if queueInput[3] == None or queueInput[3] == 'root':
          parent = queueInput[2]
        else:
          parent = queueInput[3]
        #print(queueInput)
        #i, j, parent = queue.get()
        if i < 0 or i >= n or j < 0 or j >= m or grid[i][j] == "#" or (i,j) in used:
            continue
        else:
            #grid[i][j] = new_color
            #print(parent)
            used.append((i,j))
            moves[parent] +=1
            queue.put((i+1, j, 'up', parent))
            queue.put((i-1, j, 'down', parent))
            queue.put((i, j+1, 'right', parent))
            queue.put((i, j-1, 'left', parent))
    return moves

def main():
  print("start")
  grid = [['0','*','0','0','0','0',],
          ['0','#','0','0','0','0',],
          ['#','#','0','0','0','0',],
          ['0','0','0','0','0','0',],
          ['0','0','0','0','0','0',],
          ['0','0','0','0','0','0',]]

  head = {'x':1, 'y':0}

  moves = flood_fill(grid, head)
  del moves['root']
  print(moves)
  print(sorted(moves.items(), key=lambda x:x[1],reverse=True))
  
main()