
import random

def build_deck():
    """Create a UNO deck"""
    colors = ["Red", "Green", "Blue", "Yellow"]
    deck = []  #where all the cards will be stored
    for color in colors:
        for num in range(10):
            deck.append(f"{color} {num}")
            if num != 0: #checking if the current num is 1 through 9
                deck.append(f"{color} {num}")
    for _ in range(4): #starts a loop thats executes four times to add wild cards
        deck.append("Wild")
    return deck

def can_play(card, top_card):
    """Check if card can be played on top card"""
    if card == "Wild":
        return True
    if "Wild" in top_card:  # If top is wild, match chosen color
        return card.startswith(top_card.split()[-1])      #can play if the card matches color or num
    return card.split()[0] == top_card.split()[0] or card.split()[1] == top_card.split()[1]

def main():
    print("=== UNO: You vs Computer ===")
    
    # Setup game
    deck = build_deck()
    random.shuffle(deck)
    
    # Deal cards
    player_hand = [deck.pop() for _ in range(7)]
    computer_hand = [deck.pop() for _ in range(7)]
    
    # Start with first card
    top_card = deck.pop()
    while top_card == "Wild":  # Make sure first card isn't wild
        deck.append(top_card)
        top_card = deck.pop()
    
    while True:
        # Player's turn
        print(f"\nTop card: {top_card}")
        print("\nYour hand:")
        for i, card in enumerate(player_hand):
            print(f"{i+1}. {card}")
        
        # Player chooses action
        choice = input("Play card number or 'd' to draw: ")
        
        if choice.lower() == 'd':
            player_hand.append(deck.pop())
            print("You drew a card")
        else:
            try:
                card_index = int(choice) - 1
                card_to_play = player_hand[card_index]
                
                if can_play(card_to_play, top_card):
                    top_card = player_hand.pop(card_index)
                    if top_card == "Wild":
                        color = input("Choose color (Red/Green/Blue/Yellow): ")
                        top_card = f"Wild - Color: {color}"
                    print(f"You played: {top_card}")
                else:
                    print("Invalid move! Card doesn't match.")
                    continue
            except:
                print("Invalid choice!")
                continue
        
        # Check if player wins
        if len(player_hand) == 0:
            print("🎉 YOU WIN! 🎉")
            break
        
        # Computer's turn
        print(f"\nComputer's turn...")
        computer_played = False
        
        # Computer tries to play a card
        for i, card in enumerate(computer_hand):
            if can_play(card, top_card):
                top_card = computer_hand.pop(i)
                if top_card == "Wild":
                    color = random.choice(["Red", "Green", "Blue", "Yellow"])
                    top_card = f"Wild - Color: {color}"
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
        
        # Check if deck is empty
        if len(deck) == 0:
            print("Deck empty! Game over.")
            break

if __name__ == "__main__":
    main()