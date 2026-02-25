"""drop_all_tables

Revision ID: b2c3d4e5f6a1
Revises: a1b2c3d4e5f6
Create Date: 2026-02-26 01:00:00.000000

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b2c3d4e5f6a1"
down_revision = "a1b2c3d4e5f6"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("choices")
    op.drop_table("menus")
    op.drop_table("features")
    op.drop_table("users")


def downgrade():
    pass
