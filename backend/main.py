from typing import List, Dict

from fastapi import FastAPI
from enum import Enum

app = FastAPI()


class ModelName(str, Enum):
    first = 'first'
    sec = 'second'
    last = 'last'


class ItemMethod(str, Enum):
    name = 'name'
    slice = 'slice'


fake_items = [{'item name': 'Foo'}, {'item name': 'Bar'}, {'item name': 'Baz'}, {'item name': 'Buz'}]


@app.get("/")
async def root() -> dict[str, str]:
    # Example url: http://127.0.0.1:8000/
    return {"message": "Hello World!"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, something: str) -> dict[str, int | str]:
    # Example url: http://127.0.0.1:8000/items/1?something=str
    return {'item_id': item_id, 'something': something}


@app.get('/items/method/{item_method}/')
async def get_item(item_method: ItemMethod, skip: int | None = None, limit: int | None = None, name: str | None = None):
    """
    This is  bad practice. Because func return value only if item_method value in values on ItemMethod.
    Otherwise, it returns an error
    """
    if item_method.value == 'name':
        # Example url http://127.0.0.1:8000/items/method/name/?name=Foo
        for fake in fake_items:
            if name in fake.values():
                return fake
    elif item_method.value == 'slice':
        # Example url http://127.0.0.1:8000/items/method/slice/?skip=0&limit=10
        return fake_items[skip:skip + limit]
    else:
        # Doesn't work
        return fake_items


@app.get('/items/')
async def get_some_items(skip: int | None = None, limit: int | None = None, name: str | None = None):
    """
    Good choice
    """
    if name:
        # Example url http://127.0.0.1:8000/items/?name=Foo
        for fake in fake_items:
            if name in fake.values():
                return fake
    elif 0 <= skip <= limit and limit >= 0:
        # Example url http://127.0.0.1:8000/items/?skip=0&limit=2
        return fake_items[skip:skip + limit]
    else:
        return fake_items


@app.get("/users/me")
async def read_me_user() -> dict[str, str]:
    # Example url http://127.0.0.1:8000/users/me
    return {'user': 'current_user'}


@app.get('/users/{user_id}')
async def get_user(user_id: int) -> dict[str, int]:
    # Example url http://127.0.0.1:8000/users/1
    return {'user': user_id}


@app.get('/users')
async def all_users() -> list[str]:
    # Example url http://127.0.0.1:8000/users
    return ['Bob', 'John', 'Miki']


@app.get('/models/{model_name}')
async def get_model(model_name: ModelName) -> dict[str, str]:
    """
    In url params you must choose one of the values specified in ModelName
    """
    if model_name is ModelName.first:
        # Example url http://127.0.0.1:8000/models/first
        return {'model_name': model_name, 'message': f'This is first model'}
    if model_name.value == 'second':
        # Example url = http://127.0.0.1:8000/models/second
        return {'model_name': model_name, 'message': f'This is second model'}
    return {'model_name': model_name, 'message': f'This is last model'}


@app.get('/files/{file_path:path}')
async def read_file(file_path: str) -> dict[str, str]:
    # Example url http://127.0.0.1:8000/files//some_storage/some_file.txt
    # Pay attention to the double slash in the file address
    return {'file path': file_path}
