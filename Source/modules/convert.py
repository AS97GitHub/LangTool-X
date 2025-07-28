"""
Conversion logic for LangTool X modules.
"""

import os
import struct
import logging
from modules.utils import read_languages_from_ini, get_language_name, read_bed_file
from modules.datfile import read_dat_header, write_dat_file_table, validate_dat_structure
from modules.txtblock import parse_text_block

def convert_to_dat(txt_path, input_dat_path, output_dat_path, mode='table'):
    """
    Converts .txt file back to .dat format.
    Performs validation and outputs diagnostics.
    """
    try:
        ini_path = os.path.join(os.path.dirname(input_dat_path), 'version.ini')
        languages = read_languages_from_ini(ini_path)
        language = get_language_name(input_dat_path, languages)
        print(f"\nProcessing files:")
        print(f"- Input text: {txt_path}")
        print(f"- Template DAT: {input_dat_path}{language}")
        print(f"- Output DAT: {output_dat_path}")
        blocks = []
        current_block = []
        with open(txt_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\r\n')
                if line.startswith('[String ID:'):
                    if current_block:
                        blocks.append(current_block)
                        current_block = []
                current_block.append(line)
            if current_block:
                blocks.append(current_block)
        print(f"\nText file info:")
        print(f"- Found {len(blocks)} text blocks")
        with open(input_dat_path, 'rb') as fdat:
            header = fdat.read(4)
            str_num = struct.unpack('<I', header)[0] & 0xFFFF
            if len(blocks) != str_num:
                msg = f"WARNING: Number of blocks in .txt ({len(blocks)}) and .dat ({str_num}) do not match!"
                print(msg)
                logging.warning(msg)
        bed_path = os.path.join(os.path.dirname(input_dat_path), 'languages.bed')
        if os.path.exists(bed_path):
            string_ids, expected_blocks = read_bed_file(bed_path)
            if len(blocks) != len(string_ids):
                msg = f"WARNING: Number of blocks in .txt ({len(blocks)}) and .bed ({len(string_ids)}) do not match!"
                print(msg)
                logging.warning(msg)
        strings = []
        empty_blocks = 0
        invalid_blocks = 0
        for block in blocks:
            string_id, text_lines = parse_text_block(block)
            if string_id is None:
                continue
            if text_lines is None:
                strings.append('')
                invalid_blocks += 1
                continue
            text = ''
            for line, needs_break in text_lines:
                text += line
                if needs_break:
                    text += '\n'
            if not text:
                empty_blocks += 1
            strings.append(text)
        multiline_blocks = sum(1 for s in strings if '\n' in s)
        single_blocks = len(strings) - multiline_blocks - empty_blocks - invalid_blocks
        print(f"\nConversion diagnostics:")
        print(f"- Total blocks: {len(strings)}")
        print(f"- Empty blocks: {empty_blocks}")
        print(f"- Invalid blocks: {invalid_blocks}")
        print(f"- Multiline blocks: {multiline_blocks}")
        print(f"- Single line blocks: {single_blocks}")
        logging.info(f"Conversion: total={len(strings)}, empty={empty_blocks}, invalid={invalid_blocks}, multiline={multiline_blocks}, single={single_blocks}")
        if write_dat_file_table(output_dat_path, strings):
            validate_dat_structure(output_dat_path)
            return True
        return False
    except Exception as e:
        print(f"Error converting file: {e}")
        logging.error(f"Error converting file: {e}")
        return False 