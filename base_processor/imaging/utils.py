import PIL
import numpy as np

import deepzoom


def convert_image_data_type(data_matrix, dtype=np.uint8):
    """Converts an numpy image matrix from one data type to another"""

    # Error handling
    if type(data_matrix) != np.ndarray:
        raise TypeError("Data matrix input for conversion of data types is not a numpy array.")
    if dtype not in [np.complex128, np.complex64,
                     np.float32, np.float64,
                     np.int16, np.int32, np.int64, np.int8,
                     np.uint16, np.uint32, np.uint64, np.uint8]:
        raise TypeError("Conversion to data type {dtype} is not currently supported".format(dtype=dtype))

    # TODO: Need to flush out each specific data type and their complexities
    if dtype == np.uint8:
        data_matrix = (data_matrix / (1.0 * np.max(data_matrix[:])) * 255.0).astype(np.uint8)
        return data_matrix
    else:
        return dtype(data_matrix)


def singleslice(arr, inds, axis):
    """ Slices an image array "arr" along specific axis/dimension "axis" at indices "inds" """
    # this does the same as np.take() except only supports simple slicing, not
    # advanced indexing, and thus is much faster
    sl = [slice(None)] * arr.ndim
    sl[axis] = inds
    return arr[sl]


def multislice(arr, axis_indx):
    """Slices an image array "arr" along many different axes and indices for each axis defined
    as tuples of (axis, index) in list axis_indx"""

    sl = [slice(None)] * arr.ndim
    for axis, index in axis_indx:
        if type(index) == list or type(index) == tuple:
            sl[axis] = index
        else:
            sl[axis] = [index]
    return arr[sl]


def encode_dzi(image, filename, tile_size=128, tile_overlap=0, tile_format="png", image_quality=1.0,
               resize_filter="bicubic"):
    """Encodes a 2-D image as a deepzoom image to filename"""

    assert isinstance(image, PIL.Image.Image)

    creator = deepzoom.ImageCreator(tile_size=tile_size, tile_overlap=tile_overlap, tile_format=tile_format,
                                    image_quality=image_quality, resize_filter=resize_filter)
    creator.create(image, filename)


def multiradix(M, n, a, i):
    if i < 0:
        yield a
    else:
        for __ in multiradix(M, n, a, i - 1):
            # Extend each multi-radix number of length i with all possible
            # 0 <= x < M[i] to get a multi-radix number of length i + 1.
            for x in range(M[i]):
                a[i] = x
                yield a


def multiradix_recursive(M):
    n = len(M)
    a = [0] * n
    return multiradix(M, n, a, n - 1)


def save_asset(image, exploded_format, filename, optimize=False, tile_size=128, tile_overlap=0, tile_format="png",
               image_quality=1.0, resize_filter="bicubic"):
    """Explode 2-Dimensional PIL Image image into format exploded_format as filename in output directory."""

    assert isinstance(image, PIL.Image.Image)
    assert len(image.size) == 2

    # TODO: Change tile size, overlap, format, interpolation method according to image resolution and size
    if exploded_format == 'dzi':
        # Encode 2D image as deepzoom image
        encode_dzi(
            image,
            filename,
            tile_size=tile_size,
            tile_overlap=tile_overlap,
            tile_format=tile_format,
            image_quality=image_quality,
            resize_filter=resize_filter
        )
    elif exploded_format != 'dzi':  # e.g. png or jpg
        image.save(
            filename,
            format="{fmt}".format(fmt=exploded_format),
            optimize=optimize
        )


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise TypeError('Boolean value expected.')
