"""empty message

Revision ID: a3074ea24c6d
Revises: 77908d9846c2
Create Date: 2024-01-03 21:44:58.978283

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a3074ea24c6d'
down_revision: Union[str, None] = '77908d9846c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('results')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('results',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('book', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('sovol', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('score', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('trues', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('falses', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('chat_id', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('date', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='results_pkey')
    )
    # ### end Alembic commands ###