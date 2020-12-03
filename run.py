from src.antlr.antlr import Helper
import argparse
from antlr4 import FileStream

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-input', '--input', help='input')
    parser.add_argument('-output', '--output', help='output')
    args = parser.parse_args()
    input_stream = FileStream(args.input)
    tree_helper = Helper(input_stream)
    tree_helper.get_image(args.output)
