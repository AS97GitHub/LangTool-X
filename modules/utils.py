"""
Utility functions for LangTool X modules.
"""

import os


def generate_missing_ids(str_num):
    """
    Generate string IDs when languages.bed is missing.
    Returns a dict {id: name} and the number of strings.
    """
    string_ids = {}
    for str_id in range(str_num):
        string_ids[str_id] = f"String_{str_id}"
    return string_ids, str_num


def read_bed_file(bed_path):
    """
    Reads .bed file and returns dictionary string_id -> string_name and total valid lines count.
    """
    string_ids = {}
    total_lines = 0
    try:
        with open(bed_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if '=' in line:
                    total_lines += 1
                    name, id_str = line.split('=')
                    name = name.strip()
                    try:
                        string_id = int(id_str.strip())
                        string_ids[string_id] = name
                    except ValueError:
                        print(f"Warning: Invalid string ID in line: {line}")
    except Exception as e:
        print(f"Error reading .bed file: {e}")
        return {}, 0
    return string_ids, total_lines


def read_languages_from_ini(ini_path='version.ini'):
    """
    Read language definitions from version.ini file.
    Returns a dict {lang_id: lang_name} or None.
    """
    languages = {}
    if not os.path.exists(ini_path):
        return None
    try:
        with open(ini_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('--'):
                    continue
                if line.startswith('LANGUAGE_'):
                    parts = [p.strip() for p in line.split('=')]
                    if len(parts) == 2:
                        name, value = parts
                        try:
                            lang_id = int(value)
                            lang_name = name.replace('LANGUAGE_', '')
                            languages[lang_id] = lang_name
                        except ValueError:
                            continue
    except Exception:
        return None
    return languages if languages else None


def get_language_name(dat_path, languages=None):
    """
    Get language name from .dat file name using version.ini mapping.
    """
    if languages is None:
        ini_path = os.path.join(os.path.dirname(dat_path), 'version.ini')
        languages = read_languages_from_ini(ini_path)
        if languages is None:
            return ""
    filename = os.path.basename(dat_path)
    if filename.startswith('language') and len(filename) >= 9:
        lang_num = filename[8:9]
        if lang_num.isdigit():
            lang_id = int(lang_num)
            if languages and lang_id in languages:
                return f" [{languages[lang_id]} ({lang_id})]"
    return "" 