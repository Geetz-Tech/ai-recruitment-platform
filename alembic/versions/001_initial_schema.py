"""Initial schema creation

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('role', sa.String(50), nullable=False),
        sa.Column('is_active', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)

    op.create_table(
        'candidates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(255), nullable=False),
        sa.Column('last_name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('phone', sa.String(20)),
        sa.Column('current_status', sa.String(50), nullable=False),
        sa.Column('summary', sa.Text()),
        sa.Column('source', sa.String(100)),
        sa.Column('linkedin_url', sa.String(500)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )
    op.create_index(op.f('ix_candidates_id'), 'candidates', ['id'], unique=False)
    op.create_index(op.f('ix_candidates_email'), 'candidates', ['email'], unique=False)

    op.create_table(
        'job_openings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('department', sa.String(100)),
        sa.Column('location', sa.String(255)),
        sa.Column('salary_min', sa.Integer()),
        sa.Column('salary_max', sa.Integer()),
        sa.Column('recruiter_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('hiring_manager_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('is_open', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_job_openings_id'), 'job_openings', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_job_openings_id'), table_name='job_openings')
    op.drop_table('job_openings')
    op.drop_index(op.f('ix_candidates_email'), table_name='candidates')
    op.drop_index(op.f('ix_candidates_id'), table_name='candidates')
    op.drop_table('candidates')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
