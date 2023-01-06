"""Create products Table

Revision ID: 97ece3c80cea
Revises: 
Create Date: 2023-01-06 15:18:17.799108

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97ece3c80cea'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("products",
                    sa.Column('id', sa.Integer, primary_key=True, index=True),
                    sa.Column('name', sa.String(256), nullable=False),
                    sa.Column('status', sa.Integer, nullable=False),
                    sa.Column('stock', sa.Integer, nullable=False),
                    sa.Column('description', sa.String(1024), nullable=True),
                    sa.Column('price', sa.Integer, nullable=False),
                    )

def downgrade():
    op.drop_table("products")
