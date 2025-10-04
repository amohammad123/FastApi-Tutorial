# python -m fastapi_cli dev main.py
from tkinter.messagebox import RETRY

from fastapi import FastAPI, Query, HTTPException, status, Path, Form, Body, File, UploadFile
from fastapi.responses import JSONResponse
from typing import Annotated, List
import random
from contextlib import asynccontextmanager
from database import Base, engine

from test_schemas import PersonCreateSchema, PersonResponseSchema

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("application starting")
    Base.metadata.create_all(engine)
    yield
    print("application ended")


app = FastAPI(lifespan=lifespan)
# app = FastAPI()

names_list = [
    {"id": 1, "name": "ali"},
    {"id": 2, "name": "ahmad"},
    {"id": 3, "name": "zahra"},
    {"id": 4, "name": "mohammad"},
    {"id": 5, "name": "sara"},
    {"id": 6, "name": "hasan"},
    {"id": 7, "name": "mirza"},
]


# @app.on_event("startup")
# async def startup_event():
#     print('starting the application============')
#
#
# @app.on_event("shutdown")
# async def startup_event():
#     print('shutdown the application============')


@app.get("/names", response_model=List[PersonResponseSchema])
def retrieve_name_list(q: Annotated[
    str | None, Query(alias="search", description="enter a name", example="ali", max_length=5)] = None):
    if q:
        return [item for item in names_list if item["name"] == q]
    return names_list


@app.get("/name/{name_id}")
def retrieve_name_detail(name_id: int = Path(title="object id", description="enter a name id")):
    for name in names_list:
        if name['id'] == name_id:
            return name

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Name not found")


@app.post("/names", status_code=status.HTTP_201_CREATED, response_model=PersonResponseSchema)
# def create_name(name: str = Body(embed=True)):
def create_name(person: PersonCreateSchema):
    name_obj = {'id': random.randint(8, 100), "name": person.name}
    new_id = random.randint(8, 100)
    names_list.append(name_obj)
    # return PersonResponseSchema(id=new_id, name=person.name)
    return name_obj
    # return JSONResponse(content={'message': 'name created successfully'}, status_code=status.HTTP_201_CREATED)


@app.put("/nameddd/{name_id}")
def update_name(name_id: int, input_name: str):
    for name in names_list:
        if name['id'] == name_id:
            name['name'] = input_name

    return {'ok'}


@app.post("/upload_file", status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    return {"file_name": file.filename, "content_type": file.content_type, "file_size": len(content)}
