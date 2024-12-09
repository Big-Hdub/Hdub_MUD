from quart import Quart
from app.models.db import init_app, initialize_db
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Quart(__name__)
    app.config['GINO_DRIVER'] = os.getenv('GINO_DRIVER')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Initialize other components like Gino, Blueprints, etc.
    init_app(app)

    @app.before_serving
    async def startup():
        await initialize_db(app)

    return app

app = create_app()
