"""add tasks table

Revision ID: e138d59a01df
Revises: e71de3ba4bf1
Create Date: 2024-03-19 11:41:54.326736

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e138d59a01df'
down_revision: Union[str, None] = 'e71de3ba4bf1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('topic', sa.LargeBinary(), nullable=False),
                    sa.Column('date', sa.DateTime(), nullable=True),
                    sa.Column('is_done', sa.Boolean(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks')
    # ### end Alembic commands ###
