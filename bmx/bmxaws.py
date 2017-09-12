#!/usr/bin/python3

import contextlib
import io
import re
import sys
import argparse

import awscli.clidriver

import bmx.bmxwrite as bmxwrite
import bmx.prompt as prompt

def create_parser():
    parser = argparse.ArgumentParser(
        prog='bmx-aws',
        usage='''

bmx-aws -h
bmx-aws [--username USERNAME] [--account ACCOUNT] [--role ROLE] CLICOMMAND CLISUBCOMMAND ...'''
)
    parser.add_argument('--username',
        help='specify username instead of being prompted')

    parser.add_argument('--account', default=None, help='the aws account name to auth against')

    parser.add_argument('--role', default=None, help='the aws role name to auth as')

    return parser

def cmd(args):
    [known_args, unknown_args] = create_parser().parse_known_args(args)

    while True:
        try:
            out = io.StringIO()
            err = io.StringIO()
            with contextlib.redirect_stdout(out):
                with contextlib.redirect_stderr(err):
                    ret = awscli.clidriver.create_clidriver().main(unknown_args)
        except SystemExit as ex:
            ret = ex.code

        if ret == 255 and (
            re.search('ExpiredToken', err.getvalue()) or
            re.search('credentials', err.getvalue())
        ):
            print("Your AWS STS token has expired.  Renewing...")

            bmxwrite.renew_credentials(known_args.username,
                                       app=known_args.account,
                                       role=known_args.role)
        else:
            break

    errstring = err.getvalue()
    if not prompt.is_empty(errstring):
        print(errstring, file=sys.stderr)

    outstring = out.getvalue()
    if not prompt.is_empty(outstring):
        print(outstring)

    return ret

def main():
    sys.exit(cmd(sys.argv))
