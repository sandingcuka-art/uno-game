import random

class UnoGame:
    def __init__(self, num_players=2):
        self.colors = ["Red", "Green", "Blue", "Yellow"]
        self.values = [str(i) for i in range(0, 10)] + ["Skip", "Reverse", "Draw Two"]
        self.deck = self.create_deck()
        self.discard_pile = []
        self.players = [[] for _ in range(num_players)]
        self.current_player = 0
        self.direction = 1  # 1 for clockwise, -1 for counterclockwise
        self.game_over = False
        
    def create_deck(self):
        """Create a complete Uno deck with all card types"""
        deck = []
        
        # Number cards (0-9)
        for color in self.colors:
            # One zero per color
            deck.append(f"{color} 0")
            # Two of each 1-9 per color
            for value in self.values[1:10]:  # 1-9 numbers
                deck.append(f"{color} {value}")
                deck.append(f"{color} {value}")
        
        # Action cards (two of each per color)
        for color in self.colors:
            for action in ["Skip", "Reverse", "Draw Two"]:
                deck.append(f"{color} {action}")
                deck.append(f"{color} {action}")
        
        # Wild cards (four of each)
        for _ in range(4):
            deck.append("Wild")
            deck.append("Wild Draw Four")
        
        random.shuffle(deck)
        return deck
    
    def deal_initial_cards(self):
        """Deal 7 cards to each player"""
        for _ in range(7):
            for player_hand in self.players:
                if self.deck:
                    player_hand.append(self.deck.pop())
    
    def start_game(self):
        """Start the game by dealing cards and placing first card"""
        self.deal_initial_cards()
        
        # Draw first card for discard pile (must be a non-wild card)
        while self.deck:
            card = self.deck.pop()
            if not card.startswith("Wild"):
                self.discard_pile.append(card)
                break
        
        print("🎴 UNO Game Started! 🎴")
        print("Special Cards:")
        print("  Skip: Next player loses turn")
        print("  Reverse: Changes direction")
        print("  Draw Two: Next player draws 2 cards")
        print("  Wild: Choose any color")
        print("  Wild Draw Four: Choose color & next player draws 4")
    
    def draw_card(self, player_index, num_cards=1):
        """Draw cards for the specified player"""
        drawn_cards = []
        for _ in range(num_cards):
            if self.deck:
                card = self.deck.pop()
                self.players[player_index].append(card)
                drawn_cards.append(card)
            else:
                # Reshuffle discard pile if deck is empty (except top card)
                if len(self.discard_pile) > 1:
                    top_card = self.discard_pile.pop()
                    self.deck = self.discard_pile
                    self.discard_pile = [top_card]
                    random.shuffle(self.deck)
                    card = self.deck.pop()
                    self.players[player_index].append(card)
                    drawn_cards.append(card)
        return drawn_cards
    
    def is_playable(self, card):
        """Check if a card can be played on the current discard pile"""
        if not self.discard_pile:
            return True
            
        top_card = self.discard_pile[-1]
        
        # Wild cards are always playable
        if card.startswith("Wild"):
            return True
        
        # Handle colored cards
        card_parts = card.split()
        card_color = card_parts[0]
        card_value = " ".join(card_parts[1:])
        
        top_parts = top_card.split()
        top_color = top_parts[0]
        top_value = " ".join(top_parts[1:])
        
        # Check if colors or values match
        return card_color == top_color or card_value == top_value
    
    def play_card(self, player_index, card_index):
        """Play a card from player's hand"""
        if 0 <= player_index < len(self.players) and 0 <= card_index < len(self.players[player_index]):
            card = self.players[player_index][card_index]
            
            if self.is_playable(card):
                # Remove card from player's hand
                played_card = self.players[player_index].pop(card_index)
                self.discard_pile.append(played_card)
                
                # Handle special cards
                self.handle_special_card(played_card, player_index)
                
                # Check if player has won
                if len(self.players[player_index]) == 0:
                    self.game_over = True
                    print(f"🎉 Player {player_index + 1} wins! 🎉")
                
                return True
        return False
    
    def handle_special_card(self, card, player_index):
        """Handle the effects of special cards"""
        if "Skip" in card:
            print("⏭️  Skip! Next player loses turn.")
            self.next_turn()
        elif "Reverse" in card:
            self.direction *= -1
            direction = "counter-clockwise" if self.direction == -1 else "clockwise"
            print(f"🔄 Reverse! Direction changed to {direction}.")
        elif "Draw Two" in card:
            next_player = (self.current_player + self.direction) % len(self.players)
            drawn_cards = self.draw_card(next_player, 2)
            print(f"➕2! Player {next_player + 1} draws 2 cards: {', '.join(drawn_cards)}")
            self.next_turn()
        elif "Wild Draw Four" in card:
            next_player = (self.current_player + self.direction) % len(self.players)
            drawn_cards = self.draw_card(next_player, 4)
            print(f"🃏➕4! Player {next_player + 1} draws 4 cards: {', '.join(drawn_cards)}")
            self.next_turn()
    
    def next_turn(self):
        """Move to the next player's turn"""
        self.current_player = (self.current_player + self.direction) % len(self.players)
    
    def get_playable_cards(self, player_index):
        """Get list of playable cards for a player"""
        return [card for card in self.players[player_index] if self.is_playable(card)]
    
    def display_game_state(self):
        """Display the current game state"""
        print(f"\n{'='*50}")
        print(f"Top card: {self.discard_pile[-1] if self.discard_pile else 'None'}")
        print(f"Current player: Player {self.current_player + 1}")
        print(f"Cards in deck: {len(self.deck)}")
        print(f"Direction: {'🔄 Counter-clockwise' if self.direction == -1 else '⏩ Clockwise'}")
        
        for i, hand in enumerate(self.players):
            print(f"Player {i + 1}: {len(hand)} cards")
            if i == self.current_player:
                print("  Your hand:")

