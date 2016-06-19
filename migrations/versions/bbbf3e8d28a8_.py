"""empty message

Revision ID: bbbf3e8d28a8
Revises: 034cc7be627d
Create Date: 2016-06-19 14:56:52.865131

"""

# revision identifiers, used by Alembic.
revision = 'bbbf3e8d28a8'
down_revision = '034cc7be627d'


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