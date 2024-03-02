from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import csv

# Definir el modelo de datos para los elementos en el CSV


class Item(BaseModel):
    id: int
    nombre: str
    edad: int
    salario: float
    fecha_nacimiento: str


# Inicializar la aplicación FastAPI
app = FastAPI()

# Ruta para obtener todos los elementos del CSV


@app.get("/items/")
async def read_items():
    items = []
    with open("data.csv", "r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            items.append(Item(**row))
    return items

# Ruta para obtener un elemento específico por su ID


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    with open("data.csv", "r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if int(row['id']) == item_id:
                return Item(**row)
    raise HTTPException(status_code=404, detail="Item not found")

# Ruta para agregar un nuevo elemento al CSV


@app.post("/items/")
async def create_item(item: Item):
    with open("data.csv", "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=item.dict().keys())
        if file.tell() == 0:  # Si el archivo está vacío, escribir encabezados
            writer.writeheader()
        writer.writerow(item.dict())
    return item
