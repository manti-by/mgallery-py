import numpy
import scipy

from PIL import Image
from memory_profiler import profile

from mgallery.utils import binary_array_to_hex


@profile
def get_image_data(
    image_path: str, image_size: int = 32, hash_size: int = 8
) -> tuple[int, int, str]:
    """
    Perceptual Hash computation.

    Implementation follows https://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html
    """
    image = Image.open(image_path)
    image = image.convert("L").resize((image_size, image_size), Image.ANTIALIAS)
    pixels = numpy.asarray(image)

    dct = scipy.fft.dctn(pixels, axes=[0, 1])
    dct_low_frequency = dct[:hash_size, :hash_size]
    dct_median = numpy.median(dct_low_frequency)

    binary_array = dct_low_frequency > dct_median
    image_hash = binary_array_to_hex(binary_array.flatten(), hash_size)
    return image.width, image.height, image_hash
