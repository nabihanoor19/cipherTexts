"""Print Rail Fence decryptions for every required depth."""

from pathlib import Path

DEFAULT_INPUT = Path(__file__).parent / "assets" / "rail_ciphertext.txt"
MIN_DEPTH = 2
MAX_DEPTH = 8


def decrypt(ciphertext: str, depth: int) -> str:
    """Decrypt a standard down-and-up Rail Fence ciphertext."""
    if depth < 2:
        raise ValueError("Rail Fence depth must be at least 2")

    cycle_length = 2 * depth - 2
    row_for_position = [
        position % cycle_length
        if position % cycle_length < depth
        else cycle_length - position % cycle_length
        for position in range(len(ciphertext))
    ]

    row_counts = [row_for_position.count(row) for row in range(depth)]
    rails = []
    start = 0
    for count in row_counts:
        rails.append(list(ciphertext[start : start + count]))
        start += count

    plaintext = []
    for row in row_for_position:
        plaintext.append(rails[row].pop(0))
    return "".join(plaintext)


def main() -> None:
    ciphertext = DEFAULT_INPUT.read_text(encoding="utf-8")
    for depth in range(MIN_DEPTH, MAX_DEPTH + 1):
        print(f"\n--- Rail Fence depth {depth} ---")
        print(decrypt(ciphertext, depth))


if __name__ == "__main__":
    main()
