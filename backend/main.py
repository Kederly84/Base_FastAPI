from enum import Enum

from fastapi import FastAPI, Query
from pydantic import Required

from models import Item

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
    """
    Don't forget about query parameters in the URL. Specified without a slash.
    """
    # Example url: http://127.0.0.1:8000/items/1?something=str
    return {'item_id': item_id, 'something': something}


@app.get('/items/method/{item_method}/')
async def get_item(item_method: ItemMethod, skip: int | None = None, limit: int | None = None, name: str | None = None):
    """
    This is bad practice. Because func return value only if item_method value in values in ItemMethod.
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


@app.get('/test/{test_id}')
async def get_test(test_id: str, flag: str | None = None, desc: str | None = None) -> dict[str, str]:
    test = {'test_id': test_id}
    # Example url http://127.0.0.1:8000/test/one
    if flag:
        # Example url http://127.0.0.1:8000/test/one&flag=flag
        test.update({'flag': flag})
    if not desc:
        # Example url http://127.0.0.1:8000/test/one&flag=flag
        test.update({'description': "This is test sample"})
    else:
        # Example url http://127.0.0.1:8000/test/one?flag=Foo&desc=Some%20desc
        test.update({'desc': desc})
    return test


@app.get('/test/{test_id}/test_item/{test_item_id}')
async def read_test_item(test_id: str, test_item_id: int, desc: str | None = None, flag: bool = False):
    result = {'test_id': test_id, 'test_item_id': test_item_id}
    # Example url http://127.0.0.1:8000/test/test_id/test_item/1
    if desc:
        # Example url http://127.0.0.1:8000/test/test_id/test_item/1?desc=some_desc
        result.update({'desc': desc})
    if flag:
        # Example url http://127.0.0.1:8000/test/test_id/test_item/1?desc=some_desc&flag=1
        result.update({'flag': flag})
    return result


@app.post('/items')
async def create_item(item: Item):
    """I test it with Postman"""
    item_dict = item.dict()
    if item.tax:
        price = item.price + item.price * item.tax
        item_dict.update({'price with tax': price})
    return item_dict


@app.put('/items/{item_id}')
async def update_item(item_id: int, item: Item,
                      some_data: str | None = Query(default=None, min_length=5, max_length=50)):
    """I test it with Postman"""
    # Wrong url http://127.0.0.1:8000/items/1?some_data=Another%20data%20big%20usless%20data%20it%20so%20long%20data%20with%20so%20many%20characters
    result = {"item_id": item_id, **item.dict()}
    if some_data:
        result.update({"some_data": some_data})
    return result


@app.get("/something")
async def get_something(question: list[str] = Query(default=Required, min_length=3)):
    """"In this case question required parameter
    You can set a required parameter as a various types
    Example url http://127.0.0.1:8000/something?question=quest&question=tion
    """
    results = {'something': [{"first_name": "Foo"}, {"second_name": "Bar"}]}
    if question:
        results.update({"question": question})
    return results


@app.get('/something_else')
async def get_something_else(
        question: str | None = Query(default=None, title="String", description="Awesome description", min_length=3,
                                     alias='some_alias')):
    """
    Other options:
    alias - replace variable name
    deprecated - mark parameter as deprecated in docs, but he is still using
    include_in_schema=False - exclude parameter from docs
    """
    result = {"something_else": [{"first_name": "Foo"}, {"second_name": "Bar"}]}
    # Example url http://127.0.0.1:8000/something_else?some_alias=alias
    if question:
        result.update({"question": question})
    return result
