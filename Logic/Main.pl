% --- Definitions of colors ---
suit(hearts).
suit(diamonds).
suit(clubs).
suit(spades).

% --- Definitions of rang ---
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

% --- Definitions ---

card(Suit, Rank) :-
    suit(Suit),
    rank(Rank).

% --- Initialization ---

create_deck(Shuffled) :-
    findall(card(Suit,Rank), card(Suit,Rank), Deck),
    random_permutation(Deck, Shuffled).

get_five_cards(Deck, Cards, Rest) :-
    Cards = [A,B,C,D,E],
    Deck = [A,B,C,D,E|Rest].

deal_cards(0, Deck, [], Deck).
deal_cards(Players, Deck, [Cards|Deal], Rest) :-
    Players > 0,
    get_five_cards(Deck, Cards, NextDeck),
    NPlayers is Players - 1,
    deal_cards(NPlayers, NextDeck, Deal, Rest).























% [NOTE] we don't need it
% write_to_file(FileName, Content) :-
%     open(FileName, write, Stream),   % otwórz plik do zapisu (nadpisanie)
%     write(Stream, Content),          % zapisz Content
%     nl(Stream),                      % dodaj znak nowej linii
%     close(Stream).                   % zamknij strumień
