from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from models import CreateGame, Game, UpdateGame

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
    return request.app.database["games"].find_one({"_id": new_game.inserted_id})


@router.get("/{id}")
def get_game(request: Request, id: str) -> Game:
    if (game := request.app.database["games"].find_one({"_id": id})) is not None:
        return game
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"game with ID {id} not found"
    )


@router.get("/")
def list_games(request: Request) -> list[Game]:
    return list(request.app.database["games"].find())


@router.put("/{id}", response_description="Update a game", response_model=Game)
def update_game(request: Request, id: str, game_update: UpdateGame) -> Game:
    game = {k: v for k, v in game_update.dict().items() if v is not None}
    if len(game) >= 1:
        update_result = request.app.database["games"].update_one(
            {"_id": id}, {"$set": game}
        )

        if update_result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Game with ID {id} not found",
            )

    if (
        existing_game := request.app.database["games"].find_one({"_id": id})
    ) is not None:
        return existing_game

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Game with ID {id} not found"
    )
