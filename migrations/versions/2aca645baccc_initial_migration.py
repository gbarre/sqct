"""initial migration

Revision ID: 2aca645baccc
Revises:
Create Date: 2020-11-02 09:39:59.919300

"""
from alembic import op
import sqlalchemy as sa
import models


# revision identifiers, used by Alembic.
revision = '2aca645baccc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.String(length=32), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('tosses',
    sa.Column('id', models.GUID(), nullable=False),
    sa.Column('elected', sa.Text(), nullable=False),
    sa.Column('user_id', sa.String(length=32), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tosses')
    op.drop_table('users')
    # ### end Alembic commands ###