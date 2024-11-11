"""Initial migration

Revision ID: 83f6df97a002
Revises:
Create Date: 2024-11-10 23:44:56.349710

"""
from typing import Sequence, Union
import os
from alembic import op
import sqlalchemy as sa
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the schema from the environment variables
SCHEMA = os.getenv("SCHEMA")

# revision identifiers, used by Alembic.
revision: str = '83f6df97a002'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create schema if it does not exist
    op.execute(f'CREATE SCHEMA IF NOT EXISTS {SCHEMA}')

    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email'),
        schema=SCHEMA
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # Drop users table
    op.drop_table('users', schema=SCHEMA)

    # Drop schema if it is empty
    op.execute(f'DROP SCHEMA IF EXISTS {SCHEMA} CASCADE')
    # ### end Alembic commands ###
