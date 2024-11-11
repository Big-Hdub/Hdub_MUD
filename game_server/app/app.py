from dotenv import load_dotenv
load_dotenv()

from quart_auth import AuthManager, login_required, current_user, AuthUser
from quart import Quart, websocket, request, redirect
from app.config.config import get_config_by_name
from app.models.user import User
from quart_cors import cors
from app.models.db import initialize_db
import asyncio
import os

config = os.getenv('QUART_ENV') or 'development'

async def create_app(config=None) -> Quart:
    app = Quart(__name__, static_folder='swaggerui')
    if config:
        app.config.from_object(get_config_by_name(config))

    app.config['GINO_DATABASE'] = os.getenv('DATABASE_URL')

    cors(app)

    AuthManager(app)

    @app.before_serving
    async def initialize():
        await initialize_db(app)


    @app.route("/login", methods=["POST"])
    async def login():
        data = await request.get_json()
        user = await User.query.where(User.username == data["username"]).gino.first()
        if user and user.password == data["password"]:
            auth_user = AuthUser(user.id)
            await auth_user.login()
            response = {"message": "Logged in"}
            return response
        return {"message": "Invalid credentials"}, 401

    @app.route("/protected")
    @login_required
    async def protected():
        return {"message": f"Hello, {current_user.id}"}

    @app.before_request
    def https_redirect():
        if os.environ.get('FLASK_ENV') == 'production':
            if request.headers.get('X-Forwarded-Proto') == 'http':
                url = request.url.replace('http://', 'https://', 1)
                code = 301
                return redirect(url, code=code)

    @app.after_request
    def inject_csrf_token(response):
        response.set_cookie(
            'csrf_token',
            secure=True if os.environ.get('FLASK_ENV') == 'production' else False,
            samesite='Strict' if os.environ.get('FLASK_ENV') == 'production' else None,
            httponly=True)
        return response

    @app.route("/")
    async def hello():
        return {"Hello": "World"}

    @app.websocket('/ws')
    async def ws():
        async with app.app_context():
            websocket.headers
            while True:
                try:
                    data = await websocket.receive()
                    print(f"Received message: {data}")
                    await websocket.send(f"Echo: {data}")
                except asyncio.CancelledError:
                    raise

    return app

def create_app_sync(config=None):
    return asyncio.run(create_app(config))

async def main():
    app = await create_app(config)
    return app

app = asyncio.run(main())

if __name__ == "__main__":
    app = asyncio.run(main())
