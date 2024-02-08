"""empty message

Revision ID: 7255d6e586b4
Revises: 49261a63c779
Create Date: 2024-02-08 00:53:53.107154

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7255d6e586b4'
down_revision: Union[str, None] = '49261a63c779'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('parents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('surname', sa.String(), nullable=True),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('farzandi', sa.String(), nullable=True),
    sa.Column('farzand_sinf', sa.String(), nullable=True),
    sa.Column('farzand_sinf_guruxi', sa.String(), nullable=True),
    sa.Column('who', sa.String(), nullable=True),
    sa.Column('chat_id', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
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
    op.drop_table('parents')
    # ### end Alembic commands ###
