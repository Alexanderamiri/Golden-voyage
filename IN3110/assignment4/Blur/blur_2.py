import cv2
import time
from numpy import array, pad


def numpyblur(image):  # Numpy implementation
    """A blur function to blur a specifically one part of an image with Numpy

    Args:
        image (uint32): padded source image
    Returns:
        A Blurred image of the source image
    """
    image = pad(image, 1, mode="edge")[:, :, 1:-1].astype("uint32")
    image = array(image)  # duplicates the incoming image as numpy array
    r = (
        image[1:-1, 1:-1, :]
        + image[:-2, 1:-1, :]
        + image[2:, 1:-1, :]
        + image[1:-1, :-2, :]
        + image[1:-1, 2:, :]
        + image[:-2, :-2, :]
        + image[:-2, 2:, :]
        + image[2:, :-2, :]
        + image[2:, 2:, :]
    ) / 9  # Blurs r by applying
    # formula to height and width axis
    return r.astype(
        "uint8"
    )  # returns blur with average of  the 9 pixels in a 3x3


if __name__ == "__main__":
    start = time.perf_counter()
    src = cv2.imread("beatles.jpg")
    dst = numpyblur(src)
    cv2.imwrite("testblur2.jpg", dst)
    finish = time.perf_counter()
    print(f"Finished in {round(finish - start, 2)} second(s)")
