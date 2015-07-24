#!/bin/sh


$(boot2docker shellinit)

export DOORBOT_DATABASE_URL=postgres://postgres:dev@$(boot2docker ip)/?sslmode=disable
export DOORBOT_USER_ACCOUNTS_DOMAIN=.doorbot.dev

source ~/venv/doorbot-api/bin/activate
