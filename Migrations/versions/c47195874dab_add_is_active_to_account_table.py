"""Add is_active to account table

Revision ID: c47195874dab
Revises: ccd433855f3f
Create Date: 2023-04-01 10:17:35.645214

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c47195874dab'
down_revision = 'ccd433855f3f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    sql = "alter table account add is_active boolean default true"
    op.execute(sql)


def downgrade() -> None:
    op.drop_column('account','is_active')