import urllib.parse

import uvicorn
from fastapi import FastAPI, status
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from deal_pages_watcher.db.query import get_watcher, create_watcher, delete_watcher, list_watchers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


class IsAnnotated(BaseModel):
    is_annotated: bool


class AnnotatedUrls(BaseModel):
    annotated_urls: list[str]


@app.post('/toggle_annotation/{url:path}', response_model=IsAnnotated, status_code=status.HTTP_200_OK)
async def toggle_annotation(url: str):
    url = urllib.parse.unquote(url)
    if watcher := get_watcher(url):
        delete_watcher(watcher)
        is_annotated = False
    else:
        create_watcher(url)
        is_annotated = True

    return {'is_annotated': is_annotated}


@app.get('/is_annotated/{url:path}', response_model=IsAnnotated, status_code=status.HTTP_200_OK)
async def check_is_annotated(url: str):
    url = urllib.parse.unquote(url)
    return {'is_annotated': get_watcher(url) is not None}


@app.get('/annotated_urls', response_model=AnnotatedUrls, status_code=status.HTTP_200_OK)
async def annotated_urls():
    return {'annotated_urls': [w.url for w in list_watchers()]}


@app.get('/', status_code=status.HTTP_204_NO_CONTENT)
async def root():
    pass


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
