# ----------------------------------------------------------------- #
#                           VECTOR CLASSES                          #
# ----------------------------------------------------------------- #

class Vector2:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    
  def tuple(self):
    return (self.x, self.y)
  
  def list(self):
    return [self.x, self.y]
  
  def dict(self):
    return {"x": self.x, "y": self.y}

class Vector3:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z
    
  def tuple(self):
    return (self.x, self.y, self.z)
  
  def list(self):
    return [self.x, self.y, self.z]
  
  def dict(self):
    return {"x": self.x, "y": self.y, "z": self.z}

# ----------------------------------------------------------------- #
#                          MATH OPERATIONS                          #
# ----------------------------------------------------------------- #

def add(v1, v2):
  (v1_v2, v2_v2) = (isinstance(v1, Vector2), isinstance(v2, Vector2))
  return Vector2(v1.x + v2.x, v1.y + v2.y) if v2_v2 else Vector3(v1.x + v2.x, v1.y + v2.y, v2.z) if v1_v2 else Vector3(v1.x + v2.x, v1.y + v2.y, v1.z if v2_v2 else v1.z + v2.z)

def subtract(v1, v2):
  (v1_v2, v2_v2) = (isinstance(v1, Vector2), isinstance(v2, Vector2))
  return Vector2(v1.x - v2.x, v1.y - v2.y) if v2_v2 else Vector3(v1.x - v2.x, v1.y - v2.y, v2.z) if v1_v2 else Vector3(v1.x - v2.x, v1.y - v2.y, v1.z if v2_v2 else v1.z - v2.z)

def multiply(v1, v2):
  (v1_v2, v2_v2) = (isinstance(v1, Vector2), isinstance(v2, Vector2))
  return Vector2(v1.x * v2.x, v1.y * v2.y) if v2_v2 else Vector3(v1.x * v2.x, v1.y * v2.y, v2.z) if v1_v2 else Vector3(v1.x * v2.x, v1.y * v2.y, v1.z if v2_v2 else v1.z * v2.z)

def divide(v1, v2):
  (v1_v2, v2_v2) = (isinstance(v1, Vector2), isinstance(v2, Vector2))
  return Vector2(v1.x / v2.x, v1.y / v2.y) if v2_v2 else Vector3(v1.x / v2.x, v1.y / v2.y, v2.z) if v1_v2 else Vector3(v1.x / v2.x, v1.y / v2.y, v1.z if v2_v2 else v1.z / v2.z)