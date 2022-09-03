# Blackjack

Game of Blackjack written in Python (version Python 3.10.2)

1 Player versus computer (the Dealer).

Goal is to end the game with a sum of their hand closer to 21 than the dealer's hand. If either side goes above 21, they have gone bust and lose the game.

Jack's, King's and Queen's are all worth a value of 10. An Ace is worth either 1 or 11, it's value is not set in stone and changes depending on the situation
i.e. if the sum of the player's hand is equal to 13 and they pick another card which ends up being an ace, the ace's value can only be equal to 1, else the player
would go bust.

Both sides get two cards from the deck to begin with. The player's two cards are both face up whilst the dealer has one card face up and one card face down.

If the player's initial hand is a card equal to a 10 and an ace, they automatically win with a "blackjack". The same goes for the dealer, however their hidden card is
turned face up before declaring the win. If both sides have a blackjack, the game is a tie.

If neither side has a blackjack, the game continues, starting with the player's turn. Here the player must choose to either stick or hit. The player chooses these 
options via input to the program. They will receive a prompt explaining correct inputs for each option ("h" to hit, "s" to stick, "q" to quit the game). If the player's
input does not match any of these prompts, an error will be printed and the player will be asked for their input again.

To stick is to declare that the player no longer wants to add any more cards to their hand from the deck. If the player chooses to hit, they are declaring that they are 
picking another card, and thus takes another card from their deck and adds it to their hand face up. It remains the player's turn until they decide to stick, or if 
they go bust by the sum of their hand exceeding 21.

If the player goes bust, the dealer automatically wins.

If the player hasn't gone bust and sticks, it is now the dealer's turn. This time, all of the dealer's cards are face up. If the sum of the dealer's hand is less 
than 17, they will take another card from the deck. This continues until either than sum of the dealer's hand is 17 or more, or if they go bust. If the dealer 
goes bust, the player wins.

If both the player and dealer haven't bone bust and both have stopped taking cards from the deck, the final hand of each is then shown and the sum of each hand is
compared.

The closest to 21 wins, however if the sums are equal to eachother, the game ends in a tie.
