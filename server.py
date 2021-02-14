from sanic import Sanic, response
from sanic.response import text, json
#logger infomation
from sanic.log import logger
from sanic import Blueprint

from aiofiles import os as async_os
from sanic.response import file_stream

app = Sanic(__name__, load_env='MYAPP_')
# app = Sanic('myapp')
"""
Configuration of Project with DB
"""
app.config.DB_NAME = 'sanicDB'
app.config['DB_USER'] = 'appuser'

db_settings = {
    'DB_HOST': 'localhost',
    'DB_NAME': 'appdb',
    'DB_USER': 'appuser'
}
app.config.update(db_settings)


# Serves files from the static folder to the URL /static
app.static('/static', './static')


# Sample Example
@app.route("/")
async def home(request):
   return response.text("Hello Sanic")


@app.route("/movie_list")
async def index(request):
   file_path = "/Users/livehealth/Downloads/imdb.json t.json"

   file_stat = await async_os.stat(file_path)
   headers = {"Content-Length": str(file_stat.st_size)}

   file_content = await file_stream(
      file_path
   )
   json_file = json.loads(file_content)
   return json_file

@app.route("/myhomepage")
async def home(request):
   logger.info('Here is your log')
   return text("My home page!")

if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=8000, debug=True)
    app.run(debug=True, access_log=True)


