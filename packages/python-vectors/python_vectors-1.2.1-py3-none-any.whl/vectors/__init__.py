# ----------------------------------------------------------------- #
#                              IMPORTS                              #
# ----------------------------------------------------------------- #

from fractions import Fraction

# ----------------------------------------------------------------- #
#                           VECTOR CLASSES                          #
# ----------------------------------------------------------------- #

class Vector2:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    
  def add(self, v):
    if isinstance(v, Vector3):
      v = Vector2(v.x, v.y)
    self.x += v.x
    self.y += v.y
  
  def subtract(self, v):
    if isinstance(v, Vector3):
      v = Vector2(v.x, v.y)
    self.x -= v.x
    self.y -= v.y
    
  def multiply(self, v):
    if isinstance(v, Vector3):
      v = Vector2(v.x, v.y)
    self.x *= v.x
    self.y *= v.y
  
  def divide(self, v):
    if isinstance(v, Vector3):
      v = Vector2(v.x, v.y)
    self.x /= v.x
    self.y /= v.y
    
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
    
  def add(self, v):
    if isinstance(v, Vector2):
      v = Vector3(v.x, v.y, 0)
    self.x += v.x
    self.y += v.y
    self.z += v.z
    
  def subtract(self, v):
    if isinstance(v, Vector2):
      v = Vector3(v.x, v.y, 0)
    self.x -= v.x
    self.y -= v.y
    self.z -= v.z
    
  def multiply(self, v):
    if isinstance(v, Vector2):
      v = Vector3(v.x, v.y, 0)
    self.x *= v.x
    self.y *= v.y
    self.z *= v.z
    
  def divide(self, v):
    if isinstance(v, Vector2):
      v = Vector3(v.x, v.y, 1)
    self.x /= v.x
    self.y /= v.y
    self.z /= v.z
    
  def tuple(self):
    return (self.x, self.y, self.z)
  
  def list(self):
    return [self.x, self.y, self.z]
  
  def dict(self):
    return {"x": self.x, "y": self.y, "z": self.z}
  
class Slope:
  def __init__(self, rise, run):
    self.rise = rise
    self.run = run
  
  def tuple(self):
    return (self.rise, self.run)
  
  def list(self):
    return [self.rise, self.run]
  
  def dict(self):
    return {"rise": self.rise, "run": self.run}
  
  def string(self):
    return f"{self.rise}/{self.run}"
  
  def simplify(self):
    fract = str(Fraction(self.rise, self.run))
    fract_split = fract.split("/") if "/" in fract else [fract, 1]
    self.rise = int(fract_split[0])
    self.run = int(fract_split[1])
    
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

def find_slope(v1, v2):
  return Slope(v2.y - v1.y, v2.x - v1.x)

# ----------------------------------------------------------------- #
#                            GENERATION                             #
# ----------------------------------------------------------------- #

def generate_square_matrix(v1, v2):
  (startX, startY) = (v1.x, v1.y)
  (endX, endY) = (v2.x, v2.y)
  matrix = []
  while startY < endY:
    row = []
    while startX < endX:
      startX += 1
      row.append(Vector2(startX, startY))
    startX = v1.x
    startY += 1
    matrix.append(row)
  return matrix