"""move user info to another table

Revision ID: 0b5a2085b3b8
Revises: 117745bdd252
Create Date: 2018-07-17 10:24:05.460628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b5a2085b3b8'
down_revision = '117745bdd252'
branch_labels = None
depends_on = None


def upgrade():
    # Remove the steam profile url column. Does not copy the data overo
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_column("steam_profile_url")

    # Create User info table
    op.create_table(
        "user_info",
        sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id"),
                  primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("value", sa.String, nullable=False),
    )


def downgrade():
    op.drop_table("user_info")
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(sa.Column("steam_profile_url", sa.String))
