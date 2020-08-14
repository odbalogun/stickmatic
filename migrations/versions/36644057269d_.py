"""empty message

Revision ID: 36644057269d
Revises: 0291dfab9ca6
Create Date: 2020-08-12 23:59:22.068172

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36644057269d'
down_revision = '0291dfab9ca6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('test')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###