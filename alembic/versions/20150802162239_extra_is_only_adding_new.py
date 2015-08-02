"""extra is_only_adding_new

Revision ID: f0ea428d204
Revises: 52b6c8317094
Create Date: 2015-08-02 16:22:39.541999

"""

# revision identifiers, used by Alembic.
revision = 'f0ea428d204'
down_revision = '52b6c8317094'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('people_synchronizations', sa.Column('is_only_adding_new', sa.Boolean(), nullable=False, server_default='1'))
    op.add_column('service_users', sa.Column('extra', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('service_users', 'extra')
    op.drop_column('people_synchronizations', 'is_only_adding_new')
