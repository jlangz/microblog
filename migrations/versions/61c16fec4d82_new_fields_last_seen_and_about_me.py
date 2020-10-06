"""new fields, last seen and about me

Revision ID: 61c16fec4d82
Revises: 9f3c0aeab7e5
Create Date: 2020-10-02 17:19:51.779096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61c16fec4d82'
down_revision = '9f3c0aeab7e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.String(length=140), nullable=True))
    op.add_column('user', sa.Column('last_see', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_see')
    op.drop_column('user', 'about_me')
    # ### end Alembic commands ###
