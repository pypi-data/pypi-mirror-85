import os
import sys
import argparse

import execute_517


def main(cli_args, prog=None):
    paths = execute_517.__path__
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'python_arguments',
        type=str,
        nargs='?',
        help='command to run in env, will be passed as arguments to the python executable.',
    )

    parser.add_argument(
        '--srcdir',
        type=str,
        default=os.getcwd(),
        help='source directory (defaults to current directory)',
    )

    parser.add_argument(
        '--version',
        '-V',
        action='version',
        version='execute-517 {} ({})'.format(execute_517.__version__, ', '.join(path for path in paths if path)),
    )

    args = parser.parse_args(cli_args)

    if not args.python_arguments:
        print("Arguments to pass to python can not be empty.")
        sys.exit(1)

    pyargs = args.python_arguments
    if isinstance(args.python_arguments, str):
        pyargs = args.python_arguments.split(" ")

    sys.exit(execute_517.run_python_in_env(args.srcdir, pyargs))


def entrypoint():
    main(sys.argv[1:])

if __name__ == '__main__':  # pragma: no cover
    main(sys.argv[1:], 'python -m execute_517')
