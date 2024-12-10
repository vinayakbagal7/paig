"""added guardrails sensitive data table

Revision ID: 10852051b189
Revises: 8026d07174b9
Create Date: 2024-12-10 17:27:32.868849

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import core.db_models.utils


# revision identifiers, used by Alembic.
revision: str = '10852051b189'
down_revision: Union[str, None] = '8026d07174b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('gr_sensitive_data',
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('guardrail_provider', sa.Enum('AWS', 'PAIG', 'LLAMA', 'OPENAI', 'MULTIPLE', name='guardrailprovider'), nullable=False),
    sa.Column('description', sa.String(length=4000), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=False),
    sa.Column('update_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_gr_sensitive_data_create_time'), 'gr_sensitive_data', ['create_time'], unique=False)
    op.create_index(op.f('ix_gr_sensitive_data_id'), 'gr_sensitive_data', ['id'], unique=False)
    op.create_index(op.f('ix_gr_sensitive_data_update_time'), 'gr_sensitive_data', ['update_time'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_gr_sensitive_data_update_time'), table_name='gr_sensitive_data')
    op.drop_index(op.f('ix_gr_sensitive_data_id'), table_name='gr_sensitive_data')
    op.drop_index(op.f('ix_gr_sensitive_data_create_time'), table_name='gr_sensitive_data')
    op.drop_table('gr_sensitive_data')
    # ### end Alembic commands ###
