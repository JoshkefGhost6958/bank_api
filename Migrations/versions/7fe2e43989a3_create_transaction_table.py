"""Create transaction table

Revision ID: 7fe2e43989a3
Revises: dc7552a18419
Create Date: 2023-04-01 10:23:55.234821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fe2e43989a3'
down_revision = 'dc7552a18419'
branch_labels = None
depends_on = None


def upgrade() -> None:
    sql = """
        CREATE TABLE transaction(
        transaction_id int auto_increment primary key not null,
        account bigint not null,
        recipient bigint not null,
        amount double not null,
        type tinyint not null,
        balance double not null,
        time datetime default current_timestamp,
        constraint transact_fk foreign key(account) references account(acc_no),
        constraint bal_check check (balance >= amount)
        );
    """
    op.execute(sql)

def downgrade() -> None:
    sql = [
        "alter table transaction drop foreign key transact_fk",
        "alter table transaction drop check bal_check;"
    ]
    for query in sql:
        op.execute(query)
    op.drop_table('transaction')
