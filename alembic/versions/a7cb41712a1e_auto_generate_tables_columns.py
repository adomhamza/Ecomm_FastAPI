"""auto generate tables & columns

Revision ID: a7cb41712a1e
Revises: a3df7caa6a70
Create Date: 2022-06-11 21:46:27.459936

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "a7cb41712a1e"
down_revision = "a3df7caa6a70"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "posts",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("published", sa.Boolean(), server_default="True", nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("user_id", sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_table(
        "votes",
        sa.Column("user_id", sa.INTEGER(), nullable=False),
        sa.Column("post_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["post_id"],
            ["posts.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "post_id"),
    )
    op.drop_table("post")
    op.create_unique_constraint(None, "users", ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "users", type_="unique")
    op.create_table(
        "post",
        sa.Column(
            "id",
            postgresql.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("title", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("content", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            "published",
            sa.BOOLEAN(),
            server_default=sa.text("true"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="post_users_fk", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name="post_pkey"),
    )
    op.drop_table("votes")
    op.drop_table("posts")
    # ### end Alembic commands ###
