# StringCreator - Advanced String Generator & Security Testing Tool

A powerful Python tool for generating random strings and security testing payloads with extensive customization options. Perfect for developers, security researchers, and QA testers.

## 🚀 Features

### String Generation
- **Alphanumeric strings** (a-z, 0-9)
- **ASCII characters** (all printable)
- **Unicode/Emoji** characters
- **Control characters** (\n, \r, \t, \0)
- **Mixed dangerous characters** for comprehensive testing
- **Custom character sets**

### Security Testing Payloads
- **SQL Injection** - 15+ payloads for database security testing
- **XSS (Cross-Site Scripting)** - 12+ HTML/JavaScript injection payloads
- **Path Traversal** - 10+ directory traversal attacks
- **Command Injection** - 13+ OS command execution payloads
- **LDAP Injection** - 8+ LDAP query manipulation payloads
- **XML/XXE Injection** - External entity injection attacks
- **SSRF (Server-Side Request Forgery)** - URL-based attacks
- **NoSQL Injection** - MongoDB and other NoSQL database attacks
- **CRLF Injection** - HTTP header injection payloads
- **JWT Manipulation** - JSON Web Token tampering payloads

### Test Data Generation
- **Swedish Personnummer (Valid)** - Generate valid Swedish social security numbers with correct Luhn check digit
- **Swedish Personnummer (Invalid)** - Generate invalid Swedish social security numbers with incorrect Luhn check digit
- **UUID v4** - Generate random universally unique identifiers
- **Credit card numbers** - Generate Luhn-valid fake card numbers (Visa/MC/Amex/Discover) for testing

### Advanced Features
- ✅ **Command-line interface** for automation
- ✅ **Interactive mode** for guided usage
- ✅ **Batch generation** - Generate multiple strings at once
- ✅ **Unique batch mode** - Guarantee no duplicates within a batch (`--unique`)
- ✅ **Validation mode** - Check personnummer, Luhn, credit card, or password strength (`--validate`)
- ✅ **Encoding support** - Base64, URL, Hex, HTML entities
- ✅ **File export** - Save as text, JSON, or CSV
- ✅ **History tracking** - Keep last 50 generations
- ✅ **Password strength checker** - Validate password quality
- ✅ **Quiet mode** - Print only the value for clean scripting (`--quiet`)
- ✅ **Clipboard integration** - Automatic copy to clipboard
- ✅ **Continuous loop mode** - Generate multiple strings without restarting

## 📋 Requirements

- Python 3.7 or higher
- Required packages:
  - `pyperclip` - Clipboard operations

## 🔧 Installation

### Option 1: Using Virtual Environment (Recommended)

1. **Navigate to the project directory**
   ```bash
   cd StringCreator
   ```

