"""
empty message

Revision ID: 946bada3d9d5
Revises:
Create Date: 2017-05-16 13:48:19.338776
"""
from __future__ import absolute_import

# revision identifiers, used by Alembic.
revision = '946bada3d9d5'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sbe_event',
    sa.Column('community_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Unicode(), nullable=False),
    sa.Column('description', sa.Unicode(), nullable=False),
    sa.Column('location', sa.Unicode(), nullable=False),
    sa.Column('start', sa.DateTime(), nullable=False),
    sa.Column('end', sa.DateTime(), nullable=True),
    sa.Column('url', sa.Unicode(), nullable=False),
    sa.Column(u'id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['community_id'], [u'community.id'], ),
    sa.ForeignKeyConstraint([u'id'], [u'entity.id'], name=u'fk_inherited_entity_id', use_alter=True),
    sa.PrimaryKeyConstraint(u'id')
    )
    op.create_table('view',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('entity_id', sa.Integer(), nullable=False),
    sa.Column('_fk_entity_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['_fk_entity_id'], [u'entity.id'], ondelete=u'SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], [u'user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('view_id', sa.Integer(), nullable=True),
    sa.Column('viewed_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['view_id'], [u'view.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint(u'administratorship_group_id_fkey', 'administratorship', type_='foreignkey')
    op.drop_constraint(u'administratorship_user_id_fkey', 'administratorship', type_='foreignkey')
    op.create_foreign_key(None, 'administratorship', 'group', ['group_id'], ['id'], onupdate=u'CASCADE', ondelete=u'CASCADE')
    op.create_foreign_key(None, 'administratorship', 'user', ['user_id'], ['id'], onupdate=u'CASCADE', ondelete=u'CASCADE')
    op.add_column(u'forum_thread', sa.Column('last_post_at', sa.DateTime(), nullable=True))
    op.drop_constraint(u'membership_user_id_fkey', 'membership', type_='foreignkey')
    op.drop_constraint(u'membership_group_id_fkey', 'membership', type_='foreignkey')
    op.create_foreign_key(None, 'membership', 'user', ['user_id'], ['id'], onupdate=u'CASCADE', ondelete=u'CASCADE')
    op.create_foreign_key(None, 'membership', 'group', ['group_id'], ['id'], onupdate=u'CASCADE', ondelete=u'CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'membership', type_='foreignkey')
    op.drop_constraint(None, 'membership', type_='foreignkey')
    op.create_foreign_key(u'membership_group_id_fkey', 'membership', 'group', ['group_id'], ['id'])
    op.create_foreign_key(u'membership_user_id_fkey', 'membership', 'user', ['user_id'], ['id'])
    op.drop_column(u'forum_thread', 'last_post_at')
    op.drop_constraint(None, 'administratorship', type_='foreignkey')
    op.drop_constraint(None, 'administratorship', type_='foreignkey')
    op.create_foreign_key(u'administratorship_user_id_fkey', 'administratorship', 'user', ['user_id'], ['id'])
    op.create_foreign_key(u'administratorship_group_id_fkey', 'administratorship', 'group', ['group_id'], ['id'])
    op.drop_table('hit')
    op.drop_table('view')
    op.drop_table('sbe_event')
    # ### end Alembic commands ###
