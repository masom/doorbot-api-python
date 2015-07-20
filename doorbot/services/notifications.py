# -*- coding: utf-8 -*-

from ..core.service import Service
from structlog import get_logger
logger = get_logger()


class Notifications(Service):
    def account_created(self, account, owner):
        logger.info(
            "Account created", account=account.__dict__, owner=owner.__dict__
        )