2. **Create a virtual environment**

   **Windows (PowerShell):**
   ```powershell
   python -m venv venv
   ```

   **Linux/Mac:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**

   **Windows (PowerShell):**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   **Windows (Command Prompt):**
   ```cmd
   venv\Scripts\activate.bat
   ```

   **Linux/Mac:**
   ```bash
   source venv/bin/activate
   ```

   > **Note**: If you get an execution policy error on Windows PowerShell, run:
   > ```powershell
   > Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   > ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Or manually install:
   ```bash
   pip install pyperclip
   ```

5. **Run the tool**
   ```bash
   python StringCreator.py
   ```

6. **Deactivate virtual environment when done**
   ```bash
   deactivate
   ```

### Option 2: Global Installation (Not Recommended)

If you prefer not to use a virtual environment:

1. **Navigate to the project directory**
   ```bash
   cd StringCreator
   ```

2. **Install dependencies globally**
   ```bash
   pip install pyperclip
   ```

3. **Run the tool**
   ```bash
   python StringCreator.py
   ```

## 🖥️ Graphical Interface (GUI)

A local desktop GUI (built with [NiceGUI](https://nicegui.io/)) is available as an
alternative to the command line. It reuses the same core, so every generator, the
validation tools, and history are available with a point-and-click interface. The GUI
ships with a custom **cyber/hacker dark theme** — neon green/cyan accents, a glowing
logo, glass-effect panels, and an animated grid background (assets live in `assets/`).

1. **Install the GUI dependencies** (in addition to the base requirements):
   ```bash
   pip install -r requirements-gui.txt
   ```

2. **Run the GUI**
   ```bash
   python gui.py
   ```
   By default this opens a **native desktop window** (via `pywebview`). To open it in a
   **browser tab** instead (no `pywebview` needed), set an environment variable:

   **Windows (PowerShell):**
   ```powershell
   $env:STRINGCREATOR_GUI_NATIVE = "0"; python gui.py
   ```

   **Linux/Mac:**
   ```bash
   STRINGCREATOR_GUI_NATIVE=0 python gui.py
   ```
   Then open <http://localhost:8080>.

The GUI has three tabs:
- **Generate** – pick a type, set length/batch/encoding/uniqueness, generate, copy, and
  export to text/JSON/CSV.
- **Validate** – check a personnummer, Luhn checksum, credit-card number, or password
  strength.
- **History** – view the most recent generations.

> **Note**: Like the CLI, the GUI is intended to run **locally for a single user** — it
> generates real attack payloads and should not be hosted or exposed on a network.

## 💻 Usage

### Interactive Mode (Default)

Simply run the script without arguments for a guided experience:

```bash
python StringCreator.py
```

You'll be prompted to:
1. Select character set type (1-15)
2. Choose payload option (for attack payloads)
3. Enter desired string length
4. Select encoding (optional)
5. Choose batch count (optional)
6. Save to file (optional)

### Command-Line Interface (CLI)

For automation and quick generation:

#### Basic String Generation
```bash
# Generate 32-byte alphanumeric string
python StringCreator.py -t 1 -l 32

# Generate 16-byte ASCII string
python StringCreator.py -t 2 -l 16

# Generate 50-byte mixed dangerous characters
python StringCreator.py -t 9 -l 50
```

#### Security Payload Generation
```bash
# Random SQL injection payload
python StringCreator.py -t 3

# All SQL injection payloads
python StringCreator.py -t 3 --all

# Random XSS payload
python StringCreator.py -t 4

# All command injection payloads
python StringCreator.py -t 8 --all
```

#### Encoding Options
```bash
# Base64 encoded string
python StringCreator.py -t 1 -l 16 -e base64

# URL encoded string
python StringCreator.py -t 2 -l 20 -e url

# Hex encoded string
python StringCreator.py -t 1 -l 24 -e hex

# HTML entity encoded string
python StringCreator.py -t 2 -l 15 -e html
```

#### Batch Generation
```bash
# Generate 5 random strings
python StringCreator.py -t 1 -l 10 -b 5

# Generate 10 passwords
python StringCreator.py -t 2 -l 16 -b 10
```

#### File Export
```bash
# Save as plain text
python StringCreator.py -t 1 -l 32 -o output.txt

# Save as JSON
python StringCreator.py -t 3 --all -o payloads.json -f json

# Save as CSV (great for batch)
python StringCreator.py -t 1 -l 20 -b 100 -o passwords.csv -f csv
```

#### Custom Character Sets
```bash
# Use custom characters
python StringCreator.py --custom "ABC123!@#" -l 20
```

#### History Management
```bash
# View generation history
python StringCreator.py --history
```

#### Disable Clipboard
```bash
# Don't copy to clipboard
python StringCreator.py -t 1 -l 32 --no-clipboard
```

## 📝 Character Set Types

| Type | Description | Use Case |
|------|-------------|----------|
| 1 | Alphanumeric only (a-z, 0-9) | Passwords, usernames, IDs |
| 2 | All ASCII characters | General testing, complex passwords |
| 3 | SQL Injection payloads | Database security testing |
| 4 | HTML/XSS payloads | Web application security testing |
| 5 | Path traversal payloads | File system security testing |
| 6 | Control characters | Input validation testing |
| 7 | Unicode/Emoji characters | Internationalization testing |
| 8 | Command injection payloads | OS command security testing |
| 9 | Mixed dangerous characters | Comprehensive input testing |
| 10 | LDAP injection payloads | Directory service security testing |
| 11 | XML/XXE injection payloads | XML parser security testing |
| 12 | SSRF payloads | Network security testing |
| 13 | NoSQL injection payloads | NoSQL database security testing |
| 14 | CRLF injection payloads | HTTP header security testing |
| 15 | JWT manipulation payloads | Token security testing |
| 16 | Swedish Personnummer (valid) | Valid Swedish SSN with correct Luhn check digit |
| 17 | Swedish Personnummer (invalid) | Invalid Swedish SSN with incorrect Luhn check digit |
| 18 | UUID v4 | Random universally unique identifiers |
| 19 | Credit card number | Luhn-valid fake card numbers (Visa/MC/Amex/Discover) for testing |

## 📊 Examples

### Example 1: Generate Strong Password
```bash
python StringCreator.py -t 2 -l 24
```
Output: `aK9#mL@2pQ$7rX!4tY&8zW`

