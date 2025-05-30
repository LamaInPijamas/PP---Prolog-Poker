from Core.Core import Core
from Variants.MCCFRAIPoker import MCCFRAIPoker
from AI.MCCFR import MCCFR


# [TODO] This will be ran on rails python env
players = [["You"], ["AI"]]
core = Core(players)
mccfr = MCCFR(input_size=7, save_path="monte_carlos_5000.pt")
mccfr.load()
poker_ai = MCCFRAIPoker(core, mccfr, 3)
poker_ai.run()