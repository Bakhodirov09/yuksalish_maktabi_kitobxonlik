"""empty message

Revision ID: e1118937bb1d
Revises: e1bdd89e525a
Create Date: 2024-01-05 19:41:33.790463

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1118937bb1d'
down_revision: Union[str, None] = 'e1bdd89e525a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rules', 'one_true_answer',
               existing_type=sa.NUMERIC(precision=2, scale=1),
               type_=sa.NUMERIC(precision=1, scale=1),
               existing_nullable=True)
    op.alter_column('rules', 'one_false_answer',
               existing_type=sa.NUMERIC(precision=2, scale=1),
               type_=sa.NUMERIC(precision=1, scale=1),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rules', 'one_false_answer',
               existing_type=sa.NUMERIC(precision=1, scale=1),
               type_=sa.NUMERIC(precision=2, scale=1),
               existing_nullable=True)
    op.alter_column('rules', 'one_true_answer',
               existing_type=sa.NUMERIC(precision=1, scale=1),
               type_=sa.NUMERIC(precision=2, scale=1),
               existing_nullable=True)
    # ### end Alembic commands ###
