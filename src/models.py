from pydantic import BaseModel, Field, Extra
from typing import Optional
from datetime import datetime
import uuid
from enums import Suit


class Model(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    created_date: datetime = Field(default_factory=lambda: datetime.now())
    updated_date: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        extra = Extra.forbid


class Card(Model):
    value: int
    suit: Suit


class Deck(Model):
    cards: list[Card] = Field(
        default_factory=lambda: [
            Card(value=value, suit=suit) for value in range(1, 14) for suit in Suit
        ]
    )
    discard: list[Card] = []


class Player(Model):
    name: str
    cards: list[Card] = []


class Game(Model):
    name: str
    deck: Deck = Field(default_factory=lambda: Deck())
    players: list[Player] = []


class CreateGame(BaseModel, extra=Extra.forbid):
    name: str
    players: list[Player] = []
