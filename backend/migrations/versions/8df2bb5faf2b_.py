"""empty message

Revision ID: 8df2bb5faf2b
Revises: c4d7f9729c0f
Create Date: 2023-08-07 12:45:42.870610

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8df2bb5faf2b'
down_revision = 'c4d7f9729c0f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('teacher_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('is_teacher', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('is_student', sa.Boolean(), nullable=False))
        batch_op.create_unique_constraint(None, ['username'])
        batch_op.create_unique_constraint(None, ['email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('is_student')
        batch_op.drop_column('is_teacher')
        batch_op.drop_column('teacher_id')

    # ### end Alembic commands ###
