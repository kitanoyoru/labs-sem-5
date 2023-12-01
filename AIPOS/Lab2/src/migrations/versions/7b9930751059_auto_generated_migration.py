"""Auto-generated migration

Revision ID: 7b9930751059
Revises: 8a973944ea4b
Create Date: 2023-12-01 04:06:33.067462

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "7b9930751059"
down_revision: Union[str, None] = "8a973944ea4b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("idx_trgm", table_name="t_location", postgresql_using="gist")
    op.drop_table("t_location")
    op.drop_index("idx_bloom", table_name="t_bloom", postgresql_using="bloom")
    op.drop_table("t_bloom")
    op.drop_table("t_reservation")
    op.drop_index("idx_fts_func", table_name="t_fts", postgresql_using="gin")
    op.drop_table("t_fts")
    op.add_column(
        "employee", sa.Column("is_trade_union_member", sa.Boolean(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("employee", "is_trade_union_member")
    op.create_table(
        "t_fts",
        sa.Column("comment", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column("ts", postgresql.TSVECTOR(), autoincrement=False, nullable=True),
    )
    op.create_index(
        "idx_fts_func",
        "t_fts",
        [sa.text("to_tsvector('english'::regconfig, comment)")],
        unique=False,
        postgresql_using="gin",
    )
    op.create_table(
        "t_reservation",
        sa.Column("room", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("from_to", postgresql.TSRANGE(), autoincrement=False, nullable=True),
    )
    op.create_table(
        "t_bloom",
        sa.Column("x1", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("x2", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("x3", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("x4", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("x5", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("x6", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("x7", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.create_index(
        "idx_bloom",
        "t_bloom",
        ["x1", "x2", "x3", "x4", "x5", "x6", "x7"],
        unique=False,
        postgresql_using="bloom",
    )
    op.create_table(
        "t_location", sa.Column("name", sa.TEXT(), autoincrement=False, nullable=True)
    )
    op.create_index(
        "idx_trgm", "t_location", ["name"], unique=False, postgresql_using="gist"
    )
    # ### end Alembic commands ###
