#!/usr/bin/env python

import argparse
from os import minor
import re as regex
import traceback
import sys

# local import
import request as extractor
import genqr
import totptest

def filter_activation_code(value):
    # This check was copied from Aruba's app, only basic validation here,
    # but the code itself has a validation rule too
    pat = regex.compile('^[2389][0-9]{17}$')
    if not pat.match(value):
        raise argparse.ArgumentTypeError('Invalid format')
    return value

def extract(activation_code, only_output, show_qr):
    seed = extractor.extract_otp(activation_code)
    print('Your seed is: {}'.format(seed))

    if not only_output:
        extractor.write_seed_file(seed)

    if show_qr:
        print_qr(seed)

def generate(seed, time):
    code = totptest.generate(seed, time)
    print('Your code is: {}'.format(code))

def print_qr(seed):
    genqr.generate_and_print(seed)



def check_python_version():
    # check majour version
    if sys.version_info.major < 3:
        print('You must use python 3 or higher')
        exit()
    
    # check minor release
    use_required = not (sys.version_info.major == 3 and sys.version_info.minor <= 6)

    return use_required

def main():
    # check version
    use_required = check_python_version()


    # parsing argument
    parser = argparse.ArgumentParser(description='This is a tool to extract ArubaOTP seed and generate OTP codes')

    # first sub command
    add_subparsers_params = {'required': True} if use_required else {}
    subparser = parser.add_subparsers(title='option', dest='option',
                                      description='What do you want to do?', **add_subparsers_params)

    # execute command
    execute_parser = subparser.add_parser('extract', help='Extract ArubaOTP seed')

    execute_parser.add_argument('activation_code', type=filter_activation_code, 
                                help='Activation code (the long number listed over the qr code)')
    execute_parser.add_argument('-o', '--only-output', action='store_true',
                                help='Do not save the OTP seed in the seed.txt file')
    execute_parser.add_argument('-q', '--show-qr', action='store_true',
                                help='Show a QR readable by OTP apps')

    # printqr command
    printqr_parser = subparser.add_parser('printqr', 
                                          help='Print a QR representation of the OTP seed for OTP apps')
    
    printqr_parser.add_argument('-s', '--seed', type=str,
                                help='Use seed in the paramter')

    # generate command
    generate_parser = subparser.add_parser('generate', help='Generate OTP by seed')

    generate_parser.add_argument('-s', '--seed', type=str,
                                 help='Use seed in the paramter')
    generate_parser.add_argument('-t', '--time', type=int,
                                 help='Generate OTP in a precise time (UnixEpoch time)')

    # parsing
    args = parser.parse_args()
    
    try:
        if   args.option == 'extract':
            extract(args.activation_code, args.only_output, args.show_qr)
        elif args.option == 'printqr':
            print_qr(args.seed)
        elif args.option == 'generate':
            generate(args.seed, args.time)
        else:
            print('Option is missing')
    except:
        traceback.print_exc()

if __name__ == '__main__':
    main()
