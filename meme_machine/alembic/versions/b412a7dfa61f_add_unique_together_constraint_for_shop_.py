"""add unique together constraint for shop item category and code name

Revision ID: b412a7dfa61f
Revises: 8ba89ef9391d
Create Date: 2018-07-07 14:48:10.809261

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "b412a7dfa61f"
down_revision = "8ba89ef9391d"
branch_labels = None
depends_on = None


def upgrade():
    # Requires that the table already fulfills the constraint
    with op.batch_alter_table("shop_item", schema=None) as batch_op:
        batch_op.create_unique_constraint(
            "uq_category_id_code_name", ["category_id", "code_name"])


def downgrade():
    with op.batch_alter_table("shop_item", schema=None) as batch_op:
        batch_op.drop_constraint("uq_category_id_code_name")
