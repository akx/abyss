import runpy
import sys

from abyss.simple import profiling


def main():
    sys.argv = sys.argv[1:]
    print(sys.argv)
    with profiling(interval=0.001):
        runpy.run_path(sys.argv[0], run_name="__main__")


if __name__ == "__main__":
    main()
