# Filename: main.py

from itertools import product
from random import choice, seed
from os import linesep

# Randomization
# seed(0)
# seed(6)
# seed(322) # dealer wins
# seed(1000) # player stay dealer hits and wins
# seed(817) # player stays multiple hits from dealer
# seed(885) # interesting play
# seed(551) # very interesting play (try stay, hit stay, and hit hit stay)
a = 0
seed(a)

# Simplified rules:
# 1. Ace is always worth 11.
# 2. You always go first, i.e. no blackjack check for dealer before player has completed their turn.
# 3. If you and the dealer get 21, the dealer automatically wins.
# 4. There are no draws.
# a = randint(0,1000)

# Sets for card creation:
suits = {'hearts', 'clubs', 'spades', 'diamonds'}
numbers = set([i for i in range(2,15)])

def create_deck(number_of_decks):  # create a deck with one or more sets of cards
    deck = []  # create an empty deck
    for i in range(number_of_decks):
        for suit in suits:
            for number in numbers:
                card = (suit, number)
                deck.append(card)
    return deck  # return the deck

def draw_card(deck):  # draw a card from the deck
    card = choice(deck)  # randomly select a card from the deck
    remove_card_from_deck(deck, card[0], card[1])  # remove the card from the deck
    return card  # return the card

def remove_card_from_deck(deck, suit, num):  # remove the drawn card from the deck
    deck.remove((suit, num))  # remove the card from the deck
    return (suit, num)  # return the card

def get_count(hand):  # count the player or dealer's hand
    count = 0
    for card in hand:
        if card[1] == 14:
            count += 11
        elif card[1] >= 11:
            count += 10
        else:
            count += card[1]
    return count

def create_blackjack_game():  # create decks for the game
    # FIRST SECTION
    '''Initialize player's hand'''
    player = []  # create an empty list for the player's cards

    '''Initialize dealer's hand'''
    dealer = []  # create an empty list for the dealer's cards

    '''Multiple decks'''
    number_of_decks = int(input("How many decks? Enter 1 or 2: "))

    '''Create deck'''
    deck = create_deck(number_of_decks)  # create a deck with one or two sets of cards

    '''Initialize discard pile'''
    discard_pile = []  # create an empty list for discarded cards

    return player, dealer, number_of_decks, deck, discard_pile

