import inspect
import random
import string
from itertools import combinations_with_replacement

import click

def makestr(chars):
    return "".join(
        random.choice(chars) for _ in range(random.randint(1, 20))
    )

def get_value(type):
    if type == int:
        return random.randint(-5, 20)
    elif type == float:
        return random.random()*25 - 5
    elif type == str:
        return random.choice(
            [
                "",
                makestr(string.ascii_letters),
                makestr(string.digits),
                makestr(string.printable),
            ],
        )
    elif type == tuple:
        nargs = random.randint(0, 5)
        return next(make_args(nargs)) if nargs else ()
    elif type == None:
        return None


def make_args(n):
    for types in combinations_with_replacement(
        [int, str, float, tuple, None],
        n
    ):
        yield tuple(get_value(t) for t in types)



def print_tests(fn, mod):
    results = {}
    ac = fn.__code__.co_argcount
    fname = fn.__qualname__
    for args in make_args(ac):
        try:
            results[args] = fn(*args)
        except Exception as e:
            results[args] = e
    print(f"\n\ndef test_{fname}():")
    for args in results:
        r = results[args]
        argstr = ', '.join(repr(arg) for arg in args)
        if isinstance(r, Exception):
            if random.random() < 0.8:
                continue  # not so many pytest.raises checks
            print(f"""    with pytest.raises({r.__class__.__qualname__}):
        {mod}.{fname}({argstr})""")
        else:
            print(f"    assert {mod}.{fname}({argstr}) == {r!r}")



@click.command()
@click.argument("filename", type=click.Path())
def cli(filename):
    m = __import__(filename[:-3])
    print(f"import pytest\n\nimport {filename[:-3]}")
    for member in dir(m):
        thing = getattr(m, member)
        if inspect.isfunction(thing):
            print_tests(thing, filename[:-3])

if __name__ == '__main__':
    cli()  # pytest: disable=no-value-for-parameter
