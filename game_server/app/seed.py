from dotenv import load_dotenv
import asyncio
from models.user import User
from models.db import db
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
SCHEMA = os.getenv('SCHEMA')
if not SCHEMA:
    raise ValueError("No SCHEMA set for the application")

print(f"Database URL: {DATABASE_URL}")
print(f"Schema: {SCHEMA}")

async def seed_users():
    try:
        print("Setting database bind...")
        await db.set_bind(DATABASE_URL)
        print("Database bind set.")

        # Add a delay to ensure the database bind is fully established
        await asyncio.sleep(1)

        print(f"Setting schema to {SCHEMA}...")
        await db.status(f'SET search_path TO {SCHEMA}')
        print(f"Schema set to {SCHEMA}.")

        print("Creating all tables...")
        await db.gino.create_all()
        print("Tables created.")
    except Exception as e:
        print(f"Error during database setup: {e}")

    # Ensure the database connection is established
    if not db.bind:
        print("Database connection not established.")
        return

    # Log the bind information
    print(f"Database bind info: {db.bind}")

    # Add a delay to ensure the database bind is fully established
    await asyncio.sleep(1)

    # Check if the Gino engine is initialized
    if not db.bind:
        print("Gino engine is not initialized yet.")
        return

    # Log the bind information again to confirm
    print(f"Database bind info after delay: {db.bind}")

    # Check the status of the connection pool
    pool_status = db.bind.raw_pool
    print(f"Connection pool status: {pool_status}")

    # Log the User model to ensure it is properly imported and initialized
    print(f"User model: {User}")

    # Check if the User model is properly connected to the database
    try:
        await User.query.gino.all()
        print("User model is properly connected to the database.")
    except Exception as e:
        print(f"Error checking User model connection: {e}")
        return

    users = [
        {"username": "user1", "password": "password1", "email": "user1@example.com"},
        {"username": "user2", "password": "password2", "email": "user2@example.com"},
        {"username": "user3", "password": "password3", "email": "user3@example.com"},
    ]

    for user_data in users:
        try:
            print(f"Creating user: {user_data['username']}")
            user = await User.create(username=user_data["username"], password=user_data["password"], email=user_data["email"])
            print(f"Created user: {user.username}")
        except Exception as e:
            print(f"Error creating user {user_data['username']}: {e}")

    print("Closing database connection...")
    await db.pop_bind().close()
    print("Database connection closed.")

if __name__ == "__main__":
    # To use this seeder file, run it from the command line:
    # $ python /home/Hdub/Hdub_MUD/game_server/app/seed.py
    asyncio.run(seed_users())
