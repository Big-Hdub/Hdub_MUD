from app.config.config import get_config_by_name
from hypercorn.config import Config
from quart import Quart, websocket
from app.models.user import User
from dotenv import load_dotenv
from app.models.db import db, init_app, initialize_db
import hypercorn.asyncio
import asyncio
import signal
import jwt
import os


load_dotenv()

def create_app(config=None):
    app = Quart(__name__)
    if config:
        app.config.from_object(get_config_by_name(config))
    else:
        app.config.from_object(get_config_by_name(os.getenv('MODE') or 'development'))
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    init_app(app)
    initialize_db(app, create_tables=False)
    return app

app = create_app()

@app.route('/')
async def home():
    return "Welcome to the Quart-Gino App!"

@app.route('/healthz')
async def health():
    return "OK", 200

@app.websocket('/ws')
async def websocket_handler():
    print("Websocket connection established.")
    token = websocket.args.get("token") if websocket.args else None
    if not token:
        print("Token required.")
        await websocket.send(f"Token required.")
        await websocket.close(code=4001, reason="Token required")
        return
    try:
        try:
            secret_key = app.config['SECRET_KEY']
            if not secret_key:
                raise ValueError("SECRET_KEY is missing.")
            user = jwt.decode(token, secret_key, algorithms=["HS256"])
        except KeyError:
            print("SECRET_KEY is not set in the app config.")
            await websocket.send("Server configuration error.")
            await websocket.close(code=4001, reason="Server configuration error")
            return
        except ValueError as e:
            print(str(e))
            await websocket.send(str(e))
            await websocket.close(code=4001, reason=str(e))
            return
        # Add the message to the queue
        message_queue.put_nowait(user["name"])
        print(f"User authenticated: {user}")
    except jwt.ExpiredSignatureError:
        await websocket.send(f"Token expired.")
        await websocket.close(code=4001, reason="Token expired")
        return
    except jwt.InvalidTokenError:
        print("Invalid token.")
        await websocket.send(f"Invalid token.")
        await websocket.close(code=4001, reason="Invalid token")
        return

async def batch_save_messages():
    while True:
        messages = []
        while not message_queue.empty():
            messages.append(await message_queue.get())
        if messages:
            await User.insert().gino.all([{"name": msg} for msg in messages])
        await asyncio.sleep(5)

message_queue = asyncio.Queue()

async def start():
    """
    Starts the game server by setting up the necessary configurations and running the server.

    This function performs the following steps:
    1. Calls the setup function to initialize the environment.
    2. Retrieves the current event loop.
    3. Creates a future object to handle server shutdown.
    4. Configures the server to bind to the specified host and port.
    5. Adds a signal handler for SIGTERM to gracefully stop the server.
    6. Starts the Hypercorn server with the specified configuration.
    7. Waits for the server and the stop future to complete, along with batch saving messages.

    Note:
        Signal handlers may not be implemented in some environments, such as Windows.

    Raises:
        NotImplementedError: If signal handlers are not implemented in the current environment.
    """
    # await db.set_bind(app.config['GINO_DATABASE'])

    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
    config = Config()
    config.bind = [f"0.0.0.0:{os.getenv('PORT', 5000)}"]

    if __name__ == "__main__":
        server = await hypercorn.asyncio.serve(app, config)
        await asyncio.gather(server, stop, batch_save_messages())

if __name__ == "__main__":
    asyncio.run(start())
