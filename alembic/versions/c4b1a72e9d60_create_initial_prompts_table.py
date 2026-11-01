"""create initial prompts table

Revision ID: c4b1a72e9d60
Revises:
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c4b1a72e9d60"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "prompts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("category", sa.String(), nullable=True),
        sa.Column("content", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=False),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_prompts_id",
        "prompts",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_prompts_title",
        "prompts",
        ["title"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_prompts_title", table_name="prompts")
    op.drop_index("ix_prompts_id", table_name="prompts")
    op.drop_table("prompts")