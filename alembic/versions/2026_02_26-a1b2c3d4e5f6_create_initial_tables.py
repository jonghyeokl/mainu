"""create_initial_tables

Revision ID: a1b2c3d4e5f6
Revises:
Create Date: 2026-02-26 00:00:00.000000

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "a1b2c3d4e5f6"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("phone_number", sa.String(), nullable=False),
        sa.Column("created_dt", sa.DateTime(), nullable=False),
        sa.Column("updated_dt", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("user_id"),
    )

    op.create_table(
        "features",
        sa.Column("feature_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("feature", sa.String(), nullable=False),
        sa.Column("available_values", postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column("created_dt", sa.DateTime(), nullable=False),
        sa.Column("updated_dt", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("feature_id"),
    )

    op.create_table(
        "menus",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("created_dt", sa.DateTime(), nullable=False),
        sa.Column("updated_dt", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "choices",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("text", sa.String(), nullable=False),
        sa.Column("parsed_features", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("selected_menu_id", sa.Integer(), nullable=False),
        sa.Column("created_dt", sa.DateTime(), nullable=False),
        sa.Column("updated_dt", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"]),
        sa.ForeignKeyConstraint(["selected_menu_id"], ["menus.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("choices")
    op.drop_table("menus")
    op.drop_table("features")
    op.drop_table("users")
