#!/bin/sh


$(boot2docker shellinit)

export DOORBOT_DATABASE_URL=postgres://postgres:dev@$(boot2docker ip)/?sslmode=disable
export DOORBOT_USER_ACCOUNTS_DOMAIN=.doorbot.dev
export DOORBOT_CELERY_BROKER_URL=redis://$(boot2docker ip):6379/0

source ~/venv/doorbot-api/bin/activate
