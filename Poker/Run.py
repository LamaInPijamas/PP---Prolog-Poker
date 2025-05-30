from Core.Core import Core
from Variants.ClassicTerminalPoker import ClassicTerminalPoker


# [TODO] This will be ran on rails python env
players = [["Daniel"], ["Ruslan"]]
core = Core(players, 3)
easy_poker = ClassicTerminalPoker(core)
easy_poker.run()
