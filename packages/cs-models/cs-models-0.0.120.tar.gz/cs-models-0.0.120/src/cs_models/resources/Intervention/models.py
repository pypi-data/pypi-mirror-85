from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)

from ...database import Base


class InterventionModel(Base):
    __tablename__ = "interventions"

    id = Column(Integer, primary_key=True)
    intervention_uid = Column(String(50), nullable=False)
    preferred_term = Column(String(256), nullable=False)
    intervention_type = Column(String(128), nullable=True)
    pharm_action_id = Column(
        Integer,
        ForeignKey('pharm_actions.id'),
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )

    __table_args__ = (UniqueConstraint("intervention_uid", "preferred_term", "pharm_action_id"),)
