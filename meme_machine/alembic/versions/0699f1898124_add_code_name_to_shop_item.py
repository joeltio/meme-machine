"""add code name to shop item

Revision ID: 0699f1898124
Revises: a12885ad2333
Create Date: 2018-06-30 16:51:59.786705

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0699f1898124"
down_revision = "a12885ad2333"
branch_labels = None
depends_on = None


def upgrade():
    # Only works if there is no data
    with op.batch_alter_table("shop_item", schema=None) as batch_op:
        batch_op.add_column(sa.Column("code_name", sa.String,
                                      server_default="", nullable=False))
        batch_op.alter_column("code_name", server_default=None)


def downgrade():
    with op.batch_alter_table("shop_item", schema=None) as batch_op:
        batch_op.drop_column("code_name")
