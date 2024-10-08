"""skill added

Revision ID: 79852de0b0c2
Revises: e078b5d7af1d
Create Date: 2024-09-06 02:21:53.570197

"""
from typing import Sequence, Union

from alembic import op
import sqlmodel
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79852de0b0c2'
down_revision: Union[str, None] = 'e078b5d7af1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('place', 'level')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('place', sa.Column('level', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
