"""Added person table

Revision ID: 497e808991cc
Revises: 78654a971722
Create Date: 2018-07-19 13:55:48.742872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '497e808991cc'
down_revision = '78654a971722'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('person',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.add_column('descriptor', sa.Column('person_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'descriptor', 'person', ['person_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'descriptor', type_='foreignkey')
    op.drop_column('descriptor', 'person_id')
    op.drop_table('person')
    # ### end Alembic commands ###
