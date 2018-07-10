"""Add constraints for raffle tables

Revision ID: 0271a3428bd4
Revises: 505c4c5ba5d7
Create Date: 2018-07-10 18:00:17.539649

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "0271a3428bd4"
down_revision = "505c4c5ba5d7"
branch_labels = None
depends_on = None


def upgrade():
    # Requires that the table already fulfills the constraint
    # Add constraint slots > 0
    with op.batch_alter_table("raffle", schema=None) as batch_op:
        batch_op.create_check_constraint(
            "ck_max_slot_not_negative", "max_slots > 0")

    # Add constraint max_slot > 0
    with op.batch_alter_table("raffle_slot", schema=None) as batch_op:
        batch_op.create_check_constraint("ck_slot_not_negative", "slots > 0")


def downgrade():
    # Cannot be implemented as SQLAlchemy does not pick up on constraitns in
    # sqlite
    raise NotImplementedError("Downgrading is not implemented.")
