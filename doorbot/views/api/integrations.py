# -*- coding: utf-8 -*-

from flask import Blueprint, request
from ...container import container
from ...middlewares import (s, validate, auth_manager)
from .view_models import Integration as IntegrationViewModel

integrations = Blueprint(
    'integrations', __name__, url_prefix='/api/integrations'
)


def index():

    integrations = container.account.integrations.all()

    return dict(
        integrations=[
            IntegrationViewModel.from_integration(integration)
            for integration in integrations
        ]
    )


def create():
    json = request.get_json()
    print(json)


integrations.add_url_rule(
    '', 'index',
    s(auth_manager, index),
    methods=['GET']
)

integrations.add_url_rule(
    '', 'create',
    s(auth_manager, validate('account_integration_create'), create),
    methods=['POST']
)
