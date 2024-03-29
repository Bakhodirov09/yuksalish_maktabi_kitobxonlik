"""empty message

Revision ID: 0350ae0943f5
Revises: 7255d6e586b4
Create Date: 2024-02-08 01:19:03.383938

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0350ae0943f5'
down_revision: Union[str, None] = '7255d6e586b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rules',
    sa.Column('one_true_answer', sa.FLOAT(precision=1), nullable=True),
    sa.Column('one_false_answer', sa.FLOAT(precision=1), nullable=True),
    sa.Column('savollar', sa.Integer(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rules')
    # ### end Alembic commands ###
