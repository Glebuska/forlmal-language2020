import argparse
from src.query_language_script import query_script


def script():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--script'
        , required=True
        , help='script language'
    )

    parser.add_argument(
        '--language'
        , required=True
        , help='path to language txt with syntax'
    )

    args = parser.parse_args()

    if query_script(args.script, args.language):
        print("String is accepted")
    else:
        print("String is declined")


script()
