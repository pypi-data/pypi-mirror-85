import argparse
from json import dumps as json_dumps

import textstat

from .cli import TextStatCli


def create_args():
    """
    Creates arguments for this main function.
    Returns the created parser object.
    """
    parser = argparse.ArgumentParser(description="Get stats about text files")
    parser.add_argument(
        "--language", "-l", default="en_US", help="Language to use as defined by en_US."
    )
    parser.add_argument(
        "--json",
        "-j",
        action="store_true",
        default=False,
        dest="use_json_output",
        help="Use argument to have the results output as json.",
    )
    parser.add_argument("path", help="Where to find these files to parse.", nargs="+")
    return parser


def render_output(textstat_cli, args):
    """
    Print results of the tests to the terminal
    """
    result = textstat_cli.to_dict()
    if args.use_json_output:
        print(json_dumps(result))
    else:
        text = ""
        for file_name in result:
            print(file_name)
            for test in result[file_name]:
                print(
                    "\t{test_name}: {score}".format(
                        test_name=test, score=result[file_name][test]
                    )
                )


if __name__ == "__main__":
    args = create_args().parse_args()
    textstat_cli = TextStatCli.from_args(args)
    render_output(textstat_cli, args)
