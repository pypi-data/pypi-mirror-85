"""Parameter space exploration tool.

See the documentation at https://github.com/amorison/parspace
"""

from itertools import product


class ParSpace:
    """Parameter space explorer.

    Example:
        >>> @ParSpace(asp=[0.5, 1, 2],
        >>>           density=[1, 10])
        >>> def launch_simu(asp, density):
        >>>     print(f"aspect ratio {asp} and density {density}")
        >>> launch_simu()
        aspect ratio 0.5 and density 1
        aspect ratio 0.5 and density 10
        aspect ratio 1 and density 1
        aspect ratio 1 and density 10
        aspect ratio 2 and density 1
        aspect ratio 2 and density 10
    """

    def __init__(self, **space):
        self._space = space

    def _sweeper(self):
        parnames = sorted(self._space.keys())
        for comb in product(*(self._space[name] for name in parnames)):
            yield dict(zip(parnames, comb))

    def __call__(self, func):
        def wrapper():
            for comb in self._sweeper():
                func(**comb)
        return wrapper
