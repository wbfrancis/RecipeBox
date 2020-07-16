"""empty message

Revision ID: d6521a767e13
Revises: 
Create Date: 2020-07-07 11:44:34.047305

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd6521a767e13'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recipe_collections',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=300), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('recipes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=300), nullable=True),
    sa.Column('ingredients', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('instructions', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('recipe_collection_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['recipe_collection_id'], ['recipe_collections.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recipes')
    op.drop_table('recipe_collections')
    # ### end Alembic commands ###