from pyswip import Prolog

prolog = Prolog()
prolog.consult("Main.pl")
hand = list(prolog.query("get_hand1(L,T)."))[0]
print(hand)