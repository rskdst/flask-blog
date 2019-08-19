"""empty message

Revision ID: 091eb5dd6022
Revises: 8443ea318dd5
Create Date: 2019-08-18 20:27:08.900607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '091eb5dd6022'
down_revision = '8443ea318dd5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('music',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=300), nullable=True),
    sa.Column('singer', sa.String(length=100), nullable=True),
    sa.Column('image', sa.String(length=200), nullable=True),
    sa.Column('src', sa.String(length=300), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('music')
    # ### end Alembic commands ###