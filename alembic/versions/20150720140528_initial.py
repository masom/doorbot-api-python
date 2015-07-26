"""initial

Revision ID: 4f913f2f63a5
Revises:
Create Date: 2015-07-20 14:05:28.865358

"""

# revision identifiers, used by Alembic.
revision = '4f913f2f63a5'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'accounts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column(
            'is_enabled', sa.Boolean(), nullable=False, server_default='1'
        ),
        sa.Column(
            'is_deleted', sa.Boolean(), nullable=False, server_default='0'
        ),
        sa.Column('host', sa.String(), nullable=False),
        sa.Column('contact_name', sa.String(), nullable=False),
        sa.Column('contact_email', sa.String(), nullable=False),
        sa.Column(
            'contact_email_confirmed', sa.Boolean(), nullable=False,
            server_default='0'
        ),
        sa.Column('contact_phone_number', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(
        'unique_host_on_accounts', 'accounts', ['host'], unique=True
    )

    op.create_table(
        'administrators',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column(
            'is_deleted', sa.Boolean(), nullable=False, server_default='0'
        ),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'integrations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('properties', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        'account_id_on_integrations', 'integrations', ['account_id']
    )

    op.create_table(
        'administrator_authentications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('administrator_id', sa.Integer(), nullable=False),
        sa.Column('provider_id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column(
            'is_deleted', sa.Boolean(), nullable=False, server_default='0'
        ),
        sa.Column('last_used_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['administrator_id'], ['administrators.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'doors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column(
            'is_deleted', sa.Boolean(), nullable=False, server_default='0'
        ),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index('account_id_on_doors', 'doors', ['account_id'])

    op.create_table(
        'devices',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('device_id', sa.String(), nullable=True),
        sa.Column('door_id', sa.Integer(), nullable=True),
        sa.Column('make', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('is_enabled', sa.Boolean(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.Column('token', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
        sa.ForeignKeyConstraint(['door_id'], ['doors.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('account_id_on_devices', 'devices', ['account_id'])
    op.create_index('token_on_devices', 'devices', ['token'], unique=True)

    op.create_table(
        'people',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=False),
        sa.Column('account_type', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('phone_number', sa.String(), nullable=True),
        sa.Column(
            'is_visible', sa.Boolean(), nullable=False, server_default='1'
        ),
        sa.Column(
            'is_available', sa.Boolean(), nullable=False, server_default='1'
        ),
        sa.Column(
            'is_deleted', sa.Boolean(), nullable=False, server_default='0'
        ),
        sa.Column(
            'notifications_enabled', sa.Boolean(), nullable=False,
            server_default='1'
        ),
        sa.Column(
            'notifications_app_enabled', sa.Boolean(), nullable=False,
            server_default='1'
        ),
        sa.Column(
            'notifications_chat_enabled', sa.Boolean(), nullable=False,
            server_default='0'
        ),
        sa.Column(
            'notifications_email_enabled', sa.Boolean(), nullable=False,
            server_default='0'
        ),
        sa.Column(
            'notifications_sms_enabled', sa.Boolean(), nullable=False,
            server_default='0'
        ),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index('account_id_on_people', 'people', ['account_id'])
    op.create_index(
        'unique_email_per_account_on_people', 'people',
        ['account_id', 'email'], unique=True
    )

    op.create_table(
        'person_authentications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=False),
        sa.Column('person_id', sa.Integer(), nullable=False),
        sa.Column('provider_id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column(
            'is_enabled', sa.Boolean(), nullable=False, server_default='1'
        ),
        sa.Column(
            'is_deleted', sa.Boolean(), nullable=False, server_default='0'
        ),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('last_used_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
        sa.ForeignKeyConstraint(['person_id'], ['people.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        'account_id_on_person_authentications', 'person_authentications',
        ['account_id']
    )
    op.create_index(
        'account_id_and_person_id_on_person_authentications',
        'person_authentications',
        ['account_id', 'person_id']
    )

    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=False),
        sa.Column('door_id', sa.Integer(), nullable=False),
        sa.Column('device_id', sa.Integer(), nullable=False),
        sa.Column('person_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
        sa.ForeignKeyConstraint(['device_id'], ['devices.id'], ),
        sa.ForeignKeyConstraint(['door_id'], ['doors.id'], ),
        sa.ForeignKeyConstraint(['person_id'], ['people.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        'account_id_on_notifications', 'notifications',
        ['account_id']
    )

    op.create_table(
        'service_users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=False),
        sa.Column('person_id', sa.Integer(), nullable=False),
        sa.Column('service', sa.String(), nullable=False),
        sa.Column('service_user_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('phone_number', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
        sa.ForeignKeyConstraint(['person_id'], ['people.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        'account_id_on_service_users', 'service_users',
        ['account_id']
    )
    op.create_index(
        'unique_service_user_per_account_on_service_users', 'service_users',
        ['account_id', 'service', 'service_user_id'],
        unique=True
    )


def downgrade():
    op.drop_table('service_users')
    op.drop_table('notifications')
    op.drop_table('person_authentications')
    op.drop_table('people')
    op.drop_table('devices')
    op.drop_table('doors')
    op.drop_table('administrator_authentications')
    op.drop_table('integrations')
    op.drop_table('administrators')
    op.drop_table('accounts')
