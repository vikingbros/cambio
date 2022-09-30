from random import choice
from typing import Union, Optional


class Card:
    def __init__(self, value: int, suit: str):
        self.value = value
        self.suit = suit
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.value}, suit={self.suit})"


class Deck:

    def __init__(self):
        suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
        self.cards = [Card(value, suit) for value in range(1, 14) for suit in suits]
        self.discard = []

    def draw(self, num_cards: int = 1) -> Union[Card, list[Card]]: 
        cards = []
        for _ in range(0, num_cards):
            cards.append(choice(self.cards))
            self.cards.remove(cards[-1])
        if len(cards) == 1:
            return cards[0]
        return cards
    
    def add_to_discard(self, card: Card) -> None:
        self.discard.append(card)



class Player:

    def __init__(self, name: str, deck: Deck, num_cards: int = 4):
        self.name = name
        self.cards = deck.draw(num_cards)
        self.show(0), self.show(1)  # TODO remove
    
    def show(self, position: int) -> Card:
        try:
            print(self.cards[position])
            return self.cards[position]
        except IndexError:
            print(f'Positon provided is out of bounds, max position possible is: {len(self.cards) - 1}')
    
    def replace(self, position: int, card: Card, deck: Optional[Deck] = None) -> None:
        if deck:
            deck.add_to_discard(self.cards[position])
        self.cards = self.cards[:position] + [card] + self.cards[position+1:]
    
    def switch(self, position: int, other_player: "Player", other_player_position: int, replace: bool = True) -> None:
        other_players_card: Card = other_player.cards[other_player_position]
        other_player.replace(position=other_player_position, card=self.cards[position])
        if replace:
            self.replace(position, other_players_card)
        else:
            self.cards[position] = None
    
    def stack(self, position: int, deck: Deck) -> None:
        if deck.discard[-1].value == self.cards[position].value: 
            deck.add_to_discard(self.cards[position])
            self.cards[position] = None
        else:
            self.cards.append(deck.draw())
    
    def stack_other_player(self, other_player_position: int, other_player: "Player", deck: Deck) -> bool:
        if deck.discard[-1].value == other_player.cards[other_player_position].value:
            deck.add_to_discard(other_player.cards[other_player_position])
            return True
        else:
            self.cards.append(deck.draw())
            return False
