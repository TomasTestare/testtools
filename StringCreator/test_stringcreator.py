"""Unit tests for StringCreator core logic."""
import base64
import urllib.parse

import pytest

import StringCreator as sc


def test_luhn_known_value():
    # 811218-987 has check digit 6
    assert sc.calculate_luhn_check_digit("811218987") == 6


def test_generated_valid_personnummer_passes_validation():
    for _ in range(200):
        pnr = sc.generate_swedish_personnummer(valid=True)
        assert sc.validate_personnummer(pnr), f"{pnr} should be valid"


def test_generated_invalid_personnummer_fails_validation():
    for _ in range(200):
        pnr = sc.generate_swedish_personnummer(valid=False)
        assert not sc.validate_personnummer(pnr), f"{pnr} should be invalid"


def test_validate_personnummer_accepts_formats():
    pnr = sc.generate_swedish_personnummer(valid=True)  # YYYYMMDD-XXXX
    digits = "".join(c for c in pnr if c.isdigit())
    assert sc.validate_personnummer(pnr)
    assert sc.validate_personnummer(digits)          # 12 digits, no dash
    assert sc.validate_personnummer(digits[2:])      # 10 digits (YYMMDD...)


def test_validate_personnummer_rejects_garbage():
    assert not sc.validate_personnummer("not-a-number")
    assert not sc.validate_personnummer("123")


def test_alphanumeric_length_and_charset():
    s = sc.generate_string(32, charset_type=1)
    assert len(s) == 32
    assert all(c.islower() or c.isdigit() for c in s)


def test_all_payloads_returns_multiple_lines():
    out = sc.generate_string(0, charset_type=3, use_all_payloads=True)
    assert "\n" in out
    assert out.count("\n") + 1 == 15  # 15 SQL payloads


@pytest.mark.parametrize("enc,expected", [
    ("base64", lambda t: base64.b64encode(t.encode()).decode()),
    ("url", lambda t: urllib.parse.quote(t)),
    ("hex", lambda t: t.encode().hex()),
])
def test_encodings(enc, expected):
    text = "Hello World!"
    assert sc.encode_string(text, enc) == expected(text)


def test_encode_html_entities():
    assert sc.encode_string("<>", "html") == "&#60;&#62;"


def test_password_strength_scoring():
    strength, score, feedback = sc.check_password_strength("aA1!aaaaaaaa")
    assert score >= 5
    assert strength in ("Strong", "Very Strong")


def test_uuid_generation_is_valid():
    import uuid as _uuid
    s = sc.generate_string(0, charset_type=18)
    parsed = _uuid.UUID(s)
    assert parsed.version == 4


def test_generated_credit_cards_pass_luhn():
    for _ in range(100):
        cc = sc.generate_string(0, charset_type=19)
        assert cc.isdigit()
        assert len(cc) in (15, 16)
        assert sc.luhn_is_valid(cc), f"{cc} should pass Luhn"


def test_luhn_is_valid_known_values():
    assert sc.luhn_is_valid("79927398713")      # classic valid Luhn example
    assert not sc.luhn_is_valid("79927398710")


def test_generate_credit_card_respects_brand():
    amex = sc.generate_credit_card("amex")
    assert amex.startswith("34") and len(amex) == 15
    visa = sc.generate_credit_card("visa")
    assert visa.startswith("4") and len(visa) == 16


def test_luhn_is_valid_rejects_empty():
    assert not sc.luhn_is_valid("")
    assert not sc.luhn_is_valid("abc")
