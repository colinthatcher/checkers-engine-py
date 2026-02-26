from fastapi import FastAPI

from checkers.checkers import Checkers

app = FastAPI()

game = Checkers()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/game", response_model=None)
def get_game() -> Checkers:
    return game