### Example 2: Generate Test Data
```bash
# Generate 100 test usernames
python StringCreator.py -t 1 -l 8 -b 100 -o usernames.txt
```

### Example 3: Security Testing
```bash
# Export all SQL injection payloads for testing
python StringCreator.py -t 3 --all -o sql_payloads.txt

# Generate URL-encoded XSS payloads
python StringCreator.py -t 4 -e url -o xss_encoded.txt
```

### Example 4: Password Strength Analysis
```bash
# Generate and check password strength (interactive mode)
python StringCreator.py
# Select option 1 or 2, enter length
# Tool will show strength rating and suggestions
```

### Example 5: Batch Export with Metadata
```bash
# Generate 50 strings with metadata in CSV
python StringCreator.py -t 2 -l 16 -b 50 -o passwords.csv -f csv
```

### Example 6: Swedish Personnummer Generation
```bash
# Generate valid Swedish personnummer
python StringCreator.py -t 16

# Generate 20 invalid Swedish personnummer for testing
python StringCreator.py -t 17 -b 20 -o invalid_ssn.txt

# Generate valid personnummer and save as CSV
python StringCreator.py -t 16 -b 100 -o personnummer.csv -f csv
```

**Example Output:**
- Valid: `19640306-3362` (correct Luhn check digit)
- Invalid: `19640306-3363` (incorrect Luhn check digit)

## 🔒 Security Notice

**⚠️ WARNING**: This tool generates real attack payloads for security testing purposes.

- **Only use on systems you own or have permission to test**
- **Never use against production systems without authorization**
- **Ensure proper ethical hacking guidelines are followed**
- **The authors are not responsible for misuse of this tool**

This tool is intended for:
- Security researchers conducting authorized penetration testing
- Developers testing application security
- QA teams validating input handling
- Educational purposes in controlled environments

## 📁 File Structure

```
StringCreator/
│
├── StringCreator.py       # Main script (CLI + interactive mode)
├── gui.py                 # NiceGUI desktop GUI (optional)
├── assets/                # GUI theme assets (logo.svg, favicon.svg)
├── requirements.txt       # Runtime dependency (pyperclip)
├── requirements-gui.txt   # Optional GUI dependencies (nicegui, pywebview)
├── test_stringcreator.py  # Core unit tests
├── test_gui.py            # GUI smoke tests
├── persnumber/           # Test personnummer CSV data
├── README.md             # This file
├── venv/                 # Virtual environment (created by you)
└── string_history.json   # Auto-generated history file
```

> **Note**: The `venv/` directory is created when you set up a virtual environment and should be added to `.gitignore` if using version control.

## 🛠️ Command-Line Arguments

