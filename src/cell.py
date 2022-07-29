class gridCell:
  def __init__(self):
    self.isSelf = False
    self.isHead = False
    self.isFood = False
    self.isOtherSnakeBody = False
    self.isOtherSnakeHead = False
    self.isObstacle = False

  def isSelf(self):
    self.isSelf = True
    self.isObstacle = True

  def isHead(self):
    self.isHead = True

  def isFood(self):
    self.isFood = True

  def isOtherSnakeBody(self):
    self.isOtherSnakeBody = True
    self.isObstacle = True
    
  def isOtherSnakeHead(self):
    self.isOtherSnakeHead = True
    self.isObstacle = True

  def __str__(self):
    if self.isObstacle:
      return '#'
    if self.isFood:
      return '*'
    if self.isHead:
      return '&'
    return '0'
    