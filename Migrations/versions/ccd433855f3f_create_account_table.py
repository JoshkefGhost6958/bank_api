"""Create account table

Revision ID: ccd433855f3f
Revises: 21c9caf013a8
Create Date: 2023-04-01 10:15:18.855329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccd433855f3f'
down_revision = '21c9caf013a8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    sql = """
        CREATE TABLE account(acc_id int auto_increment primary key not null,
        owner_id int not null,
        acc_no bigint unique not null,
        card_no bigint unique not null,
        createdAt datetime default current_timestamp,
        pin varchar(100) not null,
        balance double default 0.0 not null,
        card_is_valid boolean default false,
        constraint user_fk foreign key(owner_id) references user(id)
        );
    """
    op.execute(sql)

def downgrade() -> None:
    sql = "Alter table account drop constraint user_fk;"
    op.execute(sql)
    op.drop_table('account')


