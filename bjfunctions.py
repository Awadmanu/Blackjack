def deal_cards(game, n_players):
    table = [Hand(p) for p in range(n_players + 1)]  # +1 for dealer
    for j in range(2):
        for i in range(n_players):
            table[i].cards.append(game.pop())
        
        table[n_players].cards.append(game.pop()) # Dealer's cards
    
    return table, game

class Hand:
    def __init__(self, player_index):
        self.cards = []
        self.player_index = player_index

    def calculate_hand_value(self):
        self.sum = 0
        aces = 0
        self.soft = False
        self.pair = False
        
        for card in self.cards:
            self.sum += card.value
            if card.rank == 'Ace':
                aces += 1
        

        while self.sum > 21 and aces > 0:
            self.sum -= 10
            aces -= 1
        
        if self.sum < 21 and aces > 0:
            self.soft = True
        
        if len(self.cards) == 2 and len(set(card.rank for card in self.cards)) == 1:
            self.pair = True

    def get_sum(self):
        self.calculate_hand_value()
        return self.sum
    
    def get_soft(self):
        self.calculate_hand_value()
        return self.soft
    
    def get_pair(self):
        self.calculate_hand_value()
        return self.pair
            
    def __str__(self):
        self.calculate_hand_value()
        return f'{[str(card) for card in self.cards]}, sum: {self.sum}, soft: {self.soft}, pair: {self.pair}'
    
def play_hand(game, table, decision, p):
    player_hand = table[p]  

    # 0 = stand, 1 = hit, 2 = double down, 3 = split
    match decision:
        case 1:  # Hit
            player_hand.cards.append(game.pop())  
        case 2: # Double down
            player_hand.cards.append(game.pop())
        case 3:  # Split
            table.insert(p + 1,Hand(player_hand.player_index)) # Create a new hand for the split
            new_hand = table[p + 1]
            new_hand.cards.append(player_hand.cards.pop())  # Move one card to the new hand
            new_hand.cards.append(game.pop())  # Add a new card to the new hand
            player_hand.cards.append(game.pop()) # Add a new card to the original hand
        case _: # Stand or invalid decision
            pass
        
    table[p] = player_hand  # Update player's hand in the table

    return table, game

def decide_best_move(dealer_card, player_hand):
    if player_hand.get_pair():
        match player_hand.cards[0].value:
            case 11:
                decision = 3 if dealer_card.value < 11 else 1
            case 10:
                decision = 0
            case 2 | 3 | 7:
                decision = 3 if dealer_card.value < 8 else 1
            case 4:
                decision = 3 if dealer_card.value in [5, 6] else 1
            case 5:
                decision = 2 if dealer_card.value < 10 else 1
            case 6:
                decision = 3 if dealer_card.value < 7 else 1
            case 8:
                decision = 2 if dealer_card.value < 10 else 1
            case 9:
                decision = 0 if dealer_card.value in [7, 10, 11] else 3
            case _:
                raise ValueError(f"Unexpected card value: {player_hand.cards[0].value}")
    elif player_hand.get_soft():
        match player_hand.get_sum():
            case 20 | 19:
                decision = 0
            case 13 | 14:
                decision = 2 if dealer_card.value in [5,6] else 1
            case 15 | 16:
                decision = 2 if dealer_card.value in [4,5,6] else 1
            case 17:
                decision = 2 if dealer_card.value in [3,4,5,6] else 1
            case 18:
                if dealer_card.value in [3,4,5,6]:
                    decision = 2
                else:
                    if dealer_card.value < 9:
                        decision = 0
                    else:
                        decision = 1
            case _:
                raise ValueError(f"Unexpected soft hand value: {player_hand.get_sum()}")
    else:
        match player_hand.get_sum():
            case 20 | 19 | 18 | 17:
                decision = 0
            case 16 | 15 | 14 | 13:
                decision = 0 if dealer_card.value < 7 else 1
            case 12:
                decision = 0 if dealer_card.value in [4,5,6] else 1
            case 11 | 10:
                decision = 2 if dealer_card.value < 10 else 1
            case 9:
                decision = 2 if dealer_card.value in [3,4,5,6] else 1
            case 8 | 7 | 6 | 5:
                decision = 1
            case _:
                raise ValueError(f"Unexpected soft hand value: {player_hand.get_sum()}")
                
    if player_hand.get_sum() >= 21:
        decision = 0

    return decision

def update_bets(bets, decision, p):
    if decision == 2:  # Double down
        bets[p] *= 2
    elif decision == 3:  # Split
        bets.insert(p+1, bets[p])  # Add a new bet for the split hand
    return bets

def check_wins(table,balance, bets, win_draw_loss, p):
    player_hand = table[p]
    dealer_hand = table[-1]  # Dealer's hand is the last in the table
    player = table[p].player_index # Player index for balance tracking
    if player_hand.get_sum() > 21:
        win_draw_loss[2] += 1  # Player loses
        balance[player] -= bets[p]
    elif dealer_hand.get_sum() > 21 or player_hand.get_sum() > dealer_hand.get_sum():
        win_draw_loss[0] += 1  # Player wins
        balance[player] += bets[p]
    elif player_hand.get_sum() == dealer_hand.get_sum():
        win_draw_loss[1] += 1 # Draw
    else:
        win_draw_loss[2] += 1  # Player loses
        balance[player] -= bets[p]

    return balance, win_draw_loss

def debug_print(n_players, table, bets, balance, g):
    for p in range(n_players):
        print(f"Player {p+1}: {table[p]}")
    # Dealer's final hand
    print(f"Dealer's: {table[n_players]}")
    print(f"Balance after game {g+1}: {balance}")
    print(f"Bets after game {g+1}: {bets}")
