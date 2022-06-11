"""add foriegn key to post table

Revision ID: a3df7caa6a70
Revises: 5fae048c682b
Create Date: 2022-06-11 20:28:53.053141

"""
from alembic import op
from sqlalchemy import INTEGER, Boolean, Column, ForeignKey, String, false
from sqlalchemy.sql.expression import text, true
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = "a3df7caa6a70"
down_revision = "5fae048c682b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("post", Column("user_id", INTEGER, nullable=False))
    op.create_foreign_key(
        "post_users_fk",
        source_table="post",
        referent_table="users",
        local_cols=["user_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )

    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name="post")
    op.drop_column("post", "user_id")
    pass
