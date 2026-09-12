"""Reconstruct the ordered hexadecimal pad fragments and decrypt the final stream."""

CIPHERTEXT_HEX = (
    "d0173a7e2d1508737ed8ff0ebdd95434a3f69d8f7dc3947106293553a64004b3edebea1a97fd56132f63f76def517744a2ec9fd72c7fae2d411de8ec0d82a346b1c0c674eeb6c9f4430f8d0390d76d1c78bcde5baf71ee83b1603f8751c75c75960e740de302815ce3f2d5"
)

FRAGMENTS = {
    1: "9154793b7e4628342c99b15af89d7a14ea98ebea0eb7fd16675d5c3cc86067dc809b867f",
    2: "e39876754011d75fdc1d5a749bdaa8f90c39e7630051b7aa41c3e47bf294800fa8ff87b5",
    3: "0f50ba67a7e6592c498bec6d9642d6e2d5040dbe68a56a42a03a4d35db61e06dd0caa8",
}


def decode_hex(value: str, label: str) -> bytes:
    """Decode a hexadecimal value and report invalid input clearly."""
    try:
        return bytes.fromhex(value)
    except ValueError as error:
        raise ValueError(f"{label} is not valid hexadecimal") from error


def decrypt(ciphertext_hex: str, fragments: dict[int, str]) -> bytes:
    """XOR the final ciphertext with fragments in their labelled order."""
    pad_hex = "".join(fragments[position] for position in sorted(fragments))
    ciphertext = decode_hex(ciphertext_hex, "Ciphertext")
    pad = decode_hex(pad_hex, "Reconstructed pad")
    if len(ciphertext) != len(pad):
        raise ValueError(
            f"Ciphertext and pad lengths differ: {len(ciphertext)} != {len(pad)} bytes"
        )
    return bytes(cipher_byte ^ pad_byte for cipher_byte, pad_byte in zip(ciphertext, pad))


def main() -> None:
    plaintext = decrypt(CIPHERTEXT_HEX, FRAGMENTS)
    print("Fragment order: 1, 2, 3")
    print(f"Reconstructed pad length: {sum(len(value) for value in FRAGMENTS.values()) // 2} bytes")
    print("\nRecovered message:")
    print(plaintext.decode("utf-8"))


if __name__ == "__main__":
    main()
