import os
from typing import Union, List


def assert_env_vars(*args) -> Union[List[str], str]:
    li = []

    for a in args:
        v = os.environ.get(a)

        if v is None:
            raise AssertionError('{} environment variable required'.format(a))

        li.append(v)

    return li[0] if len(li) == 1 else li


def env_vars(*args) -> Union[List[str], str]:
    li = []

    for a in args:
        v = os.environ.get(a)

        if v is None:
            li.append(None)
        else:
            li.append(v)

    return li[0] if len(args) == 1 else li
