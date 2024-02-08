"""empty message

Revision ID: 8973ae992802
Revises: cee08f4b7e1e
Create Date: 2024-01-03 21:34:47.733372

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8973ae992802'
down_revision: Union[str, None] = 'cee08f4b7e1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('results', sa.Column('date', sa.FLOAT(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('results', 'date')
    # ### end Alembic commands ###
