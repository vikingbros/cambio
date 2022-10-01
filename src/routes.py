from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from uuid import UUID
from models import CreateGame, Game, Player

router = APIRouter(prefix="/game")


@router.post(
    "/",
    response_description="Create a new game",
    status_code=status.HTTP_201_CREATED,
    response_model=Game,
)
def create_game(request: Request, create_game: CreateGame = Body(...)) -> Game:

    game = jsonable_encoder(Game(**create_game.dict()))
    new_game = request.app.database["games"].insert_one(game)
    created_game = request.app.database["games"].find_one({"_id": new_game.inserted_id})
    return created_game


def update_game(
    request: Request, game_id: UUID, player: Player = Body(...)
) -> Game:
    game = request.app.database["games"].find_one({"_id": game_id})
    game.players.append(jsonable_encoder(player))

