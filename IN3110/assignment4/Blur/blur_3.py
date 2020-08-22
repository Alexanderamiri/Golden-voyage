from numba import jit
from numpy import pad
import cv2
import time


@jit
def numbablur(src, image):  # Numba implementation
    """A blur function to blur a specifically one part of an image with Numba

    Args:
        src (uint8): source image
        image (uint32): source image padded at the edges

    Returns:
        A Blurred image of the source image
    """
    dst = src
    for c in range(len(dst[0, 0, :])):  # For each color
        for h in range(1, len(dst) + 1):  # for each pixel in the height
            for w in range(1, len(dst[0]) + 1):  # for each pixel in the width
                dst[h - 1, w - 1, c] = (
                    image[h, w, c]
                    + image[h - 1, w, c]
                    + image[h + 1, w, c]
                    + image[h, w - 1, c]
                    + image[h, w + 1, c]
                    + image[h - 1, w - 1, c]
                    + image[h - 1, w + 1, c]
                    + image[h + 1, w - 1, c]
                    + image[h + 1, w + 1, c]
                ) / 9
    return dst


if __name__ == "__main__":
    start = time.perf_counter()
    src = cv2.imread("beatles.jpg")
    image = pad(src, 1, mode="edge")[:, :, 1:-1]
    image = image.astype("uint32")
    dst = numbablur(src, image)
    dst = dst.astype("uint8")
    cv2.imwrite("testblur3.jpg", dst)
    finish = time.perf_counter()
    print(f"Finished in {round(finish - start, 2)} second(s)")