```
usage: StringCreator.py [-h] [-t {1-19}] [-l LENGTH] [--all]
                        [-e {base64,url,hex,html}] [-b BATCH] [--unique]
                        [-o OUTPUT] [-f {text,json,csv}]
                        [--no-clipboard] [--quiet]
                        [--validate TYPE VALUE]
                        [--history] [--custom CUSTOM]
                        [--seed SEED] [--version]

Advanced String Generator & Security Testing Tool

optional arguments:
  -h, --help            show this help message and exit
  -t TYPE, --type TYPE  Character set type (1-19)
  -l LENGTH, --length LENGTH
                        String length in bytes
  --all                 Generate all payloads (for payload types)
  -e ENCODE, --encode ENCODE
                        Encoding format (base64, url, hex, html)
  -b BATCH, --batch BATCH
                        Number of strings to generate
  --unique              Ensure generated values in a batch are unique
  -o OUTPUT, --output OUTPUT
                        Output file path
  -f FORMAT, --format FORMAT
                        Output file format (text, json, csv)
  --no-clipboard        Do not copy to clipboard
  --quiet               Print only the generated value (no extra messages)
  --validate TYPE VALUE
                        Validate VALUE of TYPE
                        (personnummer|luhn|creditcard|password)
  --history             View generation history
  --custom CUSTOM       Custom character set
  --seed SEED           Seed the RNG for reproducible test data (not secure)
  --version             Show program version and exit
```

> **Note**: Random alphanumeric/ASCII/custom strings are generated with Python's
> `secrets` module (cryptographically secure) and are **not** affected by `--seed`.
> `--seed` only makes payload and personnummer selection reproducible.

### Validation mode

Check existing values instead of generating them:

```bash
python StringCreator.py --validate personnummer 19640306-3362
python StringCreator.py --validate creditcard 4586379705104281
python StringCreator.py --validate luhn 79927398713
python StringCreator.py --validate password "MyP@ssw0rd!"
```

> **Note**: Random alphanumeric/ASCII/custom strings are generated with Python's
> `secrets` module (cryptographically secure) and are **not** affected by `--seed`.
> `--seed` only makes payload and personnummer selection reproducible.

## 🧪 Running Tests

```bash
pip install pytest
pytest
```

The GUI smoke tests in `test_gui.py` are skipped automatically if `nicegui` is not
installed, so the core suite runs with just `pytest` + `pyperclip`.

## 🔥 Advanced Use Cases

### 1. Automated Test Data Generation
```bash
# Generate test data for CI/CD pipeline
for i in {1..10}; do
  python StringCreator.py -t 1 -l 16 --no-clipboard >> testdata.txt
done
```

### 2. Security Audit Script
```bash
# Export all payload types for security audit
python StringCreator.py -t 3 --all -o sql_payloads.txt
python StringCreator.py -t 4 --all -o xss_payloads.txt
python StringCreator.py -t 8 --all -o cmd_payloads.txt
```

### 3. Password Policy Testing
```bash
# Generate various password lengths to test policy
python StringCreator.py -t 2 -l 8 -b 10 -o short_passwords.txt
python StringCreator.py -t 2 -l 16 -b 10 -o medium_passwords.txt
python StringCreator.py -t 2 -l 32 -b 10 -o long_passwords.txt
```

### 4. Integration with Other Tools
```bash
# Pipe output to other security tools
python StringCreator.py -t 3 --all --no-clipboard | your-security-scanner
```

## 📚 History Feature

The tool automatically tracks your last 50 generations in `string_history.json`:

```bash
# View history in interactive mode
python StringCreator.py
# Choose option 0

# Or via CLI
python StringCreator.py --history
```

History includes:
- Timestamp
- Character set type
- String length
- Generated content (first 100 chars)
- Byte size

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new payload types
- Improve documentation
- Add new features

## 📄 License

This tool is provided for educational and authorized security testing purposes only.

## 👨‍💻 Author

Created by Tomas Lindqvist for security testing and development purposes.

## 🔗 Quick Reference

| Command | Description |
|---------|-------------|
| `python StringCreator.py` | Interactive mode |
| `python StringCreator.py -t 1 -l 32` | Generate alphanumeric string |
| `python StringCreator.py -t 3 --all` | All SQL injection payloads |
| `python StringCreator.py --history` | View history |
| `python StringCreator.py -t 1 -l 16 -b 10 -o file.txt` | Batch to file |

---

**Happy Testing! 🚀🔒**

For more information or support, please refer to the script's help:
```bash
python StringCreator.py --help
```
