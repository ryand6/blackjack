"""
Author : Ryan <ryandowney64@yahoo.com>
Date   : 2022-08-31
"""


import random
from typing import NamedTuple, Optional
import os
import sys
import time


p_vals = []
d_vals = []


class PlayerCard():
    side = "Player"
    suit = None
    card = None
    val = 0
    num_aces = 0


class DealerCard(PlayerCard):
    side = "Dealer"
    hidden = False


class State(NamedTuple):
    quit: bool = False
    hit: bool = False
    stick: bool = False
    error: Optional[str] = None
    blackjack: bool = False
    bust: bool = False


def main():
    state = State()

    suits = ["♠", "♥", "♦", "♣"]
    cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    deck = []
    for i in range(len(suits)):
        for j in range(len(cards)):
            deck += [(cards[j], suits[i])]
            deck = list(deck)

    clear()
    
    pcards = []
    global p_vals
    p_ace = False
    p_10 = False

    for x in range(1, 3):

        # randomly pick a card from the deck to form part of the player's starting hand
        get_card(PlayerCard, deck)

        # if ace hasn't been found before in hand
        if not p_ace:
            p_ace = is_ace(PlayerCard)

        # if card equivalent to 10 hasn't been found before in hand
        if not p_10:
            p_10 = is_10(PlayerCard)

        # remove the card from the deck when picked
        deck.remove((PlayerCard.card, PlayerCard.suit))

        # show the players starting hand card by card
        print(f"Player card {x} : ")
        
        time.sleep(0.5)  

        print(f"{print_card(PlayerCard)}")

        # create list containing ascii art as strings for each card in hand
        pcards.append(print_card(PlayerCard))

        # call function to get the value of the player's card
        get_card_val(PlayerCard, sum(p_vals))

        # create list containing the value of each card in the player's hand
        p_vals.append(PlayerCard.val)

        time.sleep(1.5)
    
    clear()

    print("Your starting cards: ")

    time.sleep(0.5)  

    # print cards using format function so that they're displayed next to eachother on the screen
    print(format_cards(pcards))

    time.sleep(1.5)

    print("Dealer's starting cards: ")

    dcards = []
    global d_vals
    d_ace = False
    d_10 = False
    for x in range(2):

        # if card is the second in the dealer's hand, mark it as a card that should be presented face down
        if x == 1:
            setattr(DealerCard, "hidden", True)

        get_card(DealerCard, deck)

        if not d_ace:
            d_ace = is_ace(DealerCard)

        if not d_10:
            d_10 = is_10(DealerCard)

        deck.remove((DealerCard.card, DealerCard.suit))

        dcards.append(print_card(DealerCard))

        get_card_val(DealerCard, sum(d_vals))

        d_vals.append(DealerCard.val)

    time.sleep(0.5)  

    print(format_cards(dcards))

    time.sleep(1)

    # change hidden attribute to False so that all dealer's cards are shown face up going forward
    setattr(DealerCard, "hidden", False)
    dcards[1] = print_card(DealerCard)

    # call function to see if there are any blackjacks
    if is_blackjack(state, p_ace, p_10):
        # replace the state so that a second blackjack can be recorded if the dealer also has one
        state._replace(blackjack=False)
        # if both have a blackjack, call the game a tie
        if is_blackjack(state, d_ace, d_10):
            print("Tie! Both Player and Dealer have blackjack!!\n")
            time.sleep(5)
            quit()
        # if only player has blackjack, they win
        else:
            print("Player wins with blackjack!!\n")
            time.sleep(5)
            quit()
    # if dealer has blackjack, show the hidden card and announce the dealer's won
    elif is_blackjack(state, d_ace, d_10):
        print("Dealer's hand: \n")
        time.sleep(0.5)  
        print(format_cards(dcards))
        print("Dealer wins with blackjack!!\n")
        time.sleep(5)
        quit()

    print("Player's turn to hit or stick: \n")

    time.sleep(0.5)  

    while True:
        state = player_turn(state)
        print()   

        time.sleep(0.5)  

        if state.error:
            print(state.error)

        # add another card from the deck to the player's hand
        if state.hit:
            time.sleep(0.5)  
            get_card(PlayerCard, deck)
            deck.remove((PlayerCard.card, PlayerCard.suit))
            pcards.append(print_card(PlayerCard))
            get_card_val(PlayerCard, sum(p_vals))
            p_vals.append(PlayerCard.val)
            # if sum of player's hand is over 21, store that they've gone bust
            if sum(p_vals) > 21:
                state = calculate_if_bust(PlayerCard, state)
            print("Player's cards: ")
            time.sleep(0.5)  
            print(format_cards(pcards))
            time.sleep(0.5)  

        # if player has gone bust, print that the dealer has won
        if state.bust:
            print("Dealer's hand: ")
            time.sleep(0.5)  
            print(format_cards(dcards))
            time.sleep(0.5)  
            print(f"Dealer wins with {sum(d_vals)}! Player has gone bust!\n")
            time.sleep(5)
            quit()

        if state.stick:
            print("Player has chosen to stick\n")
            time.sleep(1)  
            break
        elif state.quit:
            sys.exit("Player has quit the game\n")
        
        state = state._replace(hit=False, bust=False, stick=False)

    time.sleep(0.5)  
    
    clear()
    
    print("Dealer's turn to hit or stick: \n")
    
    time.sleep(0.5)  

    while True:
        time.sleep(0.5)

        if sum(d_vals) < 17:
            get_card(DealerCard, deck) 
            deck.remove((DealerCard.card, DealerCard.suit))
            dcards.append(print_card(DealerCard))
            get_card_val(DealerCard, sum(d_vals))
            d_vals.append(DealerCard.val)
            print("Dealer's cards: ")
            time.sleep(0.5)  
            print(format_cards(dcards))
            time.sleep(0.5)   
        elif sum(d_vals) > 21:
            state = calculate_if_bust(DealerCard, state)
            if state.bust:
                print("Player's hand: ")
                time.sleep(0.5)  
                print(format_cards(pcards))
                time.sleep(0.5)  
                print(f"Player wins with {sum(p_vals)}! Dealer has gone bust!\n")
                time.sleep(5)
                quit()
        else:
            break

    clear()

    # if neither has gone bust after making their plays, print the hand of both the player and dealer
    print("Player's final cards: \n")
    time.sleep(0.5)  
    print(format_cards(pcards))
    time.sleep(0.5)  

    print("Dealer's final cards: \n")
    time.sleep(0.5)  
    print(format_cards(dcards))
    time.sleep(0.5)

    # declare winner based on closest hand to 21
    if sum(p_vals) < sum(d_vals):
        print(f"Dealer wins with {sum(d_vals)}!!\n")
        time.sleep(5)
        quit()
    elif sum(p_vals) > sum(d_vals):
        print(f"Player wins with {sum(p_vals)}!!\n")
        time.sleep(5)
        quit()
    else:
        print(f"It's a tie!\n")   
        time.sleep(5)
        quit()


