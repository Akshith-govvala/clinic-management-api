"""Initial migration - create tables.

Revision ID: 001_initial
Revises:
Create Date: 2026-08-18 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers
revision: str = "001_initial"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    # Create patients table
    op.create_table(
        "patients",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("phone", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_patients_id", "patients", ["id"], unique=False)

    # Create doctors table
    op.create_table(
        "doctors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("specialization", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_doctors_id", "doctors", ["id"], unique=False)

    # Create appointments table
    op.create_table(
        "appointments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("doctor_id", sa.Integer(), nullable=False),
        sa.Column("appointment_start", sa.DateTime(), nullable=False),
        sa.Column("appointment_end", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["patient_id"],
            ["patients.id"],
        ),
        sa.ForeignKeyConstraint(
            ["doctor_id"],
            ["doctors.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_appointments_id", "appointments", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_appointments_id", table_name="appointments")
    op.drop_table("appointments")
    op.drop_index("ix_doctors_id", table_name="doctors")
    op.drop_table("doctors")
    op.drop_index("ix_patients_id", table_name="patients")
    op.drop_table("patients")
