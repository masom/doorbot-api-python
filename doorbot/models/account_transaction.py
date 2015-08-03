# -*- coding: utf-8 -*-

import datetime
from ..core.model import DeclarativeBase
from sqlalchemy import Column, DateTime, Index, Integer, Numeric, Text


class AccountTransaction(DeclarativeBase):
    __tablename__ = 'account_transactions'

    id = Column(Integer, nullable=False, primary_key=True)
    account_id = Column(Integer, nullable=False)

    debit = Column(Numeric, nullable=True)
    credit = Column(Numeric, nullable=True)

    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

Index('account_id_on_account_transactions', AccountTransaction.account_id)
