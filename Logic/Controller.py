from pyswip import Prolog

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
  

# ------------------ [ Core Poker class ] ------------------ # 
class CorePoker:
  prolog = Prolog()
  deck = []
  players = []
  deal = []
  
  def __init__(self, players):
    if(2 > len(players) or len(players) > 10): 
      raise ValueError("Invalid numbers of players!!!")

    # Set Players
    for i in range(len(players)):
      self.players.append(Player(i, players[i]))

    # Initialized game
    self.prolog.consult("Main.pl")
    self.deck = list(self.prolog.query("create_deck(Deck)"))[0]['Deck']
    deal = list(self.prolog.query(f"deal_cards({len(players)}, {self.deck}, Deal, Rest)"))[0]
    self.deck = deal['Rest']
    self.deal = deal['Deal']

  def __str__(self):
    string = ""
    for i in range(len(self.players)):
      string += str(self.players[i]) + " " + str(self.deal[i]) + "\n"
    string += str(self.deck)
    return string

  def getPlayersInfo(self):
    table = []
    for i in range(len(self.players)):
      table.append([self.players[i].getInfo(), self.deal[i]])
    return table


# ------------------ [ Main ] ------------------ # 
core = CorePoker([["Daniel"], ["Ruslan"]])
print(core)

