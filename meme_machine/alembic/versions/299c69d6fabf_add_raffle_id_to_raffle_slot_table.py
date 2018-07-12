"""Add raffle id to raffle slot table

Revision ID: 299c69d6fabf
Revises: 72dfdc5352c6
Create Date: 2018-07-11 21:27:23.327478

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "299c69d6fabf"
down_revision = "72dfdc5352c6"
branch_labels = None
depends_on = None


def upgrade():
    # Note that SQLite does not enforce foreign key constraints unless the
    # pragma for foreign keys is set

    # Requires the table to be empty
    with op.batch_alter_table("raffle_slot", schema=None) as batch_op:
        # Drop the primary key constraint of the user_id column by dropping the
        # column
        batch_op.drop_column("user_id")
        # Add the new columns
        batch_op.add_column(sa.Column("id", sa.Integer, primary_key=True))

        # Add the user_id column
        batch_op.add_column(sa.Column("user_id", sa.Integer, nullable=False))
        # Create foreing key constraint
        batch_op.create_foreign_key("fk_user_id_user_id", "user",
                                    ["user_id"], ["id"])

        # Add the raffle_id column
        batch_op.add_column(sa.Column("raffle_id", sa.Integer,
                                      nullable=False))
        # Create foreign key constraint
        batch_op.create_foreign_key("fk_raffle_id_raffle_id", "raffle",
                                    ["raffle_id"], ["id"])


def downgrade():
    # Requires the table to be empty
    with op.batch_alter_table("raffle_slot", schema=None) as batch_op:
        # Drop all columns
        batch_op.drop_column("id")
        # batch_op.drop_column("user_id")
        batch_op.drop_column("raffle_id")

        # Recreate the user_id column as the primary key
        batch_op.add_column(sa.Column("user_id", sa.Integer, primary_key=True))
        # Create foreign key
        batch_op.create_foreign_key("fk_user_id_user_id", "user",
                                    ["user_id"], ["id"])
