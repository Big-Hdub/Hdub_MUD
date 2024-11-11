from dotenv import load_dotenv
import os
load_dotenv()
from quart import Quart
from gino import Gino
import gino_quart

environment = os.getenv("QUART_ENV")
SCHEMA = os.getenv("SCHEMA")

db = Gino()

def add_prefix_for_prod(attr):
    return f"{SCHEMA}.{attr}"

print(f"Environment: {environment}")
print(f"Schema: {SCHEMA}")

def init_app(app: Quart):
    app.config['GINO_DATABASE'] = os.getenv("DATABASE_URL")
    app.config['GINO_POOL_SIZE'] = 10
    app.config['GINO_MAX_INACTIVE_CONNECTION_LIFETIME'] = 300
    # Ensure the database connection is properly set up
    async def setup_db():
        await db.set_bind(app.config['GINO_DATABASE'])
    app.before_serving(setup_db)

async def initialize_db(app: Quart):
    async with app.app_context():
        await db.gino.create_all()
