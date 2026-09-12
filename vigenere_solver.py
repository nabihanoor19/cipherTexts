"""Derive and decrypt the personalized Vigenere transmission."""

from pathlib import Path

ROLL_DIGITS = "230967"
KEY_LENGTH = 10
DEFAULT_INPUT = Path(__file__).parent / "assets" / "vigenere_ciphertext.txt"


def derive_key(roll_digits: str) -> str:
    """Calculate K_i = (d_i + i) mod 26 using the repeated roll digits."""
    if not roll_digits.isdigit():
        raise ValueError("Roll number must contain digits only")
    if not roll_digits:
        raise ValueError("Roll number must not be empty")

    key_values = [
        (int(roll_digits[index % len(roll_digits)]) + index) % 26
        for index in range(KEY_LENGTH)
    ]
    return "".join(chr(ord("A") + value) for value in key_values)


def decrypt(ciphertext: str, key: str) -> str:
    """Decrypt letters while preserving nonletters and their key position."""
    result = []
    key_index = 0
    for character in ciphertext:
        if not ("A" <= character.upper() <= "Z"):
            result.append(character)
            continue

        cipher_value = ord(character.upper()) - ord("A")
        key_value = ord(key[key_index % len(key)]) - ord("A")
        plain_value = (cipher_value - key_value) % 26
        replacement = chr(ord("A") + plain_value)
        result.append(replacement.lower() if character.islower() else replacement)
        key_index += 1
    return "".join(result)


def main() -> None:
    ciphertext = DEFAULT_INPUT.read_text(encoding="utf-8")
    key = derive_key(ROLL_DIGITS)
    plaintext = decrypt(ciphertext, key)

    print(f"Derived key: {key}")
    print("\nRecovered plaintext:")
    print(plaintext)


if __name__ == "__main__":
    main()
