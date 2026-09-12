"""Frequency analysis and partial-map solver for the monoalphabetic transmission."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

DEFAULT_INPUT = Path(__file__).parent / "assets" / "mono_ciphertext.txt"

COMPLETED_MAP = {
    "A": "E",
    "B": "H",
    "C": "Z",
    "D": "C",
    "E": "D",
    "F": "W",
    "G": "G",
    "H": "B",
    "I": "V",
    "J": "I",
    "K": "S",
    "L": "N",
    "M": "O",
    "N": "F",
    "O": "M",
    "P": "Y",
    "Q": "T",
    "R": "X",
    "S": "Q",
    "T": "L",
    "U": "R",
    "V": "U",
    "W": "P",
    "X": "K",
    "Z": "A",
}


def crib_mapping(ciphertext: str, plaintext: str) -> dict[str, str]:
    """Build a cipher-to-plain mapping from a confirmed word pair."""
    if len(ciphertext) != len(plaintext):
        raise ValueError("Crib words must have equal lengths")

    mapping: dict[str, str] = {}
    reverse: dict[str, str] = {}
    for cipher_letter, plain_letter in zip(ciphertext.upper(), plaintext.upper()):
        previous_plain = mapping.get(cipher_letter)
        previous_cipher = reverse.get(plain_letter)
        if previous_plain not in (None, plain_letter):
            raise ValueError("The crib gives conflicting substitutions")
        if previous_cipher not in (None, cipher_letter):
            raise ValueError("The crib is not a valid substitution")
        mapping[cipher_letter] = plain_letter
        reverse[plain_letter] = cipher_letter
    return mapping


def parse_map(value: str) -> dict[str, str]:
    """Parse entries such as z=a,w=p into a cipher-to-plain map."""
    mapping: dict[str, str] = {}
    for entry in value.split(","):
        pair = entry.strip().upper()
        if not pair:
            continue
        if "=" not in pair or len(pair.split("=")) != 2:
            raise ValueError(f"Invalid map entry: {entry!r}; use CIPHER=PLAIN")
        cipher_letter, plain_letter = pair.split("=")
        if len(cipher_letter) != 1 or len(plain_letter) != 1:
            raise ValueError(f"Invalid map entry: {entry!r}; use single letters")
        mapping[cipher_letter] = plain_letter
    return mapping


def decrypt(text: str, mapping: dict[str, str]) -> str:
    """Replace mapped letters and show unknown letters as underscores."""
    result = []
    for character in text:
        replacement = mapping.get(character.upper())
        if replacement is None:
            result.append("_" if character.isalpha() else character)
        elif character.islower():
            result.append(replacement.lower())
        else:
            result.append(replacement)
    return "".join(result)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument(
        "--map",
        default="",
        help="Additional cipher-to-plain pairs, for example z=a,w=p",
    )
    arguments = parser.parse_args()
    ciphertext = arguments.input.read_text(encoding="utf-8")

    frequencies = Counter(letter for letter in ciphertext.upper() if letter.isalpha())
    print("Letter frequencies:")
    for letter, count in frequencies.most_common():
        print(f"{letter}: {count}")

    mapping = dict(COMPLETED_MAP)
    mapping.update(parse_map(arguments.map))

    print("\nCipher-to-plain map:")
    print(" ".join(f"{cipher}={plain}" for cipher, plain in sorted(mapping.items())))
    print("\nRecovered plaintext:")
    print(decrypt(ciphertext, mapping))


if __name__ == "__main__":
    main()
