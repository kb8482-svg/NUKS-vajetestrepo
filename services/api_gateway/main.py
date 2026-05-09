from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import List

from models import Base, Item as ItemModel
from database import engine, SessionLocal

app = FastAPI()

# Create tables
# podatkovan baza generir tabelo
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class ItemCreate(BaseModel):
    name: str
    description: str = None

class ItemRead(ItemCreate):
    id: int

    class Config:
        orm_mode = True

async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

# dekorator @, edino kar dela
@app.get("/")
def read_root():
    return "TODO app"

# pišemo pot, api enpoint , http metoda
@app.post("/items/", response_model=ItemRead)
async def create_item(item: ItemCreate, session: AsyncSession = Depends(get_session)):
    return "todo"

@app.get("/items/", response_model=List[ItemRead])
async def read_items(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(ItemModel))
    return result.scalars().all()

@app.get("/items/{item_id}", response_model=ItemRead)
async def read_item(item_id: int, session: AsyncSession = Depends(get_session)):
    return "todo"

#posodabljanje
# put /v1/api/items/ {id} da je dobro zavarovano
@app.put("/items/{item_id}", response_model=ItemRead)
async def update_item(item_id: int, item: ItemCreate, session: AsyncSession = Depends(get_session)):
    return "todo"

#brišemo stvari
@app.delete("/items/{item_id}")
async def delete_item(item_id: int, session: AsyncSession = Depends(get_session)):
    return "todo"

