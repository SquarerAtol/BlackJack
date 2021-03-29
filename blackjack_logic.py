import random
import os 
from constants import *
import pygame
import numpy as np
import itertools

class Deck:
    def __init__(self):
        self.cards = []
        self.card = None
        self.build()

    def build(self):
        for rank in RANKS:
            for suit in SUITS:
                self.cards.append((rank, suit))
                #self.cards_images = "".join('img/' + card + '.png')
        #self.cards_images = [j for i in self.cards_images for j in i]
        
    def shuffle(self):
        random.shuffle(self.cards)
        

    def deal(self):
        self.card = self.cards.pop()
        return self.cards.pop()

    # def card_img(self):
    #     #return self.cards_images.pop(self.cards_images)
    #     print(self.cards)
    #     print(self.cards_images)
    def __str__(self):
        # return a string representing the deck
        return " ".join( [ str(card) for card in self.cards ] )


class Hand(Deck):
    def __init__(self):
        self.cards = []
        self.card_val = []
        self.card = None
        self.rank = 0 


    
    def add_card(self, card):
        self.cards.append(card)
        self.card = card

    def calc_hand(self):
        self.rank = 0
        has_ace = False
        for card in self.cards:
            if card.rank.isnumeric():
                self.rank += int(card.rank)
            else:
                if card.rank == "A":
                    has_ace = True
                    self.rank += 11
                else:
                    self.rank += 10

        if has_ace and self.rank > 21:
            self.rank -= 10 

    def get_rank(self):
        self.calc_hand()
        return self.rank 

    def player_display(self):
        for card in self.cards:
            dealer_cards = "".join((card[0], card[1]))
            self.card_val.append(dealer_cards)

    def dealer_display(self):
        for card in self.cards:
            dealer_cards = "".join((card[0], card[1]))
            self.card_val.append(dealer_cards)
            
            
            
    # def dealer_display_second(self):
    #     for card in self.cards:
    #         card = "".join((card[0], card[1]))
    #         img_card = pygame.image.load('img/' + card + '.png').convert()
    #     return img_card[1]




class Game(Hand):
    def __init__(self):
        pass
    
    def play(self):
        playing = True

        while playing:
            self.deck = Deck()
            self.deck.shuffle()

            self.player_hand = Hand()
            self.dealer_hand = Hand(dealer=True)

            for i in range(2):
                self.player_hand.add_card(self.deck.deal())
                self.dealer_hand.add_card(self.deck.deal())

            print("Your hand is:")
            self.player_hand.player_display()
            print()
            print("Dealer's hand is:")
            self.dealer_hand.dealer_display()

            game_over = True


            while game_over:
                player_with_blackjack, dealer_with_blackjack = self.check_if_blackjack()
                if player_with_blackjack or dealer_with_blackjack:
                    game_over = False
                    self.show_blackjack_results(
                        player_with_blackjack, dealer_with_blackjack)
                    continue

                if self.dealer_is_over():
                    print("Dealer busted you won!")
                    game_over = False

                    self.player_hand.add_card(self.deck.deal())
                    self.player_hand.display()
                    if self.player_is_over():
                        print("You have busted dealer won")
                        game_over = False

                else:
                    player_hand_rank = self.player_hand.get_rank()
                    dealer_hand_rank = self.dealer_hand.get_rank()

                    print("Final Results:")
                    print("Your hand:", player_hand_rank)
                    print("Dealer's hand:", dealer_hand_rank)

                    if player_hand_rank > dealer_hand_rank:
                        print("You Win!")
                    elif player_hand_rank == dealer_hand_rank:
                        print("Tie")
                    else:
                        print("Dealer Wins!")
                    game_over = False

            again = input("Play again? [Y/N]")
            while again.lower() not in ["y", "n"]:
                again = input("Please enter Y or N ")
            if again.lower() == 'n':
                print("Thanks for playing!")
                playing = False
            else:
                game_over = False

    def player_is_over(self):
        return self.player_hand.get_rank() > 21

    def dealer_is_over(self):
        return self.dealer_hand.get_rank() > 21

    def check_if_blackjack(self):
        player = False
        dealer = False
        if self.player_hand.get_rank() == 21:
            player = True
        if self.dealer_hand.get_rank() == 21:
            dealer = True

        return player, dealer

    def show_blackjack_results(self, player_with_blackjack, dealer_with_blackjack):
        if player_with_blackjack and dealer_with_blackjack:
            print("Both players have blackjack! Draw!")
        elif player_with_blackjack:
            print("You have blackjack! You win!")
        elif dealer_with_blackjack:
            print("Dealer has blackjack! Dealer wins!")