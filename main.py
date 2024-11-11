import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from containers import Container
from middlewares import create_middlewares
from user.interface.controllers.user_controller import router as user_router
from note.interface.controllers.note_controller import router as note_router

app = FastAPI()
app.container = Container()

app.include_router(user_router)
app.include_router(note_router)

create_middlewares(app)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content=exc.errors()
    )


@app.get("/")
def hello():
    return {"Hello": "FastAPI"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)
