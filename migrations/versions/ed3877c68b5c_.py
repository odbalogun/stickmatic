"""empty message

Revision ID: ed3877c68b5c
Revises: 92eba8416a79
Create Date: 2020-08-17 13:34:00.738284

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed3877c68b5c'
down_revision = '92eba8416a79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('purchase_history', sa.Column('wallet_balance', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('purchase_history', 'wallet_balance')
    # ### end Alembic commands ###
