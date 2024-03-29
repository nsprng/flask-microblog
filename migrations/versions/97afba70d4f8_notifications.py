"""notifications

Revision ID: 97afba70d4f8
Revises: 7967aaeef0ce
Create Date: 2019-08-05 10:22:04.724489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97afba70d4f8'
down_revision = '7967aaeef0ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('recipient_id', sa.Integer(), nullable=True),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['recipient_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_timestamp'), 'message', ['timestamp'], unique=False)
    op.create_table('notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.Float(), nullable=True),
    sa.Column('payload_json', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_name'), 'notification', ['name'], unique=False)
    op.create_index(op.f('ix_notification_timestamp'), 'notification', ['timestamp'], unique=False)
    op.drop_index('ix_messsage_timestamp', table_name='messsage')
    op.drop_table('messsage')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('messsage',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('sender_id', sa.INTEGER(), nullable=True),
    sa.Column('recipient_id', sa.INTEGER(), nullable=True),
    sa.Column('body', sa.VARCHAR(length=140), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['recipient_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_messsage_timestamp', 'messsage', ['timestamp'], unique=False)
    op.drop_index(op.f('ix_notification_timestamp'), table_name='notification')
    op.drop_index(op.f('ix_notification_name'), table_name='notification')
    op.drop_table('notification')
    op.drop_index(op.f('ix_message_timestamp'), table_name='message')
    op.drop_table('message')
    # ### end Alembic commands ###
