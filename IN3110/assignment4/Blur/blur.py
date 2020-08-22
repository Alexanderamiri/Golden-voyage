from numpy import pad
import cv2
import argparse
from Blur.blur_1 import pythonblur
from Blur.blur_2 import numpyblur
from Blur.blur_3 import numbablur


def blur_image(input_filename, output_filename=None):
    """
    A blur function to blur a any image using numpyblur

    Args:
        input_filename (str) : Input filename name as <input_filename.jpg>
        output_filename (str) : output file name as <output_filename.jpg>
    Returns:
        if a a outputfile name is specified it returns creates a jpg with the output file name
        if not it returns the blurred image of the source

    """
    image = cv2.imread(input_filename, 1)
    image = pad(image, 1, mode="edge")[:, :, 1:-1]
    image = image.astype("uint32")
    dst = numpyblur(image)
    dst.astype("uint8")
    if output_filename != None:
        cv2.imwrite(str(output_filename), dst)
        return dst
    else:
        return dst  # returns the blurred image but doesnt make a .jpg


def blurs(dict):
    """
    A blur function to blur images using a choosen blurring implementation

    Args:
        dict (dict): Dictionary {'Implementation'=, 'Input'=, 'Output'=}
            Implementation: 'numba' / 'numpy' / 'python'
            Input : input filename <name.jpg>
            Output : output filename <name.jpg>
        --help for information about the function
    Returns:
        returns blurred image with choosen implementation

    """
    if dict["Implementation"] == "numba":
        src = cv2.imread(dict["Input"])
        im = pad(src, 1, mode="edge")[:, :, 1:-1]
        im = im.astype("uint32")
        blurd = numbablur(src, im)
        blurd = blurd.astype("uint8")
        cv2.imwrite(dict["Output"], blurd)

    if dict["Implementation"] == "numpy":
        src = cv2.imread(dict["Input"])
        blurd = numpyblur(src)
        blurd = blurd.astype("uint8")
        cv2.imwrite(dict["Output"], blurd)

    if dict["Implementation"] == "python":
        src = cv2.imread(dict["Input"])
        blurd = pythonblur(src)
        blurd = blurd.astype("uint8")
        cv2.imwrite(dict["Output"], blurd)


def funct():
    parser = argparse.ArgumentParser(
        description="Blurs an image"
        "To use write : python blur.py"
        " <numba/numpy/python> "
        "<image file to be blurred> <blurred image filename> \n"
        "The program will choose between three different "
        "implementation of the same algorithm",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )  # creates parser

    parser.add_argument(
        "Implementation", help="Choose python/numpy/numba"
    )  # adds implementation choice input
    parser.add_argument(
        "Input",
        help="Choose which jpg file to blur, has to be <imagename.jpg>",
    )  # adds inputfile name choice
    parser.add_argument(
        "Output",
        help="Choose the name of the blurred image output, has to be <imagename.jpg>",
    )  # adds output name choice
    inputs = parser.parse_args()
    arguments = vars(inputs)  # creates a dictiornary
    blurs(arguments)


funct()
