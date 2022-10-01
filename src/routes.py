from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder

from models import CreateGame, Game

router = APIRouter(prefix="/game")


@router.post(
    "/",
    response_description="Create a new game",
    status_code=status.HTTP_201_CREATED,
    response_model=Game,
)
def create_game(request: Request, create_game: CreateGame = Body(...)) -> Game:

    game = jsonable_encoder(Game(**create_game.dict()))
    print("hi")
    new_game = request.app.database["games"].insert_one(game)
    print(game["_id"])
    print(new_game.inserted_id)
    created_game = request.app.database["games"].find_one({"_id": new_game.inserted_id})
    print(created_game)
    return created_game
