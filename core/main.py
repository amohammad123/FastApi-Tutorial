from typing import Annotated, List

from fastapi import FastAPI, Query, HTTPException, status, Path, Depends
from fastapi.responses import JSONResponse

from contextlib import asynccontextmanager

from sqlalchemy.orm import Session

from database import Base, engine, get_db, Person
from schemas import PersonCreateSchema, PersonResponseSchema, PersonUpdateSchema


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Base.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/names", response_model=List[PersonResponseSchema])
def retrieve_name_list(
        q: Annotated[str | None, Query(alias="search", description="enter a name", example="ali", max_length=5)] = None,
        db: Session = Depends(get_db)):
    query = db.query(Person)

    if q:
        query = query.filter_by(name=q)

    result = query.all()

    return result


@app.post("/names", status_code=status.HTTP_201_CREATED, response_model=PersonResponseSchema)
def create_name(request: PersonCreateSchema, db: Session = Depends(get_db)):
    new_person = Person(name=request.name)
    db.add(new_person)
    db.commit()
    db.refresh(new_person)

    return new_person


@app.get("/name/{name_id}", response_model=PersonResponseSchema)
def retrieve_name_detail(name_id: int = Path(title="object id", description="enter a name id"),
                         db: Session = Depends(get_db)):
    result = db.query(Person).filter_by(id=name_id).one_or_none()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Name not found")

    return result


@app.put("/name/{name_id}", response_model=PersonResponseSchema)
def update_name(request: PersonUpdateSchema, name_id: int, db: Session = Depends(get_db)):
    person = db.query(Person).filter_by(id=name_id).one_or_none()

    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Name not found")

    person.name = request.name
    db.commit()
    db.refresh(person)
    return person


@app.delete("/name/{name_id}")
def remove_name(name_id: int, db: Session = Depends(get_db)):
    person = db.query(Person).filter_by(id=name_id).one_or_none()

    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Name not found")

    db.delete(person)
    db.commit()

    return JSONResponse(content={'detail': 'person deleted successfully'}, status_code=status.HTTP_200_OK)
