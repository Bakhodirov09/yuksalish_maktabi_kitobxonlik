"""empty message

Revision ID: f9aa57663dbf
Revises: 8ba40a37c4b3
Create Date: 2024-01-01 23:31:10.056726

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f9aa57663dbf'
down_revision: Union[str, None] = '8ba40a37c4b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students', sa.Column('full_name', sa.String(), nullable=True))
    op.drop_column('students', 'name')
    op.drop_column('students', 'surname')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students', sa.Column('surname', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('students', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('students', 'full_name')
    # ### end Alembic commands ###
