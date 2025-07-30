#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LangTool X - FlatOut 2/Ultimate Carnage/Head On language DAT/TXT/BED converter and extractor.
Provides CLI tools for extracting and converting language files.
"""

import sys
import os
import logging
from modules.extract import extract_strings
from modules.convert import convert_to_dat

# Setup logging to file
logging.basicConfig(
    filename='langtool.log', filemode='a', level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

def exit_with_pause():
    """
    Exit program with pause to keep window open.
    """
    input("Press Enter to exit...")
    sys.exit()

def print_usage():
    """
    Print usage information and examples for the CLI.
    """
    executable_name = os.path.basename(sys.argv[0])
    print(f"""
Usage:
  {executable_name} --extract --dat input.dat --bed input.bed --txt output.txt
  {executable_name} --convert --dat input.dat --bed input.bed --txt input.txt --out output.dat

Options:
  --extract            Extract text from .dat to .txt
  --convert            Convert .txt back to .dat
  --dat, -d            Path to .dat file
  --bed, -b            Path to .bed file
  --txt, -t            Path to .txt file (input or output)
  --out, -o            Output .dat file (for --convert)
  --original-d, -od    Path to original .dat file (for --extract, outputs original text as //...//)

Examples:
  {executable_name} --extract --dat language0.dat --bed languages.bed --txt language0.txt
  {executable_name} --extract --dat language0.dat --bed languages.bed --txt language0.txt --original-d language0.dat
  {executable_name} --convert --dat language0.dat --bed languages.bed --txt language0.txt --out new_language0.dat
""")
    exit_with_pause()


def main():
    """
    Main entry point: parse CLI arguments and run the requested action.
    """
    args = sys.argv[1:]
    if not args:
        print_usage()
        return
    action = None
    dat_path = None
    bed_path = None
    txt_path = None
    out_path = None  # Output path for .dat
    original_dat_path = None  # Path to original dat file
    i = 0
    while i < len(args):
        if args[i] == '--extract':
            action = 'extract'
            i += 1
        elif args[i] == '--convert':
            action = 'convert'
            i += 1
        elif args[i] in ('--dat', '-d'):
            if i + 1 < len(args):
                dat_path = args[i + 1]
                i += 2
            else:
                print("Error: Missing value for --dat/-d")
                return
        elif args[i] in ('--bed', '-b'):
            if i + 1 < len(args):
                bed_path = args[i + 1]
                i += 2
            else:
                print("Error: Missing value for --bed/-b")
                return
        elif args[i] in ('--txt', '-t'):
            if i + 1 < len(args):
                txt_path = args[i + 1]
                i += 2
            else:
                print("Error: Missing value for --txt/-t")
                return
        elif args[i] in ('--out', '-o'):
            if i + 1 < len(args):
                out_path = args[i + 1]
                i += 2
            else:
                print("Error: Missing value for --out/-o")
                return
        elif args[i] in ('--original-d', '-od'):
            if i + 1 < len(args):
                original_dat_path = args[i + 1]
                i += 2
            else:
                print("Error: Missing value for --original-d/-od")
                return
        else:
            print(f"Error: Unknown argument '{args[i]}'")
            return
    if not action:
        print("Error: Must specify --extract or --convert")
        return
    if action == 'extract':
        if not all([dat_path, bed_path, txt_path]):
            print("Error: Missing required arguments for extraction.\nRequired: --dat input.dat --bed input.bed --txt output.txt")
            return
    else:  # action == 'convert'
        if not all([dat_path, bed_path, txt_path, out_path]):
            print("Error: Missing required arguments for conversion.\nRequired: --dat input.dat --bed input.bed --txt input.txt --out output.dat")
            return
    if not os.path.exists(dat_path):
        print(f"Error: File {dat_path} not found.")
        return
    if not os.path.exists(bed_path):
        print(f"Error: File {bed_path} not found.")
        return
    if action == 'convert' and not os.path.exists(txt_path):
        print(f"Error: File {txt_path} not found.")
        return
    if action == 'extract':
        if extract_strings(dat_path, bed_path, txt_path, original_dat_path=original_dat_path):
            print(f"Text successfully extracted to {txt_path}")
        else:
            print("An error occurred while extracting text")
    else:  # action == 'convert'
        if convert_to_dat(txt_path, dat_path, out_path):
            print(f"Text successfully converted to {out_path}")
        else:
            print("An error occurred while converting text")

if __name__ == "__main__":
    main() 