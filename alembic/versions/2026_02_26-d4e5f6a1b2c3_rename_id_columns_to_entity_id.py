"""rename_id_columns_to_entity_id

Revision ID: d4e5f6a1b2c3
Revises: c3d4e5f6a1b2
Create Date: 2026-02-26 03:00:00.000000

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d4e5f6a1b2c3"
down_revision = "c3d4e5f6a1b2"
branch_labels = None
depends_on = None


def upgrade():
    # Drop FK before renaming referenced column
    op.drop_constraint("choices_selected_menu_id_fkey", "choices", type_="foreignkey")

    # Rename menus.id → menus.menu_id
    op.alter_column("menus", "id", new_column_name="menu_id")

    # Rename choices.id → choices.choice_id
    op.alter_column("choices", "id", new_column_name="choice_id")

    # Recreate FK pointing to renamed column
    op.create_foreign_key(
        "choices_selected_menu_id_fkey",
        "choices",
        "menus",
        ["selected_menu_id"],
        ["menu_id"],
    )


def downgrade():
    op.drop_constraint("choices_selected_menu_id_fkey", "choices", type_="foreignkey")

    op.alter_column("menus", "menu_id", new_column_name="id")
    op.alter_column("choices", "choice_id", new_column_name="id")

    op.create_foreign_key(
        "choices_selected_menu_id_fkey",
        "choices",
        "menus",
        ["selected_menu_id"],
        ["id"],
    )
