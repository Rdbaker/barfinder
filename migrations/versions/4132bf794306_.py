"""Adds ON DELETE CASCADE to business_tag.[tag_id|business_id] cols

Revision ID: 4132bf794306
Revises: a0202a937831
Create Date: 2017-04-27 23:21:03.929384

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4132bf794306'
down_revision = 'a0202a937831'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'business_tag_tag_id_fkey', 'business_tag', type_='foreignkey')
    op.drop_constraint(u'business_tag_business_id_fkey', 'business_tag', type_='foreignkey')
    op.create_foreign_key(None, 'business_tag', 'tag', ['tag_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'business_tag', 'business', ['business_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'business_tag', type_='foreignkey')
    op.drop_constraint(None, 'business_tag', type_='foreignkey')
    op.create_foreign_key(u'business_tag_business_id_fkey', 'business_tag', 'business', ['business_id'], ['id'])
    op.create_foreign_key(u'business_tag_tag_id_fkey', 'business_tag', 'tag', ['tag_id'], ['id'])
    # ### end Alembic commands ###
