import random

def build_deck():
    """Create a complete UNO deck with all special cards"""
    colors = ["Red", "Green", "Blue", "Yellow"]
    deck = []
    
    # Number cards (0-9)
    for color in colors:
        deck.append(f"{color} 0") # One zero per color
        for num in range(1, 10): # Two of each 1-9
            deck.append(f"{color} {num}")
            deck.append(f"{color} {num}")
     
     
    # Action cards (Two of each per color)
    for color in colors:
        for _ in range(2):
            deck.append(f"{color} Skip")
            deck.append(f"{color} Reverse") 
            deck.append(f"{color} Draw Two")
    
    # Wild cards (Four of each)
    for _ in range(4):
        deck.append("Wild")
        deck.append("Wild Draw Four")
    
    return deck

def can_play(card, top_card):
    """Check if card can be played on top card"""
    if "Wild" in card:
        return True
    
    # If top card is a wild card with chosen color
    if "Color:" in top_card:
        chosen_color = top_card.split("Color: ")[1]
        return card.startswith(chosen_color)
    
    # Normal card matching (color or value)
    top_parts = top_card.split()
    card_parts = card.split()
    return card_parts[0] == top_parts[0] or card_parts[1] == top_parts[1]

def main():
    print("=== UNO: You vs Computer ===")
    
    # Setup game
    deck = build_deck()
    random.shuffle(deck)
    
    # Deal cards
    player_hand = [deck.pop() for _ in range(7)] # Start with 7 cards
    computer_hand = [deck.pop() for _ in range(7)]
    
    # Start with first non-wild card
    top_card = deck.pop()
    while "Wild" in top_card:
        deck.append(top_card)
        top_card = deck.pop()
    
    player_turn = True # True = player's turn, False = computer's turn
    skip_turn = False
    draw_amount = 0
    
    while True:
        if skip_turn:
            print("\n⏭️ Your turn was skipped!")
            skip_turn = False
            player_turn = not player_turn
            continue
        
        if draw_amount > 0:
            print(f"\n➕ Draw {draw_amount} cards!")
            if player_turn:
                for _ in range(draw_amount):
                    player_hand.append(deck.pop())
                print("You drew the cards!")
            else:
                for _ in range(draw_amount):
                    computer_hand.append(deck.pop())
                print("Computer drew the cards!")
            draw_amount = 0
            player_turn = not player_turn
            continue
        
        # Player's turn
        if player_turn:
            print(f"\nTop card: {top_card}")
            print("\nYour hand:")
            for i, card in enumerate(player_hand):
                print(f"{i+1}. {card}")
            
            choice = input("Play card number or 'd' to draw: ")
            
            if choice.lower() == 'd':
                player_hand.append(deck.pop())
                print("You drew a card")
                player_turn = False
            else:
                try:
                    card_index = int(choice) - 1
                    card_to_play = player_hand[card_index]
                    
                    if can_play(card_to_play, top_card):
                        top_card = player_hand.pop(card_index)
                        
                        # Handle special cards
                        if "Wild" in top_card:
                            color = input("Choose color (Red/Green/Blue/Yellow): ")
                            top_card = f"Wild - Color: {color}"
                            if "Draw Four" in top_card:
                                draw_amount = 4
                                print("➕ Computer must draw 4 cards!")
                        
                        elif "Skip" in top_card:
                            skip_turn = True
                            print("⏭️ Computer's turn skipped!")
                        
                        elif "Reverse" in top_card:
                            # In 2-player, Reverse acts like Skip
                            skip_turn = True
                            print("🔄 Reverse! Computer's turn skipped!")
                        
                        elif "Draw Two" in top_card:
                            draw_amount = 2
                            print("➕ Computer must draw 2 cards!")
                        
                        print(f"You played: {top_card}")
                        
                        # Check win
                        if len(player_hand) == 0:
                            print("🎉 YOU WIN! 🎉")
                            break
                        
                        # Only switch turns if no special card effect
                        if draw_amount == 0 and not skip_turn:
                            player_turn = False
                            
                    else:
                        print("Invalid move! Card doesn't match.")
                except:
                    print("Invalid choice!")
        
        # Computer's turn
        else:
            print(f"\n💻 Computer's turn...")
            computer_played = False
            
            for i, card in enumerate(computer_hand):
                if can_play(card, top_card):
                    top_card = computer_hand.pop(i)
                    
                    # Handle special cards
                    if "Wild" in top_card:
                        color = random.choice(["Red", "Green", "Blue", "Yellow"])
                        top_card = f"Wild - Color: {color}"
                        if "Draw Four" in top_card:
                            draw_amount = 4
                            print("➕ You must draw 4 cards!")
                    
                    elif "Skip" in top_card:
                        skip_turn = True
                        print("⏭️ Your turn skipped!")
                    
                    elif "Reverse" in top_card:
                        skip_turn = True
                        print("🔄 Reverse! Your turn skipped!")
                    
                    elif "Draw Two" in top_card:
                        draw_amount = 2
                        print("➕ You must draw 2 cards!")
                    
                    print(f"Computer played: {top_card}")
                    computer_played = True
                    break
            
            if not computer_played:
                computer_hand.append(deck.pop())
                print("Computer drew a card")
            
            # Check if computer wins
            if len(computer_hand) == 0:
                print("💻 Computer wins!")
                break
            
            # Only switch turns if no special card effect
            if draw_amount == 0 and not skip_turn:
                player_turn = True
        
        # Check if deck is empty
        if len(deck) == 0:
            print("Deck empty! Game over.")
            break

if __name__ == "__main__":
    main() 