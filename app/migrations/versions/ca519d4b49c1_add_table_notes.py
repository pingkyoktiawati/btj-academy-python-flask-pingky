"""add table notes

Revision ID: ca519d4b49c1
Revises: 24104b6e1e0c
Create Date: 2024-01-21 10:46:42.173887

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca519d4b49c1'
down_revision = '24104b6e1e0c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "notes",
        sa.Column("note_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("content", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True),
        sa.Column("deleted_at", sa.DateTime, nullable=True),
        sa.Column(
            "created_by", sa.Integer, sa.ForeignKey("users.user_id"), nullable=True
        ),
        sa.Column(
            "updated_by", sa.Integer, sa.ForeignKey("users.user_id"), nullable=True
        ),
        sa.Column(
            "deleted_by", sa.Integer, sa.ForeignKey("users.user_id"), nullable=True
        ),
    )


def downgrade() -> None:
    op.drop_table("notes")
