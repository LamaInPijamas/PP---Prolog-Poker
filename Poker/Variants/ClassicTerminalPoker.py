# ------------------ [ Includes ] ------------------ # 
from Core.Core import Core
import os

# ------------------ [ Easy Poker class ] ------------------ # 
class ClassicTerminalPoker:
  core = None
  player_move = 0
  def __init__(self, core : Core):
    self.core = core

  def clear_terminal(self):
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

  # Terminal version
  def run(self):
      self.clear_terminal()

      for round_no in range(self.core.rounds):
        self.core.reset()

        for i in range(len(self.core.players)):
            player = self.core.players[i]
            hand = self.core.deal[i]
            print(f"--- Round {round_no + 1} ---")
            print(f"{player.nick}")
            input("Press to show deal")
            print(f"Hand: {hand}")
            print(f"Choose up to {self.core.max_draw} cards to draw (indexes 0–4). Type any non-digit to finish:".format(self.core.max_draw))
            cards = []
            for _ in range(self.core.max_draw):
                print("> ", end="")
                card = input()
                if card.isdigit() and (0 <= int(card) <= 4): 
                  cards.append(int(card))
                else: 
                  break
            self.core.draw(i, cards)
            self.clear_terminal()

      # Evaluation phase
      points = self.core.evaluate()
      print("\n--- Results ---")
      for i, player in enumerate(self.core.players):
          print(f"{player.nick} final hand: {self.core.deal[i]} -> Points: {points[i]}")

      winner = points.index(max(points))
      print(f"\n🏆 Winner of Round {round_no + 1}: {self.core.players[winner].nick}!\n")