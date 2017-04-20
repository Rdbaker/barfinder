"""empty message

Revision ID: 266930f92d64
Revises: a6db32044d2a
Create Date: 2017-04-19 22:23:05.577526

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '266930f92d64'
down_revision = 'a6db32044d2a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('raw_ai_message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('raw_fb_message', sa.Column('created_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('raw_ai_message')
    # ### end Alembic commands ###
