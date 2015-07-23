# -*- coding: utf-8 -*-

from flask import Blueprint, request
from ...container import container
from ...middlewares import (s, validate, auth_manager)
from .view_models import Integration as IntegrationViewModel
from ...models.integrations import (
    available_integrations, polymorph_integration
)


integrations = Blueprint(
    'integrations', __name__, url_prefix='/api/integrations'
)


def index():

    integrations = container.account.integrations.all()

    return dict(
        integrations=[
            IntegrationViewModel.from_integration(
                polymorph_integration(integration)
            )
            for integration in integrations
        ]
    )


def create():
    json = request.get_json()

    instance = None
    for integration in available_integrations:
        if integration.name == json['integration']['name']:
            instance = integration()
            break

    if not instance:
        return dict(), 400

    instance.properties = {}
    for name, value in json['integration'].items():
        if name not in integration.__properties__:
            continue

        instance.properties[name] = value

    instance.name = integration.name
    instance.is_active = json['integration'].get('is_active', False)
    container.account.integrations.append(instance)
    container.database.commit()

    return dict(
        integration=IntegrationViewModel.from_integration(instance)
    ), 201


integrations.add_url_rule(
    '', 'index',
    s(auth_manager, index),
    methods=['GET']
)

integrations.add_url_rule(
    '', 'create',
    s(auth_manager, validate('integration_create'), create),
    methods=['POST']
)
