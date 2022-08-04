from queue import Queue
#flood fill implementation 

class gridCell:
  def __init__(self): #important attributes to know for each cell in the grid
    self.isSelf = False 
    self.myHead = False
    self.isFood = False
    self.isOtherSnakeBody = False
    self.isOtherSnakeHead = False
    self.isObstacle = False

  #setter functions
  def thisIsSelf(self):
    self.isSelf = True
    self.myHead = False
    self.isFood = False
    self.isOtherSnakeBody = False
    self.isOtherSnakeHead = False
    self.isObstacle = True

  def thisIsHead(self):
    self.isSelf = True
    self.myHead = True
    self.isFood = False
    self.isOtherSnakeBody = False
    self.isOtherSnakeHead = False
    self.isObstacle = False

  def thisIsFood(self):
    self.isSelf = False
    self.myHead = False
    self.isFood = True
    self.isOtherSnakeBody = False
    self.isOtherSnakeHead = False
    self.isObstacle = False

  def thisIsOtherSnakeBody(self):
    self.isSelf = False
    self.myHead = False
    self.isFood = False
    self.isOtherSnakeBody = True
    self.isOtherSnakeHead = False
    self.isObstacle = True
    
  def thisIsOtherSnakeHead(self):
    self.isSelf = False
    self.myHead = False
    self.isFood = False
    self.isOtherSnakeBody = False
    self.isOtherSnakeHead = True
    self.isObstacle = True


  #str representation is nice for logs
  def __str__(self):
    if self.myHead:
      return '&'
    if self.isObstacle:
      return '#'
    if self.isFood:
      return '*'
    return '0'

    
class grid():
  def __init__(self, gridSize, data):
    #we want to initialize a 2D array representation of the board given the game state
    board = data['board']
    self.grid = []
    for i in range(gridSize):
      row = []
      for j in range(gridSize):
        row.append(gridCell())
      self.grid.append(row)

    for food in board['food']: #add all food
      self.grid[food['y']][food['x']].thisIsFood()

    for snake in board['snakes']: #add all enemy snakes
      for part in snake['body']: 
        cell = self.grid[part['y']][part['x']]
        cell.isOtherSnakeBody = True
        cell.isObstacle = True
      head = snake['head']
      self.grid[head['y']][head['x']].thisIsOtherSnakeHead()
      #self.grid[head['y']][head['x']].thisIsObstacle()

    for part in data['you']['body']: #add yourself to the board
      self.grid[part['y']][part['x']].thisIsSelf()
      #self.grid[part['y']][part['x']].thisIsObstacle()

    myHead = data['you']['head']
    self.grid[myHead['y']][myHead['x']].thisIsHead()

  def getGrid(self):
    return self.grid

  def serialize(self): 
    #turns 2D array of ojects into 2D array of strings
    #grid.serialize() to see the gamestate at any point
    serializedArray = []
    for row in self.grid:
      serializedArray.append([str(x) for x in row])
    return serializedArray

def flood_fill(grid, head):
  #return the best move
  n = len(grid)
  m = len(grid[0])
  i, j = head['y'], head['x']
  moves = {'right':0, 'left':0, 'up':0, 'down':0, 'root':0}
  if grid[i][j].isObstacle:
      return moves

  queue = Queue()
  queue.put((i, j, 'root', None))
  used = []
  while not queue.empty():
      queueInput = queue.get()
      i, j = queueInput[0], queueInput[1]
      if queueInput[3] == None or queueInput[3] == 'root':
        parent = queueInput[2]
      else:
        parent = queueInput[3]
      if i < 0 or i >= n or j < 0 or j >= m or grid[i][j].isObstacle or (i,j) in used:
          continue
      else:
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
  print(moves)
#main()