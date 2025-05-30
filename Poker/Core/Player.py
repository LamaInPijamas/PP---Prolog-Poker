# ------------------ [ Player class ] ------------------ # 
class Player:
  id = -1
  nick = ""
  points = 0
  def __init__(self, id, properties, points = 0):
    self.id = id
    self.nick = properties[0]
    self.points = points
  
  def __str__(self):
    return str(self.id) + ": " + self.nick + " " + str(self.points)
  
  def getInfo(self):
    return [self.id, self.nick, self.points]