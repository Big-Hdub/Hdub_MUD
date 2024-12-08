from quart import Quart
from app.models.db import init_app, initialize_db

def create_app():
    app = Quart(__name__)
    init_app(app)
    return app

app = create_app()

@app.before_serving
async def startup():
    await initialize_db(app)
