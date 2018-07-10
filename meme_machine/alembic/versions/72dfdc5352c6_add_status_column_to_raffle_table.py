"""add status column to raffle table

Revision ID: 72dfdc5352c6
Revises: 0271a3428bd4
Create Date: 2018-07-10 21:46:35.206014

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "72dfdc5352c6"
down_revision = "0271a3428bd4"
branch_labels = None
depends_on = None


def upgrade():
    # Only works if there is no data
    with op.batch_alter_table("raffle", schema=None) as batch_op:
        batch_op.add_column(sa.Column("status", sa.String,
                                      server_default="CLOSED", nullable=False))
        batch_op.alter_column("status", server_default=None)


def downgrade():
    with op.batch_alter_table("raffle", schema=None) as batch_op:
        batch_op.drop_column("status")
