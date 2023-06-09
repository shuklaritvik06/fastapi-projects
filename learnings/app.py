from fastapi import FastAPI, Query, Path, Body, Cookie, Form, Header, BackgroundTasks, File, APIRouter, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse, PlainTextResponse
from enum import Enum
from typing import Annotated, List, Union, Optional
from pydantic import BaseModel, Field, EmailStr
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)
app.include_router(router)


class Hello(str, Enum):
    Ritvik = "ritvik"
    Ramesh = "ramesh"


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


class ISBN(BaseModel):
    publisher: str = None
    address: str = None


class Item(BaseModel):
    name: str = Field(min_length=5, max_length=100)
    price: float = Field(description="This is price", gt=100.00, lt=20000.00)
    phone: str = Field(regex="^[0-9]{10}$")
    is_offer: Optional[bool] = None
    students: List[str] = ["ramesh", "rakesh"]
    isbn: Union[ISBN, None] = None
    email: EmailStr | None


@app.get("/hello/{name}", response_description="This is a response", summary="Summary")
async def read_item(name: Annotated[str, Path(..., max_length=20)], item: Annotated[Item, Body(examples={
    "normal": {
        "summary": "This is a normal schema",
        "description": "This is normal",
        "value": {
            "name": "Ramesh",
            "price": 230.20,
            "phone": "8929223295",
            "is_offer": True,
            "isbn": {
                "publisher": "Publisher One",
                "address": "Address One"
            },
            "email": "ramesh@gmail.com"
        }
    }
})],
                    q: Annotated[str | None, Query(max_length=10,
                                                   min_length=3,
                                                   description="This is the query passed")] = None,
                    address_id: Annotated[str | None, Cookie()] = None):
    """
    Hello I am Doc
    """
    return {
        "path": name,
        "query": q,
        "item": item,
        "address_id": address_id
    }


@app.get("/redirect")
async def redirect():
    return RedirectResponse(url="https://www.youtube.com")


@app.get("/json")
async def json():
    return JSONResponse(content={"message": "Hello"})


@app.post("/form")
async def form_handle(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {
        "username": username,
        "password": password
    }


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


def task(data: str):
    with open("./file.txt", "a+") as f:
        f.write(data + "\n")


@app.get("/header")
async def header(x_token: Annotated[str, Header()], background: BackgroundTasks):
    background.add_task(task, data=x_token)
    return {"header": x_token}
