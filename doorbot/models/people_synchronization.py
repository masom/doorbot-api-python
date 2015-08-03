# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy import (
    Boolean, Column, DateTime, Integer, ForeignKey, Enum, Index
)
from ..core.model import DeclarativeBase, JobStatuses
from structlog import get_logger
from ..db import db
from .person import Person

logger = get_logger()


class PeopleSynchronization(DeclarativeBase):
    __tablename__ = 'people_synchronizations'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    status = Column(
        Enum(*JobStatuses.to_list(), name="job_statuses"), nullable=False,
        default=JobStatuses.PENDING
    )

    is_only_adding_new = Column(Boolean, nullable=False, default=True)

    def synchronize(self):

        integration_id = self.account.synchronize_people_with_integration_id

        integration = self.account.integrations.filter_by(
            is_active=True,
            id=integration_id
        ).first()

        if not integration:
            self.status = JobStatuses.FAILED

            logger.info(
                'PeopleSynchronization integration not found',
                integration_id=integration_id,
                account_id=self.account_id,
                people_synchronization_id=self.id
            )

            db.session.commit()

            return False

        people_by_emails = {
            person.email: person
            for person in self.account.people.all()
        }
        existing_service_users_id = {
            user.service_user_id: user
            for user in self.account.service_users.all()
        }

        service_users = integration.adapter.fetch_people()
        for service_user in service_users:
            existing_service_user = existing_service_users_id.get(
                service_user.service_user_id,
                None
            )

            if existing_service_user:
                if self.is_only_adding_new:
                    continue

                existing_service_user.person.name = service_user.name
            else:
                person = people_by_emails.get(service_user.email, None)
                if person:
                    if not self.is_only_adding_new:
                        person.name = service_user.name
                        person.title = service_user.title
                        person.phone_number = service_user.phone_number

                else:
                    person = Person()
                    person.email = service_user.email
                    person.name = service_user.name
                    person.phone_number = service_user.phone_number
                    person.title = service_user.title

                    self.account.people.append(person)

                service_user.account_id = self.account_id
                person.service_users.append(service_user)

        db.session.commit()
        return True

Index(
    'account_id_on_people_synchronizations', PeopleSynchronization.account_id
)
