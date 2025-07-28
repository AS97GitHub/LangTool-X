"""
Extraction logic for LangTool X modules.
"""

import os
import logging
from modules.utils import read_languages_from_ini, get_language_name, read_bed_file
from modules.datfile import read_dat_file_table

def extract_strings(dat_path, bed_path, output_path, mode='table', original_dat_path=None):
    """
    Extracts strings from .dat file and saves them to .txt.
    If original_dat_path is provided, also outputs original strings as //...// before translation.
    Performs validation and outputs diagnostics.
    """
    try:
        ini_path = os.path.join(os.path.dirname(dat_path), 'version.ini')
        languages = read_languages_from_ini(ini_path)
        language = get_language_name(dat_path, languages)
        print(f"\nProcessing files:")
        print(f"- DAT file: {dat_path}{language}")
        print(f"- BED file: {bed_path}")
        print(f"- Output: {output_path}")
        if original_dat_path:
            original_ini_path = os.path.join(os.path.dirname(original_dat_path), 'version.ini')
            original_languages = read_languages_from_ini(original_ini_path)
            original_language = get_language_name(original_dat_path, original_languages)
            print(f"- Original DAT: {original_dat_path}{original_language}")
        string_ids, expected_blocks = read_bed_file(bed_path)
        print(f"\nBED file info:")
        print(f"- Found {len(string_ids)} string IDs")
        print(f"- Expected blocks: {expected_blocks}")
        str_num, strings = read_dat_file_table(dat_path)
        original_strings = None
        if original_dat_path:
            orig_num, orig_strings = read_dat_file_table(original_dat_path)
            if orig_num != str_num:
                print(f"WARNING: Number of strings in original DAT ({orig_num}) and current DAT ({str_num}) do not match!")
            original_strings = orig_strings
        if len(string_ids) != str_num:
            msg = f"WARNING: Number of strings in .dat ({str_num}) and .bed ({len(string_ids)}) do not match!"
            print(msg)
            logging.warning(msg)
        file_size = os.path.getsize(dat_path)
        if str_num == 0:
            msg = "ERROR: No strings found in .dat file."
            print(msg)
            logging.error(msg)
            return False
        text_offset = str_num * 8 + 4
        print(f"\nDAT file structure:")
        print(f"- Number of strings: {str_num}")
        print(f"- Text section offset: 0x{text_offset:X}")
        print(f"- Header size: {text_offset} bytes")
        print(f"- Total file size: {file_size} bytes")
        print(f"- Text section size: {file_size - text_offset} bytes")
        empty_blocks = 0
        invalid_blocks = 0
        multiline_blocks = 0
        single_blocks = 0
        with open(output_path, 'w', encoding='utf-8') as out:
            for string_id, text in enumerate(strings):
                string_name = string_ids.get(string_id, f"String_{string_id}")
                if '\n' in text:
                    out.write(f"[String ID: {string_id}] [{string_name}] [Do not remove {{LF}} tags]\n")
                    multiline_blocks += 1
                else:
                    out.write(f"[String ID: {string_id}] [{string_name}]\n")
                    single_blocks += 1
                # Output original string if present
                if original_strings and string_id < len(original_strings):
                    orig_text = original_strings[string_id]
                    if orig_text == '':
                        out.write('//{EMPTY}//\n')
                    elif orig_text == '{INVALID}':
                        out.write('//{INVALID}//\n')
                    else:
                        # Convert multiline text to multiple lines with {LF} tags
                        orig_lines = orig_text.split('\n')
                        out.write('//')
                        for i, line in enumerate(orig_lines):
                            out.write(line)
                            if i < len(orig_lines) - 1:
                                out.write('{LF}\n')
                        out.write('//\n')
                if text:
                    lines = text.split('\n')
                    for i, line in enumerate(lines):
                        out.write(line)
                        if i < len(lines) - 1:
                            out.write('{LF}\n')
                        elif i == len(lines) - 1 and line:
                            out.write('\n')
                else:
                    out.write('{EMPTY}\n')
                    empty_blocks += 1
                out.write('\n')
        print(f"\nExtraction complete:")
        print(f"- Total blocks: {str_num}")
        print(f"- Empty blocks: {empty_blocks}")
        print(f"- Invalid blocks: {invalid_blocks}")
        print(f"- Multiline blocks: {multiline_blocks}")
        print(f"- Single line blocks: {single_blocks}")
        logging.info(f"Extraction: total={str_num}, empty={empty_blocks}, invalid={invalid_blocks}, multiline={multiline_blocks}, single={single_blocks}")
        return True
    except Exception as e:
        print(f"Error processing file: {e}")
        logging.error(f"Error processing file: {e}")
        return False 