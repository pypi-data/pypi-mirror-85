from typing import List, Any


def list_chunks(l: List[Any], n: int) -> List[List[Any]]:
    """Yield successive n-sized chunks from l.


        >>> list(list_chunks(['a', 'b', 'c', 'd'], 2))
        [['a', 'b'], ['c', 'd']]

        >>> list(list_chunks(list(range(11)), 3))
        [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10]]

        >>> list(list_chunks(list(range(10)), 30))
        [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
    """

    return [l[i:i + n] for i in range(0, len(l), n)]
