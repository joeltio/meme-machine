"""add positive constraint to raffle slot slots

Revision ID: 117745bdd252
Revises: 299c69d6fabf
Create Date: 2018-07-16 17:21:06.507062

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "117745bdd252"
down_revision = "299c69d6fabf"
branch_labels = None
depends_on = None


def upgrade():
    # The table should already meet this constraint
    with op.batch_alter_table("raffle_slot", schema=None) as batch_op:
        batch_op.create_check_constraint("ck_slots_positive", "slots > 0")


def downgrade():
    # The only way to do this (for now) is to drop the column and recreate it
    raise NotImplementedError()
    # If you are sure you want to do this, comment the line above
    with op.batch_alter_table("raffle_slot", schema=None) as batch_op:
        batch_op.drop_column("slots")
        batch_op.add_column(sa.Column("slots", sa.Integer,
                                      server_default="", nullable=False))
        batch_op.alter_column("slots", server_default=None)
