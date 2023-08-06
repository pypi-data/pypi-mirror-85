"""Console script for pony_sayz."""
import argparse
import sys


def main():
    """Console script for pony_sayz."""
    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    args = parser.parse_args()

    #print("Arguments: " + str(args._))
    #print("Replace this message by putting your code into "
    #      "pony_sayz.cli.main")
    msg = '(empty)'

    if (len(args._) > 0):
        msg = args._[0]
    
    nr_traces = len(msg) + 4
    traces = '-' * nr_traces

    filepath = './data/rainbow.pony'
    line_nr = 1

    with open(filepath, encoding='utf-8') as fp:
        lines = fp.readlines()
        for line in lines:
            if line_nr > 21:
                if ('balloon10' in line):
                    print(traces)
                    print(line.replace('balloon10',msg).replace('$','').replace('\n',''))
                    print(traces)
                else:
                    print(line.replace('\n','').replace('$','')) 
            line_nr += 1

    return 0


def load_file():
    print('Load pony data file here.')


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
