"""notification delivery

Revision ID: 529d35e4a8b4
Revises: 4f913f2f63a5
Create Date: 2015-07-26 19:02:33.334218

"""

# revision identifiers, used by Alembic.
revision = '529d35e4a8b4'
down_revision = '4f913f2f63a5'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'people_synchronizations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column(
            'status', sa.Enum(
                'pending', 'scheduled', 'running', 'failed', 'success',
                'error', name='job_statuses'
            ),
            nullable=False
        ),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        'account_id_on_people_synchronizations', 'people_synchronizations',
        ['account_id'], unique=False
    )
    op.create_table(
        'notification_deliveries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=False),
        sa.Column('notification_id', sa.Integer(), nullable=False),
        sa.Column('integration_id', sa.Integer(), nullable=False),
        sa.Column('response', sa.Text(), nullable=True),
        sa.Column(
            'status', sa.Enum(
                'pending', 'scheduled', 'running', 'failed', 'success',
                'error', name='job_statuses'
            ),
            nullable=False
        ),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
        sa.ForeignKeyConstraint(['integration_id'], ['integrations.id'], ),
        sa.ForeignKeyConstraint(['notification_id'], ['notifications.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        'account_id_on_notification_deliveriess', 'notification_deliveries',
        ['account_id'], unique=False
    )


def downgrade():
    op.drop_index(
        'account_id_on_notification_deliveriess',
        table_name='notification_deliveries'
    )
    op.drop_table('notification_deliveries')
    op.drop_index(
        'account_id_on_people_synchronizations',
        table_name='people_synchronizations'
    )
    op.drop_table('people_synchronizations')