def play_blackjack_game():  # play the game

    player, dealer, number_of_decks, deck, discard_pile = create_blackjack_game()  # return decks from create_blackjack_game

    def add_to_discard_pile(card):  # add drawn card to the discard pile
        discard_pile.append((card))
        return discard_pile

    '''Display dealer's cards'''
    def display_dealer(dealer, start=False):  # display the dealer's cards, False = none hidden, True = one hidden
        if start:  # start equals True until the dealer hits
            the_output = [dealer[0], ('?', '?')]
            print("Dealer's cards:", the_output)
        else:
            print("Dealer's cards:", dealer)

    '''Display player's cards'''
    def display_player(player):  # display the player's cards
        print("Player's cards:", player)

    def draw_first_hand():  # start a new round
        '''Draw first hand of cards'''
        visible_dealer_card = draw_card(deck)  # draw a card
        dealer.append((visible_dealer_card[0], visible_dealer_card[1]))  # add the card to the dealer's hand
        add_to_discard_pile((visible_dealer_card[0], visible_dealer_card[1]))  # add the card to the discard pile

        hidden_dealer_card = draw_card(deck)  # draw a card
        dealer.append((hidden_dealer_card[0], hidden_dealer_card[1]))  # add the card to the dealer's hand
        # to keep the card hidden it's not added to the discard pile

        for draw_for_player in range(2):  # draw two cards for the player
            card = draw_card(deck)  # draw a card
            player.append((card[0], card[1]))  # add the card to the player's hand
            add_to_discard_pile((card[0], card[1]))  # add the card to the discard pile

        display_dealer(dealer, start=True)  # display the dealer's first hand, one card hidden

        display_player(player)  # display the player's first hand, both cards showing

        return visible_dealer_card, hidden_dealer_card

    def prepare_for_new_round():
        dealer.clear()
        player.clear()
        print("*** New Round ***")
        draw_first_hand()
        new_round()

    def new_round():  # start a new round
        '''Check player's cards to see if BUST'''
        if get_count(player) > 21:
            print("SCORE -- Player:", get_count(player), " Dealer:", get_count(dealer))
            print("Player BUST \nDealer WINS!")
            prepare_for_new_round()
            no_stays = True

        '''Check player's cards to see if WIN'''
        if get_count(player) == 21:

            '''Display dealer's cards'''
            display_dealer(dealer, start=False)  # both cards visible
            add_to_discard_pile((hidden_dealer_card[0], hidden_dealer_card[1]))

            '''If dealer equals 21 then dealer WINS'''
            if get_count(dealer) == 21:
                print("SCORE -- Player:", get_count(player), " Dealer:", get_count(dealer))
                print("Dealer WINS!")
                prepare_for_new_round()
                no_stays = True

            '''If dealer does not equal 21 then player WINS'''
            if get_count(dealer) != 21:
                print("SCORE -- Player:", get_count(player), " Dealer:", get_count(dealer))
                print("Player WINS!")
                prepare_for_new_round()
                no_stays = True

        no_stays = True  # player has not yet stayed, so one dealer card is hidden

        '''Card counting'''
        def card_counting():  # calculate the probability of drawing a picture card
            picture_cards_in_deck = 12 * number_of_decks  # 12 equals number of picture cards in one deck
            for discard_card in discard_pile:
                if discard_card[1] in range(11, 14):
                    picture_cards_in_deck -= 1
            # print("Discard pile:", discard_pile)  # displays the discard pile
            print("Picture probability:", round((picture_cards_in_deck / len(deck) * 100)), "%")
            if no_stays:  # if player hasn't stayed yet, hide dealer's score
                print("SCORE -- Player:", get_count(player), " Dealer: tbd")
            else:  # if player has stayed at least once, show dealer's score
                print("SCORE -- Player:", get_count(player), " Dealer:", get_count(dealer))
            # print("Player OK")  # print that player is OK

        '''Check player's cards to see if OK'''
        if get_count(player) < 21:
            card_counting()  # display probability of drawing a picture card

        player_action = input('Press h to hit, s to stand, q to quit: ').lower().strip(linesep)
        while player_action not in ('s', 'h', 'q'):
            player_action = input('Press h to hit, s to stand, q to quit: ').lower().strip(linesep)

        if player_action == 'q':
            return 0

        while player_action != 'q' and len(deck) >= 4:

            '''Player selects h to hit'''
            if player_action == 'h':

                # SECOND SECTION
                '''Draw card from deck and append to player'''
                card = draw_card(deck)  # draw a card
                player.append((card[0], card[1]))  # add the card to the player's hand
                add_to_discard_pile(card)  # add the card to the discard pile

                '''Check if player has stayed yet'''
                if no_stays:

                    '''Continue to hide one of the dealer's cards'''
                    display_dealer(dealer, start=True)  # True = one hidden

                    '''Display player's cards'''
                    display_player(player)

                    '''Check player's cards to see if OK'''
                    if get_count(player) < 21:
                        card_counting()

                    '''Check player's cards to see if BUST'''
                    if get_count(player) > 21:
                        print("SCORE -- Player:", get_count(player), " Dealer:", get_count(dealer))
                        print("Player BUST \nDealer WINS!")
                        prepare_for_new_round()
                        no_stays = True

                    '''Check player's cards to see if WIN'''
                    if get_count(player) == 21:

                        '''Display dealer's cards'''
                        display_dealer(dealer, start=False)  # False = none hidden

                        "Check if dealer's cards also equal 21"
                        if get_count(dealer) == 21:
                            print("SCORE -- Player:", get_count(player), " Dealer:", get_count(dealer))
                            print("Dealer WINS!")
                            prepare_for_new_round()
                            no_stays = True
                        else:
                            print("SCORE -- Player:", get_count(player), " Dealer:", get_count(dealer))
                            print("Player WINS!")
                            prepare_for_new_round()
                            no_stays = True

                else:  # after the player's first stay, stop hiding one of the dealer's cards

                    '''Display dealer's cards'''
                    display_dealer(dealer, start=False)  # False = none hidden

                    '''Display player's cards'''
                    display_player(player)

                    '''Check player's cards to see if OK'''
                    if get_count(player) < 21:
                        card_counting()

                    '''Check player's cards to see if BUST'''
                    if get_count(player) > 21:
                        print("SCORE -- Player:", get_count(player), " Dealer:", get_count(dealer))
                        print("Player BUST \nDealer WINS!")
                        prepare_for_new_round()
                        no_stays = True

                    '''Check player's cards to see if WIN'''
                    if get_count(player) == 21:
                        print("SCORE -- Player:", get_count(player), " Dealer:", get_count(dealer))
                        print("Player WINS!")
                        prepare_for_new_round()
                        no_stays = True
            else:

                '''Player selects s to stand'''
                if player_action == 's':

                    # THIRD SECTION
                    if no_stays:  # if this is the player's first stay
                        '''Display both of dealer's cards'''
                        display_dealer(dealer, start=False)  # False = none hidden
                        add_to_discard_pile(
                            (hidden_dealer_card[0], hidden_dealer_card[1]))  # add the hidden card to the discard pile
                        no_stays = False

                    '''Check dealer's cards to see if BUST'''
                    if get_count(dealer) > 21:
                        print("SCORE -- Player:", get_count(player), " Dealer:", get_count(dealer))
                        print("Dealer BUST \n Player WINS!")
                        prepare_for_new_round()
                        no_stays = True

                    '''Check dealer's cards to see if WIN'''
                    if get_count(dealer) == 21:
                        print("SCORE -- Player:", get_count(player), " Dealer:", get_count(dealer))
                        print("Dealer WINS!")
                        prepare_for_new_round()
                        no_stays = True

                    '''If dealer is less than 17, draw a card '''
                    if get_count(dealer) < 17:
                        print("SCORE -- Player:", get_count(player), " Dealer:", get_count(dealer))
                        print("Dealer hits")
                        card = draw_card(deck)  # draw a card
                        dealer.append((card[0], card[1]))  # add card to dealer's hand
                        add_to_discard_pile(card)  # add card to discard pile

                        '''Display dealer's cards'''
                        display_dealer(dealer, start=False)  # False = none hidden

                        '''Display player's cards'''
                        display_player(player)

                        '''Check dealer's cards to see if OK'''
                        if get_count(dealer) < 17:
                            print("SCORE -- Player:", get_count(player), " Dealer:", get_count(dealer))
                            # print("Dealer OK")
                            card_counting()

                        '''Check dealer's cards to see if BUST'''
                        if get_count(dealer) > 21:
                            print("SCORE -- Player:", get_count(player), " Dealer:", get_count(dealer))
                            print("Dealer BUST \nPlayer WINS!")
                            prepare_for_new_round()
                            no_stays = True

                        '''Check dealer's cards to see if WIN'''
                        if get_count(dealer) == 21:
                            print("SCORE -- Player:", get_count(player), " Dealer:", get_count(dealer))
                            print("Dealer WINS!")
                            prepare_for_new_round()
                            no_stays = True

                    '''If dealer is 17 or greater but less than 21'''
                    if 17 <= get_count(dealer) < 21:

                        '''If player is greater than dealer then player WINS'''
                        if get_count(player) > get_count(dealer):
                            print("SCORE -- Player:", get_count(player), " Dealer:", get_count(dealer))
                            print("Player is greater than dealer \nPlayer WINS!")
                            prepare_for_new_round()
                            no_stays = True
                        else:
                            # print("SCORE -- Player:", get_count(player), " Dealer:", get_count(dealer))
                            print("Dealer stays")
                            card_counting()

            player_action = input('press h to hit, s to stand, q to quit: ').lower().strip(linesep)
            while player_action not in ('s', 'h', 'q'):
                player_action = input('press h to hit, s to stand, q to quit: ').lower().strip(linesep)
            if player_action == 'q':
                return 0

    visible_dealer_card, hidden_dealer_card = draw_first_hand()
    new_round()

    if len(deck) <= 4:
        print("Game Over (no cards in deck)")  # end the game if there are not enough cards in the deck

if __name__ == '__main__':
    play_blackjack_game()  # start the blackjack game


'''Test Cases'''
# Test Case 1
# seed = 322
# Dealer stays on 17 to 20
# Player hits to bust
# Expected result: Dealer wins

# Test Case 2
# seed = 1000
# Player stays on 17 to 20
# Dealer hits to 21
# Expected result: Dealer wins

# Test Case 3
# seed = 817
# Player stays on 17 to 20
# Dealer hits to bust
# Expected result: Player wins
