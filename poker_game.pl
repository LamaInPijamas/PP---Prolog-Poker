% --- Definicja kolorów ---
suit(hearts).
suit(diamonds).
suit(clubs).
suit(spades).

% --- Definicja rang ---
rank(2).
rank(3).
rank(4).
rank(5).
rank(6).
rank(7).
rank(8).
rank(9).
rank(10).
rank(jack).
rank(queen).
rank(king).
rank(ace).

card(Suit, Rank) :-
    suit(Suit),
    rank(Rank).

deck(Deck) :-
    findall(card(Suit,Rank), card(Suit,Rank), Deck).

shuffle_deck(Shuffled) :-
    deck(Deck),
    random_permutation(Deck, Shuffled).

get_hand1(L, T) :-
    shuffle_deck(D),
    D = [X,Y,Z,W,H|T],
    L = [X,Y,Z,W,H].

write_to_file(FileName, Content) :-
    open(FileName, write, Stream),   % otwórz plik do zapisu (nadpisanie)
    write(Stream, Content),          % zapisz Content
    nl(Stream),                      % dodaj znak nowej linii
    close(Stream).                   % zamknij strumień
