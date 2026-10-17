import sys

from .errors import LbsError
from .interpreter import run_source


def main():
    try:
        output = run_source(sys.stdin.read())
    except LbsError as exc:
        print(exc, file=sys.stderr)
        return 1

    print('Execution finished.')
    print('\n'.join(output))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
