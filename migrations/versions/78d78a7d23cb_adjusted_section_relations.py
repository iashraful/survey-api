"""adjusted-section-relations

Revision ID: 78d78a7d23cb
Revises: f9b968761519
Create Date: 2021-09-16 07:07:17.467849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78d78a7d23cb'
down_revision = 'f9b968761519'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sections', sa.Column('survey_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'sections', 'surveys', ['survey_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'sections', type_='foreignkey')
    op.drop_column('sections', 'survey_id')
    # ### end Alembic commands ###