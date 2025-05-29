# ------------------ [ Include ] ------------------ # 
from pyswip import Prolog
import os

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
  
  def __init__(self, players : list):
    if(1 > len(players) or len(players) > 10): 
      raise ValueError("Invalid numbers of players!!!")
    # Set Players
    for i in range(len(players)):
      self.players.append(Player(i, players[i]))
    # Initialized game
    self.prolog.consult("Main.pl")
    self.reset()

  def __str__(self):
    string = ""
    for i in range(len(self.players)):
      string += str(self.players[i]) + " " + str(self.deal[i]) + "\n"
    string += str(self.deck)
    return string
  
  def reset(self):
    self.deck = list(self.prolog.query("create_deck(Deck)"))[0]['Deck']
    deal = list(self.prolog.query(f"deal_cards({'['+','.join(str(len(self.players)))+']'}, {self.deck}, Deal, Rest)"))[0]
    self.deck = deal['Rest']
    self.deal = deal['Deal']
  
  def draw(self, playerId : int, cardsIndex : list):
    if(len(cardsIndex) > 3):
      raise ValueError("Chosen to many cards!!!")
    if(playerId > len(self.players)):
      raise ValueError(f"No player with index {playerId}!!!")
    update = list(self.prolog.query(f"draw({'['+','.join(self.deck)+']'}, {'['+','.join(self.deal[playerId])+']'}, {cardsIndex}, Deal, Deck)"))[0]
    self.deal[playerId] = update['Deal']
    self.deck = update['Deck']

  def evaluate(self):
    deals = []
    for hand in self.deal:
        string = '[' + ', '.join(hand) + ']'
        deals.append(string)
    return list(self.prolog.query(f"evaluate({'['+','.join(deals)+']'}, Points)"))[0]['Points']

  def getPlayersInfo(self):
    table = []
    for i in range(len(self.players)):
      table.append([self.players[i].getInfo(), self.deal[i]])
    return table

# ------------------ [ Core Poker class ] ------------------ # 
class EasyPoker:
  core = None
  player_move = 0
  rounds = 1
  def __init__(self, core : CorePoker, rounds = 1):
    self.core = core
    self.rounds = rounds

  def clear_terminal(self):
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

  # Terminal version
  def run(self):
    self.clear_terminal()
    for _ in range(self.rounds):
      for i in range(len(self.core.players)):
        print(self.core.players[i])
        input("Show deal: press enter")
        print(self.core.deal[i])
        cards = []
        print("Chose cards to draw (type exit to end)")
        for j in range(3):
          print("> ", end="")
          card = input()
          if(card.isdigit() and (0 <= int(card) <= 4)):
            cards.append(int(card))
          else: break
        self.clear_terminal()
        self.core.draw(i, cards) 
    return self.core.evaluate()
    

# ------------------ [ Main ] ------------------ # 
core = CorePoker([["Daniel"], ["Ruslan"]])
game = EasyPoker(core, 2)
print(game.run())