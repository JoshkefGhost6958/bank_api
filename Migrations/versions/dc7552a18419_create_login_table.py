"""Create login table

Revision ID: dc7552a18419
Revises: c47195874dab
Create Date: 2023-04-01 10:19:58.091829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc7552a18419'
down_revision = 'c47195874dab'
branch_labels = None
depends_on = None


def upgrade() -> None:
    sql = """
        Create table login(id int not null,
        username varchar(16) primary key not null,
        password varchar(100) not null,
        disabled boolean default true,
        constraint log_fk foreign key(id) references user(id)) 
    """
    op.execute(sql)


def downgrade() -> None:
    sql = "alter table login drop foreign key log_fk"
    op.execute(sql)
    op.drop_table('login')
    
