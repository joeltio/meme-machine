"""create config table

Revision ID: a12885ad2333
Revises: 9a224d04200a
Create Date: 2018-06-25 22:57:40.375172

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a12885ad2333"
down_revision = "9a224d04200a"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "config",
        sa.Column("name", sa.String, primary_key=True),
        sa.Column("value", sa.String, nullable=False),
    )


def downgrade():
    op.drop_table("config")
