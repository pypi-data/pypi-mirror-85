from cli import cli_parser
import os
import argcomplete
from dotenv import load_dotenv
load_dotenv()

def main():
    """Main executable function"""
    parser = cli_parser.get_parser()
    argcomplete.autocomplete(parser)
    #args = parser.parse_args()
    #args.func(args)


if __name__ == '__main__':
    main()


