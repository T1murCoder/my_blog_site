"""убрал порядок постов

Revision ID: 62bb37a6d549
Revises: 18b16e9ef14a
Create Date: 2023-04-15 15:00:33.566485

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62bb37a6d549'
down_revision = '18b16e9ef14a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.create_foreign_key(None, 'comments', 'users', ['author_id'], ['id'], ondelete='CASCADE')
    op.alter_column('posts', 'post_tg_url',
               existing_type=sa.NUMERIC(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'post_tg_url',
               existing_type=sa.NUMERIC(),
               nullable=False)
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.create_foreign_key(None, 'comments', 'users', ['author_id'], ['id'])
    # ### end Alembic commands ###
