"""Account sync with integration

Revision ID: 57fea30b19ea
Revises: 529d35e4a8b4
Create Date: 2015-08-01 09:57:35.847842

"""

# revision identifiers, used by Alembic.
revision = '57fea30b19ea'
down_revision = '529d35e4a8b4'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('accounts', sa.Column('synchronize_people_with_integration_id', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('accounts', 'synchronize_people_with_integration_id')
