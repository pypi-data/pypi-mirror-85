class ModuleNotFoundIgnore:
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is ModuleNotFoundError:
            pass
        return True


import re
from py2store.misc import get_obj

protocol_sep_p = re.compile("(\w+)://(.+)")

protocols = dict()

with ModuleNotFoundIgnore():
    from haggle import KaggleDatasets

    kaggle_data = KaggleDatasets()


    def get_kaggle_data(key):
        if key.startswith('kaggle://'):
            key = key[len('kaggle://'):]
        return kaggle_data[key]


    protocols['kaggle'] = get_kaggle_data

with ModuleNotFoundIgnore():
    from graze import Graze

    graze = Graze().__getitem__
    protocols['http'] = graze
    protocols['https'] = graze


def grab(key):
    if '://' in key:
        m = protocol_sep_p.match(key)
        if m:
            protocol, ref = m.groups()
            protocol_func = protocols.get(protocol, None)
            if protocol_func is None:
                raise KeyError(f"Unrecognized protocol: {protocol}")
            else:
                return protocol_func(key)
    return get_obj(key)


grab.prototols = list(protocols)

import urllib

DFLT_USER_AGENT = "Wget/1.16 (linux-gnu)"


def url_2_bytes(
        url, chk_size=1024, user_agent=DFLT_USER_AGENT
):
    def content_gen():
        req = urllib.request.Request(url)
        req.add_header("user-agent", user_agent)
        with urllib.request.urlopen(req) as response:
            while True:
                chk = response.read(chk_size)
                if len(chk) > 0:
                    yield chk
                else:
                    break

    return b"".join(content_gen())
