'''
random for card shuffling
'''
import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
         'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7,
          'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10,
          'King': 10, 'Ace': 11}
PLAYING = True


class Card:
    '''
    Card Class
    '''
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:
    '''
    Deck Class
    '''
    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit, rank))

    def shuffle(self):
        '''
        Method to shuffle the deck
        '''
        random.shuffle(self.all_cards)

    def deal(self):
        '''
        Method to deal one card from the deck
        '''
        return self.all_cards.pop()

    def __str__(self):
        deck_comp = ''
        for card in self.all_cards:
            deck_comp += '\n ' + card.__str__()
        return 'The deck has: ' + deck_comp


class Hand:
    '''
    Deck Class
    '''
    def __init__(self):
        self.cards = []  # start with an empty list
        self.value = 0   # start with zero value
        self.aces = 0    # keep track of aces

    def add_card(self, card):
        '''
        Method to add a card to the player's Hand
        '''
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        '''
        Method to adjust the value of the hand
        '''
        while self.value > 21 and self.aces >= 1:
            self.value -= 9
            self.aces -= 1

    def __str__(self):
        hand = ''
        for card in self.cards:
            hand += '\n\t' + card.__str__()
        return hand


class Chips:
    '''
    Chips Class
    '''
    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        '''
        Adjusts players total bet
        '''
        self.total += (2*self.bet)

    def lose_bet(self):
        '''
        Adjusts players total bet
        '''
        self.total -= self.bet


class Player:
    '''
    Player Class
    '''
    def __init__(self, namee):
        self.name = namee
        self.hand = Hand()

    def hit(self, my_deck):
        '''
        Called when the user wants another card
        '''
        self.hand.add_card(my_deck.deal())
        self.hand.adjust_for_ace()

    def __str__(self):
        return f'Player {self.name} has {self.hand} cards.'


def show_all_cards(pl, d):
    '''
    Show the player and dealers hand
    '''
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(f'{pl.name}\'s cards: {pl.hand}')
    print(f'    Value of hand: {pl.hand.value}')
    print(f'Dealer\'s cards:\t{d.hand}')
    print(f'    Value of hand: {d.hand.value}')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')


def show_some_cards(pl, d):
    '''
    Show the player and some of the dealers hand
    '''
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(f'{pl.name}\'s cards: {pl.hand}')
    print(f'    Value of hand: {pl.hand.value}')
    print(f'Dealer\'s cards:\n\t{d.hand.cards[0]}\n\t?')
    print(f'    Value of hand: {values[d.hand.cards[0].rank]}')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')


if __name__ == "__main__":
    ROUND = 0
    name = input("Hello, welcome to BlackJack!\nPlease enter your name: ")
    chips = Chips()
    # Loop for new games
    while PLAYING:
        # game set up
        deck = Deck()
        deck.shuffle()
        player = Player(name)
        dealer = Player("Dealer")
        player.hit(deck)
        player.hit(deck)
        dealer.hit(deck)
        dealer.hit(deck)

        # take bet
        CHIP = True
        while CHIP:
            print(f'\nYou have {chips.total} chips.')
            player_bet = input("Please input your bet: ")
            try:
                b = int(player_bet)
            except ValueError:
                print('Invalid bet!')
                continue
            else:
                if chips.total >= b > 0:
                    chips.bet = b
                    CHIP = False
                elif chips.total < b:
                    print("Bet too high!")
                elif b <= 0:
                    print("You cannot bet a negative amount!")

        # GAMEPLAY
        GAME = True
        while GAME:
            # show cards
            show_some_cards(player, dealer)
            try:
                play = input('Would you like to HIT or STAND: ')
                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

                play = play.lower()
            except TypeError:
                print('invalid type')

            if (play in ('hit', 'h')) and player.hand.value <= 21:
                player.hit(deck)
            if player.hand.value > 21:
                print(f'{player.name}\'s cards: {player.hand}')
                print(f'    Value of hand: {player.hand.value}')
                print('BUST!!!')
                chips.lose_bet()
                GAME = False
            if play in ('stand', 's'):
                print(f'Dealer\'s cards: {dealer.hand}')
                while dealer.hand.value < 17:
                    dealer.hit(deck)
                    print(f'Dealer\'s added card: {dealer.hand.cards[-1]}')
                if (dealer.hand.value <= 21 and
                        dealer.hand.value > player.hand.value):
                    show_all_cards(player, dealer)
                    print("Dealer wins!")
                    chips.lose_bet()
                    GAME = False
                elif dealer.hand.value > 21:
                    show_all_cards(player, dealer)
                    print(f'Dealer BUST, {player.name} wins!')
                    chips.win_bet()
                    GAME = False
                elif dealer.hand.value < player.hand.value:
                    show_all_cards(player, dealer)
                    print(f"BLACKJACK!! {player.name} Wins")
                    chips.win_bet()
                    GAME = False
                elif dealer.hand.value == player.hand.value:
                    show_all_cards(player, dealer)
                    print('Push!')
                    GAME = False
        print(f'\nYou have {chips.total} chips.')
        if chips.total <= 0:
            print('You lost all of your chips! Would you like to buy more?')
            pp = input('Buy more? (Y/N): ')
            if pp in ('y', 'Y', 'yes', 'YES', 'Yes'):
                print('You have sold you soul to the gambing gods!')
                print('You have recieved 1000000 chips!')
                chips.total += 1000000
        p = input('Play again? (Y/N): ')
        if p in ('n', 'N', 'no', 'NO', 'No'):
            PLAYING = False
        elif p not in ('y', 'Y', 'yes', 'YES', 'Yes'):
            print('Invalid! You\'re playing again >:)')
    print('Nice playing with you! Come again soon!')
