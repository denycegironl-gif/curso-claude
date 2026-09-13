"""states catalog

Revision ID: 89caf812c827
Revises: 3a8360e04d4b
Create Date: 2026-09-12 21:11:53.588998

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '89caf812c827'
down_revision: str | Sequence[str] | None = '3a8360e04d4b'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

states_table = sa.table(
    "states",
    sa.column("code", sa.String),
    sa.column("sort_order", sa.Integer),
)

CATALOG = [
    {"code": "PENDIENTE", "sort_order": 1},
    {"code": "EN_CURSO", "sort_order": 2},
    {"code": "BLOQUEADA", "sort_order": 3},
    {"code": "HECHA", "sort_order": 4},
]


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "states",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(length=20), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.UniqueConstraint("code", name="uq_states_code"),
    )

    connection = op.get_bind()
    insert_stmt = sa.dialects.postgresql.insert(states_table).values(CATALOG)
    insert_stmt = insert_stmt.on_conflict_do_nothing(index_elements=["code"])
    connection.execute(insert_stmt)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("states")
