import os
from quart import Quart
from gino import Gino
from dotenv import load_dotenv

load_dotenv()
SCHEMA = os.getenv("SCHEMA")
url = os.getenv("DATABASE_URL")

db = Gino()

def add_prefix_for_prod(attr):
    return f"{SCHEMA}.{attr}"

async def initialize_db(app: Quart, create_tables: bool = False):
    await db.set_bind(app.config['GINO_DATABASE'])
    if create_tables:
        await db.gino.create_all()
    return db

def init_app(app: Quart):
    app.config['GINO_DATABASE'] = os.getenv("DATABASE_URL")
    app.config['GINO_POOL_SIZE'] = 10
    app.config['GINO_MAX_INACTIVE_CONNECTION_LIFETIME'] = 300

    async def setup_db():
        await db.set_bind(app.config['GINO_DATABASE'])
    app.before_serving(setup_db)
