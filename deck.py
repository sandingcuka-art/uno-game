import random

COLORS = ["Red", "Green", "Blue", "Yellow"]
NUMBERS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

def create_deck():
    """Create a simple Uno deck with number cards only"""
    deck = []
    for color in COLORS:
        for number in NUMBERS:
            deck.append(f"{color} {number}")
            if number != "0":  # Only one zero per color
                deck.append(f"{color} {number}")  # Two of other numbers
    random.shuffle(deck)
    return deck

def deal_cards(deck, num_players):
    """Deal 5 cards to each player"""
    hands = []
    for _ in range(num_players):
        hand = []
        for _ in range(5):
            if deck:
                hand.append(deck.pop())
        hands.append(hand)
    return hands

def can_play(card, top_card):
    """Check if a card can be played"""
    card_color, card_number = card.split()
    top_color, top_number = top_card.split()
    return card_color == top_color or card_number == top_number

def show_hand(player_hand, top_card):
    """Show player's hand and which cards can be played"""
    print(f"\nTop card: {top_card}")
    print("Your cards:")
    for i, card in enumerate(player_hand):
        if can_play(card, top_card):
            print(f"  {i+1}. {card} [CAN PLAY]")
        else:
            print(f"  {i+1}. {card}")

def play_game():
    """Main game function"""
    print("🎴 Welcome to Simple UNO! 🎴")
    print("Match cards by color or number!")
    
    # Setup game
    deck = create_deck()
    hands = deal_cards(deck, 2)  # 2 players
    discard_pile = [deck.pop()]  # Start with one card
    
    current_player = 0
    game_over = False
    
    while not game_over:
        print(f"\n{'='*40}")
        print(f"Player {current_player + 1}'s turn!")
        
        # Show current player's hand
        show_hand(hands[current_player], discard_pile[-1])
        
        # Check if player has any playable cards
        playable_cards = [card for card in hands[current_player] 
                         if can_play(card, discard_pile[-1])]
        
        if playable_cards:
            # Player chooses a card to play
            while True:
                try:
                    choice = input("\nChoose a card to play (number) or 'd' to draw: ")
                    
                    if choice.lower() == 'd':
                        # Draw a card
                        if deck:
                            new_card = deck.pop()
                            hands[current_player].append(new_card)
                            print(f"You drew: {new_card}")
                            break
                        else:
                            print("No cards left to draw!")
                            continue
                    
                    # Play a card
                    card_index = int(choice) - 1
                    if 0 <= card_index < len(hands[current_player]):
                        chosen_card = hands[current_player][card_index]
                        
                        if can_play(chosen_card, discard_pile[-1]):
                            # Play the card
                            hands[current_player].pop(card_index)
                            discard_pile.append(chosen_card)
                            print(f"You played: {chosen_card}")
                            
                            # Check for win
                            if len(hands[current_player]) == 0:
                                print(f"🎉 Player {current_player + 1} wins! 🎉")
                                game_over = True
                            break
                        else:
                            print("You can't play that card! Choose another.")
                    else:
                        print("Invalid card number!")
                        
                except ValueError:
                    print("Please enter a number or 'd'!")
        else:
            # No playable cards - must draw
            print("No playable cards. Drawing a card...")
            if deck:
                new_card = deck.pop()
                hands[current_player].append(new_card)
                print(f"You drew: {new_card}")
            else:
                print("No cards left to draw!")
        
        # Switch to other player if game isn't over
        if not game_over:
            current_player = 1 - current_player  # Switch between 0 and 1
    
    print("\nThanks for playing! 🎴")

# Start the game
if __name__ == "__main__":
    play_game()