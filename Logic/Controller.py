from pyswip import Prolog

# Player class 
class Player:
  id = -1
  def __init__(self, id):
    self.id = id

# Base Game initialization and actions in poker
class Poker:
  prolog = Prolog()
  deck = []
  deal = []
  
  def __init__(self, players=2):
    if(2 > players or players > 10): 
      raise ValueError("Invalid numbers of players!!!")

    self.prolog.consult("Main.pl")
    self.deck = list(self.prolog.query("create_deck(Deck)"))[0]['Deck']
    deal = list(self.prolog.query(f"deal_cards({players}, {self.deck}, Deal, Rest)"))[0]
    self.deck = deal['Rest']
    self.deal = deal['Deal']

  def getPlayerInfo(playerId):
    pass

  def check(self, playerId):
    pass

  def fold(self, playerId):
    pass

  def bet(self, playerId, amount):
    pass






game = Poker(2)
