class Vector2:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    
  def tuple(self):
    return (self.x, self.y)

class Vector3:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z
    
  def tuple(self):
    return (self.x, self.y, self.z)
  