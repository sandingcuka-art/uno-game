import random 
def buildDeck():
    deck = []
    colours = ["Red", "Green", "Yellow", "Blue"]
    values = [0,1,2,3,4,5,6,7,8,9,"Draw Two", "Skip","Reverse"]
    wilds = ["Wild", "Wild Drew Four"]
    for colour in colours:
        for value in values:
            cardVal = "{} {}".format(colour, value)
            deck.append(cardVal)
            if value != 0:
                deck.append(cardVal)
    for i in range(4):
             deck.append(wilds[0])
             deck.append(wilds[1])
   
        
    return deck
#shuffles
#deck -> list

def shuffleDeck(deck):
    for cardPos in range(len(deck)):
        randPos = random.randint(0,107)
        deck[cardPos], deck[randPos] = deck[randPos], deck[cardPos]
    return deck
        

#draw cards
def drawCards(numCards):
    cardsDrawn = []
    for x in range(numCards):
        cardsDrawn.append(unoDeck.pop(0))
    return cardsDrawn    
        
def showHand(player, playerHand):
    print("Player {}".format(player+1))
    print("Your Hnad")
    print("-----------------")
    for  card in playerHand:
        print(card)
        print("")
        
        
unoDeck = buildDeck()
unoDeck = shuffleDeck(unoDeck)
discards = []
print(unoDeck)

players = []
numPlayers = int(input("How many players?"))
while numPlayers <2 or numPlayers>4:
    numPlayers = int(input("Invalid. Please enter a number"))
for player in range(numPlayers):
    players.append(drawCards(5))
    
print(players)
                   
playerTurn = 0
playDirection = 1 
playing = True
discards.append(unoDeck.pop(0))

while playing: 
    showHand(playerTurn,players[playerTurn])
    print("Card on top of discard pile: {}".format(discards[-1]))