# ------------------ [ Include ] ------------------ # 
from Core.Player import Player
from pyswip import Prolog
import os

# ------------------ [ Core Poker class ] ------------------ # 
class Core:
  prolog = Prolog()
  deck = []
  players = []
  deal = []
  max_draw = 3
  rounds = 3
  
  def __init__(self, players : list, rounds : int = 3, max_draw : int = 3):
    if(1 > len(players) or len(players) > 10): 
      raise ValueError("Invalid numbers of players!!!")
    if(max_draw < 0 or max_draw > 4):
      raise ValueError("Invalid max draw!!!")
    if(rounds < 0):
      raise ValueError("Invalid rounds!!!")
    self.max_draw = max_draw
    self.rounds = rounds
    
    # Set Players
    for i in range(len(players)):
      self.players.append(Player(i, players[i]))
    # Initialized game
    self.prolog.consult("Logic.pl")
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
    if(len(cardsIndex) > self.max_draw):
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