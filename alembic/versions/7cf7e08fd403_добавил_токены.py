"""добавил токены

Revision ID: 7cf7e08fd403
Revises: 62bb37a6d549
Create Date: 2023-04-16 20:43:46.897837

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7cf7e08fd403'
down_revision = '62bb37a6d549'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    '''op.create_table('tokens',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('token', sa.String(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint(None, 'comments', type_='foreignkey')
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
    op.drop_table('tokens')
    # ### end Alembic commands ###
