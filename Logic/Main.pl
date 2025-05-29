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

get_five_cards(Deck, [], Deck) :- length(Deck, L), L < 5.
get_five_cards([A,B,C,D,E|Rest], [A,B,C,D,E], Rest) :- length([A,B,C,D,E|Rest], L), L >= 5.

deal_cards(0, Deck, [], Deck).
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






% --- Poker Evaluation --- %
evaluate([], []).
evaluate([Hand|RestHands], [Point|RestPoints]) :-
    evaluate_hand(Hand, Point),
    evaluate(RestHands, RestPoints).

evaluate_hand(Hand, Points) :-
    ( royal_flush(Hand)       -> Points = 10
    ; straight_flush(Hand)    -> Points = 9
    ; four_of_a_kind(Hand)    -> Points = 8
    ; full_house(Hand)        -> Points = 7
    ; flush(Hand)             -> Points = 6
    ; straight(Hand)          -> Points = 5
    ; three_of_a_kind(Hand)   -> Points = 4
    ; two_pairs(Hand)         -> Points = 3
    ; one_pair(Hand)          -> Points = 2
    ; high_card(Hand)         -> Points = 1
    ).
  
% -- Helpers -- %
rank_value(2, 2).
rank_value(3, 3).
rank_value(4, 4).
rank_value(5, 5).
rank_value(6, 6).
rank_value(7, 7).
rank_value(8, 8).
rank_value(9, 9).
rank_value(10, 10).
rank_value(jack, 11).
rank_value(queen, 12).
rank_value(king, 13).
rank_value(ace, 14).

card_less(card(Rank1, _), card(Rank2, _)) :-
    rank_value(Rank1, V1),
    rank_value(Rank2, V2),
    V1 < V2.

compare_cards(Order, card(R1, S1), card(R2, S2)) :-
    rank_value(R1, V1),
    rank_value(R2, V2),
    ( V1 < V2 -> Order = <
    ; V1 > V2 -> Order = >
    ; % If ranks equal, compare suits alphabetically
      compare(Order, S1, S2)
    ).

sort_cards(Hand, SortedHand) :-
    predsort(compare_cards, Hand, SortedHand).

extract_ranks([], []).
extract_ranks([card(Rank, _) | T], [Rank | RT]) :-
    extract_ranks(T, RT).

count_rank([], _, 0).
count_rank([H|T], H, N) :-
    count_rank(T, H, N1),
    N is N1 + 1.
count_rank([H|T], X, N) :-
    H \= X,
    count_rank(T, X, N).

consecutive_ranks([_]).
consecutive_ranks([card(R1, _), card(R2, _)|T]) :-
    rank_value(R1, V1),
    rank_value(R2, V2),
    V2 =:= V1 + 1,
    consecutive_ranks([card(R2, _)|T]).

all_same_suit([card(_, _)]) :- !.
all_same_suit([card(_, Suit), card(_, Suit)|T]) :-
    all_same_suit([card(_, Suit)|T]).







% --- Poker Ranks --- %
royal_flush(Hand) :-
    length(Hand, 5),
    sort_cards(Hand, Sorted),
    Sorted = [
        card(10, Suit),
        card(jack, Suit),
        card(queen, Suit),
        card(king, Suit),
        card(ace, Suit)
    ].

straight_flush(Hand) :-
    length(Hand, 5),
    sort_cards(Hand, Sorted),
    all_same_suit(Sorted),
    consecutive_ranks(Sorted).

four_of_a_kind(Hand) :-
    length(Hand, 5),
    extract_ranks(Hand, Ranks),
    member(R, Ranks),
    count_rank(Ranks, R, 4).

full_house(Hand) :-
    length(Hand, 5),
    extract_ranks(Hand, Ranks),
    sort(Ranks, Unique),
    member(R1, Unique),
    member(R2, Unique),
    R1 \= R2,
    count_rank(Ranks, R1, 3),
    count_rank(Ranks, R2, 2).

flush(Hand) :-
    length(Hand, 5),
    all_same_suit(Hand).

straight(Hand) :-
    length(Hand, 5),
    sort_cards(Hand, Sorted),
    consecutive_ranks(Sorted).

three_of_a_kind(Hand) :-
    length(Hand, 5),
    extract_ranks(Hand, Ranks),
    member(R, Ranks),
    count_rank(Ranks, R, 3),
    \+ full_house(Hand).   % exclude full house (3+2)

two_pairs(Hand) :-
    length(Hand, 5),
    extract_ranks(Hand, Ranks),
    sort(Ranks, UniqueRanks),
    findall(R, (member(R, UniqueRanks), count_rank(Ranks, R, 2)), Pairs),
    length(Pairs, 2).

one_pair(Hand) :-
    length(Hand, 5),
    extract_ranks(Hand, Ranks),
    sort(Ranks, UniqueRanks),
    findall(R, (member(R, UniqueRanks), count_rank(Ranks, R, 2)), Pairs),
    length(Pairs, 1).

high_card(Hand) :-
    length(Hand, 5),
    \+ one_pair(Hand),
    \+ two_pairs(Hand),
    \+ three_of_a_kind(Hand),
    \+ straight(Hand),
    \+ flush(Hand),
    \+ full_house(Hand),
    \+ four_of_a_kind(Hand),
    \+ straight_flush(Hand),
    \+ royal_flush(Hand).

test_ranks(Royal_Flush, Straight_Flush, Four_Of_A_Kind, Full_House, Flush, Straight, Three_Of_A_King, Two_Pairs, One_Pair, High) :- 
    evaluate_hand([
        card(ace, spades),
        card(king, spades),
        card(queen, spades),
        card(jack, spades),
        card(10, spades)
    ], Royal_Flush),
   evaluate_hand([
        card(6, hearts),
        card(7, hearts),
        card(8, hearts),
        card(9, hearts),
        card(10, hearts)
    ], Straight_Flush),
    evaluate_hand([
        card(9, hearts),
        card(9, spades),
        card(9, diamonds),
        card(9, clubs),
        card(king, hearts)
    ], Four_Of_A_Kind),
    evaluate_hand([
       card(queen, hearts),
       card(queen, clubs),
       card(queen, spades),
       card(jack, diamonds),
       card(jack, hearts)
   ], Full_House),
   evaluate_hand([
       card(2, diamonds),
       card(6, diamonds),
       card(10, diamonds),
       card(jack, diamonds),
       card(king, diamonds)
   ], Flush),
   evaluate_hand([
       card(6, hearts),
       card(7, diamonds),
       card(8, clubs),
       card(9, spades),
       card(10, hearts)
   ], Straight),
   evaluate_hand([
        card(king, hearts),
        card(king, spades),
        card(king, diamonds),
        card(9, clubs),
        card(2, hearts)
    ], Three_Of_A_King),
    evaluate_hand([
    card(4, hearts),
    card(4, clubs),
    card(7, spades),
    card(7, diamonds),
    card(king, hearts)
    ], Two_Pairs),
    evaluate_hand([
    card(3, diamonds),
    card(3, clubs),
    card(9, hearts),
    card(10, spades),
    card(ace, diamonds)
    ], One_Pair),
    evaluate_hand([
    card(2, hearts),
    card(5, clubs),
    card(9, diamonds),
    card(jack, spades),
    card(ace, hearts)
    ], High).
