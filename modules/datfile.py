"""
DAT file operations for LangTool X modules.
"""

import struct
import os
import logging


def read_dat_header(dat_file):
    """
    Reads .dat file header and returns number of strings and text section offset.
    """
    header = dat_file.read(4)
    if len(header) < 4:
        raise Exception("Invalid .dat file: file too small")
    str_num = struct.unpack('<I', header)[0] & 0xFFFF
    entry_data = dat_file.read(8)
    if len(entry_data) < 8:
        raise Exception("Invalid .dat file: string table truncated")
    text_offset = struct.unpack('<I', entry_data[:4])[0]
    return str_num, text_offset


def read_dat_file_table(dat_path):
    """
    Read .dat file using string offset table method.
    Returns (number of strings, list of strings).
    """
    try:
        with open(dat_path, 'rb') as f:
            header = f.read(4)
            str_num = struct.unpack('<I', header)[0] & 0xFFFF
            strings = []
            for _ in range(str_num):
                str_pos = struct.unpack('<I', f.read(4))[0]
                str_len = struct.unpack('<I', f.read(4))[0]
                last_pos = f.tell()
                f.seek(str_pos)
                str_data = f.read(str_len * 2)  # *2 for UTF-16
                text = str_data.decode('utf-16le', errors='replace')
                strings.append(text)
                f.seek(last_pos)
            return str_num, strings
    except Exception as e:
        print(f"Error reading .dat file: {e}")
        logging.error(f"Error reading .dat file: {e}")
        return 0, []


def write_dat_file_table(output_path, strings):
    """
    Write .dat file using string offset table method.
    Returns True on success, False on error.
    """
    try:
        with open(output_path, 'wb') as f:
            str_num = len(strings)
            f.write(struct.pack('<H', str_num))    # Number of strings (2 bytes)
            f.write(struct.pack('<H', 0))          # Null word (2 bytes)
            str_pos = str_num * 8 + 4  # Initial offset
            positions = []
            for text in strings:
                str_len = len(text)
                positions.append((str_pos, str_len))
                str_pos += str_len * 2 + 2  # *2 for UTF-16 + 2 for separator
            for pos, length in positions:
                f.write(struct.pack('<I', pos))    # Position (4 bytes)
                f.write(struct.pack('<I', length)) # Length (4 bytes)
            for text in strings:
                encoded = text.encode('utf-16le')
                f.write(encoded)
                f.write(struct.pack('<H', 0))  # Separator (2 bytes)
            return True
    except Exception as e:
        print(f"Error writing .dat file: {e}")
        logging.error(f"Error writing .dat file: {e}")
        return False


def validate_dat_structure(dat_path):
    """
    Validate .dat file structure: check offsets and lengths for overlaps and bounds.
    """
    try:
        with open(dat_path, 'rb') as f:
            header = f.read(4)
            str_num = struct.unpack('<I', header)[0] & 0xFFFF
            entries = []
            for _ in range(str_num):
                str_pos = struct.unpack('<I', f.read(4))[0]
                str_len = struct.unpack('<I', f.read(4))[0]
                entries.append((str_pos, str_len))
            file_size = os.path.getsize(dat_path)
            text_offset = str_num * 8 + 4
            for idx, (pos, length) in enumerate(entries):
                if pos < text_offset or pos + length * 2 > file_size:
                    msg = f"WARNING: String {idx} position/length out of bounds: pos={pos}, len={length}"
                    print(msg)
                    logging.warning(msg)
            for idx, (pos, length) in enumerate(entries):
                rng = (pos, pos + length * 2)
                for other_idx, (op, ol) in enumerate(entries):
                    if idx != other_idx:
                        orng = (op, op + ol * 2)
                        if max(rng[0], orng[0]) < min(rng[1], orng[1]):
                            msg = f"WARNING: Overlap between string {idx} and {other_idx}"
                            print(msg)
                            logging.warning(msg)
    except Exception as e:
        msg = f"Error validating .dat structure: {e}"
        print(msg)
        logging.error(msg) 