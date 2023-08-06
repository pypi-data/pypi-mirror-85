import argparse
from limber.cli.generate_terraform import terraform

def get_parser():
    cli_parser = argparse.ArgumentParser(description='List the content of a folder')

    cli_parser.add_argument('--gcp-keyfile',
                           metavar='key-file',
                           type=str,
                           help='Google Cloud Keyfile')

    cli_parser.add_argument('--gcp-project',
                           metavar='project',
                           type=str,
                           help='Google Cloud Project')

    args = cli_parser.parse_args()

    t = terraform()
    t.create_terraform_configuration()