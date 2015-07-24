# -*- coding: utf-8 -*-

from flask import Blueprint, request
from ...container import container
from ...middlewares import (s, validate, auth_manager)
from .view_models import Integration as IntegrationViewModel
from ...models import Integration

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
    account = container.account

    instance = Integration(json['integration']['name'])
    if not instance.adapter:
        return dict(), 400

    exists = account.integrations.filter_by(name=instance.name).first()
    if exists and exists.allow_multiple is False:
        return dict(), 400

    instance.properties = {}
    for name, value in json['integration'].items():
        if name not in instance.adapter.properties:
            continue

        instance.properties[name] = value

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
