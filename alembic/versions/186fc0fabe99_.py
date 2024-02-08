"""empty message

Revision ID: 186fc0fabe99
Revises: 31e98645a3b0
Create Date: 2024-01-07 00:42:22.805663

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '186fc0fabe99'
down_revision: Union[str, None] = '31e98645a3b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('parent_results',
    sa.Column('id_raqam', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('surname', sa.String(), nullable=True),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('who', sa.String(), nullable=True),
    sa.Column('farzand_sinfi', sa.String(), nullable=True),
    sa.Column('farzand_sinfi_guruxi', sa.String(), nullable=True),
    sa.Column('book', sa.String(), nullable=True),
    sa.Column('score', sa.FLOAT(), nullable=True),
    sa.Column('trues', sa.Integer(), nullable=True),
    sa.Column('falses', sa.Integer(), nullable=True),
    sa.Column('date', sa.String(), nullable=False),
    sa.Column('chat_id', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id_raqam')
    )
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
    op.drop_table('parent_results')
    # ### end Alembic commands ###
