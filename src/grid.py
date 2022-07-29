from cell import gridCell

class grid():
  def __init__(self, gridSize, board):
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
      self.grid[head['y']['x']].isOtherSnakeHead = True
      self.grid[head['y']['x']].isObstacle = True

    for part in board['you']['body']:
      self.grid[part['y']][part['x']].isSelf = True
      self.grid[part['y']][part['x']].isObstacle = True

    myHead = board['you']['head']
    self.grid[myHead['y']][myHead['x']].isHead = True

  def getGrid(self):
    return self.grid

  def serialize(self):
    print(self.grid)