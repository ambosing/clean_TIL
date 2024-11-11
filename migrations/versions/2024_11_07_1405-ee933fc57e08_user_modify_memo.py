"""user - modify memo

Revision ID: ee933fc57e08
Revises: b3c5ae7b083a
Create Date: 2024-11-07 14:05:55.773561

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'ee933fc57e08'
down_revision: Union[str, None] = 'b3c5ae7b083a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('User', sa.Column('memo', sa.Text(), nullable=True))
    op.drop_column('User', 'user')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('User', sa.Column('user', mysql.TEXT(), nullable=True))
    op.drop_column('User', 'memo')
    # ### end Alembic commands ###
