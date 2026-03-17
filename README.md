<p align="center">
  <img src="logo2.png" width="300">
</p>

### <p align="center">A command-line tool for extracting and converting game language files stored in binary `.dat` format.</p>

## About
LangTool X is designed for modders, translators, and enthusiasts working with language files from several racing games. These games store in-game text in binary `.dat` files, which are not human-readable and cannot be edited directly.

LangTool X allows you to:
- Extract text strings from `.dat` files into a plain `.txt` format.
- Convert edited `.txt` files back into `.dat` using the original `.dat` as a base.
- Process string IDs using a `.bed` file (required for all operations).
- Validate language file structure during processing.
- Extract with original text reference from another .dat file using `--original-d` option.

## Quick example

### Extract

#### Python script:
```sh
python langtool_x.py --extract -d language0.dat -b languages.bed -t language0.txt
```
#### Windows executable:
```sh
langtool_x.exe --extract -d language0.dat -b languages.bed -t language0.txt
```
### Convert

#### Python script:
```sh
python langtool_x.py --convert -d language0.dat -b languages.bed -t language0.txt -o new_language0.dat
```
#### Windows executable:
```sh
langtool_x.exe --convert -d language0.dat -b languages.bed -t language0.txt -o new_language0.dat
```

## Supported Games

LangTool X supports language files from these games:

- FlatOut
- FlatOut 2
- FlatOut: Ultimate Carnage
- FlatOut: Head On
- Sega Rally Revo (PSP)

## Tested Platforms
- Tested on Windows 10, Ubuntu 24.04, and Debian 12
- macOS support is untested

## Features

- Cross-platform CLI tool
- No third-party Python dependencies.
- Long and short command-line options
- Validation and diagnostics

## Usage

> ⚠️ All arguments (`--dat`, `--bed`, `--txt` / `-d`, `-b`, `-t`) are required.

### Python script

> ⚠️ On Windows, you can use either `python` or `py` to run the script, depending on your Python installation.

> ⚠️ On Linux/macOS you may need to use `python3` instead of `python`.

#### Extract strings from `.dat` to `.txt`:

```sh
python langtool_x.py --extract --dat language0.dat --bed languages.bed --txt language0.txt
```
Or using short options:
```sh
python langtool_x.py --extract -d language0.dat -b languages.bed -t language0.txt
```

#### Extract with original text reference (`--original-d` / `-od`):
```sh
python langtool_x.py --extract --dat language5.dat --bed languages.bed --txt language5.txt --original-d language0.dat
```
Or using short options:
```sh
python langtool_x.py --extract -d language5.dat -b languages.bed -t language5.txt -od language0.dat
```

#### Convert edited `.txt` back to `.dat`:
```sh
python langtool_x.py --convert --dat language0.dat --bed languages.bed --txt language0.txt --out new_language0.dat
```
Or using short options:
```sh
python langtool_x.py --convert -d language0.dat -b languages.bed -t language0.txt -o new_language0.dat
```

### Windows executable

> ⚠️ If you downloaded the pre-built executable `langtool_x.exe`.

#### Extract strings from `.dat` to `.txt`:
```sh
langtool_x.exe --extract --dat language0.dat --bed languages.bed --txt language0.txt
```
Or using short options:
```sh
langtool_x.exe --extract -d language0.dat -b languages.bed -t language0.txt
```

#### Extract with original text reference (`--original-d` / `-od`):
```sh
langtool_x.exe --extract --dat language5.dat --bed languages.bed --txt language5.txt --original-d language0.dat
```
Or using short options:
```sh
langtool_x.exe --extract -d language5.dat -b languages.bed -t language5.txt -od language0.dat
```

#### Convert edited `.txt` back to `.dat`:
```sh
langtool_x.exe --convert --dat language0.dat --bed languages.bed --txt language0.txt --out new_language0.dat
```
Or using short options:
```sh
langtool_x.exe --convert -d language0.dat -b languages.bed -t language0.txt -o new_language0.dat
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

## Special Tags

LangTool X uses several special tags in the `.txt` output format. These tags must be preserved when editing translation files.

- `{LF}` — Line break.  
  Used to represent a newline inside a string stored in the `.dat` file.
- `{EMPTY}` — Empty string.  
  Indicates that the string block in the `.dat` file contains no text.
- `{INVALID}` — Invalid or placeholder string.  
  Used internally when a string block cannot be interpreted correctly.
- `// ... //` — Original text reference.  
  When using the `--original-d` option, the original string from another `.dat` file is written between `//` markers.  
  This text is **ignored** when converting `.txt` back to `.dat` and is provided only as a reference for translators.

## Translation Rules

When editing extracted `.txt` files, follow these rules to avoid breaking the structure of the `.dat` file.

**1. Do not modify block headers**

Lines like:

```
[String ID: 31] [PS2_DNAS2_SS_SERVER_BUSY]
```

must remain unchanged. They are used to map strings back to the correct positions in the `.dat` file.

**2. Do not remove `{LF}` tags**

`{LF}` represents a line break inside the original string. Removing or changing it may break text formatting in the game.

**3. Do not remove empty blocks**

If a block contains `{EMPTY}`, keep it unless you intentionally want to add text.

**4. Original text (`//...//`) is ignored**

Lines between `// ... //` are reference text when using `--original-d`.
They are **not included** when converting the file back to `.dat`.

**5. Do not change the order of blocks**

Strings must remain in the same order as in the extracted file.

**6. Encoding**

The `.txt` file must remain **UTF-8 encoded**.

Following these rules ensures that the file can be converted back to `.dat` without errors.

## Building

**Requirements:** Python 3.6 or newer

### Windows

You can build a standalone `.exe` using [PyInstaller](https://pyinstaller.org/):

```cmd
pip install pyinstaller
pyinstaller --onefile langtool_x.py
```

The compiled executable will be located in `dist\langtool_x.exe`

**Optional flags:**
- `--icon=icon.ico` - add custom icon
- `--name=LangToolX` - custom executable name

> ⚠️ **Note:** Some antivirus software may flag PyInstaller executables as false positives.

### Linux / macOS

Build executable:

```bash
pip3 install pyinstaller
pyinstaller --onefile langtool_x.py
chmod +x ./dist/langtool_x  # if needed
```

The compiled binary will be located in `./dist/langtool_x`

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

## Credits

- Developed by AS97.
- **Inspired by the original "FO2 LangTool" developed by Burs.**
- **Developed using the [Cursor](https://www.cursor.so/) editor with assistance from AI tools such as ChatGPT and Claude.**

*Feel free to contribute or report issues via GitHub!*
