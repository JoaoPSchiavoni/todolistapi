from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from todolist_api.schemas import Message

app = FastAPI(title='FastAPI de To Do List')


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Ola mundo!'}


@app.get('/ex', response_class=HTMLResponse)
def ola_mundo_html():
    return """
    <html>
      <head>
        <title> Nosso olá mundo!</title>
      </head>
      <body>
        <h1> Olá Mundo </h1>
      </body>
    </html>"""
