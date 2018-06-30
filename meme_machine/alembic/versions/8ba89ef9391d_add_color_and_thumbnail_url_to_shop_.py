"""add color and thumbnail url to shop item category

Revision ID: 8ba89ef9391d
Revises: 0699f1898124
Create Date: 2018-06-30 20:37:06.961736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8ba89ef9391d"
down_revision = "0699f1898124"
branch_labels = None
depends_on = None


def upgrade():
    # Only works if there is no data
    with op.batch_alter_table("shop_item_category", schema=None) as batch_op:
        # Add color column
        batch_op.add_column(sa.Column("color", sa.String(6),
                                      server_default="", nullable=False))
        batch_op.alter_column("color", server_default=None)

        # Add thumbnail url column
        batch_op.add_column(sa.Column("thumbnail_url", sa.String,
                                      server_default="", nullable=False))
        batch_op.alter_column("thumbnail_url", server_default=None)


def downgrade():
    with op.batch_alter_table("shop_item_category", schema=None) as batch_op:
        batch_op.drop_column("color")
        batch_op.drop_column("thumbnail_url")
