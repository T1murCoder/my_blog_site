"""добавил фидбек

Revision ID: 20c163a1bf2a
Revises: c295037c79de
Create Date: 2023-04-23 21:22:21.069517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20c163a1bf2a'
down_revision = 'c295037c79de'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
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
