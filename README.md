# LangTool X for FlatOut Series and Sega Rally Revo (PSP)

A command-line tool for extracting and converting language files used in FlatOut, FlatOut 2, FlatOut: Ultimate Carnage, FlatOut: Head On and Sega Rally Revo (PSP).

## About

LangTool X is designed for modders, translators, and enthusiasts working with the language files of FlatOut, FlatOut 2, FlatOut: Ultimate Carnage, FlatOut: Head On and Sega Rally Revo (PSP). The game stores all in-game text in binary `.dat` files, which are not human-readable and cannot be edited directly. LangTool X allows you to:
- Extract all text strings from `.dat` files into a plain `.txt` format.
- Convert edited `.txt` files back into `.dat`.
- Map string IDs to human-readable names using `.bed` files.
- Validate the structure of language files.
- Extract with original text reference using `--original-d` option.

## Features

- Cross-platform: works on Windows and Linux
- Both CLI and standalone `.exe` (via PyInstaller)
- Diagnostics and validation
- Short and long command-line options
- Original text reference for translation assistance

## Usage

> On Windows, you can use either `python` or `py` to run the script, depending on your Python installation.

Extract strings from a `.dat` file:
```sh
# Windows
python langtool_x.py --extract --dat language0.dat --bed languages.bed --txt language0.txt
# or with short options:
python langtool_x.py --extract -d language0.dat -b languages.bed -t language0.txt

# Linux
python3 langtool_x.py --extract --dat language0.dat --bed languages.bed --txt language0.txt
# or with short options:
python3 langtool_x.py --extract -d language0.dat -b languages.bed -t language0.txt
```

Extract with original text reference:
```sh
# Windows
python langtool_x.py --extract --dat language5.dat --bed languages.bed --txt language5.txt --original-d language0.dat
# or with short options:
python langtool_x.py --extract -d language5.dat -b languages.bed -t language5.txt -od language0.dat

# Linux
python3 langtool_x.py --extract --dat language5.dat --bed languages.bed --txt language5.txt --original-d language0.dat
# or with short options:
python3 langtool_x.py --extract -d language5.dat -b languages.bed -t language5.txt -od language0.dat
```

Convert `.txt` file back to `.dat`:
```sh
# Windows
python langtool_x.py --convert --dat language0.dat --bed languages.bed --txt language0.txt --out new_language0.dat
# or with short options:
python langtool_x.py --convert -d language0.dat -b languages.bed -t language0.txt -o new_language0.dat

# Linux
python3 langtool_x.py --convert --dat language0.dat --bed languages.bed --txt language0.txt --out new_language0.dat
# or with short options:
python3 langtool_x.py --convert -d language0.dat -b languages.bed -t language0.txt -o new_language0.dat
```

## Command-Line Options

- `--extract` / `--convert` — Select extraction or conversion mode
- `--dat`, `-d` — Path to the `.dat` file
- `--bed`, `-b` — Path to the `.bed` file
- `--txt`, `-t` — Path to the `.txt` file (input or output)
- `--out`, `-o` — Output `.dat` file (for conversion)
- `--original-d`, `-od` — Path to original `.dat` file (for extraction, outputs original text as `//...//`)
- `--help`, `-h` — Show help message

## Output Format

When using `--original-d`, the output `.txt` file will contain original text in the format:
```
[String ID: 31] [PS2_DNAS2_SS_SERVER_BUSY] [Do not remove {LF} tags]
//The network authentication server is busy.{LF}
Please try again later.//
Сервер проверки перегружен.{LF}
Повторите попытку позднее.
```

The original text (between `//...//`) is automatically ignored when converting back to `.dat`.

## Building

**Requirements:** Python 3.6 or newer

### Windows

You can build a standalone `.exe` using [PyInstaller](https://pyinstaller.org/):

Build .exe:
```sh
pip install pyinstaller
pyinstaller --onefile langtool_x.py
/dist/langtool_x.exe
```

### Linux

Build executable:
```sh
pip3 install pyinstaller
pyinstaller --onefile langtool_x.py
chmod +x ./dist/langtool_x  # if needed
```

## Project Structure

```
LangTool_X/Source/
    ├── langtool_x.py 
    └── modules/
        ├── convert.py
        ├── datfile.py
        ├── extract.py
        ├── txtblock.py
        └── utils.py
```

## License

MIT License. See [LICENSE](LICENSE).

## Credits

- Developed by AS97.
- **Inspired by the original "FO2 LangTool" developed by Burs.**
- **This Python version was developed in the [Cursor](https://www.cursor.so/) editor with the help of AI assistants: ChatGPT and Claude.**

*Feel free to contribute or report issues via GitHub!*
