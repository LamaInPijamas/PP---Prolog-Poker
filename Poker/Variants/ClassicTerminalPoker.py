# ------------------ [ Includes ] ------------------ # 
from Core.Core import Core
import os

# ------------------ [ Easy Poker class ] ------------------ # 
class ClassicTerminalPoker:
  core = None
  player_move = 0
  rounds = 1
  def __init__(self, core : Core, rounds = 1):
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
        for j in range(self.core.max_draw):
          print("> ", end="")
          card = input()
          if(card.isdigit() and (0 <= int(card) <= 4)):
            cards.append(int(card))
          else: break
        self.clear_terminal()
        self.core.draw(i, cards) 
    print(self.core.evaluate())