import urllib.parse

import uvicorn
from fastapi import FastAPI, status
from pydantic import BaseModel
from starlette.responses import Response

from deal_pages_watcher.db.query import get_watcher, create_watcher, delete_watcher

app = FastAPI()


class IsAnnotated(BaseModel):
    is_annotated: bool


@app.post('/annotate/{url:path}')
async def toggle_annotation(url: str):
    url = urllib.parse.unquote(url)
    if watcher := get_watcher(url):
        delete_watcher(watcher)
    else:
        create_watcher(url)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get('/is_annotated/{url:path}', response_model=IsAnnotated, status_code=status.HTTP_200_OK)
async def check_is_annotated(url: str):
    url = urllib.parse.unquote(url)
    return {'is_annotated': get_watcher(url) is not None}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
