"""add user table

Revision ID: 5fae048c682b
Revises: 4b1596867456
Create Date: 2022-06-11 19:45:41.553596

"""
from alembic import op
from sqlalchemy import INTEGER, Boolean, Column, ForeignKey, String
from sqlalchemy.sql.expression import text, true
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = "5fae048c682b"
down_revision = "4b1596867456"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        Column(
            "id",
            INTEGER,
            nullable=False,
            unique=True,
            primary_key=True,
            autoincrement=True,
        ),
        Column(
            "email",
            String,
            nullable=False,
            unique=True,
        ),
        Column(
            "password",
            String,
            nullable=False,
        ),
        Column(
            "created_at",
            TIMESTAMP(timezone=true),
            server_default=text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("users")
    pass
