"""empty message

Revision ID: 6abbe930dc2a
Revises: 3fc0d373cd8c
Create Date: 2024-01-05 22:33:55.213494

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6abbe930dc2a'
down_revision: Union[str, None] = '3fc0d373cd8c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('parent_results', 'trues',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('parent_results', 'falses',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('rules', 'one_true_answer',
               existing_type=sa.REAL(),
               type_=sa.FLOAT(precision=1),
               existing_nullable=True)
    op.alter_column('rules', 'one_false_answer',
               existing_type=sa.REAL(),
               type_=sa.FLOAT(precision=1),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rules', 'one_false_answer',
               existing_type=sa.FLOAT(precision=1),
               type_=sa.REAL(),
               existing_nullable=True)
    op.alter_column('rules', 'one_true_answer',
               existing_type=sa.FLOAT(precision=1),
               type_=sa.REAL(),
               existing_nullable=True)
    op.alter_column('parent_results', 'falses',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    op.alter_column('parent_results', 'trues',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    # ### end Alembic commands ###
