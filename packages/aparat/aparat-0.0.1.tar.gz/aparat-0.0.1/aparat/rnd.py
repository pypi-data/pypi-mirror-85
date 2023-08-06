import random
import string


def random_alphanum(length: int) -> str:
    """
    Creates random alphanumeric string with length given.
    """
    chars = string.ascii_letters + string.digits

    return ''.join((random.choice(chars)) for x in range(length))
