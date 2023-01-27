def binary_array_to_hex(binary_array: list, hash_size: int = 8):
    """Create a hex string from a binary array."""
    bit_string = "".join(str(x) for x in 1 * binary_array)
    return f"{int(bit_string, 2):{hash_size}x}"
