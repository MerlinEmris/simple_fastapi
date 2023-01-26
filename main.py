import datetime
from typing import Optional

from fastapi import FastAPI, Path

from pydantic import BaseModel

# App init
app = FastAPI()

products = [
    {'id': 1, 'name': "Karaca", 'desc': "Oran gowy kastyum", 'date': "10/02/2022"},
    {'id': 2, 'name': "Meleje", 'desc': "Oran gowy kastyum", 'date': "10/02/2022"},
    {'id': 3, 'name': "Saryja", 'desc': "Oran gowy kastyum", 'date': "10/02/2022"}
]

class Product(BaseModel):
    id: int
    name: Optional[str]=""
    desc: Optional[str]=""
    date: Optional[str]=datetime.date.today().__str__()


@app.get(path="/")
def index():
    return {"name": "first data"}


@app.get(path="/product/{id}")
def items(id: int = Path(default=None,description="Enter id of the product you want to get",gt=0))-> object:
    response: object = {"data": "not found"}
    for item in products:
        if item['id'] == id:
            response = {"data": item}
    return response


@app.get(path="/product")
def search_product(name: Optional[str]=None)->object:
    response: object = {"data": "not found"}
    result = []
    for product in products:
        if product['name'] == name:
            result.append(product)
    if len(result)>0:
        response = {"data": result}
    return response


@app.post(path='/create-product')
def create_product(product: Product):
    is_product_exists = False
    for prod,index in products:
        if prod['id'] == product['id']:
            products[index] = product
            is_product_exists = True
    if not is_product_exists:
        products.append(product)
    return products


@app.delete(path="/delete-product")
def delete_product(id: int):
    response: object = {"data": "not found"}
    for index in range(0,len(products)):
        if products[index]['id'] == id:
            del products[index]
            response = {"data": products}
    return response
