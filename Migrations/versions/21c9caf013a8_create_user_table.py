"""Create user table

Revision ID: 21c9caf013a8
Revises: 
Create Date: 2023-04-01 10:12:58.458735

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21c9caf013a8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    sql = """
       CREATE TABLE user(id int primary key auto_increment not null,
       fname varchar(25) not null,lname varchar(25) not null,
       age int,national_id int unique not null,
       kra_pin varchar(12) unique not null); 
    """
    op.execute(sql)


def downgrade() -> None:
    op.drop_table('user')
