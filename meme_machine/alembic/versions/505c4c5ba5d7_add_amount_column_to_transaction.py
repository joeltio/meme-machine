"""add amount column to transaction

Revision ID: 505c4c5ba5d7
Revises: b412a7dfa61f
Create Date: 2018-07-07 16:39:38.947159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "505c4c5ba5d7"
down_revision = "b412a7dfa61f"
branch_labels = None
depends_on = None


def upgrade():
    # Only works if there is no data
    with op.batch_alter_table("transaction", schema=None) as batch_op:
        batch_op.add_column(sa.Column("amount", sa.Integer,
                                      server_default="1", nullable=False))
        batch_op.alter_column("amount", server_default=None)

        # Add check constraint to disallow non-positive values
        batch_op.create_check_constraint("ck_amount_positive", "amount > 0")


def downgrade():
    with op.batch_alter_table("transaction", schema=None) as batch_op:
        # Automaticall removes the check constraint as well
        batch_op.drop_column("amount")
