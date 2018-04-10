import os

import errno
from datetime import datetime

from os import path

import config


def get_file_path(user, directory='dm_logs'):
    return config.ROOT_DIR + os.sep + directory + os.sep + user.name + '_' + user.discriminator + '.log'


def get_latest_date_utc(user):
    try:
        return datetime.utcfromtimestamp(path.getmtime(get_file_path(user)))
    except FileNotFoundError:
        return None


def write_to_file(user, messages):
    file_path = get_file_path(user)

    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.makedirs(os.path.dirname(file_path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    if len(messages) > 0:
        with open(file_path, mode='a') as file:
            file.write('\n'.join(
                [config.dm_log_format.format(ts=m.timestamp if not m.edited_timestamp else m.edited_timestamp,
                                             u=m.author, uid=m.author.id, content=m.content) for m in
                 reversed(messages)]))
            file.write('\n')
