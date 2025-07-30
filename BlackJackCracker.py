#BlackJack Cracker
import random
import bjfunctions as bjf 
import os

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = self.calculate_value(rank)

    def calculate_value(self, rank):
        if rank in ['Jack', 'Queen', 'King']:
            return 10
        elif rank == 'Ace':
            return 11
        else:
            match rank:
                case '2':
                    return 2
                case '3':
                    return 3
                case '4':
                    return 4
                case '5':
                    return 5
                case '6':
                    return 6
                case '7':
                    return 7
                case '8':
                    return 8
                case '9':
                    return 9
                case '10':
                    return 10
                case _:
                    raise ValueError("Invalid card rank")
        return int(rank) if rank.isdigit() else 0


    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
class Deck:
    def __init__(self):
        self.cards = []
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))
    
    def shuffle(self):
        random.shuffle(self.cards)

# Initialize game variables
n_decks = 6 
N_PLAYERS = 1
n_players = N_PLAYERS 
n_games = 10000
win_draw_loss = [0] * 3
bot_place = random.randint(0, n_players - 1)  # Randomly select AI position
balance = [1000] * n_players  # Starting balance for each player
deck_penetration = 0.2  # Percentage of the deck to be used before reshuffling

# Function to start a match
def restart_match(n_decks):
    game = []
    for i in range(n_decks):
        deck = Deck()
        game.extend(deck.cards)

    # Shuffle the game deck
    random.shuffle(game)
    
    return game

# Restart the match with a new shuffled deck
game = restart_match(n_decks)
total_hands = 0

for g in range(n_games):
    n_players = N_PLAYERS  # Reset player count for each game
    
    # Initialize the table and bets
    bets = [1] * n_players
    [table, game] = bjf.deal_cards(game, n_players)
    
    p = 0
    while p < n_players:
        player_hand = table[p]
        dealer_card = table[n_players].cards[0]
        decision = 1 # Start with a hit decision

        while player_hand.get_sum() < 21 and decision != 0:
            # os.system('cls')
            # print(player_hand)
            # print(f"Dealer's card value: {dealer_card.value}")

            decision = 1 # Default to hit
            if table[p].player_index == bot_place:
                decision = bjf.decide_best_move(dealer_card, player_hand)
            else:
                decision = bjf.decide_best_move(dealer_card, player_hand)

            #print(f"Decision: {decision}")
            
            bets = bjf.update_bets(bets, decision, p)
            [table, game] = bjf.play_hand(game, table, decision, p)
            
            if decision == 2:
                #print(player_hand)
                decision = 0 # After doubling down, player stands automatically
            if decision == 3:
                n_players += 1  # Increase player count for split

        # Check for blackjack
        if player_hand.get_sum() == 21 and len(player_hand.cards) == 2:
            bets[p] *= 1.5
        
        #print(player_hand)

        total_hands += 1
        p += 1

    # Dealer's turn
    dealer_hand = table[n_players]
    while dealer_hand.get_sum() < 17:
            dealer_hand.cards.append(game.pop())

    # Calculate results for each player
    for p in range(n_players):
        [balance, win_draw_loss] = bjf.check_wins(table,balance, bets, win_draw_loss, p)

    # For debugging purposes
    # bjf.debug_print(n_players, table, bets, balance, g)

    if len(game) < n_decks * 52 * deck_penetration:
        game = restart_match(n_decks)

# Print final statistics after all games
print(f"Balance after {total_hands} hands: {balance}")
print(f"Final statistics: wins: {round(win_draw_loss[0] * 100/(total_hands), 2)}%   draws: {round(win_draw_loss[1] * 100/(total_hands), 2)}%   losses: {round(win_draw_loss[2] * 100/(total_hands),2)}%")
            
            

