"""some fixes

Revision ID: 27ae0f11a8ae
Revises: 5bca8e150f0e
Create Date: 2023-04-15 14:27:38.830471

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27ae0f11a8ae'
down_revision = '5bca8e150f0e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    '''op.drop_constraint(None, 'comments', type_='foreignkey')
    op.create_foreign_key(None, 'comments', 'users', ['author_id'], ['id'], ondelete='CASCADE')
    op.alter_column('posts', 'post_tg_url',
               existing_type=sa.NUMERIC(),
               nullable=True)'''
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'post_tg_url',
               existing_type=sa.NUMERIC(),
               nullable=False)
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.create_foreign_key(None, 'comments', 'users', ['author_id'], ['id'])
    # ### end Alembic commands ###