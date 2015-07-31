# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, ForeignKey, Enum, Index
from ..core.model import DeclarativeBase, JobStatuses


class PeopleSynchronization(DeclarativeBase):
    __tablename__ = 'people_synchronizations'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    status = Column(
        Enum(*JobStatuses.to_list(), name="job_statuses"), nullable=False,
        default=JobStatuses.PENDING
    )

    def synchronize(self):

        integration = self.account.integrations.filter_by(
            is_enabled=True, is_deleted=False,
            name=self.account.synchronize_people_with_integration
        ).first()

        if not integration:
            return False

        integration.synchronize_people()
        return True

Index(
    'account_id_on_people_synchronizations', PeopleSynchronization.account_id
)
