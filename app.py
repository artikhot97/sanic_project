from sanic import Sanic
from sanic.response import json
from my_blueprint import bp
from gino import Gino
import asyncio

app = Sanic('myapp')
app.config.DB_NAME = 'appdb'
app.config['DB_USER'] = 'appuser'


db_settings = {
    'DB_HOST': 'localhost',
    'DB_NAME': 'appdb',
    'DB_USER': 'appuser'
}
app.config.update(db_settings)

app.blueprint(bp)
from gino import Gino

db = Gino()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    fullname = db.Column(db.String)


class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(None, db.ForeignKey('users.id'))
    email_address = db.Column(db.String, nullable=False)


async def main():
    async with db.with_bind('postgresql://localhost/gino'):
        await db.gino.create_all()
        await User.create(name='jack', fullname='Jack Jones')
        print(await User.query.gino.all())

# asyncio.get_event_loop().run_until_complete(main())

@app.route('/hello')
async def test(request):
    return json({'hello': 'world'})

@app.route("/json")
def post_json(request):
  return json({ "received": True, "message": request.json })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)