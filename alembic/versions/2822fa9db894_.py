"""empty message

Revision ID: 2822fa9db894
Revises: e1118937bb1d
Create Date: 2024-01-05 19:45:28.698251

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2822fa9db894'
down_revision: Union[str, None] = 'e1118937bb1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rules', 'one_true_answer',
               existing_type=sa.NUMERIC(precision=1, scale=1),
               type_=sa.FLOAT(precision=1),
               existing_nullable=True)
    op.alter_column('rules', 'one_false_answer',
               existing_type=sa.NUMERIC(precision=1, scale=1),
               type_=sa.FLOAT(precision=1),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rules', 'one_false_answer',
               existing_type=sa.FLOAT(precision=1),
               type_=sa.NUMERIC(precision=1, scale=1),
               existing_nullable=True)
    op.alter_column('rules', 'one_true_answer',
               existing_type=sa.FLOAT(precision=1),
               type_=sa.NUMERIC(precision=1, scale=1),
               existing_nullable=True)
    # ### end Alembic commands ###