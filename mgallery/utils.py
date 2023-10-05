from setuptools import glob

from mgallery.settings import GALLERY_PATH, FILE_TYPES


def binary_array_to_hex(binary_array: list, hash_size: int = 8) -> str:
    """Create a hex string from a binary array."""
    bit_string = "".join(str(x) for x in 1 * binary_array)
    return f"{int(bit_string, 2):{hash_size}x}"


def get_gallery_file_list(recursive: bool = True) -> list:
    """Return files in the gallery recursively."""
    files = []
    for ext in (f"**/*.{ext}" for ext in FILE_TYPES):
        files.extend(glob.glob(f"{GALLERY_PATH}/{ext.upper()}", recursive=recursive))
        files.extend(glob.glob(f"{GALLERY_PATH}/{ext.lower()}", recursive=recursive))
    return files
