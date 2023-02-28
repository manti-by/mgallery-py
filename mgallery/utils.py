from setuptools import glob

from mgallery.settings import GALLERY_PATH


def binary_array_to_hex(binary_array: list, hash_size: int = 8) -> str:
    """Create a hex string from a binary array."""
    bit_string = "".join(str(x) for x in 1 * binary_array)
    return f"{int(bit_string, 2):{hash_size}x}"


def get_gallery_file_list(recursive: bool = True) -> list:
    """Return files in the gallery recursively."""
    files = []
    for ext in ("**/*.jpg", "**/*.jpeg", "**/*.png", "**/*.gif"):
        files.extend(glob.glob(f"{GALLERY_PATH}/{ext}", recursive=recursive))
    return files
