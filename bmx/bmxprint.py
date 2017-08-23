#!/usr/bin/python3

import sys
import json
import argparse

from . import bmxwrite

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', help='the Okta username')
    parser.add_argument(
        '--duration',
        default=3600,
        help='the requested STS-token lease duration'
    )

    formatting_group = parser.add_mutually_exclusive_group()
    formatting_group.add_argument(
        '-j',
        help='format the credentials as JSON',
        action='store_true'
    )
    formatting_group.add_argument(
        '-b',
        help='format the credentials for Bash',
        action='store_true'
    )
    formatting_group.add_argument(
        '-p',
        help='format the credentials for PowerShell',
        action='store_true'
    )

    return parser

def json_format_credentials(credentials):
    return json.dumps(
        {
            'AccessKeyId': credentials['AccessKeyId'],
            'SecretAccessKey': credentials['SecretAccessKey'],
            'SessionToken': credentials['SessionToken']
        },
        indent=4
    )

def bash_format_credentials(credentials):
    return """export AWS_ACCESS_KEY_ID='{}'
export AWS_SECRET_ACCESS_KEY='{}'
export AWS_SESSION_TOKEN='{}'""".format(
    credentials['AccessKeyId'],
    credentials['SecretAccessKey'],
    credentials['SessionToken']
)

def powershell_format_credentials(credentials):
    return """$env:AWS_ACCESS_KEY_ID = '{}'
$env:AWS_SECRET_ACCESS_KEY = '{}'
$env:AWS_SESSION_TOKEN = '{}'""".format(
    credentials['AccessKeyId'],
    credentials['SecretAccessKey'],
    credentials['SessionToken']
)

def format_credentials(args, credentials):
    formatted_credentials = None

    if args.b:
        formatted_credentials = bash_format_credentials(credentials)
    elif args.p:
        formatted_credentials = powershell_format_credentials(credentials)
    else:
        formatted_credentials = json_format_credentials(credentials)

    return formatted_credentials

def cmd(args):
    known_args = create_parser().parse_known_args(args)[0]

    credentials = bmxwrite.get_credentials(
        known_args.username,
        known_args.duration
    )

    print(format_credentials(known_args, credentials))

    return 0

def main():
    sys.exit(cmd(sys.argv))
