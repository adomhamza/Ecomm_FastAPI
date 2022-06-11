"""create post table

Revision ID: 4b1596867456
Revises: 
Create Date: 2022-06-11 18:58:36.802076

"""
from alembic import op
from sqlalchemy import INTEGER, Boolean, Column, ForeignKey, String
from sqlalchemy.sql.expression import text, true
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = "4b1596867456"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "post",
        Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=text("uuid_generate_v4()"),
            unique=True,
            nullable=False,
        ),
        Column("title", String, nullable=False),
        Column("content", String, nullable=False),
        Column("published", Boolean, server_default="True", nullable=False),
        Column(
            "created_at",
            TIMESTAMP(timezone=true),
            server_default=text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("post")
    pass
