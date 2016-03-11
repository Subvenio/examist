"""Adding PDF paper downloads and conversion to HTML.

Revision ID: 4c21720db4f0
Revises: 6598bfa4b4e8
Create Date: 2016-03-05 17:36:31.001291

"""

# revision identifiers, used by Alembic.
revision = '4c21720db4f0'
down_revision = '6598bfa4b4e8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('paper_download',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('path', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Enum('unavailable', 'pending', 'available', name='paper_download_status'), nullable=True),
    sa.Column('paper_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['paper_id'], ['paper.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('paper_download')
    ### end Alembic commands ###