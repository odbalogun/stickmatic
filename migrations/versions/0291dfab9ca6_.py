"""empty message

Revision ID: 0291dfab9ca6
Revises: 
Create Date: 2020-08-12 23:57:42.175455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0291dfab9ca6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('test')
    # ### end Alembic commands ###