def human_turn(game):
    """Handle a human player's turn"""
    player_index = game.current_player
    print(f"\nPlayer {player_index + 1}'s turn!")
    
    playable_cards = game.get_playable_cards(player_index)
    
    if not playable_cards:
        print("No playable cards. Drawing a card...")
        drawn_card = game.draw_card(player_index)
        print(f"You drew: {drawn_card[0]}")
        
        # Check if drawn card is playable
        if game.is_playable(drawn_card[0]):
            print("You can play the drawn card!")
            card_index = game.players[player_index].index(drawn_card[0])
            game.play_card(player_index, card_index)
        else:
            game.next_turn()
    else:
        print("Your hand:")
        for i, card in enumerate(game.players[player_index]):
            marker = " ✅" if card in playable_cards else " ❌"
            print(f"  {i + 1}. {card}{marker}")
        
        while True:
            try:
                choice = input("\nChoose a card to play (number) or 'd' to draw: ")
                if choice.lower() == 'd':
                    drawn_card = game.draw_card(player_index)
                    print(f"You drew: {drawn_card[0]}")
                    break
                else:
                    card_index = int(choice) - 1
                    if game.play_card(player_index, card_index):
                        print(f"You played: {game.discard_pile[-1]}")
                        break
                    else:
                        print("Invalid card choice. Try again.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter a valid card number or 'd'.")

def computer_turn(game):
    """Handle a computer player's turn"""
    player_index = game.current_player
    print(f"\nPlayer {player_index + 1}'s turn (Computer)")
    
    playable_cards = game.get_playable_cards(player_index)
    
    if not playable_cards:
        print("Computer draws a card.")
        game.draw_card(player_index)
        game.next_turn()
    else:
        # Simple AI: play the first playable card
        card_to_play = playable_cards[0]
        card_index = game.players[player_index].index(card_to_play)
        game.play_card(player_index, card_index)
        print(f"Computer plays: {card_to_play}")
        
        # Computer says "Uno!" if they have one card left
        if len(game.players[player_index]) == 1:
            print("Computer says: UNO!")

def main():
    """Main game loop"""
    print("🎴 Welcome to UNO! 🎴")
    
    # Get number of players
    while True:
        try:
            num_players = int(input("Enter number of players (2-4): "))
            if 2 <= num_players <= 4:
                break
            else:
                print("Please enter a number between 2 and 4.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Create and start game
    game = UnoGame(num_players)
    game.start_game()
    
    # Main game loop
    while not game.game_over:
        game.display_game_state()
        
        # For this version, all players are human
        human_turn(game)
        
        # Move to next turn if game not ended
        if not game.game_over:
            game.next_turn()
    
    print("\n🎊 Game Over! Thanks for playing! 🎊")

if __name__ == "__main__":
    main()