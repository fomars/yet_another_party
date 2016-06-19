"""empty message

Revision ID: 3c690ff8b1f6
Revises: 380607bbf115
Create Date: 2016-06-19 03:22:28.000703

"""

# revision identifiers, used by Alembic.
revision = '3c690ff8b1f6'
down_revision = '380607bbf115'

"""empty message

Revision ID: 102506b297ef
Revises: bf7a4a70e10b
Create Date: 2016-06-18 18:13:36.379655

"""


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
