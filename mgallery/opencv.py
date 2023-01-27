import numpy
import cv2

from memory_profiler import profile

from mgallery.utils import binary_array_to_hex


@profile
def get_image_data(
    image_name: str, image_size: int = 32, hash_size: int = 8
) -> tuple[int, int, str]:
    """
    Perceptual Hash computation.

    Implementation follows https://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html
    """
    original_image = cv2.imread(image_name)
    image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    image = cv2.resize(image, (image_size, image_size))
    dct = cv2.dct(numpy.float32(numpy.asarray(image)))

    dct_low_frequency = dct[:hash_size, :hash_size]
    dct_median = numpy.median(dct_low_frequency)

    binary_array = dct_low_frequency > dct_median
    image_hash = binary_array_to_hex(binary_array.flatten(), hash_size)
    return original_image.shape[0], original_image.shape[1], image_hash
