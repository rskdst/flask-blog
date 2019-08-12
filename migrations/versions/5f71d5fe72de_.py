"""empty message

Revision ID: 5f71d5fe72de
Revises: 99160c38a757
Create Date: 2019-08-09 15:12:07.745517

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5f71d5fe72de'
down_revision = '99160c38a757'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('article', 'update_date',
               existing_type=mysql.DATETIME(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('article', 'update_date',
               existing_type=mysql.DATETIME(),
               nullable=True)
    # ### end Alembic commands ###