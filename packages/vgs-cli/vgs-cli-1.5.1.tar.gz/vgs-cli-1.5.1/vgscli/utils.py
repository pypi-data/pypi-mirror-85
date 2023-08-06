import json
from datetime import datetime

import yaml
import os
import socket
import errno
import time

from collections import OrderedDict


class Literal(str):
    pass


class Quoted(str):
    pass


def quoted_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')


def literal_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')


def ordered_dict_presenter(dumper, data):
    return dumper.represent_dict(data.items())


yaml.add_representer(Quoted, quoted_presenter)
yaml.add_representer(OrderedDict, ordered_dict_presenter)
yaml.add_representer(Literal, literal_presenter)


def expired(exp):
    return time.time() > exp


def is_file_accessible(path, mode='r'):
    file_exists = os.path.exists(path) and os.path.isfile(path)
    if not file_exists:
        return False

    """
    Check if the file or directory at `path` can
    be accessed by the program using `mode` open flags.
    """
    try:
        f = open(path, mode)
        f.close()
    except IOError:
        return False
    return True


def is_port_accessible(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((host, port))
    except socket.error as e:
        return e.errno != errno.EADDRINUSE
    s.close()
    return True


def silent_file_remove(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


def to_timestamp(date):
    try:
        return int(datetime.timestamp(date))
    except (TypeError, ValueError):
        return None


def to_json(body):
    try:
        return json.loads(body.text)
    except Exception as ex:
        raise ex


def dump_yaml(data):
    return yaml.dump(data, default_flow_style=False, indent=2, width=1024)


def update_and_normalize(dump_data, process_listener, api_call_function, normalize):
    payloads = yaml.full_load(dump_data)
    results = []
    for data_item in payloads['data']:
        item_id = data_item['id']
        payload = {'data': data_item}
        result = api_call_function(item_id, payload)
        if process_listener:
            process_listener(item_id)
        results.append(result.body['data'])

    results = normalize(results)

    updated = {
        'version': 1,
        'data': results,
    }

    return dump_yaml(updated)


# Initially there were dev/sandbox/live environments, but currently there is only dev and prod.
# So in order to stay backward compatible with sandbox/live we try to resolve everything that is not dev as prod
def resolve_env(env):
    if env == "dev":
        return env
    else:
        return "prod"
