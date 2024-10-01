from fastapi import FastAPI, Path
from starlette import status
from logic import fetch_items, fetch_item
from routers import items

app = FastAPI()
app.include_router(items.router)

@app.get("/", status_code=status.HTTP_200_OK)
async def read_list():
    items = fetch_items()

    return {"items": items}

@app.get("/{id_item}", status_code=status.HTTP_200_OK)
async def read_item(id_item: int = Path(gt=0)):
    item = fetch_item(id_item)

    return item

@app.post("/", status_code=status.HTTP_201_CREATED)
async def create():
    return {"message": "create"}

@app.put("/{id_item}", status_code=status.HTTP_204_NO_CONTENT)
async def update(id_item: int):
    return {"message": "modify id: " + str(id_item) }

@app.delete("/{id_item}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id_item: int):
    return {"message": "delete id: " + str(id_item)}

@app.get('/healthy')
def health_check():
    return {'status': 'Healthy'}
