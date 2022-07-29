import cell

class grid():
  def __init__(self, gridSize, board):
    self.grid = []
    for i in range(gridSize):
      row = []
      for j in range(gridSize):
        row.append(cell())
      self.grid.append(row)

    for food in board['food']:
      self.grid[food['y']][food['x']].isFood()

    for snake in board['snakes']:
      for part in snake['body']:
        self.grid[part['y']][part['x']].isOtherSnakeBody()
      head = snake['head']
      self.grid[head['y']['x']].isOtherSnakeHead()

    for part in board['you']['body']:
      self.grid[part['y']][part['x']].isSelf()

    myHead = board['you']['head']
    self.grid[myHead['y']][myHead['x']].isHead()

  def getGrid(self):
    return self.grid

  def serialize(self):
    print(self.grid)