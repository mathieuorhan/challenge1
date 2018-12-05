"""Parsing code for DICOMS and contour files"""

import pydicom as dicom
from pydicom.errors import InvalidDicomError

import numpy as np
from PIL import Image, ImageDraw


def parse_contour_file(filename):
    """Parse the given contour filename

    :param filename: filepath to the contourfile to parse
    :return: list of tuples holding x, y coordinates of the contour
    """

    coords_lst = []

    with open(filename, 'r') as infile:
        for line in infile:
            coords = line.strip().split()

            x_coord = float(coords[0])
            y_coord = float(coords[1])
            coords_lst.append((x_coord, y_coord))

    return coords_lst


def parse_dicom_file(filename):
    """Parse the given DICOM filename

    :param filename: filepath to the DICOM file to parse
    :return: dictionary with DICOM image data
    """

    try:
        dcm = dicom.read_file(filename)
        dcm_image = dcm.pixel_array

        try:
            intercept = dcm.RescaleIntercept
        except AttributeError:
            intercept = 0.0
        try:
            slope = dcm.RescaleSlope
        except AttributeError:
            slope = 0.0

        if intercept != 0.0 and slope != 0.0:
            dcm_image = dcm_image*slope + intercept
        dcm_dict = {'pixel_data' : dcm_image}
        return dcm_dict
    except InvalidDicomError:
        return None


def poly_to_mask(polygon, width, height):
    """Convert polygon to mask

    :param polygon: list of pairs of x, y coords [(x1, y1), (x2, y2), ...]
     in units of pixels
    :param width: scalar image width
    :param height: scalar image height
    :return: Boolean mask of shape (height, width)
    """

    # http://stackoverflow.com/a/3732128/1410871
    img = Image.new(mode='L', size=(width, height), color=0)
    ImageDraw.Draw(img).polygon(xy=polygon, outline=0, fill=1)
    mask = np.array(img).astype(bool)
    return mask


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    contour = parse_contour_file("final_data/contourfiles/SC-HF-I-1/i-contours/IM-0001-0048-icontour-manual.txt")
    dicom = parse_dicom_file("final_data/dicoms/SCD0000101/48.dcm")
    img = dicom['pixel_data']

    width, height = img.shape

    mask = poly_to_mask(contour, width, height)
    plt.imshow(img, cmap='gray', interpolation=None)
    plt.imshow(mask, cmap='gray', interpolation=None, alpha = 0.3)
    plt.show()
    