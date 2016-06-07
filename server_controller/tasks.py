from __future__ import absolute_import
from celery import shared_task
from valve.source.rcon import RCON


@shared_task
def rcon_send(server, command):
    with RCON((server.ip, server.port), server.password) as rcon:
        return rcon(command)

