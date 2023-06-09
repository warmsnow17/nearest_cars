"""initial migration

Revision ID: 6d4d135c8231
Revises: 
Create Date: 2023-05-26 13:00:22.841311

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '6d4d135c8231'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('state', sa.String(), nullable=True),
    sa.Column('zip_code', sa.Integer(), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cargo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pick_up_location_id', sa.Integer(), nullable=True),
    sa.Column('delivery_location_id', sa.Integer(), nullable=True),
    sa.Column('weight', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['delivery_location_id'], ['location.id'], ),
    sa.ForeignKeyConstraint(['pick_up_location_id'], ['location.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('truck',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('unique_number', sa.String(), nullable=True),
    sa.Column('current_location_id', sa.Integer(), nullable=True),
    sa.Column('load_capacity', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['current_location_id'], ['location.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('truck')
    op.drop_table('cargo')
    op.drop_table('location')
    # ### end Alembic commands ###
