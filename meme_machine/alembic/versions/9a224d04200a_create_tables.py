"""create tables

Revision ID: 9a224d04200a
Revises:
Create Date: 2018-06-20 15:35:51.000336

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9a224d04200a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # User table
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("snowflake", sa.String, nullable=False, unique=True),
        sa.Column("username", sa.String, nullable=False),
        sa.Column("discriminator", sa.String, nullable=False),
        sa.Column("steam_profile_url", sa.String),
        # Constraints
        sa.UniqueConstraint("username", "discriminator"),
    )

    # Credit table
    op.create_table(
        "credit",
        sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id"),
                  primary_key=True),
        sa.Column("credits", sa.Integer, nullable=False),
        # Constraints
        sa.CheckConstraint("credits >= 0"),
    )

    # Credit Action table
    op.create_table(
        "credit_action",
        sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id"),
                  primary_key=True),
        # The datetime stored is the last active datetime + random cooldown
        # So, after the datetime, the user will be rewarded for being active
        sa.Column("next_active", sa.DateTime, nullable=False),
        # The same as above, but for dailies
        sa.Column("next_daily", sa.DateTime, nullable=False),
    )

    # Auth table
    op.create_table(
        "admin",
        sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id"),
                  primary_key=True),
    )

    # Category table
    op.create_table(
        "shop_item_category",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("display_name", sa.String, nullable=False),
        sa.Column("code_name", sa.String, nullable=False, unique=True),
    )

    # Shop Item table
    op.create_table(
        "shop_item",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("category_id", sa.Integer,
                  sa.ForeignKey("shop_item_category.id"), nullable=False),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("cost", sa.Integer, nullable=False),
        sa.Column("stock", sa.Integer, nullable=False),
        # Constraints
        sa.CheckConstraint("cost > 0"),
        sa.CheckConstraint("stock >= 0"),
    )

    # Transaction table
    op.create_table(
        "transaction",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("initiator_user_id", sa.Integer, sa.ForeignKey("user.id"),
                  nullable=False),
        sa.Column("item_id", sa.Integer, sa.ForeignKey("shop_item.id"),
                  nullable=False),
        sa.Column("status", sa.Integer, nullable=False),
    )

    # Raffle Slot table
    op.create_table(
        "raffle_slot",
        sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id"),
                  primary_key=True),
        sa.Column("slots", sa.Integer, nullable=False),
    )

    # Raffle table
    op.create_table(
        "raffle",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("max_slots", sa.Integer, nullable=False),
        sa.Column("item", sa.String, nullable=False),
    )


def downgrade():
    op.drop_table("raffle")
    op.drop_table("raffle_slot")
    op.drop_table("transaction")
    op.drop_table("shop_item")
    op.drop_table("shop_item_category")
    op.drop_table("admin")
    op.drop_table("credit_action")
    op.drop_table("credit")
    op.drop_table("user")
