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

get_five_cards([A,B,C,D,E|Rest], [A,B,C,D,E], Rest).

deal_cards(0, Deck, [], Deck).
deal_cards(Players, Deck, [Cards|Deal], Rest) :-
    Players > 0,
    get_five_cards(Deck, Cards, NextDeck),
    NPlayers is Players - 1,
    deal_cards(NPlayers, NextDeck, Deal, Rest).

% --- Core Poker Actions ---
get_one_cards([A|Rest], A, Rest).

replace_at_index([_|T], 0, NewValue, [NewValue|T]).
replace_at_index([H|T], Index, NewValue, [H|R]) :-
    Index > 0,
    Index1 is Index - 1,
    replace_at_index(T, Index1, NewValue, R).

draw(Deck, Deal, [], Deal, Deck).
draw(Deck, Deal, [Index|Indexes], NewDeal, NewDeck) :- 
    get_one_cards(Deck, Card, RestDeck),
    replace_at_index(Deal, Index, Card, NewDeal),
    draw(RestDeck, NewDeal, Indexes, _, NewDeck).