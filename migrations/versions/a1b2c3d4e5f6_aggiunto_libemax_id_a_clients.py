"""aggiunto libemax_id a clients

Revision ID: a1b2c3d4e5f6
Revises: fdceeeba7cf8
Create Date: 2026-04-18 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = 'fdceeeba7cf8'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('clients', schema=None) as batch_op:
        batch_op.add_column(sa.Column('libemax_id', sa.Integer(), nullable=True))
        batch_op.create_unique_constraint('uq_clients_libemax_id', ['libemax_id'])


def downgrade():
    with op.batch_alter_table('clients', schema=None) as batch_op:
        batch_op.drop_constraint('uq_clients_libemax_id', type_='unique')
        batch_op.drop_column('libemax_id')