def calculate_if_bust(Card, state):
    global p_vals, d_vals

    if Card.side == "Player": 
        vals = p_vals
    elif Card.side == "Dealer": 
        vals = d_vals
    
    while sum(vals) > 21:
        if Card.num_aces > 0:
            ace_index = vals.index(11)
            vals[ace_index] = 1
            Card.num_aces = Card.num_aces - 1
        else:
            return state._replace(bust=True)
    
    return state


def is_ace(Card):
    return Card.card == "A"


def is_10(Card):
    return Card.card in ["10", "J", "Q", "K"]


def is_blackjack(State, ace, _10) -> State:
    if all([ace, _10]):
        return State._replace(blackjack=True)


def clear():
    return os.system('cls' if os.name == 'nt' else 'clear')


def format_cards(cards):
    # format the cards as ascii art so that the can be printed side by side to form the player's hand
    card_split = [card.split("\n") for card in cards]
    zipped = zip(*card_split)
    output = ""
    for elems in zipped:
        output += "  ".join(elems) + "\n"
    return output


def player_turn(State) -> State:
    # ask for the player's input, checking for any errors
    move = input("What is your move? [h to hit] [s to stick] [q to quit] ")
    if move not in ["h", "s", "q"]:
        return State._replace(error=f'Input "{move}" invalid - please enter either "h" to hit, or "s" to stick. Otherwise enter "q" to quit game\n')
    elif move == "h":
        return State._replace(hit=True)
    elif move == "s":
        return State._replace(stick=True)
    elif move == "q":
        return State._replace(quit=True)


def print_card(Card):
    # second dealer's cards dealt is shown face down and therefore hidden
    if Card.side == "Dealer":
        if Card.hidden == True:
            return r"""
 ____________________ 
|                    |
|       ______       |
|      /  __  \      |
|     /  /  \  \     |
|     \ /    \  \    |
|           /  /     |
|          /  /      |
|         |  |       |
|         |__|       |
|          __        |
|         |__|       |
|                    |
|____________________|
"""
    # if the card is a 10, need special formatting to account for the extra character
    if Card.card == "10":
        return f"""
 ____________________ 
|                    |
|   {Card.card}               |
|                    |
|                    |
|                    |
|                    |
|         {Card.suit}          |
|                    |
|                    |
|                    |
|                    |
|                {Card.card}  |
|____________________|
"""
    else:
        return f"""
 ____________________ 
|                    |
|   {Card.card}                |
|                    |
|                    |
|                    |
|                    |
|         {Card.suit}          |
|                    |
|                    |
|                    |
|                    |
|                {Card.card}   |
|____________________|
"""


def get_card(Card, deck):
    # update the card class' suit and card attributes once picked from the deck
    card = random.choice(deck)
    setattr(Card, "suit", card[1])
    setattr(Card, "card", card[0])
    return Card


def get_card_val(Card, sum):
    val = Card.val
    card = Card.card

    if card in ["2", "3", "4", "5", "6", "7", "8", "9", "10"]:
        setattr(Card, "val", int(card))
    # Jack, Queen and King values are all equal to 10
    elif card in ["J", "Q", "K"]:
        setattr(Card, "val", 10)
    # if the card is an ace, it is equal to 11 unless the sum of the hand is equal to 11 or more
    if card == "A":
        val = 11 if sum < 11 else 1
        if val == 11:
            Card.num_aces += 1
        setattr(Card, "val", val)
    return Card


if __name__ == "__main__":
    main()