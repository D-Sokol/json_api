"""Create tables for advertisements and photos

Revision ID: d486e941c5db
Revises: 
Create Date: 2019-12-28 21:25:34.590205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd486e941c5db'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('advertisements',
    sa.Column('advert_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('advert_id')
    )
    op.create_table('photos',
    sa.Column('photo_id', sa.Integer(), nullable=False),
    sa.Column('advert_id', sa.Integer(), nullable=False),
    sa.Column('photo_link', sa.String(length=150), nullable=False),
    sa.ForeignKeyConstraint(['advert_id'], ['advertisements.advert_id'], ),
    sa.PrimaryKeyConstraint('photo_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('photos')
    op.drop_table('advertisements')
    # ### end Alembic commands ###