"""empty message

Revision ID: 92eba8416a79
Revises: e563c1cbd7a2
Create Date: 2020-08-17 12:33:12.441453

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92eba8416a79'
down_revision = 'e563c1cbd7a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('purchase_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('wallet_id', sa.Integer(), nullable=False),
    sa.Column('products', sa.Text(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('date_created', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['wallet_id'], ['wallets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('purchase_history')
    # ### end Alembic commands ###
