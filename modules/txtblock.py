"""
TXT block parsing for LangTool X modules.
"""

import re

def parse_text_block(lines):
    """
    Parse text block from .txt file and return (string_id, text content).
    Returns (int, list of (line, needs_line_break)) or (None, None).
    """
    if not lines:
        return None, None
    header = lines[0]
    id_match = re.match(r'\[String ID: (\d+)\]', header)
    if not id_match:
        return None, None
    string_id = int(id_match.group(1))
    text = []
    in_original_block = False  # Track if we're inside //...// block
    for line in lines[1:]:
        if not line:
            continue
        if line == '{EMPTY}':
            return string_id, []
        if line == '{INVALID}':
            return string_id, None
        # Check for start of original text block
        if line.startswith('//'):
            in_original_block = True
            # Check if this line also ends with // (single line block)
            if line.endswith('//'):
                in_original_block = False
            continue
        # Check for end of original text block (for multiline blocks)
        if in_original_block and line.endswith('//'):
            in_original_block = False
            continue
        # Skip lines inside original text block
        if in_original_block:
            continue
        if line.endswith('{LF}'):
            text.append((line[:-4], True))  # (text, needs_line_break)
        else:
            text.append((line, False))
    return string_id, text 