"""empty message

Revision ID: 3628506a4f8f
Revises: 4062abf514ba
Create Date: 2016-06-19 15:26:30.546558

"""

# revision identifiers, used by Alembic.
revision = '3628506a4f8f'
down_revision = '4062abf514ba'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


def upgrade():
    conn = op.get_bind()
    conn.execute(text("""insert into
                             search_criteria
                             (text)
                         values
                             ('city')""".format()))
    conn.execute(text("""insert into
        search_criteria
        (text)
    values
        ('purpose')""".format()))
    conn.execute(text("""insert into
        search_criteria
        (text)
    values
        ('metro')""".format()))
    conn.execute(text("""insert into
        search_criteria
        (text)
    values
        ('bill')""".format()))
    conn.execute(text("""insert into
        search_criteria
        (text)
    values
        ('features')""".format()))
    conn.execute(text("""insert into
        search_criteria
        (text)
    values
        ('type')""".format()))
    conn.execute(text("""insert into
        search_criteria
        (text)
    values
        ('cuisine')""".format()))


def downgrade():
    pass
